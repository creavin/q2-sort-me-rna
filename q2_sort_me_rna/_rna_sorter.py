# ----------------------------------------------------------------------------
# Copyright (c) 2016-2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from .util import dummy_func
from qiime2.plugin import SemanticType


def foobar(echo_phrase: str) -> None:
    """Render user provided source files into a QIIME 2 visualization template.


    Parameters
    ----------
    source_files : str, or list of str
        Files to be rendered and written to the output_dir.
    output_dir : str
        The output_dir provided to a visualiation function by the QIIME 2
        framework.
    context : dict, optional
        The context dictionary to be rendered into the source_files. The
        same context will be provided to all templates being rendered.

    """
    print(echo_phrase)

    dummy_func()

    return SemanticType('Phrase')
