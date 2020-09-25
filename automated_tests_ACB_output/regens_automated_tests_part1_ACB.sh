#!/bin/bash
#BSUB -J automated_tests_part1_ACB
#BSUB -o automated_tests_part1_ACB.out
#BSUB -e automated_tests_part1_ACB.err
#BSUB -R "rusage[mem=6000MB]"
#BSUB -M 6000MB
source activate PyTriadsim

cd ../

python regens.py --in input_files/ACB --out correctness_testing_ACB/ACB_simulated --simulate_nbreakpoints 4 --simulate_nsamples 10000 \
--phenotype continuous --mean_phenotype 5.75 --population_code ACB --human_genome_version hg19 --noise 0.5 \
--causal_SNP_IDs_path input_files/causal_SNP_IDs.txt --major_minor_assignments_path input_files/major_minor_assignments.txt \
--betas_path input_files/betas.txt --SNP_phenotype_map_path input_files/SNP_phenotype_map.txt --test_functionality test_correctness
