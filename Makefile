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
	qiime sort-me-rna sort-rna \
	--p-ref "./rrna_references.fasta"  \
	--p-reads "./synthetic_data.fastq" \
	--p-workdir "./$(q2smr_output_dir)" \
	--o-aligned-seq "./$(q2smr_output_dir)/qiime-output" \
	--verbose

try: clean 
	mkdir $(q2smr_output_dir)
	qiime sort-me-rna sort-rna \
	--p-ref "./rrna_references.fasta"  \
	--p-reads "./synthetic_data.fastq" \
	--p-workdir "./$(q2smr_output_dir)" \
	--p-fastx true \
	--o-aligned-seq "./$(q2smr_output_dir)/qiime-output" \
	--verbose

run1: clean 
	mkdir $(q2smr_output_dir)
	qiime sort-me-rna sort-rna \
	--p-ref "./rrna_references.fasta"  \
	--p-reads "./synthetic_data.fastq" \
	--p-workdir "./$(q2smr_output_dir)" \
	--p-passes "1,1,1" \
	--o-aligned-seq "./$(q2smr_output_dir)/qiime-output" \
	--verbose

peek: 
	qiime tools peek ./$(q2smr_output_dir)/qiime-output.qza 

full: install clean blast_cache test run peek