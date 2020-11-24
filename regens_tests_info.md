## Summary

There is one file named `run_all_tests.sh` in REGENS' repository. If you run REGENS in an anaconda envrionment named `regens` (follow the installation instructions in the README), then running the command `bsub < run_all_tests.sh` will run the majority of tests that regens downloads. There are four testing folders: 

1. correctness_testing_ACB
2. correctness_testing_GBR
3. runtime_testing
4. unit_testing_files

WARNING: the runtime_testing files are not ready to run. They all contain the line `#BSUB -m lambda[i]`, where i is the node. Change this to your node names and make sure that all nodes that you use have identical processors. 

REQUIREMENTS: running `run_all_tests.sh` submits 3 parallel jobs. The correctness_testing jobs take roughly 4.5GB of RAM 2.5 minutes each to complete. The unit_testing jobs take less than 1GB of RAM and 30 seconds to complete. If you want to run one job at a time, then you should run the following files consecutively (paths are all relative to your working directory):

1. correctness_testing_ACB/regens_automated_tests_part1_ACB.sh
2. correctness_testing_GBR/regens_automated_tests_part1_GBR.sh
3. unit_testing_files/unit_tests.sh

Note: all tests take a relatively long time to run, and in general, should not be ran if using regens to simulate a large quantity of data. Tests that `run_all_tests.sh` will run are described below. 

## Testing REGENS' correctness

The tests in `correctness_testing_ACB` and `correctness_testing_GBR` ensure that the most important parts of the regens algorithm work correctly for two different samples. Specifically, it tests four different things:

1. For all possible breakpoint intervals (to which dataset SNPs are not yet assigned) that the expected number of breakpoints in each interval is, on average, equal to the observed number of breakpoints in each interval. It does this for every chromosome, and names the output png file for the ith chromosome `expected_vs_actual_breakpoint_counts_full_range_chr[i].png`. Files corresponding to the ACB and GBR profiles get written into the corresponding correctness_testing folders. 
2. It checks that no breakpoint location is drawn twice for any simulated individual (Each breakpoint can only be drawn once per individual). 
3. It checks that every SNP being used as a breakpoint boundary matches back to the genomic interval in which it resides.
4. It checks that every filled segment of a simulated genome is equivalent to the correct genomic segment of the correct individual. 

Steps 1 and 2 show that breakpoints are drawn from the correct distribution, step 3 shows that drawn breakpoints are mapped to the correct input dataset SNPs to use as boundaries, and step 4 shows that the genotypes inserted into the resulting empty segments are the correct genotypes. If all of these things are true, then the regens algorithm probably works correctly. PySnpTools may contain errors, but this is unlikely. The output of part one is shown in one png file per chromosome. The output of parts 2, 3, and 4 are print statements that get written into the .out file from running `regens_automated_tests_part1_ACB.sh` and `regens_automated_tests_part1_GBR.sh`

If you install plink and cython, then you can also run `regens_automated_tests_optional_part2_LD_getter_GBR.sh.` and `regens_automated_tests_optional_part2_LD_getter_ACB.sh` (both in their respective folders). Doing so will produce the figures `GBR_real_vs_sim_r_val_maf_comparision.png` and `GBR_real_vs_sim_r_vs_distance_profile_comparison.png`. The first figure shows that samples simulated by regens have the same SNP correlations and maf values (with some random noise) as are measured in the real dataset. The second figure shows that the relationship between SNP correlation strength and distance between SNPs is the same for both the real and simulated data. These tests are not included in `run_all_tests.sh` because of the nevessary extra software that needs to be downloaded. 

## Unit tests for REGENS

The tests in `unit_testing_files` confirm, for the first chromosome in the 1000 genomes ACB population only, that actual output is exactly equal to correct reference output at a specific random seed. As such, testing regens with the unit tests is much faster than using the correctness tests, and regens' functionality really doesn't change across populations or chromosomes. These unit tests confirm that the following intermediate output objects equal what they should:

1. correct centimorgans_to_probabilities function output
2. correct choice_with_periodic_replacement function output
3. correct draw_breakpoints function output
4. correct get_samples_fast_breakpoint_interval_minor_allele_counts output (i.e. the total number of minor alleles per segment)
5. correct get_samples_fast_simulated_individual_minor_allele_counts output (i.e. the total number of minor alleles per simulated individual)
6. correct get_samples_fast_SNP_minor_allele_counts output (i.e. the total number of minor alleles per SNP)
7. correct reduce_recomb_rate_info function output
8. correct SNP_positions_to_rcmb_intervals function first output
9. correct SNP_positions_to_rcmb_intervals function second output

Note that, with 4, 5, and 6, the imported genotypes are too large to check for equality directly, so we compare the minor allele counts summed over a single dimension for all three dimensions. It is exceedingly improbable that all of these counts will match perfectly if the numpy arrays themselves do not. All outputs are print statements, so they're written into the .out file from running `unit_tests.sh`

## Efficiency tests for REGENS

The `runtime_testing` folder contains scripts that simply run regens 10 times in the same way. The jobs being run are started by running the following files:

1. runtime_testing/regens1.sh
2. runtime_testing/regens2.sh
3. runtime_testing/regens3.sh
4. runtime_testing/regens4.sh
5. runtime_testing/regens5.sh
6. runtime_testing/regens6.sh
7. runtime_testing/regens7.sh
8. runtime_testing/regens8.sh
9. runtime_testing/regens9.sh
10. runtime_testing/regens10.sh

Each file above contains the specification `#BSUB -m lambda[i]`, which should be removed before use on your system. The `runtime_testing/regens_main.sh` file runs all ten files listed above simultaneouslty. Each job takes requires roughly 10 GB of ram and takes 5 minutes to complete, so these jobs are not included in `run_all_tests.sh`.

## Efficiency tests for Triadsim

The `runtime_testing` folder also contains scripts that run triadsim 10 times in the same way:

1. runtime_testing/triadsim1.sh
2. runtime_testing/triadsim2.sh
3. runtime_testing/triadsim3.sh
4. runtime_testing/triadsim4.sh
5. runtime_testing/triadsim5.sh
6. runtime_testing/triadsim6.sh
7. runtime_testing/triadsim7.sh
8. runtime_testing/triadsim8.sh
9. runtime_testing/triadsim9.sh
10. runtime_testing/triadsim10.sh

You need to install triadsim before attempting to run them. Each replicate requires over 6 hours and 50GB of RAM to run. The `runtime_testing/triadsim_main.sh` file runs all ten files listed above simultaneouslty. Triadsim's runtime distribution is skewed. Roughly 1 or 2 out of every 10 triadsim runs will take roughly double its normal ammount of time or longer to run.  
