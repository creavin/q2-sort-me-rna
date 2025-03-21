# ----------------------------------------------------------------------------
# Copyright (c) 2016-2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import pandas as pd

from q2_types.feature_data import BLAST6Format, DNAFASTAFormat
from q2_types_genomics.per_sample_data import SAMDirFmt
from q2_types.per_sample_sequences \
    import CasavaOneEightSingleLanePerSampleDirFmt

from q2_sort_me_rna._rna_sorter import sort_rna as align


def align_sequences(
    ref: DNAFASTAFormat,
    reads: CasavaOneEightSingleLanePerSampleDirFmt,
    workdir: str = None,
    kvdb: str = None,
    idx_dir: str = None,
    readb: str = None,
    fastx: bool = None,
    sam: bool = None,
    sq: bool = None,
    blast: str = None,
    aligned: str = None,
    other: str = None,
    num_alignments: int = None,
    no_best: bool = None,
    min_lis: int = None,
    print_all_reads: bool = None,
    paired: bool = None,
    paired_in: bool = None,
    paired_out: bool = None,
    out2: bool = None,
    sout: bool = None,
    zip_out: bool = None,
    match: int = None,
    mismatch: int = None,
    gap_open: int = None,
    gap_ext: int = None,
    e: float = None,
    f: bool = None,
    n: bool = None,
    r: bool = None,
    id: float = None,
    coverage: float = None,
    de_novo_otu: bool = None,
    otu_map: bool = None,
    passes: str = None,
    edges: int = None,
    num_seeds: bool = None,
    full_search: int = None,
    pid: bool = None,
    a: int = None,
    threads: int = None,
    index: int = None,
    l: float = None,
    m: float = None,
    v: bool = None,
    interval: int = None,
    max_pos: int = None,
    h: bool = None,
    version: bool = None,
    dbg_put_db: bool = None,
    cmd: bool = None,
    task: int = None,
    dbg_level: int = None) \
        -> (BLAST6Format, CasavaOneEightSingleLanePerSampleDirFmt, SAMDirFmt):
    arg_value_dict = locals()

    for arg in arg_value_dict:
        if arg in ['blast', 'fastx', 'sam'] and arg_value_dict[arg] is None:
            arg_value_dict[arg] = 1
    return align(**arg_value_dict)


def otu_mapping(
    ref: DNAFASTAFormat,
    reads: CasavaOneEightSingleLanePerSampleDirFmt,
    workdir: str = None,
    kvdb: str = None,
    idx_dir: str = None,
    readb: str = None,
    fastx: bool = None,
    sam: bool = None,
    sq: bool = None,
    blast: str = None,
    aligned: str = None,
    other: str = None,
    num_alignments: int = None,
    no_best: bool = None,
    min_lis: int = None,
    print_all_reads: bool = None,
    paired: bool = None,
    paired_in: bool = None,
    paired_out: bool = None,
    out2: bool = None,
    sout: bool = None,
    zip_out: bool = None,
    match: int = None,
    mismatch: int = None,
    gap_open: int = None,
    gap_ext: int = None,
    e: float = None,
    f: bool = None,
    n: bool = None,
    r: bool = None,
    id: float = None,
    coverage: float = None,
    de_novo_otu: bool = None,
    otu_map: bool = None,
    passes: str = None,
    edges: int = None,
    num_seeds: bool = None,
    full_search: int = None,
    pid: bool = None,
    a: int = None,
    threads: int = None,
    index: int = None,
    l: float = None,
    m: float = None,
    v: bool = None,
    interval: int = None,
    max_pos: int = None,
    h: bool = None,
    version: bool = None,
    dbg_put_db: bool = None,
    cmd: bool = None,
    task: int = None,
    dbg_level: int = None) \
        -> (BLAST6Format, CasavaOneEightSingleLanePerSampleDirFmt,
            SAMDirFmt, pd.DataFrame):
    arg_value_dict = locals()

    for arg in arg_value_dict:
        if arg in ['blast', 'fastx', 'sam', 'otu_map'] and \
                arg_value_dict[arg] is None:
            arg_value_dict[arg] = 1

    return align(**arg_value_dict)


def denovo_otu_mapping(
    ref: DNAFASTAFormat,
    reads: CasavaOneEightSingleLanePerSampleDirFmt,
    workdir: str = None,
    kvdb: str = None,
    idx_dir: str = None,
    readb: str = None,
    fastx: bool = None,
    sam: bool = None,
    sq: bool = None,
    blast: str = None,
    aligned: str = None,
    other: str = None,
    num_alignments: int = None,
    no_best: bool = None,
    min_lis: int = None,
    print_all_reads: bool = None,
    paired: bool = None,
    paired_in: bool = None,
    paired_out: bool = None,
    out2: bool = None,
    sout: bool = None,
    zip_out: bool = None,
    match: int = None,
    mismatch: int = None,
    gap_open: int = None,
    gap_ext: int = None,
    e: float = None,
    f: bool = None,
    n: bool = None,
    r: bool = None,
    id: float = None,
    coverage: float = None,
    de_novo_otu: bool = None,
    otu_map: bool = None,
    passes: str = None,
    edges: int = None,
    num_seeds: bool = None,
    full_search: int = None,
    pid: bool = None,
    a: int = None,
    threads: int = None,
    index: int = None,
    l: float = None,
    m: float = None,
    v: bool = None,
    interval: int = None,
    max_pos: int = None,
    h: bool = None,
    version: bool = None,
    dbg_put_db: bool = None,
    cmd: bool = None,
    task: int = None,
    dbg_level: int = None) \
        -> (BLAST6Format, CasavaOneEightSingleLanePerSampleDirFmt,
            SAMDirFmt, pd.DataFrame, CasavaOneEightSingleLanePerSampleDirFmt):

    arg_value_dict = locals()

    for arg in arg_value_dict:
        if arg in ['blast', 'fastx', 'sam', 'otu_map', 'de_novo_otu'] and \
                arg_value_dict[arg] is None:
            arg_value_dict[arg] = 1

    return align(**arg_value_dict)
