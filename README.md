# q2-sort-me-rna

![Build Status](https://github.com/qiime2/q2templates/workflows/ci/badge.svg)

## Overview

`q2-sort-me-rna` is a plugin for [QIIME 2](https://qiime2.org/), designed to seamlessly integrate with the [SortMeRNA](https://github.com/sortmerna/sortmerna) package. This plugin accepts all parameters listed in the [SortMeRNA manual](https://sortmerna.readthedocs.io/en/latest/manual4.0.html#usage). Note that the formatting of the plugin parameters differs slightly; they are lowercased and use hyphenation, whereas SortMeRNA uses a mix of underscores and capitalization.

## Limitations

- **Input Format**: SortMeRNA accepts sequence reads in both the FASTA and FASTQ formats. However, this plugin only accepts reads in the FASTQ format. For the reference database, it is perfectly fine to use FASTA.

- **QIIME Types**: QIIME types must be non-empty. During OTU mapping, it is possible for no elements to be mapped, and in this case, an exception will be thrown.

## Examples

Set the location of the input and output artifacts. Ensure that these locations exist before proceeding.

```bash
sortmerna_work_dir = out
q2smr_output_dir = output
art_dir = ./q2_sort_me_rna/tests/assets
seq_dir = ./q2_sort_me_rna/tests/assets/seq
```

### Align the Raw Reads

```bash
qiime sort-me-rna sort-rna \
--i-reads "$(art_dir)/raw_sequence.qza" \
--i-ref "$(art_dir)/rrna_references.qza"  \
--p-workdir "./$(q2smr_output_dir)" \
--output-dir "./$(q2smr_output_dir)/qiime-output" \
--verbose
```

### Align the Raw Reads and Produce an OTU Mapping

```bash
qiime sort-me-rna otu-mapping \
--i-reads "$(art_dir)/raw_sequence.qza" \
--i-ref "$(art_dir)/rrna_references.qza"  \
--p-workdir "./$(q2smr_output_dir)" \
--p-id 0.12 \
--p-coverage 0.12 \
--output-dir "./$(q2smr_output_dir)/qiime-output" \
--verbose
```

### Align the Raw Reads and Produce an OTU Mapping with Denovo Reads

```bash
qiime sort-me-rna denovo-otu-mapping \
--i-reads "$(art_dir)/raw_sequence.qza" \
--i-ref "$(art_dir)/rrna_references.qza"  \
--p-workdir "./$(q2smr_output_dir)" \
--p-id 0.7 \
--p-coverage 0.7 \
--output-dir "./$(q2smr_output_dir)/qiime-output" \
--verbose
```

Feel free to reach out if you have any questions or encounter issues. Happy sorting!