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
    description="QIIME 2 plugin for SortMeRNA",
    license='BSD-3-Clause',
    url='https://qiime2.org',
    entry_points={
        'qiime2.plugins':
        ['q2-sort-me-rna=q2_sort_me_rna.plugin_setup:plugin']
        # TODO create and connect to entry point
    },
    package_data={
        'q2_sort_me_rna': [  # TODO remove these templates if not used
            # 'assets/index.html', 'citations.bib'  # TODO add assets
            'templates/*.html',
            'templates/assets/css/*.css',
            'templates/assets/js/*.js',
            'templates/assets/img/*.png',
            'templates/assets/fonts/glyphicons-*'
        ]
    },
    zip_safe=False,
)
