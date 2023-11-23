sortmerna_work_dir = out
q2smr_output_dir = output

install: 
	pip install -e .

clean: 
	rm -rdf $(sortmerna_work_dir)
	rm -rdf output

lint:
	q2lint
	flake8

test:
	py.test
#	py.test --cov=q2_emperor #  TODO: see why emp offers this functionality

blast_cache:
	qiime dev refresh-cache

sortmerna:
	rm -fdr $(sortmerna_work_dir)
	sortmerna --ref ./rrna_references.fasta \
	--reads ./synthetic_data.fastq \
	--workdir $(sortmerna_work_dir)

run: clean 
	mkdir $(q2smr_output_dir)
	qiime sort-me-rna sort-rna-union \
	--p-ref "./rrna_references.fasta"  \
	--p-reads "./synthetic_data.fastq" \
	--p-workdir "./$(q2smr_output_dir)" \
	--o-aligned-seq "./$(q2smr_output_dir)/qiime-output" \
	--verbose

dev: clean 
	mkdir $(q2smr_output_dir)
	qiime sort-me-rna sort-rna-union \
	--p-ref "./rrna_references.fasta"  \
	--p-reads "./synthetic_data.fastq" \
	--p-workdir "./$(q2smr_output_dir)" \
	--p-fastx true \
	--o-aligned-seq "./$(q2smr_output_dir)/qiime-output" \
	--verbose

run_with_passes_arg: clean 
	mkdir $(q2smr_output_dir)
	qiime sort-me-rna sort-rna-blas \
	--p-ref "./rrna_references.fasta"  \
	--p-reads "./synthetic_data.fastq" \
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

peek: 
	qiime tools peek ./$(q2smr_output_dir)/qiime-output.qza 

full: install clean blast_cache test run peek