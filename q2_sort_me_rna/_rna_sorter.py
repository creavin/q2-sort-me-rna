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
import glob

from q2_types.feature_data import BLAST6Format
from q2_types.per_sample_sequences \
    import CasavaOneEightSingleLanePerSampleDirFmt

from q2_types_genomics.per_sample_data import SAMDirFmt


def sort_rna(
        ref: str,
        reads,
        reads_reverse: str = None,
        workdir: str = None,
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

    # In theory, SortMeRNA can handle gzipped files,
    # but in practice it produces empty files for
    # some outputs (.sam, denovo reads)
    input_file = _get_read_file(reads)
    _un_gzip_file(input_file, f'{arg_value_dict["workdir"]}/reads.fastq')
    arg_value_dict['reads'] = f'{arg_value_dict["workdir"]}/reads.fastq'

    command = 'sortmerna'
    parameters = _parse_parameters(arg_value_dict)
    command_string = f'{command} {" ".join(parameters)}'

    _call_shell_command(command_string)

    smr_output_dir = f'{workdir}/out'
    smr_output_files = os.listdir(f'{smr_output_dir}')

    for smr_file in smr_output_files:
        extension = os.path.splitext(smr_file)[1]
        if _is_gun_zipped(smr_file):
            extension = '.' + smr_file.split('.')[-2]

        if extension == '.blast':
            blast_aligned_seq = _construct_blast_fmt(smr_output_dir, smr_file)
        elif _is_fastx_(extension):
            if _is_denovo_otu(smr_file):
                denovo_otu_aligned_seq = \
                    _construct_fastx_fmt(smr_output_dir,
                                         smr_file, "denovo_aligned_seq")
            else:
                fastx_aligned_seq = \
                    _construct_fastx_fmt(smr_output_dir, smr_file)
        elif extension == '.sam':
            sam_aligned_seq = _construct_sam_fmt(smr_output_dir, smr_file)
        elif smr_file == 'otu_map.txt':
            otu_mapping = _construct_otu_mapping(smr_output_dir, smr_file)

        print(locals())

    result = [blast_aligned_seq, fastx_aligned_seq, sam_aligned_seq]
    if 'otu_mapping' in locals():
        result.append(otu_mapping)

    if 'denovo_otu_aligned_seq' in locals():
        result.append(denovo_otu_aligned_seq)

    return tuple(result)


def _parse_parameters(arg_value_dict):
    uppercase_args = ['sq', 'f', 'n', 'r', 'l']
    hyphenated_args = ['idx_dir', 'no_best', 'zip_out', 'dbg_level']
    duplicate_args = {"reads_reverse": "reads"}
    parameters = []

    # Assumption that the transformations are mutually exclusive
    for arg in arg_value_dict:
        if not (value := arg_value_dict[arg]) or arg == "arg_value_dict":
            continue
        elif arg in hyphenated_args:
            # Some SortMe params must be hyphenated e.g idx_dir -> idx-dir
            arg = arg.replace('_', '-')
        elif arg in uppercase_args:
            # Some SortMe params must be uppercase # e.g sq -> SQ
            arg = arg.upper()
        elif arg in duplicate_args:
            arg = duplicate_args[arg]

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


# TODO: add fasta support
def _construct_fastx_fmt(smr_output_dir, file, output_name="aligned_sequence"):
    if not _is_gun_zipped(file):
        _gzip_file(f'{smr_output_dir}/{file}',
                   f'{smr_output_dir}/{file}.gz')
        file = f'{file}.gz'

    unzipped_extension = '.' + file.split('.')[-2]
    if _is_fastq(unzipped_extension):
        unzipped_extension = '.fastq'
        full_ext = f'{unzipped_extension}.{file.split(".")[-1]}'
        fastx_fmt = CasavaOneEightSingleLanePerSampleDirFmt()
        shutil.copy(f'{smr_output_dir}/{file}',
                    f"{str(fastx_fmt)}/{output_name}_L999_R1_001{full_ext}")
    # elif _is_fasta(unzipped_extension):
    #     unzipped_extension = '.fasta'
    #     full_ext = f'{unzipped_extension}.{file.split(".")[-1]}'
    #     fastx_fmt = DNAFASTAFormat()
    #     shutil.copy(f'{smr_output_dir}/{file}',
    #                 f"{str(fastx_fmt)}/aligned_sequence{full_ext}")
    else:
        raise ValueError(f'Unsupported file type: {unzipped_extension}')

    return fastx_fmt


def _construct_sam_fmt(smr_output_dir, file):
    sam_fmt = SAMDirFmt()

    if _is_gun_zipped(file):
        unzipped_file = os.path.splitext(file)[0]
        _un_gzip_file(f'{smr_output_dir}/{file}',
                      f'{smr_output_dir}/{unzipped_file}')
        file = unzipped_file

    shutil.copy(f'{smr_output_dir}/{file}', f"{str(sam_fmt)}")
    return sam_fmt


def _construct_otu_mapping(smr_output_dir, file):
    in_file = f'{smr_output_dir}/{file}'
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


def _un_gzip_file(gzip_file_path, output_file_path):
    with gzip.open(gzip_file_path, 'rb') as f_in, \
              open(output_file_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)


def _is_gun_zipped(file):
    return os.path.splitext(file)[1] == '.gz'


def _is_denovo_otu(file):
    return "_denovo." in file


def _is_fastx_(extension):
    return _is_fastq(extension) or _is_fasta(extension)


def _is_fastq(extension):
    # https://en.wikipedia.org/wiki/FASTQ_format
    return extension in ('.fq', '.fastq')


def _is_fasta(extension):
    # https://en.wikipedia.org/wiki/FASTA_format
    return extension in ('.fasta', '.fas', '.fa', '.fna', '.ffn',
                         '.faa', '.mpfa', '.frn')


def _get_read_file(reads_artifact):
    gz_files = glob.glob(os.path.join(str(reads_artifact), '*.gz'))

    print("The files are")
    for gz_file in gz_files:
        print(gz_file)

    assert len(gz_files) == 1

    return gz_files[0]
