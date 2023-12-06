# ----------------------------------------------------------------------------
# Copyright (c) 2016-2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from qiime2.plugin import Plugin, Str, Bool, Int, Float, Citations
from q2_types.sample_data import SampleData
from q2_types.per_sample_sequences import SequencesWithQuality
from q2_types.feature_data import  BLAST6, FeatureData
from q2_types.feature_table import FeatureTable, Frequency
from q2_types_genomics.per_sample_data import SequenceAlignmentMap

import q2_sort_me_rna
from q2_sort_me_rna import _rna_sorter_signatures as rna_sorter
from q2_sort_me_rna import _rna_sorter as true_rna_sorter


plugin = Plugin(
    name='sort-me-rna',
    version=q2_sort_me_rna.__version__,
    website='https://github.com/qiime2/q2-sort-me-rna',
    package='q2_sort_me_rna',
    description=('Plugin for calling SortMeRNA.'),  # TODO expand
    short_description='Plugin for calling SortMeRNA.',
)


citations = Citations.load('citations.bib', package='q2_sort_me_rna')

all_sort_me_rna_parameters = {
        'ref': Str,
        'reads': Str,
        'workdir': Str,
        'kvdb': Str,
        'idx_dir': Str,
        'readb': Str,
        'fastx': Bool,
        'sam': Bool,
        'sq': Bool,
        'blast': Str,
        'aligned': Str, # string/bool
        'other': Str, # string/bool
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
        'id': Float, # documentation is wrong, must be a float
        'coverage': Float, # documentation is wrong, must be a float
        'de_novo_otu': Bool,
        'otu_map': Bool,
         # [ADVANCED]
        'passes': Str, # "INT,INT,INT"
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
        'h': Bool ,
        'version': Bool,
         # [DEVELOPER]
        'dbg_put_db': Bool,
        'cmd': Bool,
        'task': Int,
        'dbg_level': Int
}

plugin.methods.register_function(
    function=true_rna_sorter.sort_rna,
    inputs={},
    parameters=all_sort_me_rna_parameters,
    outputs=[ 
        ('blast_aligned_seq', FeatureData[BLAST6]),
        ('fastx_aligned_seq', SampleData[SequencesWithQuality]),
        ('sam_aligned_seq', SampleData[SequenceAlignmentMap]),
        ('otu_mapping', FeatureTable[Frequency]),
        # ('', FeatureData[BLAST6]),
        ],
    input_descriptions={},
    parameter_descriptions={
    },
    output_descriptions={
    },
    name='Foobar test method',
    description=('This is a test method that does nothing but print the input')
)

plugin.methods.register_function(
    function=rna_sorter.sort_rna_blast,
    inputs={},
    parameters=all_sort_me_rna_parameters,
    outputs=[ ('aligned_seq', FeatureData[BLAST6])],
    input_descriptions={},
    parameter_descriptions={
    },
    output_descriptions={
        'aligned_seq': "foobar"
    },
    name='Foobar test method',
    description=('This is a test method that does nothing but print the input')
)

plugin.methods.register_function(
    function=rna_sorter.sort_rna_fastx,
    inputs={},
    parameters=all_sort_me_rna_parameters,
    outputs=[ ('aligned_seq', SampleData[SequencesWithQuality])],
    input_descriptions={},
    parameter_descriptions={
    },
    output_descriptions={
        'aligned_seq': "foobar"
    },
    name='Foobar test method',
    description=('This is a test method that does nothing but print the input')
)

plugin.methods.register_function(
    function=rna_sorter.sort_rna_sam,
    inputs={},
    parameters=all_sort_me_rna_parameters,
    outputs=[ ('aligned_seq', SampleData[SequenceAlignmentMap])],
    input_descriptions={},
    parameter_descriptions={
    },
    output_descriptions={
        'aligned_seq': "foobar"
    },
    name='Foobar test method',
    description=('This is a test method that does nothing but print the input')
)

plugin.methods.register_function(
    function=rna_sorter.sort_rna_otu,
    inputs={},
    parameters=all_sort_me_rna_parameters,
    outputs=[ ('aligned_seq',FeatureTable[Frequency])],
    input_descriptions={},
    parameter_descriptions={
    },
    output_descriptions={
        'aligned_seq': "foobar"
    },
    name='Foobar test method',
    description=('This is a test method that does nothing but print the input')
)

