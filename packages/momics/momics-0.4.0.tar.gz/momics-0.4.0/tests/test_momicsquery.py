import json
import multiprocessing
import os
import pickle
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import pyranges as pr
import pytest

from momics.momics import Momics
from momics.query import MomicsQuery
from momics.aggregate import aggregate

multiprocessing.set_start_method("spawn", force=True)


@pytest.mark.order(2)
def test_momicsquery_tracks(momics_path: str, bed1: str):
    mom = Momics(momics_path)
    q = MomicsQuery(mom, "I:990-1010").query_tracks()
    assert len(q.coverage) == 4
    assert len(q.coverage["bw2"]["I:990-1010"]) == 20
    assert q.to_df()["chrom"].__eq__(pd.Series(["I"] * 20)).all()

    q = MomicsQuery(mom, "I").query_tracks()
    assert len(q.coverage) == 4
    print(q.coverage["bw2"].keys())
    assert len(q.coverage["bw2"]["I:0-10000"]) == 10000

    q = MomicsQuery(mom, "I").query_tracks()
    assert len(q.coverage) == 4
    assert len(q.coverage["bw2"]["I:0-10000"]) == 10000

    bed = pr.read_bed(bed1)
    q = MomicsQuery(mom, bed).query_tracks()
    assert list(q.coverage.keys()) == ["bw2", "custom", "bw3", "bw4"]

    q = MomicsQuery(mom, bed).query_tracks(threads=2)
    assert list(q.coverage.keys()) == ["bw2", "custom", "bw3", "bw4"]

    q = MomicsQuery(mom, bed).query_tracks(threads=2, tracks=["bw2", "bw3"])
    assert list(q.coverage.keys()) == ["bw2", "bw3"]


@pytest.mark.order(2)
def test_momicsquery_seq(momics_path: str):
    mom = Momics(momics_path)
    q = MomicsQuery(mom, "I:0-10").query_sequence()
    assert len(q.seq) == 1
    assert q.seq["nucleotide"]["I:0-10"] == "ATCGATCGAT"

    q = MomicsQuery(mom, "I:9990-10000").query_sequence()
    assert len(q.seq) == 1
    assert q.seq["nucleotide"]["I:9990-10000"] == "TTCCGGTTCC"


@pytest.mark.order(2)
def test_momicsquery_seq2(momics_path: str, bed1: str):
    mom = Momics(momics_path)
    q = MomicsQuery(mom, "I:0-10").query_sequence()
    bed = pr.read_bed(bed1)
    q = MomicsQuery(mom, bed).query_sequence()
    assert len(q.seq["nucleotide"]) == 3
    print(q.seq["nucleotide"].keys())
    assert q.seq["nucleotide"]["I:0-10"] == "ATCGATCGAT"
    assert q.to_SeqRecord()[0].id == "I:0-10"


@pytest.mark.order(2)
def test_momicsquery_seq3(momics_path: str):
    mom = Momics(momics_path)
    q = MomicsQuery(mom, "I:0-10").query_sequence()
    q = MomicsQuery(mom, "I").query_sequence()
    assert len(q.seq["nucleotide"]["I:0-10000"]) == 10000


@pytest.mark.order(2)
def test_momicsquery_seq4(momics_path: str, bed1: str):
    mom = Momics(momics_path)
    q = MomicsQuery(mom, "I:0-10").query_sequence()
    bed = pr.read_bed(bed1)
    q = MomicsQuery(mom, bed).query_sequence()
    assert q.seq["nucleotide"]["I:0-10"] == "ATCGATCGAT"


@pytest.mark.order(2)
def test_momicsquery_seq5(momics_path: str, bed1: str):
    mom = Momics(momics_path)
    bed = pr.read_bed(bed1)
    print(bed)
    q = MomicsQuery(mom, "I:0-10").query_sequence()
    assert q.seq["nucleotide"]["I:0-10"] == "ATCGATCGAT"
    q = MomicsQuery(mom, bed).query_sequence(threads=2)
    assert q.seq["nucleotide"]["I:0-10"] == "ATCGATCGAT"


@pytest.fixture
def temp_json_file():
    """Fixture to create a temporary JSON for testing."""
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_json_file = Path(temp_file.name)
        yield temp_json_file
    temp_json_file.unlink()


@pytest.fixture
def temp_npz_file():
    """Fixture to create a temporary NPZ for testing."""
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_npz_file = Path(temp_file.name)
        yield temp_npz_file
    temp_npz_file.unlink()


@pytest.mark.order(2)
def test_to_json_npz(momics_path: str, temp_json_file: Path, temp_npz_file: Path):
    mom = Momics(momics_path)
    q = MomicsQuery(mom, "I:0-10").query_sequence().query_tracks()

    q.to_json(temp_json_file)
    q.to_npz(temp_npz_file)

    with open(temp_json_file) as json_file:
        data = json.load(json_file)
    assert list(data.keys()) == ["bw2", "custom", "bw3", "bw4", "nucleotide"]
    assert data["nucleotide"]["I:0-10"] == "ATCGATCGAT"

    data = np.load(temp_npz_file, allow_pickle=True)
    seq = pickle.loads(data["seq"])
    cov = pickle.loads(data["coverage"])
    print(cov.keys())
    assert seq["nucleotide"]["I:0-10"] == "ATCGATCGAT"
    assert list(cov.keys()) == ["bw2", "custom", "bw3", "bw4", "nucleotide"]
    assert list(cov["bw2"].keys()) == ["I:0-10"]


@pytest.mark.order(2)
def test_aggregate(momics_path: str):
    mom = Momics(momics_path)
    b = mom.bins(3, 1)["I", 6990:7010]
    chrom_sizes = {chrom: size for chrom, size in zip(mom.chroms().chrom, mom.chroms().length)}
    q = MomicsQuery(mom, b).query_tracks()
    cov = q.coverage
    x = aggregate(cov, b, chrom_sizes)
    print(x.keys())
    assert list(x.keys()) == ["bw2", "custom", "bw3", "bw4"]
    assert [len(y) for y in x["bw2"].values()] == [10000, 20000, 30000]
    assert x["bw2"]["I"].shape == (10000,)

    x = aggregate(cov, b, chrom_sizes, type="mean")
    assert x["bw2"]["I"].shape == (10000,)
    vec = x["bw2"]["I"][6985:7015] - np.array([0] * 3 + [0.06] * 12 + [0.07] * 12 + [0] * 3) < 1e-6
    assert sum(vec) == 30

    x = aggregate(cov, b, chrom_sizes, type="sum")
    assert x["bw2"]["I"].shape == (10000,)
    res = np.array([0] * 3 + [0.06, 0.12] + [0.18] * 10 + [0.21] * 10 + [0.14, 0.07] + [0] * 3)
    vec = x["bw2"]["I"][6985:7015] - res < 1e-6
    assert sum(vec) == 30

    x = aggregate(cov, b, chrom_sizes, prefix="tmp__")
    assert x["bw2"]["I"].shape == (10000,)
    vec = x["bw2"]["I"][6985:7015] - np.array([0] * 3 + [0.06] * 12 + [0.07] * 12 + [0] * 3) < 1e-6
    assert sum(vec) == 30
    tracks = mom.tracks().label
    print(tracks)
    assert [os.path.exists("tmp___" + track + ".bw") for track in tracks].count(True) == 4
