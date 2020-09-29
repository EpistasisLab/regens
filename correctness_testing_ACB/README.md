1. `automated_tests_part1_ACB.sh` can be run from the directory that it's in on a linux machine. 

2. If you are using Windows, then run the command in `automated_tests_part1_ACB.sh` from the regens folder.

3. Replace all instances of "\" linebreak characters with "^" if you are using windows. 

4. Output includes `automated_tests_part1_ACB.out`, the expected vs actual breakpoint count png figures,
and simulated gwas data (not initially present) that takes roughly 2GB of space. The png figures should
show that the theoretically expected number of instances of each possible breakpoint varies one to one 
with the actual number of simulated breakpoints. Random noise is expected. The `automated_tests_part1_ACB.out`
file should show that the same breakpoint is never drawn more than once for a given simulated individual, that
all breakpoint interval indices from the rcmb file map correctly to SNP indices from the plink file, and that
all simulated individuals are comprised from the correct SNP subsets in the correct input genomes. 

5. If you install plink and cython, then you can also run `regens_automated_tests_optional_part2_LD_getter_ACB.sh.`
(or an equivalent windows command following the instructions from steps 2 and 3). Doing so will produce the figures
`ACB_real_vs_sim_r_val_maf_comparision.png` and `ACB_real_vs_sim_r_vs_distance_profile_comparison.png`. The first
figure shows that samples simulated by regens have the same SNP correlations and maf values (with some random noise)
as are measured in the real dataset. The second figure shows that the relationship between SNP correlation strength
and distance between SNPs is the same for both the real and simulated data. 