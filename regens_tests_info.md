There are four testing folders:
1. correctness_testing_ACB
2. correctness_testing_GBR
3. runtime_testing
4. unit_testing_files

Note: all tests take a relatively long time to run, and in general, should not be ran if using regens to simulate a large quantity of data. 

The tests in `correctness_testing_ACB` and `correctness_testing_GBR` ensure that the most important parts of the regens algorithm work correctly for two different samples. Specifically, it tests four different things:

1. For all possible breakpoint intervals (to which dataset SNPs are not yet assigned) that the expected number of breakpoints in each interval is, on average, equal to the observed number of breakpoints in each interval. It does this for every chromosome, and names the files for the ith chromosome `expected_vs_actual_breakpoint_counts_full_range_chr[i].png`. Files corresponding to the ACB and GBR profiles get written into the corresponding correctness_testing folders. 
2. It checks that no breakpoint location is drawn twice for any simulated individual (Each breakpoint can only be drawn once per individual). 
3. It checks that every SNP being used as a breakpoint boundary matches back to the genomic interval in which it resides.
4. It checks that every filled segment of a simulated genome matches back to the correct genomic segment of the correct individual. 

Steps 1 and 2 show that breakpoints are drawn from the correct distribution, step 3 shows that drawn breakpoints are mapped to the correct input dataset SNPs to use as boundaries, and step 4 shows that the genotypes inserted into the resulting empty segments are the correct genotypes. If all of these things are true, then the regens algorithm works correctly. PySnpTools may contain errors, but this is unlikely. 

The tests in `unit_testing_files` confirm, for the first chromosome in the 1000 genomes ACB population only, that actual output is exactly equal to the expected output at a specific random seed. As such, testing regens with the unit tests is much faster than using the correctness tests, and regens' functionality really doesn't change across populations or chromosomes. These unit tests confirm that the following intermediate output objects equal what they should:

1. correct centimorgans_to_probabilities function output
2. correct choice_with_periodic_replacement function output
3. correct draw_breakpoints function output
4. correct get_samples_fast_breakpoint_interval_minor_allele_counts output (i.e. the total number of minor alleles per segment)
5. correct get_samples_fast_simulated_individual_minor_allele_counts output (i.e. the total number of minor alleles per simulated individual)
6. correct get_samples_fast_SNP_minor_allele_counts output (i.e. the total number of minor alleles per SNP)
7. correct reduce_recomb_rate_info function output
8. correct SNP_positions_to_rcmb_intervals function first output
9. correct SNP_positions_to_rcmb_intervals function second output

Note that, with 4, 5, and 6, the imported genotypes are too large to check for equality directly, so we compare the minor allele counts summed over a single dimension for all three dimensions. It is exceedingly improbable that all of these counts will match perfectly if the numpy arrays themselves do not. 


