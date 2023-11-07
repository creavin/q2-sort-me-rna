# ----------------------------------------------------------------------------
# Copyright (c) 2016-2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import subprocess
import pandas as pd


def sort_rna(ref: str, 
            reads: str,
            # COMMON
            workdir: str = 'out',
            kvdb: str = None,
            idx_dir: str = None, # hyphenated
            readb: str = None,
            fastx: bool = None,
            sam: bool = None,
            sq: bool = None,
            blast: str = None,
            #  aligned = None, # string/bool
            #  other = None, # string/bool
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
            # passes = None, (int, int, int)
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
            # ) -> FeatureData[BLAST6]:
            ) -> pd.DataFrame:
    arg_value_dict = locals()
    print(locals())

    command = 'sortmerna'
    command_delimiter = ' '
    parameters = []

    uppercase_args = ['sq', 'f', 'n', 'r', 'l']
    hyphenated_args = ['idx_dir', 'no_best', 'zip_out', 'dbg_level']

    for arg in arg_value_dict:
        if not (value := arg_value_dict[arg]) or arg == "arg_value_dict":
            continue

        if arg in hyphenated_args:
            arg = arg.replace('_', '-') # e.g idx_dir -> idx-dir

        if arg in uppercase_args:
            arg = arg.upper() # e.g sq -> SQ

        if len(arg) == 1: # single letter args use "-" e.g -e, -f, -h
            parameters.append(f'-{arg} {value}')
        else:
            parameters.append(f'--{arg} {value}')

    command_string = f'{command}{command_delimiter}{" ".join(parameters)}'
    try:
        subprocess.run(command_string, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        raise e
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e
        
    return pd.read_csv(f'{workdir}/out/aligned.blast', sep='\t', header=None)
    # return Artifact.import_data('FeatureData[BLAST6]', './out/out/aligned.blast')
    # return pd.DataFrame()
    # asx = SemanticType('aligned_seq')
    # return Artifact.import_data(asx, view="./out/out/aligned.blast")
    # return FeatureData[BLAST6]
    # return SemanticType('aligned_seq')
    # return DirectoryFormat("./out", "r")
