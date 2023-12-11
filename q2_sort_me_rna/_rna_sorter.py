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
        workdir: str,
        # [COMMON]
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
    parameters = _parse_parameters(arg_value_dict)
    command_string = f'{command} {" ".join(parameters)}'

    _call_shell_command(command_string)

    smr_output_dir = f'{workdir}/out'
    smr_output_files = os.listdir(f'{smr_output_dir}')

    for smr_file in smr_output_files:
        extension = os.path.splitext(smr_file)[1]

        if extension == '.blast':
            blast_aligned_seq = _construct_blast_fmt(smr_output_dir, smr_file)
        elif extension == '.fq':
            fastx_aligned_seq = _construct_fastx_fmt(smr_output_dir, smr_file)
        elif extension == '.sam':
            sam_aligned_seq = _construct_sam_fmt(smr_output_dir, smr_file)
        elif smr_file == 'otu_map.txt':
            otu_mapping = _construct_otu_mapping(smr_output_dir, smr_file)

    if 'otu_mapping' in locals():
        return blast_aligned_seq, fastx_aligned_seq, \
            sam_aligned_seq, otu_mapping
    else:
        return blast_aligned_seq, fastx_aligned_seq, sam_aligned_seq


def _parse_parameters(arg_value_dict):
    uppercase_args = ['sq', 'f', 'n', 'r', 'l']
    hyphenated_args = ['idx_dir', 'no_best', 'zip_out', 'dbg_level']
    hard_coded_args = ['blast', 'fastx', 'sam']
    parameters = []

    # Assumption that the transformations are mutually exclusive
    for arg in arg_value_dict:
        # Always set to true so all alignment types are produced
        if arg in hard_coded_args:
            arg_value_dict[arg] = 1

        if not (value := arg_value_dict[arg]) or arg == "arg_value_dict":
            continue
        elif arg in hyphenated_args:
            # Some SortMe params must be hyphenated e.g idx_dir -> idx-dir
            arg = arg.replace('_', '-')
        elif arg in uppercase_args:
            # Some SortMe params must be uppercase # e.g sq -> SQ
            arg = arg.upper()
        
        # Single char args use "-" instead of "--" e.g -e, -f, -h
        if len(arg) == 1:
            parameters.append(f'-{arg} {value}')
        else:
            parameters.append(f'--{arg} {value}')

    return parameters


def _call_shell_command(command_string):
    try:
        subprocess.run(command_string, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        raise e
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e


def _construct_blast_fmt(smr_output_dir, file):
    blast_fmt = BLAST6Format()
    shutil.copy(f'{smr_output_dir}/{file}', f"{str(blast_fmt)}")
    return blast_fmt


def _construct_fastx_fmt(smr_output_dir, file):
    # TODO handle case where already gzipped
    fastq_fmt = CasavaOneEightSingleLanePerSampleDirFmt()

    _gzip_file(f'{smr_output_dir}/aligned.fq',
               f'{smr_output_dir}/aligned.fastq.gz')
    shutil.copy(f'{smr_output_dir}/aligned.fastq.gz',
                f"{str(fastq_fmt)}/sample_name_L999_R1_001.fastq.gz")

    print(f"fastq_fmt: {fastq_fmt}")
    print(f"fastq_fmt manifest: \n{fastq_fmt.manifest}")

    return fastq_fmt


def _construct_sam_fmt(smr_output_dir, file):
    sam_fmt = SAMDirFmt()
    shutil.copy(f'{smr_output_dir}/aligned.sam', f"{str(sam_fmt)}")

    return sam_fmt


def _construct_otu_mapping(smr_output_dir, file):
    in_file = f'{smr_output_dir}/otu_map.txt'
    out_file = f'{smr_output_dir}/processed_otu_map.txt'

    awk_command = \
        f"awk -F'\t' '{{print $1, NF-1}}' {in_file} > {out_file}"
    subprocess.run(awk_command, shell=True)
    mapping = pd.read_csv(out_file, index_col='Ref Sequence',
                          sep=' ', names=['Ref Sequence', 'Count'])

    return mapping


def _gzip_file(input_file, output_file):
    with open(input_file, 'rb') as f_in:
        with gzip.open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

