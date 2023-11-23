from typing import Union

from q2_types.feature_data import BLAST6Format
from q2_types.per_sample_sequences import CasavaOneEightSingleLanePerSampleDirFmt

from ._rna_sorter import sort_rna

def sort_rna_union(
            ref: str, 
            reads: str,
            # [COMMON]
            workdir: str = 'out',
            kvdb: str = None,
            idx_dir: str = None, # hyphenated
            readb: str = None,
            fastx: bool = None,
            sam: bool = None,
            sq: bool = None,
            blast: str = None,
            aligned: str = None, # string/bool
            other: str = None, # string/bool
            num_alignments: int = None, 
            no_best: bool = None, # TODO needs to by hyphenated, check if mistake
            min_lis: int = None,
            print_all_reads: bool = None,
            paired: bool = None,
            paired_in: bool = None,
            paired_out: bool = None,
            out2: bool = None,
            sout: bool = None,
            zip_out: bool = None, # TODO needs to by hyphenated, check if mistake
            match: int = None,
            mismatch: int = None,
            gap_open: int = None,
            gap_ext: int = None,
            e: float = None,
            f: bool = None,
            n: bool = None,
            r: bool = None,
            # [OTU_PICKING]
            id: int = None,
            coverage: int = None,
            de_novo_otu: bool = None,
            otu_map: bool = None,
            # [ADVANCED]
            passes: str = None, # (int,int,int)
            edges: int = None,
            num_seeds: bool = None,
            full_search: int = None,
            pid: bool = None,
            a: int = None,
            threads: int = None,
            # [INDEXING]
            index: int = None,
            l: float = None,
            m: float = None,
            v: bool = None,
            interval: int = None,
            max_pos: int = None,
            # [HELP]
            h: bool  = None,
            version: bool = None,
            # [DEVELOPER]
            dbg_put_db: bool = None,
            cmd: bool = None,
            task: int = None,
            dbg_level: int = None, # hyphenated
            # ) -> CasavaOneEightSingleLanePerSampleDirFmt:
            ) -> Union[BLAST6Format, CasavaOneEightSingleLanePerSampleDirFmt]:
    kwargs = locals()
    return sort_rna(**kwargs)

# Alias for sort_rna with BLAST6Format return type
sort_rna_blast = sort_rna_union

# Alias for sort_rna with CasavaOneEightSingleLanePerSampleDirFmt return type
sort_rna_casava = sort_rna_union
