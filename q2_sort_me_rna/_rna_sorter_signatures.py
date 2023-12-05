import pandas as pd

from q2_types.feature_data import BLAST6Format
from q2_types.per_sample_sequences import CasavaOneEightSingleLanePerSampleDirFmt

from q2_types_genomics.per_sample_data import SAMDirFmt

from q2_sort_me_rna._rna_sorter import sort_rna

def sort_rna_blast(
            ref: str, 
            reads: str,
            
            workdir: str = 'out',
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
            
            h: bool  = None,
            version: bool = None,
            
            dbg_put_db: bool = None,
            cmd: bool = None,
            task: int = None,
            dbg_level: int = None, 
            ) -> BLAST6Format:

    arg_value_dict = locals()
    return sort_rna(**arg_value_dict)

def sort_rna_fastx(
            ref: str, 
            reads: str,
            
            workdir: str = 'out',
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
            
            h: bool  = None,
            version: bool = None,
            
            dbg_put_db: bool = None,
            cmd: bool = None,
            task: int = None,
            dbg_level: int = None, 
            ) -> CasavaOneEightSingleLanePerSampleDirFmt:

    arg_value_dict = locals()
    return sort_rna(**arg_value_dict)

def sort_rna_sam(
            ref: str, 
            reads: str,
            
            workdir: str = 'out',
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
            
            h: bool  = None,
            version: bool = None,
            dbg_put_db: bool = None,
            cmd: bool = None,
            task: int = None,
            dbg_level: int = None, 
            ) -> SAMDirFmt:

    arg_value_dict = locals()
    return sort_rna(**arg_value_dict)

def sort_rna_otu(
            ref: str, 
            reads: str,
            
            workdir: str = 'out',
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
            
            h: bool  = None,
            version: bool = None,
            dbg_put_db: bool = None,
            cmd: bool = None,
            task: int = None,
            dbg_level: int = None, 
            ) -> pd.DataFrame:

    arg_value_dict = locals()
    return sort_rna(**arg_value_dict)
