#!/bin/bash
#BSUB -J run_all_tests
#BSUB -o run_all_tests.out
#BSUB -e run_all_tests.err

bsub < correctness_testing_ACB/regens_automated_tests_part1_ACB.sh
bsub < correctness_testing_GBR/regens_automated_tests_part1_GBR.sh
bsub < unit_testing_files/unit_tests.sh
bsub < runtime_testing/regens_main.sh