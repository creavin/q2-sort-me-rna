# ----------------------------------------------------------------------------
# Copyright (c) 2016-2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import subprocess
import pandas as pd
import os
import gzip
import shutil
from typing import Union

from q2_types.feature_data import FeatureData, BLAST6
from q2_types.feature_data import BLAST6Format
from q2_types.per_sample_sequences import CasavaOneEightSingleLanePerSampleDirFmt

DEBUG = True

def sort_rna(
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
            id: float = None, # documentation is wrong, must be a float
            coverage: float = None, # documentation is wrong, must be a float
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
            ) -> Union[(BLAST6Format, CasavaOneEightSingleLanePerSampleDirFmt, pd.DataFrame)]:

    if DEBUG:
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

    if True:
        command_string = f'{command}{command_delimiter}{" ".join(parameters)}'
        try:
            subprocess.run(command_string, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {e}")
            raise e
        except Exception as e:
            print(f"An error occurred: {e}")
            raise e

    # Handle Output
    output_files = os.listdir(f'{workdir}/out')
    for file in output_files:
        extension = os.path.splitext(file)[1]
        if extension == '.log': # TODO handle log file
            continue

        if file == 'aligned.blast':
            blast_fmt = BLAST6Format()
            print(blast_fmt)
            shutil.copy(f'{workdir}/out/aligned.blast', f"{str(blast_fmt)}")
            print(blast_fmt.view(pd.DataFrame))
            return blast_fmt

        # TODO handle case where already gzipped
        if extension == '.fq':
            fastq_fmt = CasavaOneEightSingleLanePerSampleDirFmt()

            _gzip_file(f'{workdir}/out/aligned.fq', f'{workdir}/out/aligned.fastq.gz')
            shutil.copy(f'{workdir}/out/aligned.fastq.gz', f"{str(fastq_fmt)}/sample_name_L999_R1_001.fastq.gz")

            print(f"fastq_fmt: {fastq_fmt}")
            print(f"fastq_fmt manifest: \n{fastq_fmt.manifest}")

            return fastq_fmt

        # TODO impl correctly
        if file == 'otu_map.txt':
            # otu_map_fmt = FeatureData[BLAST6]()
            # shutil.copy(f'{workdir}/out/otu_map.txt', f"{str(otu_map_fmt)}")

            # print(f"otu_map_fmt: {otu_map_fmt}")
            # print(f"otu_map_fmt view: \n{otu_map_fmt.view(pd.DataFrame)}")
            # return otu_map_fmt
            df = pd.read_table(f'{workdir}/out/otu_map.txt', sep='\t', header=None)
            return df


        # TODO: No SAMfmt. This is a dummy impl
        if extension == '.sam':
            sam_fmt = CasavaOneEightSingleLanePerSampleDirFmt()

            shutil.copy(f'{workdir}/out/aligned.sam', f"{str(sam_fmt)}/sample_name_L999_R1_001.sam")

            print(f"sam_fmt: {sam_fmt}")
            print(f"sam_fmt manifest: \n{sam_fmt.manifest}")

            return sam_fmt
        

def _gzip_file(input_file, output_file):
    with open(input_file, 'rb') as f_in:
        with gzip.open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)