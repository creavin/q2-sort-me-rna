# ----------------------------------------------------------------------------
# Copyright (c) 2016-2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from qiime2.plugin import Plugin, Str, Bool, Int, Float, Citations, TypeMatch
from q2_types.sample_data import SampleData
from q2_types.per_sample_sequences \
    import SequencesWithQuality, PairedEndSequencesWithQuality
from q2_types.feature_data import BLAST6, FeatureData, Sequence
from q2_types.feature_table import FeatureTable, Frequency
from q2_types_genomics.per_sample_data import SequenceAlignmentMap

import q2_sort_me_rna
from q2_sort_me_rna import _rna_sorter_signatures as rna_sorter


plugin = Plugin(
    name='sort-me-rna',
    version=q2_sort_me_rna.__version__,
    website='https://github.com/qiime2/q2-sort-me-rna',
    package='q2_sort_me_rna',
    description=('A QIIME2 wrapper for the sequence alignment ' +
                 'tool SortMeRNA.'),
    short_description='A QIIME2 wrapper for the sequence alignment ' +
                      'tool SortMeRNA.',
)

citations = Citations.load('citations.bib', package='q2_sort_me_rna')

# The parameters names are chosen to match the sortmerna man page
# To be consistent, the names are lowercased and hyphens are underscores
all_sort_me_rna_parameters = {
        'workdir': Str,
        'kvdb': Str,
        'idx_dir': Str,
        'readb': Str,
        'fastx': Bool,
        'sam': Bool,
        'sq': Bool,
        'blast': Str,
        'aligned': Str,  # string/bool
        'other': Str,  # string/bool
        'num_alignments': Int,
        'no_best': Bool,
        'min_lis': Int,
        'print_all_reads': Bool,
        'paired': Bool,
        'paired_in': Bool,
        'paired_out': Bool,
        'out2': Bool,
        'sout': Bool,
        'zip_out': Bool,
        'match': Int,
        'mismatch': Int,
        'gap_open': Int,
        'gap_ext': Int,
        'e': Float,
        'f': Bool,
        'n': Bool,
        'r': Bool,
        # [OTU_PICKING]
        'id': Float,  # SMR documentation is wrong, must be a float
        'coverage': Float,  # SMR documentation is wrong, must be a float
        'de_novo_otu': Bool,
        'otu_map': Bool,
        # [ADVANCED]
        'passes': Str,  # "INT,INT,INT"
        'edges': Int,
        'num_seeds': Bool,
        'full_search': Int,
        'pid': Bool,
        'a': Int,
        'threads': Int,
        # [INDEXING]
        'index': Int,
        'l': Float,
        'm': Float,
        'v': Bool,
        'interval': Int,
        'max_pos': Int,
        # [HELP]
        'h': Bool,
        'version': Bool,
        # [DEVELOPER]
        'dbg_put_db': Bool,
        'cmd': Bool,
        'task': Int,
        'dbg_level': Int
}

T = TypeMatch([SequencesWithQuality, PairedEndSequencesWithQuality])
plugin.methods.register_function(
    function=rna_sorter.align_sequences,
    inputs={
        'ref': FeatureData[Sequence],
        'reads': SampleData[T]
    },
    parameters=all_sort_me_rna_parameters,
    outputs=[
        ('blast_aligned_seq', FeatureData[BLAST6]),
        ('fastx_aligned_seq', SampleData[SequencesWithQuality]),
        ('sam_aligned_seq', SampleData[SequenceAlignmentMap]),
        ],
    input_descriptions={},
    parameter_descriptions={},
    output_descriptions={
        'blast_aligned_seq': 'Aligned reads in the BLAST format',
        'fastx_aligned_seq': 'Aligned reads in the FASTA/FASTQ format',
        'sam_aligned_seq': 'Aligned reads SAM format'
    },
    name='Align the sequences',
    description=('''
                 For single-ended or paired sequence, align them with respect
                 to a reference sequence database and return all three
                 alignment types: blast, fastx, and sam. Consult the SortMeRNA
                 documentation for more information on the parameters.
                 ''')
)

plugin.methods.register_function(
    function=rna_sorter.otu_mapping,
    inputs={
        'ref': FeatureData[Sequence],
        'reads': SampleData[T]
    },
    parameters=all_sort_me_rna_parameters,
    outputs=[
        ('blast_aligned_seq', FeatureData[BLAST6]),
        ('fastx_aligned_seq', SampleData[SequencesWithQuality]),
        ('sam_aligned_seq', SampleData[SequenceAlignmentMap]),
        ('otu_mapping', FeatureTable[Frequency]),
        ],
    input_descriptions={},
    parameter_descriptions={
    },
    output_descriptions={
        'blast_aligned_seq': 'Aligned reads in the BLAST format',
        'fastx_aligned_seq': 'Aligned reads in the FASTA/FASTQ format',
        'sam_aligned_seq': 'Aligned reads SAM format',
        'otu_mapping': 'OTU map of the aligned reads'
    },
    name='Align and OTU map the sequences',
    description=('''
                 For single-ended or paired sequence, align them with respect
                 to a reference sequence database and return all three
                 alignment types: blast, fastx, and sam.  Additionally,
                 produce an otu mapping of the aligned sequences. Consult the
                 SortMeRNA documentation for more information on the
                 parameters.
                 ''')
)

plugin.methods.register_function(
    function=rna_sorter.denovo_otu_mapping,
    inputs={
        'ref': FeatureData[Sequence],
        'reads': SampleData[T]
    },
    parameters=all_sort_me_rna_parameters,
    outputs=[
        ('blast_aligned_seq', FeatureData[BLAST6]),
        ('fastx_aligned_seq', SampleData[SequencesWithQuality]),
        ('sam_aligned_seq', SampleData[SequenceAlignmentMap]),
        ('otu_mapping', FeatureTable[Frequency]),
        ('denovo_aligned_seq', SampleData[SequencesWithQuality]),
        ],
    input_descriptions={},
    parameter_descriptions={
    },
    output_descriptions={
    },
    name='Align and OTU map (with De Novo reads of) the sequences',
    description=('''
                 For single-ended or paired sequence, align them with respect
                 to a reference sequence database and return all three
                 alignment types: blast, fastx, and sam.  Additionally,
                 produce an otu mapping of the aligned sequences and a fastx
                 file with the de novo reads. Consult the SortMeRNA
                 documentation for more information on the parameters.
                 ''')
)
