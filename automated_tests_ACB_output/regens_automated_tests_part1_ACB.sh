#!/bin/bash
#BSUB -J automated_tests_part1_ACB
#BSUB -o automated_tests_ACB_output/automated_tests_part1_ACB.out
#BSUB -e automated_tests_ACB_output/automated_tests_part1_ACB.err
#BSUB -R "rusage[mem=10000MB]"
#BSUB -M 10000MB
source activate PyTriadsim

python regens.py --in ACB --out automated_tests_ACB_output/ACB_simulated --simulate_nbreakpoints 4 \
--simulate_nsamples 20000 --phenotype continuous --mean_phenotype 5.75 --population_code ACB --human_genome_version hg19 \
--noise 0.5 --causal_SNP_IDs_path causal_SNP_IDs.txt --major_minor_assignments_path major_minor_assignments.txt \
--betas_path betas.txt --SNP_phenotype_map_path SNP_phenotype_map.txt --test_functionality yes
