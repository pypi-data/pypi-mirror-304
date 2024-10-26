import os
import random
from typing import Final

import numpy as np
import pyBigWig
import pytest
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

NO_SKIP_OPTION: Final[str] = "--no-skip"


def pytest_addoption(parser):
    parser.addoption(NO_SKIP_OPTION, action="store_true", default=False, help="also run skipped tests")


def pytest_collection_modifyitems(config, items: list):
    if config.getoption(NO_SKIP_OPTION):
        for test in items:
            test.own_markers = [marker for marker in test.own_markers if marker.name not in ("skip", "skipif")]


@pytest.fixture(scope="session")
def momics_path(tmp_path_factory):
    p = os.path.join(tmp_path_factory.getbasetemp(), "test.momics")
    return p


@pytest.fixture(scope="session")
def momics_path2(tmp_path_factory):
    p = os.path.join(tmp_path_factory.getbasetemp(), "test2.momics")
    return p


@pytest.fixture(scope="session")
def fa1(tmp_path_factory):
    p = os.path.join(tmp_path_factory.getbasetemp(), "fa1")
    nucleotides = ["A", "T", "C", "G"]
    chrom_seqs = {
        "I": "ATCGATCGAT" + "".join(random.choices(nucleotides, k=10000 - 20)) + "TTCCGGTTCC",
        "II": "TCGATCGATA" + "".join(random.choices(nucleotides, k=20000 - 10)),
        "III": "CGATCGATAT" + "".join(random.choices(nucleotides, k=30000 - 10)),
    }
    records = []
    for chrom, sequence in chrom_seqs.items():
        record = SeqRecord(Seq(sequence), id=chrom, description="")
        records.append(record)

    with open(p, "w") as output_handle:
        SeqIO.write(records, output_handle, "fasta")

    return p


@pytest.fixture(scope="session")
def fa2(tmp_path_factory):
    p = os.path.join(tmp_path_factory.getbasetemp(), "fa2")
    nucleotides = ["A", "T", "C", "G"]
    chrom_seqs = {
        "I": "".join(random.choices(nucleotides, k=2000)),
        "II": "".join(random.choices(nucleotides, k=1000)),
        "III": "".join(random.choices(nucleotides, k=500)),
    }
    records = []
    for chrom, sequence in chrom_seqs.items():
        record = SeqRecord(Seq(sequence), id=chrom, description="")
        records.append(record)

    with open(p, "w") as output_handle:
        SeqIO.write(records, output_handle, "fasta")

    return p


@pytest.fixture(scope="session")
def bw1(tmp_path_factory):
    p = os.path.join(tmp_path_factory.getbasetemp(), "bw1")
    bw = pyBigWig.open(p, "w")
    chrom_sizes = {"I": 10000, "II": 20000, "III": 30000}
    bw.addHeader(list(chrom_sizes.items()))
    for chrom, size in chrom_sizes.items():
        intervals = [(i, i + 1000, np.random.rand()) for i in range(0, size, 1000)]
        intervals = [(i, i + 1000, i / 100000) for i in range(0, size, 1000)]
        bw.addEntries(
            [chrom] * len(intervals),
            starts=[x[0] for x in intervals],
            ends=[x[1] for x in intervals],
            values=[x[2] for x in intervals],
        )
    bw.close()
    return p


@pytest.fixture(scope="session")
def bw2(tmp_path_factory):
    p = os.path.join(tmp_path_factory.getbasetemp(), "bw2")
    bw = pyBigWig.open(p, "w")
    chrom_sizes = {"I": 10000, "II": 50000, "III": 30000, "IV": 40000}
    bw.addHeader(list(chrom_sizes.items()))
    for chrom, size in chrom_sizes.items():
        intervals = [(i, i + 1000, np.random.rand()) for i in range(0, size, 1000)]
        bw.addEntries(
            [chrom] * len(intervals),
            starts=[x[0] for x in intervals],
            ends=[x[1] for x in intervals],
            values=[x[2] for x in intervals],
        )
    bw.close()
    return p


@pytest.fixture(scope="session")
def bw3(tmp_path_factory):
    p = os.path.join(tmp_path_factory.getbasetemp(), "bw3")
    bw = pyBigWig.open(p, "w")
    chrom_sizes = {"I": 10005, "II": 50001, "III": 30002, "IV": 40011}
    bw.addHeader(list(chrom_sizes.items()))
    for chrom, size in chrom_sizes.items():
        intervals = [(i, i + 1000, np.random.rand()) for i in range(0, size, 1000)]
        bw.addEntries(
            [chrom] * len(intervals),
            starts=[x[0] for x in intervals],
            ends=[x[1] for x in intervals],
            values=[x[2] for x in intervals],
        )
    bw.close()
    return p


@pytest.fixture(scope="session")
def fa3(tmp_path_factory):
    p = os.path.join(tmp_path_factory.getbasetemp(), "fa3")
    nucleotides = ["A", "T", "C", "G"]
    chrom_seqs = {
        "I": "ATCGATCGAT" + "".join(random.choices(nucleotides, k=10005 - 20)) + "TTCCGGTTCC",
        "II": "".join(random.choices(nucleotides, k=50001)),
        "III": "".join(random.choices(nucleotides, k=30002)),
        "IV": "".join(random.choices(nucleotides, k=40011)),
    }
    records = []
    for chrom, sequence in chrom_seqs.items():
        record = SeqRecord(Seq(sequence), id=chrom, description="")
        records.append(record)

    with open(p, "w") as output_handle:
        SeqIO.write(records, output_handle, "fasta")

    return p


@pytest.fixture(scope="session")
def bed1(tmp_path_factory):
    p = os.path.join(tmp_path_factory.getbasetemp(), "bed1")
    bed = [["I", 0, 10], ["I", 20, 30], ["II", 20, 25]]
    with open(p, "w") as bedf:
        for chrom, start, end in bed:
            bedf.write(f"{chrom}\t{start}\t{end}\n")
    return p
