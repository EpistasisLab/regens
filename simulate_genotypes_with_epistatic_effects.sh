#!/bin/bash
#BSUB -J simulate_genotypes_without_effects
#BSUB -o simulate_genotypes_without_effects.out
#BSUB -e simulate_genotypes_without_effects.err
#BSUB -R "rusage[mem=6000MB]"
#BSUB -M 6000MB
#BSUB -m lambda20
#BSUB -n 1
source activate PyTriadsim

python regens.py \
--in input_files/ACB --out ACB_simulated \
--simulate_nbreakpoints 4 --simulate_nsamples 10000 \
--phenotype continuous --mean_phenotype 5.75 \
--population_code ACB --human_genome_version hg19 --noise 0.5 \
--causal_SNP_IDs_path input_files/causal_SNP_IDs2.txt \
--major_minor_assignments_path input_files/major_minor_assignments2.txt \
--SNP_phenotype_map_path input_files/SNP_phenotype_map2.txt \
--betas_path input_files/betas.txt