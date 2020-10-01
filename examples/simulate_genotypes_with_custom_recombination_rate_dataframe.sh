#!/bin/bash
#BSUB -J simulate_genotypes_with_custom_recombination_rate_dataframe
#BSUB -o simulate_genotypes_with_custom_recombination_rate_dataframe.out
#BSUB -e simulate_genotypes_with_custom_recombination_rate_dataframe.err
#BSUB -R "rusage[mem=6000MB]"
#BSUB -M 6000MB
#BSUB -m lambda20
#BSUB -n 1
source activate PyTriadsim

cd ../

python regens.py \
--in input_files/ACB \
--out examples/ACB_simulated \
--simulate_nsamples 10000 \
--simulate_nbreakpoints 4 \
--recombination_file_path_prefix input_files/hg19_ACB_renamed_as_custom/custom_chr_