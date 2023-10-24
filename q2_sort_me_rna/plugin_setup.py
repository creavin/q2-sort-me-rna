# ----------------------------------------------------------------------------
# Copyright (c) 2016-2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import q2_sort_me_rna
from q2_sort_me_rna import _rna_sorter as rna_sorter

from qiime2.plugin import (Plugin, Str, SemanticType, Choices, Int, Bool, Range,
                           Float, Set, Visualization, Metadata, MetadataColumn,
                           Categorical, Numeric, Citations)
from q2_types.ordination import PCoAResults

citations = Citations.load('citations.bib', package='q2_diversity')

plugin = Plugin(
    name='sort-me-rna',
    version=q2_sort_me_rna.__version__,
    website='https://github.com/qiime2/q2-sort-me-rna',
    package='q2_sort_me_rna',
    description=('Plugin for calling SortMeRNA.'),  # TODO expand
    short_description='Plugin for calling SortMeRNA.',
)

phrase = SemanticType('Phrase')
plugin.register_semantic_types(phrase)

plugin.methods.register_function(
    function=rna_sorter.foobar,
    inputs={},
    parameters={
        'echo_phrase': Str,
    },
    outputs=[
        ('semantic_echo_phrase', phrase),
    ],
    input_descriptions={},
    parameter_descriptions={
        'echo_phrase': ('dummy test to be printed')
    },
    output_descriptions={
        'semantic_echo_phrase': ("semantic type of the echo phrase")
    },
    name='Foobar test method',
    description=('This is a test method that does nothing but print the input')
)
