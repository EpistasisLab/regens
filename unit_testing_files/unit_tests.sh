#!/bin/bash
#BSUB -J unit_tests
#BSUB -o unit_tests.out
#BSUB -e unit_tests.err
source activate PyTriadsim

cd ../

python regens.py --in input_files/ACB --out unit_testing_files/ACB_simulated --simulate_nbreakpoints 4 --simulate_nsamples 1000 \
--phenotype continuous --mean_phenotype 5.75 --population_code ACB --human_genome_version hg19 --noise 0.5 \
--causal_SNP_IDs_path input_files/causal_SNP_IDs.txt --major_minor_assignments_path input_files/major_minor_assignments.txt \
--betas_path input_files/betas.txt --SNP_phenotype_map_path input_files/SNP_phenotype_map.txt --test_functionality test_units
