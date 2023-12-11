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

from q2_types.feature_data import BLAST6Format
from q2_types.per_sample_sequences \
    import CasavaOneEightSingleLanePerSampleDirFmt

from q2_types_genomics.per_sample_data import SAMDirFmt


def sort_rna(
        ref: str,
        reads: str,
        # [COMMON]
        workdir: str = 'out',
        kvdb: str = None,
        idx_dir: str = None,  # hyphenated
        readb: str = None,
        fastx: bool = None,
        sam: bool = None,
        sq: bool = None,
        blast: str = None,
        aligned: str = None,  # string/bool
        other: str = None,  # string/bool
        num_alignments: int = None,
        no_best: bool = None,  # TODO needs to by hyphenated, check if mistake
        min_lis: int = None,
        print_all_reads: bool = None,
        paired: bool = None,
        paired_in: bool = None,
        paired_out: bool = None,
        out2: bool = None,
        sout: bool = None,
        zip_out: bool = None,  # TODO needs to by hyphenated, check if mistake
        match: int = None,
        mismatch: int = None,
        gap_open: int = None,
        gap_ext: int = None,
        e: float = None,
        f: bool = None,
        n: bool = None,
        r: bool = None,
        # [OTU_PICKING]
        id: float = None,  # documentation is wrong, must be a float
        coverage: float = None,  # documentation is wrong, must be a float
        de_novo_otu: bool = None,
        otu_map: bool = None,
        # [ADVANCED]
        passes: str = None,  # (int,int,int)
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
        h: bool = None,
        version: bool = None,
        # [DEVELOPER]
        dbg_put_db: bool = None,
        cmd: bool = None,
        task: int = None,
        dbg_level: int = None,  # hyphenated
        ):

    arg_value_dict = locals()

    command = 'sortmerna'
    parameters = []

    uppercase_args = ['sq', 'f', 'n', 'r', 'l']
    hyphenated_args = ['idx_dir', 'no_best', 'zip_out', 'dbg_level']
    hard_coded_args = ['blast', 'fastx', 'sam']

    for arg in arg_value_dict:
        if arg in hard_coded_args:
            arg_value_dict[arg] = 1

        if not (value := arg_value_dict[arg]) or arg == "arg_value_dict":
            continue

        if arg in hyphenated_args:
            arg = arg.replace('_', '-')  # e.g idx_dir -> idx-dir

        if arg in uppercase_args:
            arg = arg.upper()  # e.g sq -> SQ

        if len(arg) == 1:  # single letter args use "-" e.g -e, -f, -h
            parameters.append(f'-{arg} {value}')
        else:
            parameters.append(f'--{arg} {value}')

    command_string = f'{command} {" ".join(parameters)}'
    try:
        subprocess.run(command_string, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        raise e
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e

    output_files = os.listdir(f'{workdir}/out')

    for file in output_files:
        extension = os.path.splitext(file)[1]

        if extension == '.blast':
            blast_fmt = BLAST6Format()
            print(blast_fmt)
            shutil.copy(f'{workdir}/out/aligned.blast', f"{str(blast_fmt)}")
            print(blast_fmt.view(pd.DataFrame))
            # return blast_fmt
            blast_aligned_seq = blast_fmt

        # TODO handle case where already gzipped
        if extension == '.fq':
            fastq_fmt = CasavaOneEightSingleLanePerSampleDirFmt()

            _gzip_file(f'{workdir}/out/aligned.fq',
                       f'{workdir}/out/aligned.fastq.gz')
            shutil.copy(f'{workdir}/out/aligned.fastq.gz',
                        f"{str(fastq_fmt)}/sample_name_L999_R1_001.fastq.gz")

            print(f"fastq_fmt: {fastq_fmt}")
            print(f"fastq_fmt manifest: \n{fastq_fmt.manifest}")

            fastx_aligned_seq = fastq_fmt
            # return fastq_fmt

        if extension == '.sam':
            sam_fmt = SAMDirFmt()
            shutil.copy(f'{workdir}/out/aligned.sam', f"{str(sam_fmt)}")

            sam_aligned_seq = sam_fmt

        if file == 'otu_map.txt':
            in_file = f'{workdir}/out/otu_map.txt'
            out_file = f'{workdir}/out/processed_otu_map.txt'

            awk_command = \
                f"awk -F'\t' '{{print $1, NF-1}}' {in_file} > {out_file}"
            subprocess.run(awk_command, shell=True)
            df = pd.read_csv(out_file, index_col='Ref Sequence',
                             sep=' ', names=['Ref Sequence', 'Count'])

            otu_mapping = df

    if 'otu_mapping' in locals() and otu_mapping is not None:
        return blast_aligned_seq, fastx_aligned_seq, \
            sam_aligned_seq, otu_mapping
    else:
        return blast_aligned_seq, fastx_aligned_seq, sam_aligned_seq


def _gzip_file(input_file, output_file):
    with open(input_file, 'rb') as f_in:
        with gzip.open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
