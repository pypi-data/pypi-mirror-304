import collections
import concurrent.futures
import logging
import os
import tempfile
import multiprocessing
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Literal, Optional, Union
import Bio
from Bio import SeqIO

import numpy as np
import pandas as pd
import pyranges as pr
import pyBigWig
import pyfaidx
import tiledb

from . import utils
from .config import MomicsConfig
from .logging import logger

lock = threading.Lock()


BULK_OVERWRITE = True
TILEDB_COMPRESSION = 2
TILEDB_CHUNKSIZE = 10000
TILEDB_POSITION_FILTERS = tiledb.FilterList(
    [
        # tiledb.DoubleDeltaFilter(),
    ],
    chunksize=TILEDB_CHUNKSIZE,
)
TILEDB_COV_FILTERS = tiledb.FilterList(
    [
        # tiledb.LZ4Filter(level=TILEDB_COMPRESSION),
        tiledb.ZstdFilter(level=TILEDB_COMPRESSION),
    ],
    chunksize=TILEDB_CHUNKSIZE,
)
TILEDB_SEQ_FILTERS = tiledb.FilterList(
    [
        # tiledb.LZ4Filter(level=TILEDB_COMPRESSION),
        tiledb.ZstdFilter(level=TILEDB_COMPRESSION),
    ],
    chunksize=TILEDB_CHUNKSIZE,
)


def _set_tiledb_tile(tile, chrom_length) -> int:
    t = min(chrom_length, tile)
    return t


class Momics:
    """
    A class to manipulate `.momics` repositories.

    `.momics` repositories are a TileDB-backed storage system for genomics data.
    They are structured as follows:

    - `./genome/chroms.tdb` - table for ingested chromosomes;
    - `./coverage/tracks.tdb` - table for ingested bigwig tracks;
    - `./annotations/features.tdb` - table for ingested feature sets.

    In each subdirectory, there is also one `.tdb` file per chromosome, which
    stores the following data:

    - In `./genome/{X}.tdb`: the reference sequence of the chromosome;
    - In `./coverage/{X}.tdb`: the coverage scores of the chromosome;
    - In `./annotations/{X}.tdb`: the genomic features of the chromosome.

    Attributes:
        path (str): Path to a `.momics` repository.
        cfg (MomicsConfig): Configuration object.
    """

    def __init__(
        self,
        path: str,
        config: Optional[MomicsConfig] = None,
    ) -> None:
        """
        Initialize the Momics class.
        By default, a `.momics` repository is created at the specified path if
        it does not already exist.

        Args:
            path (str): Path to a `.momics` repository.
        """

        self.path = path
        if config is None:
            config = MomicsConfig()
        self.cfg = config

        ## Check if folder exists. If not, create it.
        if not utils._repo_exists(self.path, self.cfg):
            self.cfg.vfs.create_dir(self.path)
            self._create_repository()
            logger.info(f"Created {self.path}")
        else:
            logger.debug(f"Found {self.path}")

    def _is_cloud_hosted(self) -> Union[str, Literal[False]]:
        if self.path.startswith(("s3://", "gcs://", "azure://")):
            return self.path.split("://")[0]
        else:
            return False

    def _build_uri(self, *subdirs: str) -> str:
        if self._is_cloud_hosted():
            return "/".join([self.path.rstrip("/"), *list(subdirs)])
        else:
            return str(Path(self.path).joinpath(*subdirs))

    def _create_repository(self) -> None:
        genome_path = self._build_uri("genome")
        coverage_path = self._build_uri("coverage")
        features_path = self._build_uri("annotations")
        tiledb.group_create(self.path, ctx=self.cfg.ctx)
        tiledb.group_create(genome_path, ctx=self.cfg.ctx)
        tiledb.group_create(coverage_path, ctx=self.cfg.ctx)
        tiledb.group_create(features_path, ctx=self.cfg.ctx)

    def _get_table(self, uri: str) -> Optional[pd.DataFrame]:
        if not self.cfg.vfs.is_dir(uri):
            raise FileExistsError(f"{uri} does not exist.")

        with tiledb.open(uri, "r", ctx=self.cfg.ctx) as A:
            if A.schema.sparse:
                a = A.df[:]
            else:
                a = A.df[0 : len(A) - 1]

        return a

    def _create_chroms_schema(self, chr_lengths: dict) -> None:
        tdb = self._build_uri("genome", "chroms.tdb")
        dom_genome = tiledb.Domain(
            tiledb.Dim(
                name="chrom_index",
                domain=(0, len(chr_lengths) - 1),
                dtype=np.uint32,
                tile=len(chr_lengths),
            )
        )
        attr_chr = tiledb.Attr(name="chrom", dtype="ascii", var=True)
        attr_length = tiledb.Attr(name="length", dtype=np.uint32)
        schema = tiledb.ArraySchema(
            ctx=self.cfg.ctx,
            domain=dom_genome,
            attrs=[attr_chr, attr_length],
            sparse=False,
        )
        tiledb.Array.create(tdb, schema)

    def _create_sequence_schema(self, tile: int) -> None:
        # Create every /genome/{chrom}.tdb
        chroms = self.chroms()
        for chrom in chroms["chrom"]:
            chrom_length = np.array(chroms[chroms["chrom"] == chrom]["length"])[0]
            tdb = self._build_uri("genome", f"{chrom}.tdb")
            dom = tiledb.Domain(
                tiledb.Dim(
                    name="position",
                    domain=(0, chrom_length),
                    dtype=np.uint32,
                    tile=_set_tiledb_tile(tile, chrom_length),
                    filters=TILEDB_POSITION_FILTERS,
                )
            )
            attr = tiledb.Attr(name="nucleotide", dtype=np.str_, filters=TILEDB_SEQ_FILTERS)
            schema = tiledb.ArraySchema(
                ctx=self.cfg.ctx,
                domain=dom,
                attrs=[attr],
                sparse=False,
            )
            tiledb.Array.create(tdb, schema)

    def _create_track_schema(self, max_bws: int, tile: int) -> None:
        # Create /coverage/tracks.tdb
        tdb = self._build_uri("coverage", "tracks.tdb")
        dom = tiledb.Domain(
            tiledb.Dim(name="idx", domain=(0, max_bws), dtype=np.uint32, tile=1),
        )
        attr1 = tiledb.Attr(name="label", dtype="ascii")
        attr2 = tiledb.Attr(name="path", dtype="ascii")
        schema = tiledb.ArraySchema(ctx=self.cfg.ctx, domain=dom, attrs=[attr1, attr2], sparse=False)
        tiledb.Array.create(tdb, schema)

        # Create every /coverage/{chrom}.tdb
        chroms = self.chroms()
        for chrom in chroms["chrom"]:
            chrom_length = np.array(chroms[chroms["chrom"] == chrom]["length"])[0]
            tdb = self._build_uri("coverage", f"{chrom}.tdb")
            dom = tiledb.Domain(
                tiledb.Dim(
                    name="position",
                    domain=(0, chrom_length),
                    dtype=np.uint32,
                    tile=_set_tiledb_tile(tile, chrom_length),
                    filters=TILEDB_POSITION_FILTERS,
                )
            )
            attr = tiledb.Attr(name="placeholder", dtype="float32", filters=TILEDB_COV_FILTERS)
            schema = tiledb.ArraySchema(
                ctx=self.cfg.ctx,
                domain=dom,
                attrs=[attr],
                sparse=False,
            )
            tiledb.Array.create(tdb, schema)

    def _create_features_schema(self, max_features: int, tile: int) -> None:
        # Create /features/tracks.tdb
        tdb = self._build_uri("annotations", "features.tdb")
        dom = tiledb.Domain(
            tiledb.Dim(name="idx", domain=(0, max_features), dtype=np.int64, tile=1),
        )
        schema = tiledb.ArraySchema(
            ctx=self.cfg.ctx,
            domain=dom,
            attrs=[
                tiledb.Attr(name="label", dtype="ascii"),
                tiledb.Attr(name="n", dtype=np.int64),
            ],
            sparse=False,
        )
        tiledb.Array.create(tdb, schema)

        # Create every /features/{chrom}.tdb
        chroms = self.chroms()
        for chrom in chroms["chrom"]:
            chrom_length = np.array(chroms[chroms["chrom"] == chrom]["length"])[0]
            tdb = self._build_uri("annotations", f"{chrom}.tdb")
            dom = tiledb.Domain(
                tiledb.Dim(
                    name="idx",
                    domain=(0, max_features),
                    dtype=np.int64,
                    tile=1,
                ),
                tiledb.Dim(
                    name="start",
                    domain=(0, chrom_length),
                    dtype=np.uint32,
                    tile=_set_tiledb_tile(tile, chrom_length),
                    filters=TILEDB_POSITION_FILTERS,
                ),
                tiledb.Dim(
                    name="stop",
                    domain=(0, chrom_length),
                    dtype=np.uint32,
                    tile=_set_tiledb_tile(tile, chrom_length),
                    filters=TILEDB_POSITION_FILTERS,
                ),
            )
            attrs = [
                tiledb.Attr(name="score", dtype="float32"),
                tiledb.Attr(name="strand", dtype="ascii"),
                tiledb.Attr(name="metadata", dtype="ascii"),
            ]
            schema = tiledb.ArraySchema(
                ctx=self.cfg.ctx,
                domain=dom,
                attrs=attrs,
                sparse=True,
            )
            tiledb.Array.create(tdb, schema)

    def _populate_track_table(self, bws: Dict[str, str]) -> None:
        n = self.tracks().shape[0]

        tdb = self._build_uri("coverage", "tracks.tdb")
        with tiledb.open(tdb, mode="w", ctx=self.cfg.ctx) as array:
            array[n : (n + len(bws))] = {
                "label": list(bws.keys()),
                "path": list(bws.values()),
            }

    def _populate_chroms_table(self, bws: Dict[str, str], threads: int) -> None:
        def _add_attribute_to_array(uri, attribute_name) -> None:
            # Check that attribute does not already exist
            has_attr = False
            with tiledb.open(uri, mode="r", ctx=self.cfg.ctx) as A:
                if A.schema.has_attr(attribute_name):
                    logger.warning(f"Label {attribute_name} already exists and will be erased.")
                    has_attr = True

            # Add attribute to array
            if not has_attr:
                new_attr = tiledb.Attr(attribute_name, dtype="float32", filters=TILEDB_COV_FILTERS)
                se = tiledb.ArraySchemaEvolution(self.cfg.ctx)
                se.add_attribute(new_attr)
                se.array_evolve(uri)

            # Check whether `placeholder` attribute still exists
            erase_placeholder = False
            with tiledb.open(uri, mode="r", ctx=self.cfg.ctx) as A:
                if A.schema.has_attr("placeholder") and A.nattr > 1:
                    erase_placeholder = True

            # If so, drop it
            if erase_placeholder:
                se = tiledb.ArraySchemaEvolution(self.cfg.ctx)
                se.drop_attribute("placeholder")
                se.array_evolve(uri)

        def _process_chrom(self, chrom, chrom_length, bws) -> None:

            tdb = self._build_uri("coverage", f"{chrom}.tdb")

            cfg = self.cfg.cfg
            cfg.update({"sm.compute_concurrency_level": 1})
            cfg.update({"sm.io_concurrency_level": 1})

            if BULK_OVERWRITE:
                logging.debug(f"Writing to {tdb} in bulk")
                #### If there are already scores in the array, do a bulk overwrite:
                ####    1) read all the existing scores into mem
                ####    2) Then re-write everything at once
                with tiledb.open(tdb, mode="r", config=cfg) as A:
                    sch = A.schema
                    attrs = [sch.attr(i).name for i in range(0, sch.nattr)]
                    if len(attrs) == 1 and attrs[0] == "placeholder":
                        orig_scores = {}
                    else:
                        orig_scores = A[0:chrom_length]

                for bwf in bws.keys():
                    # Add bw label to array attributes
                    _add_attribute_to_array(tdb, bwf)

                    # Ingest bigwig scores for this bw and this chrom
                    with pyBigWig.open(bws[bwf]) as bw:
                        arr = bw.values(chrom, 0, chrom_length, numpy=True)
                        orig_scores[bwf] = arr

                # Re-write appended scores to chrom array
                with tiledb.open(tdb, mode="w", config=cfg) as A:
                    A[0:chrom_length] = orig_scores

            else:
                logging.debug(f"Writing to {tdb} iteratively")
                #### Alternatively, `attr` argument can be used when
                #### optening to the array. So one can iterate over each
                #### attribute, re-open the tdb, write the corresponding data, etc.
                #### But this somehow takes longer
                for bwf in bws.keys():
                    # Add bw label to array attributes
                    _add_attribute_to_array(tdb, bwf)

                    # Ingest bigwig scores for this bw and this chrom
                    with pyBigWig.open(bws[bwf]) as bw:
                        arr = bw.values(chrom, 0, chrom_length, numpy=True)

                    # Write scores to tiledb array
                    with tiledb.open(tdb, mode="w", config=cfg, attr=bwf) as A:
                        A[0:chrom_length] = arr

                # Consolidate the modified array
                tiledb.consolidate(tdb, config=cfg)
                tiledb.vacuum(tdb, config=cfg)

            ####
            ####
            ####
            ####

            cfg.update({"sm.compute_concurrency_level": multiprocessing.cpu_count() - 1})
            cfg.update({"sm.io_concurrency_level": multiprocessing.cpu_count() - 1})

        def _log_task_completion(future, chrom, ntasks, completed_tasks) -> None:
            if future.exception() is not None:
                logger.error(f"Tracks ingestion over {chrom} failed with exception: " f"{future.exception()}")
            else:
                with lock:
                    completed_tasks[0] += 1
                logger.debug(f"task {completed_tasks[0]}/{ntasks} :: " f"ingested tracks over {chrom}.")

        tasks = []
        chroms = self.chroms()
        for chrom in chroms["chrom"]:
            chrom_length = np.array(chroms[chroms["chrom"] == chrom]["length"])[0]
            tasks.append((chrom, chrom_length))
        ntasks = len(chroms)
        completed_tasks = [0]
        threads = min(threads, ntasks)

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            for chrom, chrom_length in tasks:
                future = executor.submit(_process_chrom, self, chrom, chrom_length, bws)
                future.add_done_callback(lambda f, c=chrom: _log_task_completion(f, c, ntasks, completed_tasks))  # type: ignore
                futures.append(future)
            concurrent.futures.wait(futures)

    def _populate_features_chroms_table(self, features: Dict[str, pr.PyRanges], threads: int) -> None:
        def _process_chrom(self, chrom, feats, registered_features) -> None:
            tdb = self._build_uri("annotations", f"{chrom}.tdb")
            cfg = self.cfg.cfg
            cfg.update({"sm.compute_concurrency_level": 1})
            cfg.update({"sm.io_concurrency_level": 1})
            for lab, inter in feats.items():
                dim1 = registered_features[registered_features["label"].isin([lab])]["idx"].iloc[0]
                d = {
                    "score": np.array([0.0] * len(inter), dtype=np.float32),
                    "strand": np.array(["*"] * len(inter), dtype=np.str_),
                    "metadata": np.array(["."] * len(inter), dtype=np.str_),
                }
                with tiledb.open(tdb, mode="w", config=cfg) as A:
                    A[[dim1] * len(inter), inter["Start"], inter["End"]] = d
            cfg.update({"sm.compute_concurrency_level": multiprocessing.cpu_count() - 1})
            cfg.update({"sm.io_concurrency_level": multiprocessing.cpu_count() - 1})

        def _log_task_completion(future, chrom, ntasks, completed_tasks) -> None:
            if future.exception() is not None:
                logger.error(f"Feature set ingestion over {chrom} failed with exception: " f"{future.exception()}")
            else:
                with lock:
                    completed_tasks[0] += 1
                logger.debug(f"task {completed_tasks[0]}/{ntasks} :: " f"ingested features over {chrom}.")

        n = self.features().shape[0]
        tdb = self._build_uri("annotations", "features.tdb")
        with tiledb.open(tdb, mode="w", ctx=self.cfg.ctx) as array:
            array[n : (n + len(features))] = {
                "label": list(features.keys()),
                "n": [len(x) for x in features.values()],
            }
        tasks = []
        chroms = self.chroms()
        for chrom in chroms["chrom"]:
            chrom_length = np.array(chroms[chroms["chrom"] == chrom]["length"])[0]
            tasks.append((chrom, chrom_length))
        ntasks = len(chroms)
        completed_tasks = [0]
        threads = min(threads, ntasks)
        registered_features = self.features()

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            for chrom, _ in tasks:
                feats = {label: inter[chrom].df for label, inter in features.items()}
                future = executor.submit(
                    _process_chrom,
                    self,
                    chrom,
                    feats,
                    registered_features,
                )
                future.add_done_callback(lambda f, c=chrom: _log_task_completion(f, c, ntasks, completed_tasks))  # type: ignore
                futures.append(future)
            concurrent.futures.wait(futures)

    def _populate_sequence_table(self, fasta: Union[str, Path], threads: int) -> None:
        def _process_chrom(self, chrom, chroms, fasta) -> None:
            tdb = self._build_uri("genome", f"{chrom}.tdb")
            chrom_length = np.array(chroms[chroms["chrom"] == chrom]["length"])[0]
            with pyfaidx.Fasta(fasta) as fa:
                # get_seq() is 1-based
                chrom_seq = fa.get_seq(chrom, 1, chrom_length + 1)
                chrom_seq = np.array(list(chrom_seq.seq), dtype=np.str_)
            cfg = self.cfg.cfg
            cfg.update({"sm.compute_concurrency_level": 1})
            cfg.update({"sm.io_concurrency_level": 1})
            with tiledb.open(tdb, mode="w", config=cfg) as A:
                A[0:chrom_length] = {"nucleotide": chrom_seq}
            cfg.update({"sm.compute_concurrency_level": multiprocessing.cpu_count() - 1})
            cfg.update({"sm.io_concurrency_level": multiprocessing.cpu_count() - 1})

        def _log_task_completion(future, chrom, ntasks, completed_tasks) -> None:
            if future.exception() is not None:
                logger.error(f"Fasta ingestion over {chrom} failed with exception: " f"{future.exception()}")
            else:
                with lock:
                    completed_tasks[0] += 1
                logger.debug(f"task {completed_tasks[0]}/{ntasks} :: " f"ingested fasta over {chrom}.")

        chroms = self.chroms()
        tasks = chroms["chrom"]
        ntasks = len(tasks)
        completed_tasks = [0]
        threads = min(threads, ntasks)
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            for chrom in tasks:
                future = executor.submit(_process_chrom, self, chrom, chroms, fasta)
                future.add_done_callback(lambda f, c=chrom: _log_task_completion(f, c, ntasks, completed_tasks))  # type: ignore
                futures.append(future)
            concurrent.futures.wait(futures)

    def chroms(self) -> pd.DataFrame:
        """Extract chromosome table from a `.momics` repository.

        Returns:
            pd.DataFrame: A data frame listing one chromosome per row
        """
        try:
            chroms = self._get_table(self._build_uri("genome", "chroms.tdb"))
        except FileExistsError:
            chroms = pd.DataFrame(columns=["chrom_index", "chrom", "length"])
        return chroms

    def seq(self, label: Optional[str] = None) -> pd.DataFrame:
        """Extract sequence table from a `.momics` repository.

        Args:
            label (str, optional): Which chromosome to extract. Defaults to None.

        Returns:
            pd.DataFrame: A data frame listing one chromosome per row,
            with first/last 10 nts.
        """
        chroms = self.chroms()
        if chroms.empty:
            raise OSError("`chroms` table has not been filled out yet.")

        try:
            tdb = self._build_uri("genome", f"{chroms['chrom'][0]}.tdb")
            _ = self._get_table(tdb)
            pass
        except FileExistsError as e:
            raise OSError("`seq` table has not been filled out yet.") from e

        if label is not None:
            if label not in chroms.chrom.values:
                raise ValueError(f"Selected attribute does not exist: '{label}'.")
            tdb = self._build_uri("genome", f"{label}.tdb")
            with tiledb.open(tdb, "r", ctx=self.cfg.ctx) as A:
                seq = A[:]["nucleotide"][:-1]
            return "".join(seq)
        else:
            chroms["seq"] = pd.Series()
            for chrom in chroms["chrom"]:
                tdb = self._build_uri("genome", f"{chrom}.tdb")
                chrom_len = chroms[chroms["chrom"] == chrom]["length"].iloc[0]
                with tiledb.open(tdb, "r", ctx=self.cfg.ctx) as A:
                    start_nt = "".join(A.df[0:9]["nucleotide"])
                    end_nt = "".join(A.df[(chrom_len - 10) : (chrom_len - 1)]["nucleotide"])
                chroms.loc[chroms["chrom"] == chrom, "seq"] = start_nt + "..." + end_nt

            return chroms

    def tracks(self, label: Optional[str] = None) -> Union[pd.DataFrame, pr.PyRanges]:
        """Extract table of ingested bigwigs.

        Returns:
            pd.DataFrame: A data frame listing one ingested bigwig file per row
        """
        if label is not None:
            tr = self.tracks()
            if label not in tr["label"].values:
                raise ValueError(f"Feature set '{label}' not found.")
            chroms = self.chroms()
            cov = {chrom: np.empty(length, dtype=object) for (chrom, length) in zip(chroms.chrom, chroms.length)}
            for chrom in chroms["chrom"]:
                tdb = self._build_uri("coverage", f"{chrom}.tdb")
                with tiledb.open(tdb, "r", ctx=self.cfg.ctx) as A:
                    cov[chrom] = A.query(attrs=[label])[:][label][:-1]
            return cov
        else:
            try:
                tracks = self._get_table(self._build_uri("coverage", "tracks.tdb"))
                if type(tracks) is not pd.DataFrame:
                    raise ValueError("Failed to fetch tracks table.")
                tracks = tracks[tracks["label"] != "\x00"]
            except FileExistsError:
                tracks = pd.DataFrame(columns=["idx", "label", "path"])
            return tracks

    def features(self, label: Optional[str] = None) -> Union[pd.DataFrame, pr.PyRanges]:
        """Extract table of ingested features sets.

        Returns:
            - if `label` is None: pd.DataFrame: A data frame listing one ingested feature set per row
            - if `label` is not None: pr.PyRanges: A PyRanges object of the specified feature set
        """
        if label is not None:
            ft = self.features()
            if label not in ft["label"].values:
                raise ValueError(f"Feature set '{label}' not found.")
            chroms = self.chroms()
            ranges = []
            for chrom in chroms["chrom"]:
                tdb = self._build_uri("annotations", f"{chrom}.tdb")
                idx = ft[ft["label"] == label]["idx"].iloc[0]
                with tiledb.open(tdb, "r", ctx=self.cfg.ctx) as A:
                    x = A.query(cond=f"idx=={idx}").df[:]
                    x.idx = x.idx.astype(str)
                    x.idx = chrom
                    ranges.append(x)
            df = pd.concat(ranges)
            df2 = pd.DataFrame(
                {
                    "Chromosome": df["idx"],
                    "Start": df["start"],
                    "End": df["stop"],
                    "strand": df["strand"],
                    "score": df["score"],
                    "metadata": df["metadata"],
                }
            )
            res = pr.PyRanges(df2)
            return res

        else:
            try:
                features = self._get_table(self._build_uri("annotations", "features.tdb"))
                if type(features) is not pd.DataFrame:
                    raise ValueError("Failed to fetch features table.")
                features = features[features["label"] != "\x00"]
            except FileExistsError:
                features = pd.DataFrame(columns=["idx", "label", "n"])
            return features

    def bins(self, width, stride, cut_last_bin_out=False) -> pr.PyRanges:
        """Generate a PyRanges of tiled genomic bins

        Args:
            width (_type_): The width of each bin.
            stride (_type_): The stride size for tiling.
            cut_last_bin_out (bool, optional): Remove the last bin of each \
                chromosome. Defaults to False.

            Remember that PyRanges are 0-based and end-exclusive.

        Returns:
            _type_: pr.PyRanges: a PyRanges object of tiled genomic bins.
        """
        bins = []
        chroms = self.chroms().set_index("chrom")["length"].to_dict()
        if chroms == {}:
            raise ValueError("Please fill out `chroms` table first.")

        for chrom, length in chroms.items():
            start = 0
            while start < length:
                end = min(start + width, length)
                bins.append({"chrom": chrom, "start": (start), "end": end})
                start += stride

        df = pd.DataFrame(bins)
        if cut_last_bin_out:
            df = df[(df["end"] - df["start"]) == width]

        bt = pr.PyRanges(chromosomes=df["chrom"], starts=df["start"], ends=df["end"])

        return bt

    def ingest_chroms(self, chr_lengths: dict, genome_version: str = "") -> "Momics":
        """Add chromosomes (and genome) information the `.momics` repository.

        Args:
            chr_lengths (dict): Chromosome lengths
            genome_version (str, optional): Genome version (default: ""). \
                Defaults to "".

        Returns:
            Momics: An updated Momics object
        """
        if not self.chroms().empty:
            raise ValueError("`chroms` table has already been filled out.")

        # Create chroms tables schema
        self._create_chroms_schema(chr_lengths)

        # Populate `chrom` array
        chr = list(chr_lengths.keys())
        length = list(chr_lengths.values())
        tdb = self._build_uri("genome", "chroms.tdb")
        with tiledb.open(tdb, "w", ctx=self.cfg.ctx) as A:
            A[0 : len(chr)] = {"chrom": np.array(chr, dtype="S"), "length": length}
            A.meta["genome_assembly_version"] = genome_version
            A.meta["timestamp"] = datetime.now().isoformat()

        return self

    def ingest_sequence(
        self,
        fasta: Path,
        threads: int = 1,
        tile: int = 32000,
    ) -> "Momics":
        """Ingest a fasta file into a Momics repository

        Args:
            fasta (str): Path to a Fasta file containing the genome reference sequence.
            threads (int, optional): Threads to parallelize I/O. Defaults to 1.
            tile (int, optional): Tile size for TileDB. Defaults to 50000.

        Returns:
            Momics: The updated Momics object
        """
        start0 = time.time()

        # Abort if `chroms` have not been filled
        chroms = self.chroms()
        if chroms.empty:
            raise ValueError("Please fill out `chroms` table first.")

        # Abort if sequence table already exists
        tdb = self._build_uri("genome", f"{chroms['chrom'][0]}.tdb")
        if self.cfg.vfs.is_dir(tdb):
            raise tiledb.cc.TileDBError(f"Error: TileDB '{tdb}' already exists.")

        # Abort if chr lengths in provided fasta do not match those in `chroms`
        utils._check_fasta_lengths(fasta, chroms)

        # Create sequence tables schema
        self._create_sequence_schema(tile)

        # Populate each `/genome/sequence/{chrom}.tdb`
        self._populate_sequence_table(fasta, threads)

        logger.info(f"Genome sequence ingested in {round(time.time() - start0,4)}s.")

        return self

    def ingest_features(
        self,
        features: dict,
        threads: int = 1,
        max_features: int = 9999,
        tile: int = 32000,
    ) -> "Momics":
        """Ingest feature sets to the `.momics` repository.

        Args:
            features (dict): Dictionary of feature sets already imported as a PyRanges.
            threads (int, optional): Threads to parallelize I/O. Defaults to 1.
            max_features (int, optional): Maximum number of feature sets. Defaults to 9999.
            tile (int, optional): Tile size. Defaults to 50000.
            compression (int, optional): Compression level. Defaults to 3.

        Returns:
            Momics: The updated Momics object
        """
        start0 = time.time()

        # Abort if `chroms` have not been filled
        if self.chroms().empty:
            raise ValueError("Please fill out `chroms` table first.")

        # Abort if features labels already exist
        utils._check_feature_names(features, self.features())

        # If `path/features/features.tdb` (and `{chroms.tdb}`) do not exist, create it
        if self.features().empty:
            self._create_features_schema(max_features, tile)

        # Populate each `path/features/{chrom}.tdb`
        self._populate_features_chroms_table(features, threads)

        logger.info(f"{len(features)} feature sets ingested in " f"{round(time.time() - start0,4)}s.")

        return self

    def ingest_tracks(
        self,
        bws: dict,
        threads: int = 1,
        max_bws: int = 9999,
        tile: int = 32000,
    ) -> "Momics":
        """Ingest bigwig coverage tracks to the `.momics` repository.

        Args:
            bws (dict): Dictionary of bigwig files
            threads (int, optional): Threads to parallelize I/O. Defaults to 1.
            max_bws (int, optional): Maximum number of bigwig files. Defaults to 9999.
            tile (int, optional): Tile size. Defaults to 50000.
            compression (int, optional): Compression level. Defaults to 3.

        Returns:
            Momics: The updated Momics object
        """
        start0 = time.time()

        # Abort if `chroms` have not been filled
        if self.chroms().empty:
            raise ValueError("Please fill out `chroms` table first.")

        # Abort if chr lengths in provided bw do not match those in `chroms`
        utils._check_chr_lengths(bws, self.chroms())

        # Abort if bw labels already exist
        utils._check_track_names(bws, self.tracks())

        # If `path/coverage/tracks.tdb` (and `{chroms.tdb}`) do not exist, create it
        if self.tracks().empty:
            self._create_track_schema(max_bws, tile)

        # Populate each `path/coverage/{chrom}.tdb`
        self._populate_chroms_table(bws, threads)

        # Populate `path/coverage/tracks.tdb`
        self._populate_track_table(bws)

        logger.info(f"{len(bws)} tracks ingested in {round(time.time() - start0,4)}s.")

        return self

    def ingest_track(
        self,
        coverage: dict,
        track: str,
        threads: int = 1,
    ) -> "Momics":
        """
        Ingest a coverage track provided as a dictionary to a `.momics` repository.
        This method is useful when you have already computed the coverage track and
        have it in memory.

        Args:
            coverage (dict): Dictionary of coverage tracks. The keys are \
                chromosome names and the values are numpy arrays.
            track (str): Label to store the track under.
            threads (int, optional): Threads to parallelize I/O. Defaults to 1.

        Returns:
            Momics: The updated Momics object
        """
        chroms = self.chroms()
        tracks = self.tracks()

        # Abort if `chroms` have not been filled
        if chroms.empty:
            raise ValueError("Please fill out `chroms` table first.")
        if tracks.empty:
            raise ValueError("Please fill out `tracks` table first.")

        # Abort if chr lengths in provided bw do not match those in `chroms`
        reference_lengths = dict(zip(chroms["chrom"], chroms["length"]))
        lengths = dict(zip(chroms["chrom"], [len(v) for k, v in coverage.items()]))
        if lengths != reference_lengths:
            raise Exception(
                f"`{track}` coverage track does not chromomosome lengths matching " f"those of the momics repository."
            )

        # Abort if bw labels already exist
        if track in set(tracks["label"]):
            raise ValueError(f"Provided label '{track}' already present in `tracks` table")

        # Save the coverage dict as a temporary bigwig file
        # and ingest it using `ingest_tracks`
        tmp_bw = tempfile.NamedTemporaryFile(delete=False)
        path = utils.dict_to_bigwig(coverage, Path(tmp_bw.name))
        self.ingest_tracks({track: path.name}, threads=threads)
        os.remove(path.name)

        return self

    def remove_track(self, track: str) -> "Momics":
        """Remove a track from a `.momics` repository.

        Args:
            track (str): Which track to remove

        Returns:
            Momics: An updated Momics object
        """
        # Abort if `track` is not listed
        tracks = self.tracks()
        chroms = self.chroms()
        utils._check_track_name(track, tracks)

        # Remove entry from each `path/coverage/{chrom}.tdb`
        # and from `path/coverage/tracks.tdb`
        for chrom in chroms["chrom"]:
            tdb = self._build_uri("coverage", f"{chrom}.tdb")
            ctx = self.cfg.ctx
            se = tiledb.ArraySchemaEvolution(ctx)
            se.drop_attribute(track)
            se.array_evolve(tdb)

        tdb = self._build_uri("coverage", "tracks.tdb")
        idx = tracks["idx"][tracks["label"] == track].values[0]
        with tiledb.open(tdb, mode="w", ctx=self.cfg.ctx) as A:
            A[idx] = {"label": None, "path": None}

        return self

    def remove(self) -> bool:
        """Remove a `.momics` repository."""
        host = self._is_cloud_hosted()
        vfs = self.cfg.vfs

        ## Remove local repo
        if not host:
            vfs.remove_dir(self.path)
            logger.info(f"Purged {self.path}")

        ## Remove S3 and GCS-hosted repo
        if host in ["s3", "gcs"]:
            vfs.remove_dir(self.path)
            logger.info(f"Purged {self.path}")

        if host == "azure":

            def remove_directory_until_success(vfs, dir_uri, max_retries=10, retry_delay=2):
                attempts = 0
                while attempts < max_retries:
                    try:
                        vfs.remove_dir(dir_uri)
                        logger.info(f"Purged {dir_uri}")
                        break
                    except tiledb.TileDBError as e:
                        attempts += 1
                        if attempts < max_retries:
                            time.sleep(retry_delay)
                        else:
                            raise e

            remove_directory_until_success(vfs, self.path)

        return True

    def export_track(self, track: str, output: Path) -> "Momics":
        """Export a track from a `.momics` repository as a `.bw` file.

        Args:
            track (str): Which track to remove
            output (Path): Prefix of the output bigwig file

        Returns:
            Momics: An updated Momics object
        """
        # Abort if `track` is not listed
        utils._check_track_name(track, self.tracks())

        # Init output file
        bw = pyBigWig.open(output, "w")
        chrom_sizes = self.chroms()[["chrom", "length"]].apply(tuple, axis=1).tolist()
        bw.addHeader(chrom_sizes)
        for chrom, chrom_length in chrom_sizes:
            tdb = self._build_uri("coverage", f"{chrom}.tdb")
            with tiledb.open(tdb, "r", ctx=self.cfg.ctx) as A:
                values0 = A.query(attrs=[track])[:][track][:-1]
            chroms = np.array([chrom] * chrom_length)
            starts = np.array(range(chrom_length))
            ends = starts + 1
            bw.addEntries(chroms, starts=starts, ends=ends, values=values0)
        bw.close()

        return self

    def export_sequence(self, output: Path) -> "Momics":
        """Export sequence from a `.momics` repository as a `.fa` file.

        Args:
            output (Path): Prefix of the output fasta file

        Returns:
            Momics: An updated Momics object
        """
        # Silence logger
        logging.disable(logging.CRITICAL)

        if os.path.exists(output):
            os.remove(output)

        # Init output file
        chroms = self.chroms()["chrom"]
        with open(output, "a") as output_handle:
            for chrom in chroms:
                seq = self.seq(chrom)
                sr = Bio.SeqRecord.SeqRecord(Bio.Seq.Seq(seq), id=chrom, description="")
                SeqIO.write(sr, output_handle, "fasta")

        return self

    def export_features(self, features: str, output: Path) -> "Momics":
        """Export a features set from a `.momics` repository as a `.bed` file.

        Args:
            features (str): Which features to remove
            output (Path): Prefix of the output BED file

        Returns:
            Momics: An updated Momics object
        """
        # Abort if `features` is not listed
        utils._check_feature_name(features, self.features())

        # Init output file
        bed = self.features(features)
        bed.to_bed(output)
        return self

    def manifest(self) -> dict:
        """
        Returns the manifest of the Momics repository. The manifest lists the
        configuration for all the arrays stored in the repository, including
        their schema, attributes, and metadata.
        """

        def is_tiledb_array(uri, ctx):
            try:
                return tiledb.object_type(uri, ctx) == "array"
            except tiledb.TileDBError:
                return False

        def is_tiledb_group(uri, ctx):
            try:
                return tiledb.object_type(uri, ctx) == "group"
            except tiledb.TileDBError:
                return False

        def get_array_schema(uri, ctx):
            try:
                with tiledb.open(uri, ctx=ctx, mode="r") as array:
                    schema = array.schema

                    d = collections.defaultdict(
                        None,
                        {
                            "uri": uri,
                            "type": "array",
                            "shape": schema.shape,
                            "sparse": schema.sparse,
                            "chunksize": schema.capacity,
                            "cell_order": schema.cell_order,
                            "tile_order": schema.tile_order,
                        },
                    )

                    d["dims"] = collections.defaultdict(None)
                    for dim in schema.domain:
                        d["dims"][dim.name] = {
                            "domain": tuple([int(i) for i in dim.domain]),
                            "dtype": str(dim.dtype),
                            "tile": int(dim.tile),
                            "filters": str(dim.filters),
                        }
                    d["dims"] = dict(d["dims"])

                    d["attrs"] = collections.defaultdict(None)
                    attrs = [schema.attr(x) for x in range(schema.nattr)]
                    for attr in attrs:
                        d["attrs"][attr.name] = {
                            "dtype": str(attr.dtype),
                            "filters": str(attr.filters),
                        }
                    d["attrs"] = dict(d["attrs"])

                    d["modification_timestamps"] = {frag.uri: frag.timestamp_range for frag in tiledb.FragmentInfoList(uri)}
                    d = dict(d)

                return d

            except Exception as e:
                print(f"Error reading array schema from {uri}: {e}")
                return None

        def get_group_metadata(uri):
            try:
                return {"uri": uri, "type": "group"}
            except Exception as e:
                print(f"Error reading group metadata from {uri}: {e}")
                return None

        def traverse_directory(base_dir, ctx):
            manifest = collections.defaultdict(None)
            for pointer in self.cfg.vfs.ls_recursive(base_dir):
                if is_tiledb_array(pointer, ctx):
                    array_info = get_array_schema(pointer, ctx)
                    if array_info:
                        manifest[pointer] = array_info
                elif is_tiledb_group(pointer, ctx):
                    group_info = get_group_metadata(pointer)
                    if group_info:
                        manifest[pointer] = group_info

            return manifest

        man = traverse_directory(self.path, self.cfg.ctx)
        return man

    def consolidate(self, vacuum: bool = True) -> Literal[True]:
        """
        Consolidates the fragments of all arrays in the repository.

        Args:
            vacuum (bool, optional): Vacuum the consolidated array. Defaults to True.
        """
        for pointer in self.cfg.vfs.ls_recursive(self.path):
            try:
                if tiledb.object_type(pointer) == "array":
                    logging.debug(f"Consolidating array at: {pointer}")
                    tiledb.consolidate(pointer)
                    if vacuum:
                        tiledb.vacuum(pointer)
            except tiledb.TileDBError as e:
                print(f"Error processing {pointer}: {e}")

        return True

    def size(self) -> int:
        """
        Returns:
            int: The size of the repository in bytes.
        """
        size = 0
        for pointer in self.cfg.vfs.ls_recursive(self.path):
            if self.cfg.vfs.is_file(pointer):
                try:
                    size += self.cfg.vfs.file_size(pointer)
                except tiledb.TileDBError as e:
                    print(f"Error processing {pointer}: {e}")
        return size
