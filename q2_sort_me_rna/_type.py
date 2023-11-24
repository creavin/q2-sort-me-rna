# ----------------------------------------------------------------------------
# Copyright (c) 2020-2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from qiime2.plugin import SemanticType


import qiime2.plugin.model as model
from q2_types.feature_data import BLAST6Format

class SMROutput(model.DirectoryFormat):
    forward = model.File(r'aligned.blast', format=BLAST6Format)


SMROutputArtifacts = SemanticType('SMROutputArtifacts')
