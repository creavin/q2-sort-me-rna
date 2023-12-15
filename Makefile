sortmerna_work_dir = out
q2smr_output_dir = output

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
	sortmerna --ref ./rrna_references.fasta \
	--reads ./synthetic_data.fastq \
	--workdir $(sortmerna_work_dir)

sortmerna_pair:
	rm -fdr $(sortmerna_work_dir)
	sortmerna --ref ./rrna_references.fasta \
	--reads ./synthetic_data_pair1.fastq \
	--reads ./synthetic_data_pair2.fastq \
	--workdir $(sortmerna_work_dir)

dev: clean 
	mkdir $(q2smr_output_dir)
	qiime sort-me-rna sort-rna \
	--p-ref "./rrna_references.fasta"  \
	--p-reads "./synthetic_data.fastq.gz" \
	--p-workdir "./$(q2smr_output_dir)" \
	--output-dir "./$(q2smr_output_dir)/qiime-output" \
	--verbose


devall: clean 
	mkdir $(q2smr_output_dir)
	qiime sort-me-rna sort-rna \
	--p-ref "./rrna_references.fasta"  \
	--p-reads "./synthetic_data.fastq" \
	--p-workdir "./$(q2smr_output_dir)" \
	--output-dir "./$(q2smr_output_dir)/qiime-output" \
	--verbose

devotu: clean 
	mkdir $(q2smr_output_dir)
	qiime sort-me-rna otu-mapping \
	--p-ref "./rrna_references.fasta"  \
	--p-reads "./synthetic_data.fastq" \
	--p-workdir "./$(q2smr_output_dir)" \
	--p-otu-map true \
	--p-id 0.12 \
	--p-coverage 0.12 \
	--output-dir "./$(q2smr_output_dir)/qiime-output" \
	--verbose

devotudenovo: clean 
	mkdir $(q2smr_output_dir)
	qiime sort-me-rna denovo-otu-mapping \
	--p-ref "./rrna_references.fasta"  \
	--p-reads "./synthetic_data.fastq" \
	--p-workdir "./$(q2smr_output_dir)" \
	--p-otu-map true \
	--p-id 0.12 \
	--p-coverage 0.12 \
	--p-de-novo-otu true \
	--output-dir "./$(q2smr_output_dir)/qiime-output" \
	--verbose

devpair: clean 
	mkdir $(q2smr_output_dir)
	qiime sort-me-rna sort-rna \
	--p-ref "./rrna_references.fasta"  \
	--p-reads "./synthetic_data_pair1.fastq" \
	--p-reads-reverse "./synthetic_data_pair2.fastq" \
	--p-workdir "./$(q2smr_output_dir)" \
	--output-dir "./$(q2smr_output_dir)/qiime-output" \
	--verbose
	

test_passes_arg: clean 
	mkdir $(q2smr_output_dir)
	qiime sort-me-rna sort-rna \
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
