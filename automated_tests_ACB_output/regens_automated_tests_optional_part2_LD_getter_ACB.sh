#!/bin/bash
#BSUB -J automated_tests_part2_ACB
#BSUB -o automated_tests_ACB_output/automated_tests_part2_ACB.out
#BSUB -e automated_tests_ACB_output/automated_tests_part2_ACB.err
#BSUB -R "rusage[mem=50000MB]"
#BSUB -M 50000MB
source activate PyTriadsim
module load plink/1.90Beta6.18

plink --bfile ACB --chr 1 --make-bed --out automated_tests_ACB_output/ACB_chr1
plink --bfile ACB --chr 2 --make-bed --out automated_tests_ACB_output/ACB_chr2
plink --bfile ACB --chr 3 --make-bed --out automated_tests_ACB_output/ACB_chr3
plink --bfile ACB --chr 4 --make-bed --out automated_tests_ACB_output/ACB_chr4
plink --bfile ACB --chr 5 --make-bed --out automated_tests_ACB_output/ACB_chr5
plink --bfile ACB --chr 6 --make-bed --out automated_tests_ACB_output/ACB_chr6
plink --bfile ACB --chr 7 --make-bed --out automated_tests_ACB_output/ACB_chr7
plink --bfile ACB --chr 8 --make-bed --out automated_tests_ACB_output/ACB_chr8
plink --bfile ACB --chr 9 --make-bed --out automated_tests_ACB_output/ACB_chr9
plink --bfile ACB --chr 10 --make-bed --out automated_tests_ACB_output/ACB_chr10
plink --bfile ACB --chr 11 --make-bed --out automated_tests_ACB_output/ACB_chr11
plink --bfile ACB --chr 12 --make-bed --out automated_tests_ACB_output/ACB_chr12
plink --bfile ACB --chr 13 --make-bed --out automated_tests_ACB_output/ACB_chr13
plink --bfile ACB --chr 14 --make-bed --out automated_tests_ACB_output/ACB_chr14
plink --bfile ACB --chr 15 --make-bed --out automated_tests_ACB_output/ACB_chr15
plink --bfile ACB --chr 16 --make-bed --out automated_tests_ACB_output/ACB_chr16
plink --bfile ACB --chr 17 --make-bed --out automated_tests_ACB_output/ACB_chr17
plink --bfile ACB --chr 18 --make-bed --out automated_tests_ACB_output/ACB_chr18
plink --bfile ACB --chr 19 --make-bed --out automated_tests_ACB_output/ACB_chr19
plink --bfile ACB --chr 20 --make-bed --out automated_tests_ACB_output/ACB_chr20
plink --bfile ACB --chr 21 --make-bed --out automated_tests_ACB_output/ACB_chr21
plink --bfile ACB --chr 22 --make-bed --out automated_tests_ACB_output/ACB_chr22

plink --bfile automated_tests_ACB_output/ACB_chr1 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_chr1
plink --bfile automated_tests_ACB_output/ACB_chr2 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_chr2
plink --bfile automated_tests_ACB_output/ACB_chr3 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_chr3
plink --bfile automated_tests_ACB_output/ACB_chr4 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_chr4
plink --bfile automated_tests_ACB_output/ACB_chr5 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_chr5
plink --bfile automated_tests_ACB_output/ACB_chr6 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_chr6
plink --bfile automated_tests_ACB_output/ACB_chr7 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_chr7
plink --bfile automated_tests_ACB_output/ACB_chr8 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_chr8
plink --bfile automated_tests_ACB_output/ACB_chr9 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_chr9
plink --bfile automated_tests_ACB_output/ACB_chr10 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_chr10
plink --bfile automated_tests_ACB_output/ACB_chr11 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_chr11
plink --bfile automated_tests_ACB_output/ACB_chr12 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_chr12
plink --bfile automated_tests_ACB_output/ACB_chr13 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_chr13
plink --bfile automated_tests_ACB_output/ACB_chr14 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_chr14
plink --bfile automated_tests_ACB_output/ACB_chr15 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_chr15
plink --bfile automated_tests_ACB_output/ACB_chr16 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_chr16
plink --bfile automated_tests_ACB_output/ACB_chr17 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_chr17
plink --bfile automated_tests_ACB_output/ACB_chr18 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_chr18
plink --bfile automated_tests_ACB_output/ACB_chr19 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_chr19
plink --bfile automated_tests_ACB_output/ACB_chr20 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_chr20
plink --bfile automated_tests_ACB_output/ACB_chr21 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_chr21
plink --bfile automated_tests_ACB_output/ACB_chr22 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_chr22

plink --bfile automated_tests_ACB_output/ACB_simulated_chr1 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_simulated_chr1
plink --bfile automated_tests_ACB_output/ACB_simulated_chr2 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_simulated_chr2
plink --bfile automated_tests_ACB_output/ACB_simulated_chr3 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_simulated_chr3
plink --bfile automated_tests_ACB_output/ACB_simulated_chr4 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_simulated_chr4
plink --bfile automated_tests_ACB_output/ACB_simulated_chr5 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_simulated_chr5
plink --bfile automated_tests_ACB_output/ACB_simulated_chr6 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_simulated_chr6
plink --bfile automated_tests_ACB_output/ACB_simulated_chr7 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_simulated_chr7
plink --bfile automated_tests_ACB_output/ACB_simulated_chr8 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_simulated_chr8
plink --bfile automated_tests_ACB_output/ACB_simulated_chr9 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_simulated_chr9
plink --bfile automated_tests_ACB_output/ACB_simulated_chr10 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_simulated_chr10
plink --bfile automated_tests_ACB_output/ACB_simulated_chr11 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_simulated_chr11
plink --bfile automated_tests_ACB_output/ACB_simulated_chr12 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_simulated_chr12
plink --bfile automated_tests_ACB_output/ACB_simulated_chr13 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_simulated_chr13
plink --bfile automated_tests_ACB_output/ACB_simulated_chr14 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_simulated_chr14
plink --bfile automated_tests_ACB_output/ACB_simulated_chr15 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_simulated_chr15
plink --bfile automated_tests_ACB_output/ACB_simulated_chr16 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_simulated_chr16
plink --bfile automated_tests_ACB_output/ACB_simulated_chr17 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_simulated_chr17
plink --bfile automated_tests_ACB_output/ACB_simulated_chr18 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_simulated_chr18
plink --bfile automated_tests_ACB_output/ACB_simulated_chr19 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_simulated_chr19
plink --bfile automated_tests_ACB_output/ACB_simulated_chr20 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_simulated_chr20
plink --bfile automated_tests_ACB_output/ACB_simulated_chr21 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_simulated_chr21
plink --bfile automated_tests_ACB_output/ACB_simulated_chr22 --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0 --out automated_tests_ACB_output/ACB_simulated_chr22

python automated_tests_ACB_output/regens_LD_getter.py --ref automated_tests_ACB_output/ACB --sim automated_tests_ACB_output/ACB_simulated

rm automated_tests_ACB_output/ACB_simulated_chr1.ld
rm automated_tests_ACB_output/ACB_chr1.bed
rm automated_tests_ACB_output/ACB_chr1.bim
rm automated_tests_ACB_output/ACB_chr1.fam
rm automated_tests_ACB_output/ACB_chr1.log
rm automated_tests_ACB_output/ACB_chr1.ld
rm automated_tests_ACB_output/ACB_simulated_chr2.ld
rm automated_tests_ACB_output/ACB_chr2.bed
rm automated_tests_ACB_output/ACB_chr2.bim
rm automated_tests_ACB_output/ACB_chr2.fam
rm automated_tests_ACB_output/ACB_chr2.log
rm automated_tests_ACB_output/ACB_chr2.ld
rm automated_tests_ACB_output/ACB_simulated_chr3.ld
rm automated_tests_ACB_output/ACB_chr3.bed
rm automated_tests_ACB_output/ACB_chr3.bim
rm automated_tests_ACB_output/ACB_chr3.fam
rm automated_tests_ACB_output/ACB_chr3.log
rm automated_tests_ACB_output/ACB_chr3.ld
rm automated_tests_ACB_output/ACB_simulated_chr4.ld
rm automated_tests_ACB_output/ACB_chr4.bed
rm automated_tests_ACB_output/ACB_chr4.bim
rm automated_tests_ACB_output/ACB_chr4.fam
rm automated_tests_ACB_output/ACB_chr4.log
rm automated_tests_ACB_output/ACB_chr4.ld
rm automated_tests_ACB_output/ACB_simulated_chr5.ld
rm automated_tests_ACB_output/ACB_chr5.bed
rm automated_tests_ACB_output/ACB_chr5.bim
rm automated_tests_ACB_output/ACB_chr5.fam
rm automated_tests_ACB_output/ACB_chr5.log
rm automated_tests_ACB_output/ACB_chr5.ld
rm automated_tests_ACB_output/ACB_simulated_chr6.ld
rm automated_tests_ACB_output/ACB_chr6.bed
rm automated_tests_ACB_output/ACB_chr6.bim
rm automated_tests_ACB_output/ACB_chr6.fam
rm automated_tests_ACB_output/ACB_chr6.log
rm automated_tests_ACB_output/ACB_chr6.ld
rm automated_tests_ACB_output/ACB_simulated_chr7.ld
rm automated_tests_ACB_output/ACB_chr7.bed
rm automated_tests_ACB_output/ACB_chr7.bim
rm automated_tests_ACB_output/ACB_chr7.fam
rm automated_tests_ACB_output/ACB_chr7.log
rm automated_tests_ACB_output/ACB_chr7.ld
rm automated_tests_ACB_output/ACB_simulated_chr8.ld
rm automated_tests_ACB_output/ACB_chr8.bed
rm automated_tests_ACB_output/ACB_chr8.bim
rm automated_tests_ACB_output/ACB_chr8.fam
rm automated_tests_ACB_output/ACB_chr8.log
rm automated_tests_ACB_output/ACB_chr8.ld
rm automated_tests_ACB_output/ACB_simulated_chr9.ld
rm automated_tests_ACB_output/ACB_chr9.bed
rm automated_tests_ACB_output/ACB_chr9.bim
rm automated_tests_ACB_output/ACB_chr9.fam
rm automated_tests_ACB_output/ACB_chr9.log
rm automated_tests_ACB_output/ACB_chr9.ld
rm automated_tests_ACB_output/ACB_simulated_chr10.ld
rm automated_tests_ACB_output/ACB_chr10.bed
rm automated_tests_ACB_output/ACB_chr10.bim
rm automated_tests_ACB_output/ACB_chr10.fam
rm automated_tests_ACB_output/ACB_chr10.log
rm automated_tests_ACB_output/ACB_chr10.ld
rm automated_tests_ACB_output/ACB_simulated_chr11.ld
rm automated_tests_ACB_output/ACB_chr11.bed
rm automated_tests_ACB_output/ACB_chr11.bim
rm automated_tests_ACB_output/ACB_chr11.fam
rm automated_tests_ACB_output/ACB_chr11.log
rm automated_tests_ACB_output/ACB_chr11.ld
rm automated_tests_ACB_output/ACB_simulated_chr12.ld
rm automated_tests_ACB_output/ACB_chr12.bed
rm automated_tests_ACB_output/ACB_chr12.bim
rm automated_tests_ACB_output/ACB_chr12.fam
rm automated_tests_ACB_output/ACB_chr12.log
rm automated_tests_ACB_output/ACB_chr12.ld
rm automated_tests_ACB_output/ACB_simulated_chr13.ld
rm automated_tests_ACB_output/ACB_chr13.bed
rm automated_tests_ACB_output/ACB_chr13.bim
rm automated_tests_ACB_output/ACB_chr13.fam
rm automated_tests_ACB_output/ACB_chr13.log
rm automated_tests_ACB_output/ACB_chr13.ld
rm automated_tests_ACB_output/ACB_simulated_chr14.ld
rm automated_tests_ACB_output/ACB_chr14.bed
rm automated_tests_ACB_output/ACB_chr14.bim
rm automated_tests_ACB_output/ACB_chr14.fam
rm automated_tests_ACB_output/ACB_chr14.log
rm automated_tests_ACB_output/ACB_chr14.ld
rm automated_tests_ACB_output/ACB_simulated_chr15.ld
rm automated_tests_ACB_output/ACB_chr15.bed
rm automated_tests_ACB_output/ACB_chr15.bim
rm automated_tests_ACB_output/ACB_chr15.fam
rm automated_tests_ACB_output/ACB_chr15.log
rm automated_tests_ACB_output/ACB_chr15.ld
rm automated_tests_ACB_output/ACB_simulated_chr16.ld
rm automated_tests_ACB_output/ACB_chr16.bed
rm automated_tests_ACB_output/ACB_chr16.bim
rm automated_tests_ACB_output/ACB_chr16.fam
rm automated_tests_ACB_output/ACB_chr16.log
rm automated_tests_ACB_output/ACB_chr16.ld
rm automated_tests_ACB_output/ACB_simulated_chr17.ld
rm automated_tests_ACB_output/ACB_chr17.bed
rm automated_tests_ACB_output/ACB_chr17.bim
rm automated_tests_ACB_output/ACB_chr17.fam
rm automated_tests_ACB_output/ACB_chr17.log
rm automated_tests_ACB_output/ACB_chr17.ld
rm automated_tests_ACB_output/ACB_simulated_chr18.ld
rm automated_tests_ACB_output/ACB_chr18.bed
rm automated_tests_ACB_output/ACB_chr18.bim
rm automated_tests_ACB_output/ACB_chr18.fam
rm automated_tests_ACB_output/ACB_chr18.log
rm automated_tests_ACB_output/ACB_chr18.ld
rm automated_tests_ACB_output/ACB_simulated_chr19.ld
rm automated_tests_ACB_output/ACB_chr19.bed
rm automated_tests_ACB_output/ACB_chr19.bim
rm automated_tests_ACB_output/ACB_chr19.fam
rm automated_tests_ACB_output/ACB_chr19.log
rm automated_tests_ACB_output/ACB_chr19.ld
rm automated_tests_ACB_output/ACB_simulated_chr20.ld
rm automated_tests_ACB_output/ACB_chr20.bed
rm automated_tests_ACB_output/ACB_chr20.bim
rm automated_tests_ACB_output/ACB_chr20.fam
rm automated_tests_ACB_output/ACB_chr20.log
rm automated_tests_ACB_output/ACB_chr20.ld
rm automated_tests_ACB_output/ACB_simulated_chr21.ld
rm automated_tests_ACB_output/ACB_chr21.bed
rm automated_tests_ACB_output/ACB_chr21.bim
rm automated_tests_ACB_output/ACB_chr21.fam
rm automated_tests_ACB_output/ACB_chr21.log
rm automated_tests_ACB_output/ACB_chr21.ld
rm automated_tests_ACB_output/ACB_simulated_chr22.ld
rm automated_tests_ACB_output/ACB_chr22.bed
rm automated_tests_ACB_output/ACB_chr22.bim
rm automated_tests_ACB_output/ACB_chr22.fam
rm automated_tests_ACB_output/ACB_chr22.log
rm automated_tests_ACB_output/ACB_chr22.ld
