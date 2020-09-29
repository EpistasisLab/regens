#!/bin/bash
#BSUB -J triadsim_main_shell
#BSUB -o triadsim_main_shell.out
#BSUB -e triadsim_main_shell.err

bsub < triadsim1.sh
bsub < triadsim2.sh
bsub < triadsim3.sh
bsub < triadsim4.sh
bsub < triadsim5.sh
bsub < triadsim6.sh
bsub < triadsim7.sh
bsub < triadsim8.sh
bsub < triadsim9.sh
bsub < triadsim10.sh
 