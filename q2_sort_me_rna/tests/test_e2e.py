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
        # TODO copy test assets to tmp dir
        self.q2smr_output_dir = tempfile.mkdtemp()
        self.q2smr_output_artifacts_dir = \
            f'{self.q2smr_output_dir}/qiime-output'

    def tearDown(self):
        shutil.rmtree(self.q2smr_output_dir)

    def test_sort_rna_end_to_end(self):
        command = [
            'qiime', 'sort-me-rna', 'sort-rna-all',
            '--p-ref', './rrna_references.fasta',
            '--p-reads', './synthetic_data.fastq',
            '--p-workdir', self.q2smr_output_dir,
            '--output-dir', self.q2smr_output_artifacts_dir
        ]

        subprocess.run(command, check=True)

        expected_artifacts = [
            "blast_aligned_seq.qza",
            "fastx_aligned_seq.qza",
            "sam_aligned_seq.qza"
        ]

        files = os.listdir(self.q2smr_output_artifacts_dir)
        for artifact in expected_artifacts:
            self.assertIn(artifact, files, "Expected file is not present")

        # expected_meta_data = {
        #     'Type': 'FeatureData[BLAST6]',
        #     'format': 'BLAST6DirectoryFormat',
        # }
        # TODO re-impl
        # self._validate_artifact_type(
        # self.q2smr_output_artifact_path, expected_meta_data)

    def test_otu_mapping_end_to_end(self):
        command = [
            'qiime', 'sort-me-rna', 'otu-mapping',
            '--p-ref', './rrna_references.fasta',
            '--p-reads', './synthetic_data.fastq',
            '--p-otu-map', 'true',
            '--p-id', '0.12',
            '--p-coverage', '0.12',
            '--p-workdir', self.q2smr_output_dir,
            '--output-dir', self.q2smr_output_artifacts_dir
        ]

        subprocess.run(command, check=True)

        expected_artifacts = [
            "blast_aligned_seq.qza",
            "fastx_aligned_seq.qza",
            "sam_aligned_seq.qza",
            "otu_mapping.qza",
        ]

        for artifact in expected_artifacts:
            files = os.listdir(self.q2smr_output_artifacts_dir)
            self.assertIn(artifact, files, "Expected file is not present")

        # expected_meta_data = {
        #     'Type': 'FeatureData[BLAST6]',
        #     'format': 'BLAST6DirectoryFormat',
        # }
        # TODO re-impl
        # self._validate_artifact_type(
        # self.q2smr_output_artifact_path, expected_meta_data)

    def _validate_artifact_type(self, file, expected_meta_data):
        command = [
            'qiime', 'tools', 'peek', file
        ]

        output = subprocess.run(command, check=True,
                                stdout=subprocess.PIPE, text=True)

        key_value_pairs = re.findall(r'(\S+):\s+(\S+)', output.stdout)
        result_dict = dict(key_value_pairs)

        err_msg = "Artifact metadata does not match the expected values"
        for key, value in expected_meta_data.items():
            self.assertEqual(result_dict[key], value, err_msg)


if __name__ == '__main__':
    unittest.main()
