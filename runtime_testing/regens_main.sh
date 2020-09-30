#!/bin/bash
#BSUB -J regens_main_shell
#BSUB -o regens_main_shell.out
#BSUB -e regens_main_shell.err

bsub < regens1.sh
bsub < regens2.sh
bsub < regens3.sh
bsub < regens4.sh
bsub < regens5.sh
bsub < regens6.sh
bsub < regens7.sh
bsub < regens8.sh
bsub < regens9.sh
bsub < regens10.sh
 