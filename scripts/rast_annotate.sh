#!/usr/bin/env bash

rast-create-genome --scientific-name "Salmonella infantis" \
		   --genetic-code 11\
		   --domain Bacteria\
		   --contigs ../data/GCF_019918175.1_ASM1991817v1_genomic.fna\
		   --genome-id S_infantis_ASM1991817v1\
		   --ncbi-taxonomy-id 595\
		   --source ttps://www.ncbi.nlm.nih.gov/assembly/GCF_019918175.1\
		   --source-id ASM1991817v1 > S_infantis.gto

rast-process-genome < S_infantis.gto > S_infantis.gto2

rast-export-genome protein_fasta < S_infantis.gto2 > S_infantis.faa

rast-export-genome seed_dir < S_infantis.gto2 > S_infantis.seed_dir.tar.gz 

mv S_inf* ../data/gem_steps_ouput/
cd ../data/gem_steps_ouput
tar -zxvf S_infantis.seed_dir.tar.gz
rm *.gto *gto2

