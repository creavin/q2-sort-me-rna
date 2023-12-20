# ----------------------------------------------------------------------------
# Copyright (c) 2016-2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from setuptools import setup, find_packages
import versioneer

setup(
    name="q2-sort-me-rna",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(),
    author="Thomas Creavin",
    author_email="thomas.creavin@gmail.com",
    description="A QIIME 2 wrapper for the sequence alignment tool SortMeRNA.",
    license='BSD-3-Clause',
    url='https://qiime2.org',
    entry_points={
        'qiime2.plugins': [
            'q2-sort-me-rna=q2_sort_me_rna.plugin_setup:plugin'
        ],
    },
    zip_safe=False,
)
