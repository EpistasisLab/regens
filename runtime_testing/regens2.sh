#!/bin/bash
#BSUB -J regens_runtime
#BSUB -o regens_runtime.out
#BSUB -e regens_runtime.err
#BSUB -R "rusage[mem=10000MB]"
#BSUB -M 10000MB
#BSUB -m lambda11
#BSUB -n 1
source activate PyTriadsim

cd ../

python regens.py --in input_files/ACB --out runtime_testing/ACB_simulated2 --simulate_nbreakpoints 4 --simulate_nsamples 20000 \
--phenotype continuous --mean_phenotype 5.75 --population_code ACB --human_genome_version hg19 --noise 0.5 \
--causal_SNP_IDs_path input_files/causal_SNP_IDs.txt --major_minor_assignments_path input_files/major_minor_assignments.txt \
--betas_path input_files/betas.txt --SNP_phenotype_map_path input_files/SNP_phenotype_map.txt
