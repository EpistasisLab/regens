#!/bin/bash
#BSUB -J simulate_genotypes_with_additive_effects
#BSUB -o simulate_genotypes_with_additive_effects.out
#BSUB -e simulate_genotypes_with_additive_effects.err
#BSUB -R "rusage[mem=6000MB]"
#BSUB -M 6000MB
#BSUB -m lambda20
#BSUB -n 1
source activate PyTriadsim

cd ../

python regens.py \
--in input_files/ACB --out examples/ACB_simulated \
--simulate_nsamples 10000 --simulate_nbreakpoints 4 \
--phenotype continuous --mean_phenotype 5.75 \
--population_code ACB --human_genome_version hg19 \
--causal_SNP_IDs_path input_files/causal_SNP_IDs.txt \
--noise 0.5 --betas_path input_files/betas.txt