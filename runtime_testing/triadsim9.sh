#!/bin/bash
#BSUB -J triadsim_runtimes
#BSUB -o triadsim_runtimes.out
#BSUB -e triadsim_runtimes.err
#BSUB -R "rusage[mem=80000MB]"
#BSUB -M 80000MB
#BSUB -m lambda18
#BSUB -n 1
module load R/3.2.5

cd ../ 

Rscript runtime_testing/triadsim9.R