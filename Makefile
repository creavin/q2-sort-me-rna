sortmerna_work_dir = out
q2smr_output_dir = output
art_dir = ./q2_sort_me_rna/tests/assets
seq_dir = ./q2_sort_me_rna/tests/assets/seq

install: 
	pip install -e .

clean: 
	rm -rdf $(sortmerna_work_dir)
	rm -rdf output

lint:
	flake8
	q2lint

test:
	py.test 

blast_cache: install
	qiime dev refresh-cache

sortmerna:
	rm -fdr $(sortmerna_work_dir)
	sortmerna --ref $(seq_dir)/rrna_references.fasta \
	--reads $(seq_dir)/synthetic_data.fastq \
	--workdir $(sortmerna_work_dir)

sortmerna_denovo:
	rm -fdr $(sortmerna_work_dir)
	sortmerna --ref $(seq_dir)/rrna_references.fasta \
	--reads $(seq_dir)/synthetic_data.fastq \
	--de_novo_otu true \
	--otu_map true \
	--sam true \
	--blast '1' \
	--fastx true \
	--id 0.7 \
	--coverage 0.7 \
	--workdir $(sortmerna_work_dir)

sortmerna_denovo_gz:
	rm -fdr $(sortmerna_work_dir)
	sortmerna --ref $(seq_dir)/rrna_references.fasta \
	--reads $(seq_dir)/synthetic_data.fastq.gz \
	--otu_map true \
	--sam true \
	--blast '1' \
	--fastx true \
	--id 0.7 \
	--coverage 0.7 \
	--workdir $(sortmerna_work_dir)

sortmerna_pair:
	rm -fdr $(sortmerna_work_dir)
	sortmerna --ref $(seq_dir)/rrna_references.fasta \
	--reads $(seq_dir)/synthetic_data_pair1.fastq \
	--reads $(seq_dir)/synthetic_data_pair2.fastq \
	--workdir $(sortmerna_work_dir)

artifact:
	qiime tools import \
	--type 'SampleData[SequencesWithQuality]' \
	--input-path seq \
	--output-path sequence_L999_R1_001.qza \
	--input-format CasavaOneEightSingleLanePerSampleDirFmt

artifact_pair:
	qiime tools import \
	--type 'SampleData[PairedEndSequencesWithQuality]' \
	--input-path seq \
	--output-path pair_sequence_L999_R1_001.qza \
	--input-format CasavaOneEightSingleLanePerSampleDirFmt

artifact_ref:
	qiime tools import \
	--type 'FeatureData[Sequence]' \
	--input-path rrna_references.fasta \
	--output-path rrna_references.qza \
	--input-format DNAFASTAFormat

dev: clean 
	mkdir $(q2smr_output_dir)
	qiime sort-me-rna sort-rna \
	--i-reads "$(art_dir)/paired_raw_sequence.qza" \
	--i-ref "$(art_dir)/rrna_references.qza"  \
	--p-workdir "./$(q2smr_output_dir)" \
	--output-dir "./$(q2smr_output_dir)/qiime-output" \
	--verbose

devall: clean 
	mkdir $(q2smr_output_dir)
	qiime sort-me-rna sort-rna \
	--i-reads "$(art_dir)/raw_sequence.qza" \
	--i-ref "$(art_dir)/rrna_references.qza"  \
	--p-workdir "./$(q2smr_output_dir)" \
	--output-dir "./$(q2smr_output_dir)/qiime-output" \
	--verbose

devall_pair: clean 
	mkdir $(q2smr_output_dir)
	qiime sort-me-rna sort-rna \
	--i-reads "$(art_dir)/paired_raw_sequence.qza" \
	--i-ref "$(art_dir)/rrna_references.qza"  \
	--p-workdir "./$(q2smr_output_dir)" \
	--output-dir "./$(q2smr_output_dir)/qiime-output" \
	--verbose

devotu: clean 
	mkdir $(q2smr_output_dir)
	qiime sort-me-rna otu-mapping \
	--i-reads "$(art_dir)/raw_sequence.qza" \
	--i-ref "$(art_dir)/rrna_references.qza"  \
	--p-workdir "./$(q2smr_output_dir)" \
	--p-id 0.12 \
	--p-coverage 0.12 \
	--output-dir "./$(q2smr_output_dir)/qiime-output" \
	--verbose

devotudenovo: clean 
	mkdir $(q2smr_output_dir)
	qiime sort-me-rna denovo-otu-mapping \
	--i-reads "$(art_dir)/raw_sequence.qza" \
	--i-ref "$(art_dir)/rrna_references.qza"  \
	--p-workdir "./$(q2smr_output_dir)" \
	--p-id 0.7 \
	--p-coverage 0.7 \
	--output-dir "./$(q2smr_output_dir)/qiime-output" \
	--verbose

devpair: clean 
	mkdir $(q2smr_output_dir)
	qiime sort-me-rna sort-rna \
	--p-ref "$(seq_dir)/rrna_references.fasta"  \
	--p-reads-reverse "$(seq_dir)/synthetic_data_pair2.fastq" \
	--p-workdir "./$(q2smr_output_dir)" \
	--output-dir "./$(q2smr_output_dir)/qiime-output" \
	--verbose
	

test_passes_arg: clean 
	mkdir $(q2smr_output_dir)
	qiime sort-me-rna sort-rna \
	--p-ref "$(seq_dir)/rrna_references.fasta"  \
	--p-reads "$(seq_dir)/synthetic_data.fastq" \
	--p-workdir "./$(q2smr_output_dir)" \
	--p-passes "1,1,1" \
	--o-aligned-seq "./$(q2smr_output_dir)/qiime-output" \
	--verbose

test_vsearch:
	mkdir -p output/outvsearch
	qiime vsearch dereplicate-sequences \
	--i-sequences output/qiime-output.qza \
	--o-dereplicated-table output/outvsearch/dereplicated-table.qza \
	--o-dereplicated-sequences output/outvsearch/dereplicated-sequences.qza 

test_vsearch_fast:
	docker run -t -i -v $(pwd):/data quay.io/qiime2/amplicon:2023.9 qiime vsearch fastq-stats \
	--i-sequences "./output/qiime-output.qza" \
	--o-visualization "./output/vsearchstats" --verbose
