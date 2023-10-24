# ----------------------------------------------------------------------------
# Copyright (c) 2016-2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import unittest
import q2_sort_me_rna._rna_sorter as rna_sorter

from qiime2.plugin import SemanticType

# from q2_sort_me_rna import df_to_html


class TestSortMeRNA(unittest.TestCase):
    def test_pytest_runs(self):
        self.assertEqual(0, 0)

    def test_foobar(self):
        result = rna_sorter.foobar("Yeet")
        self.assertEqual(result, SemanticType('Phrase'))


if __name__ == "__main__":
    unittest.main()
