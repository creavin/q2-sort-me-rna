# ----------------------------------------------------------------------------
# Copyright (c) 2016-2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import re
import shutil
import subprocess
import os
import tempfile
import unittest

class TestSortRNA(unittest.TestCase):

    def setUp(self):
        self.q2smr_output_dir = tempfile.mkdtemp()
        self.q2smr_output_artifact_path = f'{self.q2smr_output_dir}/qiime-output.qza'


    def tearDown(self):
        shutil.rmtree(self.q2smr_output_dir)


    def test_sort_rna_end_to_end_blas(self):
        command = [
            'qiime', 'sort-me-rna', 'sort-rna-blast',
            '--p-ref', './rrna_references.fasta',
            '--p-reads', './synthetic_data.fastq',
            '--p-workdir', self.q2smr_output_dir,
            '--o-aligned-seq', self.q2smr_output_artifact_path
        ]

        subprocess.run(command, check=True)

        self.assertIn('qiime-output.qza', os.listdir(self.q2smr_output_dir), "Expected file is not present")

        expected_meta_data = {
            'Type': 'FeatureData[BLAST6]',
            'format': 'BLAST6DirectoryFormat',
        }
        self._validate_artifact_type(self.q2smr_output_artifact_path, expected_meta_data)


    def test_sort_rna_end_to_end_fastx(self):
        command = [
            'qiime', 'sort-me-rna', 'sort-rna-fastx',
            '--p-ref', './rrna_references.fasta',
            '--p-reads', './synthetic_data.fastq',
            '--p-fastx', 'true',
            '--p-workdir', self.q2smr_output_dir,
            '--o-aligned-seq', self.q2smr_output_artifact_path
        ]

        subprocess.run(command, check=True)

        self.assertIn('qiime-output.qza', os.listdir(self.q2smr_output_dir), "Expected file is not present")

        expected_meta_data = {
            'Type': 'SampleData[SequencesWithQuality]',
            'format': 'SingleLanePerSampleSingleEndFastqDirFmt',
        }
        self._validate_artifact_type(self.q2smr_output_artifact_path, expected_meta_data)


    def _validate_artifact_type(self, file, expected_meta_data):
        command = [
            'qiime', 'tools', 'peek', file
        ]

        output = subprocess.run(command, check=True, stdout=subprocess.PIPE, text=True)

        key_value_pairs = re.findall(r'(\S+):\s+(\S+)', output.stdout)
        result_dict = dict(key_value_pairs)

        for key, value in expected_meta_data.items():
            self.assertEqual(result_dict[key], value, 
                             "Artifact metadata does not match the expected values")

if __name__ == '__main__':
    unittest.main()
