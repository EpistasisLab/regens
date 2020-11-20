#!/bin/bash
#BSUB -J get_1000_genomes_files
#BSUB -o get_1000_genomes_files.out
#BSUB -e get_1000_genomes_files.error
module load plink/1.90Beta
module load plink/2.0

#IMPORTANT: This file is not ready to run. It only lists the plink operations that were used to make the processed 1000 genomes datasets.

# gets 1000 genome files
# wget -O all_1000_genomes.pgen.zst https://www.dropbox.com/s/afvvf1e15gqzsqo/all_phase3.pgen.zst?dl=1
# wget -O all_1000_genomes.pvar.zst https://www.dropbox.com/s/op9osq6luy3pjg8/all_phase3.pvar.zst?dl=1
# wget -O all_1000_genomes.psam https://www.dropbox.com/s/nhfhskyy50sqsf1/phase3_orig.psam?dl=1

# decompresses 1000 genome files
plink2 --zst-decompress all_1000_genomes.pgen.zst > all_1000_genomes.pgen
plink2 --zst-decompress all_1000_genomes.pvar.zst > all_1000_genomes.pvar

# removes variants without at least 5 instances, without which, every european subpopulation cannot have an instance.
plink2 --pfile all_1000_genomes --maf 0.002 --make-pgen --out all_1000_genomes_filtered
rm all_1000_genomes.pgen
rm all_1000_genomes.pvar

# removes non-autosomes, filters multi-allelic variants, filters, and seperates european subpopulations.
# This makes the all_1000_genomes_[POPULATION]_filter.txt file for every population.
python all_1000_genomes_subpop_filter_getter.py
plink2 --pfile all_1000_genomes_filtered --max-alleles 2 --chr 1-22 --keep all_1000_genomes_ACB_filter.txt --make-bed --out all_1000_genomes_ACB
plink2 --pfile all_1000_genomes_filtered --max-alleles 2 --chr 1-22 --keep all_1000_genomes_ASW_filter.txt --make-bed --out all_1000_genomes_ASW
plink2 --pfile all_1000_genomes_filtered --max-alleles 2 --chr 1-22 --keep all_1000_genomes_BEB_filter.txt --make-bed --out all_1000_genomes_BEB
plink2 --pfile all_1000_genomes_filtered --max-alleles 2 --chr 1-22 --keep all_1000_genomes_CDX_filter.txt --make-bed --out all_1000_genomes_CDX
plink2 --pfile all_1000_genomes_filtered --max-alleles 2 --chr 1-22 --keep all_1000_genomes_CEU_filter.txt --make-bed --out all_1000_genomes_CEU
plink2 --pfile all_1000_genomes_filtered --max-alleles 2 --chr 1-22 --keep all_1000_genomes_CHB_filter.txt --make-bed --out all_1000_genomes_CHB
plink2 --pfile all_1000_genomes_filtered --max-alleles 2 --chr 1-22 --keep all_1000_genomes_CHS_filter.txt --make-bed --out all_1000_genomes_CHS
plink2 --pfile all_1000_genomes_filtered --max-alleles 2 --chr 1-22 --keep all_1000_genomes_CLM_filter.txt --make-bed --out all_1000_genomes_CLM
plink2 --pfile all_1000_genomes_filtered --max-alleles 2 --chr 1-22 --keep all_1000_genomes_ESN_filter.txt --make-bed --out all_1000_genomes_ESN
plink2 --pfile all_1000_genomes_filtered --max-alleles 2 --chr 1-22 --keep all_1000_genomes_FIN_filter.txt --make-bed --out all_1000_genomes_FIN
plink2 --pfile all_1000_genomes_filtered --max-alleles 2 --chr 1-22 --keep all_1000_genomes_GBR_filter.txt --make-bed --out all_1000_genomes_GBR
plink2 --pfile all_1000_genomes_filtered --max-alleles 2 --chr 1-22 --keep all_1000_genomes_GIH_filter.txt --make-bed --out all_1000_genomes_GIH
plink2 --pfile all_1000_genomes_filtered --max-alleles 2 --chr 1-22 --keep all_1000_genomes_GWD_filter.txt --make-bed --out all_1000_genomes_GWD
plink2 --pfile all_1000_genomes_filtered --max-alleles 2 --chr 1-22 --keep all_1000_genomes_IBS_filter.txt --make-bed --out all_1000_genomes_IBS
plink2 --pfile all_1000_genomes_filtered --max-alleles 2 --chr 1-22 --keep all_1000_genomes_ITU_filter.txt --make-bed --out all_1000_genomes_ITU
plink2 --pfile all_1000_genomes_filtered --max-alleles 2 --chr 1-22 --keep all_1000_genomes_JPT_filter.txt --make-bed --out all_1000_genomes_JPT
plink2 --pfile all_1000_genomes_filtered --max-alleles 2 --chr 1-22 --keep all_1000_genomes_KHV_filter.txt --make-bed --out all_1000_genomes_KHV
plink2 --pfile all_1000_genomes_filtered --max-alleles 2 --chr 1-22 --keep all_1000_genomes_LWK_filter.txt --make-bed --out all_1000_genomes_LWK
plink2 --pfile all_1000_genomes_filtered --max-alleles 2 --chr 1-22 --keep all_1000_genomes_MSL_filter.txt --make-bed --out all_1000_genomes_MSL
plink2 --pfile all_1000_genomes_filtered --max-alleles 2 --chr 1-22 --keep all_1000_genomes_MXL_filter.txt --make-bed --out all_1000_genomes_MXL
plink2 --pfile all_1000_genomes_filtered --max-alleles 2 --chr 1-22 --keep all_1000_genomes_PEL_filter.txt --make-bed --out all_1000_genomes_PEL
plink2 --pfile all_1000_genomes_filtered --max-alleles 2 --chr 1-22 --keep all_1000_genomes_PJL_filter.txt --make-bed --out all_1000_genomes_PJL
plink2 --pfile all_1000_genomes_filtered --max-alleles 2 --chr 1-22 --keep all_1000_genomes_PUR_filter.txt --make-bed --out all_1000_genomes_PUR
plink2 --pfile all_1000_genomes_filtered --max-alleles 2 --chr 1-22 --keep all_1000_genomes_STU_filter.txt --make-bed --out all_1000_genomes_STU
plink2 --pfile all_1000_genomes_filtered --max-alleles 2 --chr 1-22 --keep all_1000_genomes_TSI_filter.txt --make-bed --out all_1000_genomes_TSI
plink2 --pfile all_1000_genomes_filtered --max-alleles 2 --chr 1-22 --keep all_1000_genomes_YRI_filter.txt --make-bed --out all_1000_genomes_YRI
rm all_1000_genomes_filtered.pgen
rm all_1000_genomes_filtered.pvar
rm all_1000_genomes_filtered.psam
rm all_1000_genomes_filtered.log
rm all_1000_genomes_ACB_filter.txt
rm all_1000_genomes_ASW_filter.txt
rm all_1000_genomes_BEB_filter.txt
rm all_1000_genomes_CDX_filter.txt
rm all_1000_genomes_CEU_filter.txt
rm all_1000_genomes_CHB_filter.txt
rm all_1000_genomes_CHS_filter.txt
rm all_1000_genomes_CLM_filter.txt
rm all_1000_genomes_ESN_filter.txt
rm all_1000_genomes_FIN_filter.txt
rm all_1000_genomes_GBR_filter.txt
rm all_1000_genomes_GIH_filter.txt
rm all_1000_genomes_GWD_filter.txt
rm all_1000_genomes_IBS_filter.txt
rm all_1000_genomes_ITU_filter.txt
rm all_1000_genomes_JPT_filter.txt
rm all_1000_genomes_KHV_filter.txt
rm all_1000_genomes_LWK_filter.txt
rm all_1000_genomes_MSL_filter.txt
rm all_1000_genomes_MXL_filter.txt
rm all_1000_genomes_PEL_filter.txt
rm all_1000_genomes_PJL_filter.txt
rm all_1000_genomes_PUR_filter.txt
rm all_1000_genomes_STU_filter.txt
rm all_1000_genomes_TSI_filter.txt
rm all_1000_genomes_YRI_filter.txt

# removes, from all subpopulations, all variants with a maf < 0.05 in any subpopulation or an hwe p value < 1E-10
plink --bfile all_1000_genomes_ACB --freq --hardy --out all_1000_genomes_ACB
plink --bfile all_1000_genomes_ASW --freq --hardy --out all_1000_genomes_ASW
plink --bfile all_1000_genomes_BEB --freq --hardy --out all_1000_genomes_BEB
plink --bfile all_1000_genomes_CDX --freq --hardy --out all_1000_genomes_CDX
plink --bfile all_1000_genomes_CEU --freq --hardy --out all_1000_genomes_CEU
plink --bfile all_1000_genomes_CHB --freq --hardy --out all_1000_genomes_CHB
plink --bfile all_1000_genomes_CHS --freq --hardy --out all_1000_genomes_CHS
plink --bfile all_1000_genomes_CLM --freq --hardy --out all_1000_genomes_CLM
plink --bfile all_1000_genomes_ESN --freq --hardy --out all_1000_genomes_ESN
plink --bfile all_1000_genomes_FIN --freq --hardy --out all_1000_genomes_FIN
plink --bfile all_1000_genomes_GBR --freq --hardy --out all_1000_genomes_GBR
plink --bfile all_1000_genomes_GIH --freq --hardy --out all_1000_genomes_GIH
plink --bfile all_1000_genomes_GWD --freq --hardy --out all_1000_genomes_GWD
plink --bfile all_1000_genomes_IBS --freq --hardy --out all_1000_genomes_IBS
plink --bfile all_1000_genomes_ITU --freq --hardy --out all_1000_genomes_ITU
plink --bfile all_1000_genomes_JPT --freq --hardy --out all_1000_genomes_JPT
plink --bfile all_1000_genomes_KHV --freq --hardy --out all_1000_genomes_KHV
plink --bfile all_1000_genomes_LWK --freq --hardy --out all_1000_genomes_LWK
plink --bfile all_1000_genomes_MSL --freq --hardy --out all_1000_genomes_MSL
plink --bfile all_1000_genomes_MXL --freq --hardy --out all_1000_genomes_MXL
plink --bfile all_1000_genomes_PEL --freq --hardy --out all_1000_genomes_PEL
plink --bfile all_1000_genomes_PJL --freq --hardy --out all_1000_genomes_PJL
plink --bfile all_1000_genomes_PUR --freq --hardy --out all_1000_genomes_PUR
plink --bfile all_1000_genomes_STU --freq --hardy --out all_1000_genomes_STU
plink --bfile all_1000_genomes_TSI --freq --hardy --out all_1000_genomes_TSI
plink --bfile all_1000_genomes_YRI --freq --hardy --out all_1000_genomes_YRI
# This puts all SNPs with a maf < 0.05 in any subpopulation or an hwe p value < 1E-10 into all_1000_genomes_SNP_filter.txt
python all_1000_genomes_SNP_filter_getter.py
plink --bfile all_1000_genomes_ACB --exclude all_1000_genomes_SNP_filter.txt --make-bed --out all_1000_genomes_ACB_filtered
plink --bfile all_1000_genomes_ASW --exclude all_1000_genomes_SNP_filter.txt --make-bed --out all_1000_genomes_ASW_filtered
plink --bfile all_1000_genomes_BEB --exclude all_1000_genomes_SNP_filter.txt --make-bed --out all_1000_genomes_BEB_filtered
plink --bfile all_1000_genomes_CDX --exclude all_1000_genomes_SNP_filter.txt --make-bed --out all_1000_genomes_CDX_filtered
plink --bfile all_1000_genomes_CEU --exclude all_1000_genomes_SNP_filter.txt --make-bed --out all_1000_genomes_CEU_filtered
plink --bfile all_1000_genomes_CHB --exclude all_1000_genomes_SNP_filter.txt --make-bed --out all_1000_genomes_CHB_filtered
plink --bfile all_1000_genomes_CHS --exclude all_1000_genomes_SNP_filter.txt --make-bed --out all_1000_genomes_CHS_filtered
plink --bfile all_1000_genomes_CLM --exclude all_1000_genomes_SNP_filter.txt --make-bed --out all_1000_genomes_CLM_filtered
plink --bfile all_1000_genomes_ESN --exclude all_1000_genomes_SNP_filter.txt --make-bed --out all_1000_genomes_ESN_filtered
plink --bfile all_1000_genomes_FIN --exclude all_1000_genomes_SNP_filter.txt --make-bed --out all_1000_genomes_FIN_filtered
plink --bfile all_1000_genomes_GBR --exclude all_1000_genomes_SNP_filter.txt --make-bed --out all_1000_genomes_GBR_filtered
plink --bfile all_1000_genomes_GIH --exclude all_1000_genomes_SNP_filter.txt --make-bed --out all_1000_genomes_GIH_filtered
plink --bfile all_1000_genomes_GWD --exclude all_1000_genomes_SNP_filter.txt --make-bed --out all_1000_genomes_GWD_filtered
plink --bfile all_1000_genomes_IBS --exclude all_1000_genomes_SNP_filter.txt --make-bed --out all_1000_genomes_IBS_filtered
plink --bfile all_1000_genomes_ITU --exclude all_1000_genomes_SNP_filter.txt --make-bed --out all_1000_genomes_ITU_filtered
plink --bfile all_1000_genomes_JPT --exclude all_1000_genomes_SNP_filter.txt --make-bed --out all_1000_genomes_JPT_filtered
plink --bfile all_1000_genomes_KHV --exclude all_1000_genomes_SNP_filter.txt --make-bed --out all_1000_genomes_KHV_filtered
plink --bfile all_1000_genomes_LWK --exclude all_1000_genomes_SNP_filter.txt --make-bed --out all_1000_genomes_LWK_filtered
plink --bfile all_1000_genomes_MSL --exclude all_1000_genomes_SNP_filter.txt --make-bed --out all_1000_genomes_MSL_filtered
plink --bfile all_1000_genomes_MXL --exclude all_1000_genomes_SNP_filter.txt --make-bed --out all_1000_genomes_MXL_filtered
plink --bfile all_1000_genomes_PEL --exclude all_1000_genomes_SNP_filter.txt --make-bed --out all_1000_genomes_PEL_filtered
plink --bfile all_1000_genomes_PJL --exclude all_1000_genomes_SNP_filter.txt --make-bed --out all_1000_genomes_PJL_filtered
plink --bfile all_1000_genomes_PUR --exclude all_1000_genomes_SNP_filter.txt --make-bed --out all_1000_genomes_PUR_filtered
plink --bfile all_1000_genomes_STU --exclude all_1000_genomes_SNP_filter.txt --make-bed --out all_1000_genomes_STU_filtered
plink --bfile all_1000_genomes_TSI --exclude all_1000_genomes_SNP_filter.txt --make-bed --out all_1000_genomes_TSI_filtered
plink --bfile all_1000_genomes_YRI --exclude all_1000_genomes_SNP_filter.txt --make-bed --out all_1000_genomes_YRI_filtered
rm all_1000_genomes_ACB.bed
rm all_1000_genomes_ACB.bim
rm all_1000_genomes_ACB.fam
rm all_1000_genomes_ACB.hardy
rm all_1000_genomes_ACB.afreq
rm all_1000_genomes_ACB_filtered.log
rm all_1000_genomes_ASW.bed
rm all_1000_genomes_ASW.bim
rm all_1000_genomes_ASW.fam
rm all_1000_genomes_ASW.hardy
rm all_1000_genomes_ASW.afreq
rm all_1000_genomes_ASW_filtered.log
rm all_1000_genomes_BEB.bed
rm all_1000_genomes_BEB.bim
rm all_1000_genomes_BEB.fam
rm all_1000_genomes_BEB.hardy
rm all_1000_genomes_BEB.afreq
rm all_1000_genomes_BEB_filtered.log
rm all_1000_genomes_CDX.bed
rm all_1000_genomes_CDX.bim
rm all_1000_genomes_CDX.fam
rm all_1000_genomes_CDX.hardy
rm all_1000_genomes_CDX.afreq
rm all_1000_genomes_CDX_filtered.log
rm all_1000_genomes_CEU.bed
rm all_1000_genomes_CEU.bim
rm all_1000_genomes_CEU.fam
rm all_1000_genomes_CEU.hardy
rm all_1000_genomes_CEU.afreq
rm all_1000_genomes_CEU_filtered.log
rm all_1000_genomes_CHB.bed
rm all_1000_genomes_CHB.bim
rm all_1000_genomes_CHB.fam
rm all_1000_genomes_CHB.hardy
rm all_1000_genomes_CHB.afreq
rm all_1000_genomes_CHB_filtered.log
rm all_1000_genomes_CHS.bed
rm all_1000_genomes_CHS.bim
rm all_1000_genomes_CHS.fam
rm all_1000_genomes_CHS.hardy
rm all_1000_genomes_CHS.afreq
rm all_1000_genomes_CHS_filtered.log
rm all_1000_genomes_CLM.bed
rm all_1000_genomes_CLM.bim
rm all_1000_genomes_CLM.fam
rm all_1000_genomes_CLM.hardy
rm all_1000_genomes_CLM.afreq
rm all_1000_genomes_CLM_filtered.log
rm all_1000_genomes_ESN.bed
rm all_1000_genomes_ESN.bim
rm all_1000_genomes_ESN.fam
rm all_1000_genomes_ESN.hardy
rm all_1000_genomes_ESN.afreq
rm all_1000_genomes_ESN_filtered.log
rm all_1000_genomes_FIN.bed
rm all_1000_genomes_FIN.bim
rm all_1000_genomes_FIN.fam
rm all_1000_genomes_FIN.hardy
rm all_1000_genomes_FIN.afreq
rm all_1000_genomes_FIN_filtered.log
rm all_1000_genomes_GBR.bed
rm all_1000_genomes_GBR.bim
rm all_1000_genomes_GBR.fam
rm all_1000_genomes_GBR.hardy
rm all_1000_genomes_GBR.afreq
rm all_1000_genomes_GBR_filtered.log
rm all_1000_genomes_GIH.bed
rm all_1000_genomes_GIH.bim
rm all_1000_genomes_GIH.fam
rm all_1000_genomes_GIH.hardy
rm all_1000_genomes_GIH.afreq
rm all_1000_genomes_GIH_filtered.log
rm all_1000_genomes_GWD.bed
rm all_1000_genomes_GWD.bim
rm all_1000_genomes_GWD.fam
rm all_1000_genomes_GWD.hardy
rm all_1000_genomes_GWD.afreq
rm all_1000_genomes_GWD_filtered.log
rm all_1000_genomes_IBS.bed
rm all_1000_genomes_IBS.bim
rm all_1000_genomes_IBS.fam
rm all_1000_genomes_IBS.hardy
rm all_1000_genomes_IBS.afreq
rm all_1000_genomes_IBS_filtered.log
rm all_1000_genomes_ITU.bed
rm all_1000_genomes_ITU.bim
rm all_1000_genomes_ITU.fam
rm all_1000_genomes_ITU.hardy
rm all_1000_genomes_ITU.afreq
rm all_1000_genomes_ITU_filtered.log
rm all_1000_genomes_JPT.bed
rm all_1000_genomes_JPT.bim
rm all_1000_genomes_JPT.fam
rm all_1000_genomes_JPT.hardy
rm all_1000_genomes_JPT.afreq
rm all_1000_genomes_JPT_filtered.log
rm all_1000_genomes_KHV.bed
rm all_1000_genomes_KHV.bim
rm all_1000_genomes_KHV.fam
rm all_1000_genomes_KHV.hardy
rm all_1000_genomes_KHV.afreq
rm all_1000_genomes_KHV_filtered.log
rm all_1000_genomes_LWK.bed
rm all_1000_genomes_LWK.bim
rm all_1000_genomes_LWK.fam
rm all_1000_genomes_LWK.hardy
rm all_1000_genomes_LWK.afreq
rm all_1000_genomes_LWK_filtered.log
rm all_1000_genomes_MSL.bed
rm all_1000_genomes_MSL.bim
rm all_1000_genomes_MSL.fam
rm all_1000_genomes_MSL.hardy
rm all_1000_genomes_MSL.afreq
rm all_1000_genomes_MSL_filtered.log
rm all_1000_genomes_MXL.bed
rm all_1000_genomes_MXL.bim
rm all_1000_genomes_MXL.fam
rm all_1000_genomes_MXL.hardy
rm all_1000_genomes_MXL.afreq
rm all_1000_genomes_MXL_filtered.log
rm all_1000_genomes_PEL.bed
rm all_1000_genomes_PEL.bim
rm all_1000_genomes_PEL.fam
rm all_1000_genomes_PEL.hardy
rm all_1000_genomes_PEL.afreq
rm all_1000_genomes_PEL_filtered.log
rm all_1000_genomes_PJL.bed
rm all_1000_genomes_PJL.bim
rm all_1000_genomes_PJL.fam
rm all_1000_genomes_PJL.hardy
rm all_1000_genomes_PJL.afreq
rm all_1000_genomes_PJL_filtered.log
rm all_1000_genomes_PUR.bed
rm all_1000_genomes_PUR.bim
rm all_1000_genomes_PUR.fam
rm all_1000_genomes_PUR.hardy
rm all_1000_genomes_PUR.afreq
rm all_1000_genomes_PUR_filtered.log
rm all_1000_genomes_STU.bed
rm all_1000_genomes_STU.bim
rm all_1000_genomes_STU.fam
rm all_1000_genomes_STU.hardy
rm all_1000_genomes_STU.afreq
rm all_1000_genomes_STU_filtered.log
rm all_1000_genomes_TSI.bed
rm all_1000_genomes_TSI.bim
rm all_1000_genomes_TSI.fam
rm all_1000_genomes_TSI.hardy
rm all_1000_genomes_TSI.afreq
rm all_1000_genomes_TSI_filtered.log
rm all_1000_genomes_YRI.bed
rm all_1000_genomes_YRI.bim
rm all_1000_genomes_YRI.fam
rm all_1000_genomes_YRI.hardy
rm all_1000_genomes_YRI.afreq
rm all_1000_genomes_YRI_filtered.log

# Remove multi-allelic SNPs
# This puts SNPs at a genomic position that has already been occupied by a different SNP into all_1000_genomes_SNP_filter_multiallelic.txt
python all_1000_genomes_get_duplicated_SNPs.py
plink --bfile all_1000_genomes_ACB_filtered --exclude all_1000_genomes_SNP_filter_multiallelic.txt --make-bed --out all_1000_genomes_ACB_filtered_biallelic
plink --bfile all_1000_genomes_ASW_filtered --exclude all_1000_genomes_SNP_filter_multiallelic.txt --make-bed --out all_1000_genomes_ASW_filtered_biallelic
plink --bfile all_1000_genomes_BEB_filtered --exclude all_1000_genomes_SNP_filter_multiallelic.txt --make-bed --out all_1000_genomes_BEB_filtered_biallelic
plink --bfile all_1000_genomes_CDX_filtered --exclude all_1000_genomes_SNP_filter_multiallelic.txt --make-bed --out all_1000_genomes_CDX_filtered_biallelic
plink --bfile all_1000_genomes_CEU_filtered --exclude all_1000_genomes_SNP_filter_multiallelic.txt --make-bed --out all_1000_genomes_CEU_filtered_biallelic
plink --bfile all_1000_genomes_CHB_filtered --exclude all_1000_genomes_SNP_filter_multiallelic.txt --make-bed --out all_1000_genomes_CHB_filtered_biallelic
plink --bfile all_1000_genomes_CHS_filtered --exclude all_1000_genomes_SNP_filter_multiallelic.txt --make-bed --out all_1000_genomes_CHS_filtered_biallelic
plink --bfile all_1000_genomes_CLM_filtered --exclude all_1000_genomes_SNP_filter_multiallelic.txt --make-bed --out all_1000_genomes_CLM_filtered_biallelic
plink --bfile all_1000_genomes_ESN_filtered --exclude all_1000_genomes_SNP_filter_multiallelic.txt --make-bed --out all_1000_genomes_ESN_filtered_biallelic
plink --bfile all_1000_genomes_FIN_filtered --exclude all_1000_genomes_SNP_filter_multiallelic.txt --make-bed --out all_1000_genomes_FIN_filtered_biallelic
plink --bfile all_1000_genomes_GBR_filtered --exclude all_1000_genomes_SNP_filter_multiallelic.txt --make-bed --out all_1000_genomes_GBR_filtered_biallelic
plink --bfile all_1000_genomes_GIH_filtered --exclude all_1000_genomes_SNP_filter_multiallelic.txt --make-bed --out all_1000_genomes_GIH_filtered_biallelic
plink --bfile all_1000_genomes_GWD_filtered --exclude all_1000_genomes_SNP_filter_multiallelic.txt --make-bed --out all_1000_genomes_GWD_filtered_biallelic
plink --bfile all_1000_genomes_IBS_filtered --exclude all_1000_genomes_SNP_filter_multiallelic.txt --make-bed --out all_1000_genomes_IBS_filtered_biallelic
plink --bfile all_1000_genomes_ITU_filtered --exclude all_1000_genomes_SNP_filter_multiallelic.txt --make-bed --out all_1000_genomes_ITU_filtered_biallelic
plink --bfile all_1000_genomes_JPT_filtered --exclude all_1000_genomes_SNP_filter_multiallelic.txt --make-bed --out all_1000_genomes_JPT_filtered_biallelic
plink --bfile all_1000_genomes_KHV_filtered --exclude all_1000_genomes_SNP_filter_multiallelic.txt --make-bed --out all_1000_genomes_KHV_filtered_biallelic
plink --bfile all_1000_genomes_LWK_filtered --exclude all_1000_genomes_SNP_filter_multiallelic.txt --make-bed --out all_1000_genomes_LWK_filtered_biallelic
plink --bfile all_1000_genomes_MSL_filtered --exclude all_1000_genomes_SNP_filter_multiallelic.txt --make-bed --out all_1000_genomes_MSL_filtered_biallelic
plink --bfile all_1000_genomes_MXL_filtered --exclude all_1000_genomes_SNP_filter_multiallelic.txt --make-bed --out all_1000_genomes_MXL_filtered_biallelic
plink --bfile all_1000_genomes_PEL_filtered --exclude all_1000_genomes_SNP_filter_multiallelic.txt --make-bed --out all_1000_genomes_PEL_filtered_biallelic
plink --bfile all_1000_genomes_PJL_filtered --exclude all_1000_genomes_SNP_filter_multiallelic.txt --make-bed --out all_1000_genomes_PJL_filtered_biallelic
plink --bfile all_1000_genomes_PUR_filtered --exclude all_1000_genomes_SNP_filter_multiallelic.txt --make-bed --out all_1000_genomes_PUR_filtered_biallelic
plink --bfile all_1000_genomes_STU_filtered --exclude all_1000_genomes_SNP_filter_multiallelic.txt --make-bed --out all_1000_genomes_STU_filtered_biallelic
plink --bfile all_1000_genomes_TSI_filtered --exclude all_1000_genomes_SNP_filter_multiallelic.txt --make-bed --out all_1000_genomes_TSI_filtered_biallelic
plink --bfile all_1000_genomes_YRI_filtered --exclude all_1000_genomes_SNP_filter_multiallelic.txt --make-bed --out all_1000_genomes_YRI_filtered_biallelic
rm all_1000_genomes_ACB_filtered.bed
rm all_1000_genomes_ACB_filtered.bim
rm all_1000_genomes_ACB_filtered.fam
rm all_1000_genomes_ACB_filtered_biallelic.log
rm all_1000_genomes_ASW_filtered.bed
rm all_1000_genomes_ASW_filtered.bim
rm all_1000_genomes_ASW_filtered.fam
rm all_1000_genomes_ASW_filtered_biallelic.log
rm all_1000_genomes_BEB_filtered.bed
rm all_1000_genomes_BEB_filtered.bim
rm all_1000_genomes_BEB_filtered.fam
rm all_1000_genomes_BEB_filtered_biallelic.log
rm all_1000_genomes_CDX_filtered.bed
rm all_1000_genomes_CDX_filtered.bim
rm all_1000_genomes_CDX_filtered.fam
rm all_1000_genomes_CDX_filtered_biallelic.log
rm all_1000_genomes_CEU_filtered.bed
rm all_1000_genomes_CEU_filtered.bim
rm all_1000_genomes_CEU_filtered.fam
rm all_1000_genomes_CEU_filtered_biallelic.log
rm all_1000_genomes_CHB_filtered.bed
rm all_1000_genomes_CHB_filtered.bim
rm all_1000_genomes_CHB_filtered.fam
rm all_1000_genomes_CHB_filtered_biallelic.log
rm all_1000_genomes_CHS_filtered.bed
rm all_1000_genomes_CHS_filtered.bim
rm all_1000_genomes_CHS_filtered.fam
rm all_1000_genomes_CHS_filtered_biallelic.log
rm all_1000_genomes_CLM_filtered.bed
rm all_1000_genomes_CLM_filtered.bim
rm all_1000_genomes_CLM_filtered.fam
rm all_1000_genomes_CLM_filtered_biallelic.log
rm all_1000_genomes_ESN_filtered.bed
rm all_1000_genomes_ESN_filtered.bim
rm all_1000_genomes_ESN_filtered.fam
rm all_1000_genomes_ESN_filtered_biallelic.log
rm all_1000_genomes_FIN_filtered.bed
rm all_1000_genomes_FIN_filtered.bim
rm all_1000_genomes_FIN_filtered.fam
rm all_1000_genomes_FIN_filtered_biallelic.log
rm all_1000_genomes_GBR_filtered.bed
rm all_1000_genomes_GBR_filtered.bim
rm all_1000_genomes_GBR_filtered.fam
rm all_1000_genomes_GBR_filtered_biallelic.log
rm all_1000_genomes_GIH_filtered.bed
rm all_1000_genomes_GIH_filtered.bim
rm all_1000_genomes_GIH_filtered.fam
rm all_1000_genomes_GIH_filtered_biallelic.log
rm all_1000_genomes_GWD_filtered.bed
rm all_1000_genomes_GWD_filtered.bim
rm all_1000_genomes_GWD_filtered.fam
rm all_1000_genomes_GWD_filtered_biallelic.log
rm all_1000_genomes_IBS_filtered.bed
rm all_1000_genomes_IBS_filtered.bim
rm all_1000_genomes_IBS_filtered.fam
rm all_1000_genomes_IBS_filtered_biallelic.log
rm all_1000_genomes_ITU_filtered.bed
rm all_1000_genomes_ITU_filtered.bim
rm all_1000_genomes_ITU_filtered.fam
rm all_1000_genomes_ITU_filtered_biallelic.log
rm all_1000_genomes_JPT_filtered.bed
rm all_1000_genomes_JPT_filtered.bim
rm all_1000_genomes_JPT_filtered.fam
rm all_1000_genomes_JPT_filtered_biallelic.log
rm all_1000_genomes_KHV_filtered.bed
rm all_1000_genomes_KHV_filtered.bim
rm all_1000_genomes_KHV_filtered.fam
rm all_1000_genomes_KHV_filtered_biallelic.log
rm all_1000_genomes_LWK_filtered.bed
rm all_1000_genomes_LWK_filtered.bim
rm all_1000_genomes_LWK_filtered.fam
rm all_1000_genomes_LWK_filtered_biallelic.log
rm all_1000_genomes_MSL_filtered.bed
rm all_1000_genomes_MSL_filtered.bim
rm all_1000_genomes_MSL_filtered.fam
rm all_1000_genomes_MSL_filtered_biallelic.log
rm all_1000_genomes_MXL_filtered.bed
rm all_1000_genomes_MXL_filtered.bim
rm all_1000_genomes_MXL_filtered.fam
rm all_1000_genomes_MXL_filtered_biallelic.log
rm all_1000_genomes_PEL_filtered.bed
rm all_1000_genomes_PEL_filtered.bim
rm all_1000_genomes_PEL_filtered.fam
rm all_1000_genomes_PEL_filtered_biallelic.log
rm all_1000_genomes_PJL_filtered.bed
rm all_1000_genomes_PJL_filtered.bim
rm all_1000_genomes_PJL_filtered.fam
rm all_1000_genomes_PJL_filtered_biallelic.log
rm all_1000_genomes_PUR_filtered.bed
rm all_1000_genomes_PUR_filtered.bim
rm all_1000_genomes_PUR_filtered.fam
rm all_1000_genomes_PUR_filtered_biallelic.log
rm all_1000_genomes_STU_filtered.bed
rm all_1000_genomes_STU_filtered.bim
rm all_1000_genomes_STU_filtered.fam
rm all_1000_genomes_STU_filtered_biallelic.log
rm all_1000_genomes_TSI_filtered.bed
rm all_1000_genomes_TSI_filtered.bim
rm all_1000_genomes_TSI_filtered.fam
rm all_1000_genomes_TSI_filtered_biallelic.log
rm all_1000_genomes_YRI_filtered.bed
rm all_1000_genomes_YRI_filtered.bim
rm all_1000_genomes_YRI_filtered.fam
rm all_1000_genomes_YRI_filtered_biallelic.log


# finally, randomly thin until only about 500000 SNPs remain.
plink --bfile all_1000_genomes_ACB_filtered_biallelic --thin-count 500000 --make-bed --out all_1000_genomes_ACB_processed
# This places the SNPs in all_1000_genomes_ACB_processed.bim into all_1000_genomes_random_filter.txt
python all_1000_genomes_random_filter_getter.py
plink --bfile all_1000_genomes_ASW_filtered_biallelic --extract all_1000_genomes_random_filter.txt --make-bed --out all_1000_genomes_ASW_processed
plink --bfile all_1000_genomes_BEB_filtered_biallelic --extract all_1000_genomes_random_filter.txt --make-bed --out all_1000_genomes_BEB_processed
plink --bfile all_1000_genomes_CDX_filtered_biallelic --extract all_1000_genomes_random_filter.txt --make-bed --out all_1000_genomes_CDX_processed
plink --bfile all_1000_genomes_CEU_filtered_biallelic --extract all_1000_genomes_random_filter.txt --make-bed --out all_1000_genomes_CEU_processed
plink --bfile all_1000_genomes_CHB_filtered_biallelic --extract all_1000_genomes_random_filter.txt --make-bed --out all_1000_genomes_CHB_processed
plink --bfile all_1000_genomes_CHS_filtered_biallelic --extract all_1000_genomes_random_filter.txt --make-bed --out all_1000_genomes_CHS_processed
plink --bfile all_1000_genomes_CLM_filtered_biallelic --extract all_1000_genomes_random_filter.txt --make-bed --out all_1000_genomes_CLM_processed
plink --bfile all_1000_genomes_ESN_filtered_biallelic --extract all_1000_genomes_random_filter.txt --make-bed --out all_1000_genomes_ESN_processed
plink --bfile all_1000_genomes_FIN_filtered_biallelic --extract all_1000_genomes_random_filter.txt --make-bed --out all_1000_genomes_FIN_processed
plink --bfile all_1000_genomes_GBR_filtered_biallelic --extract all_1000_genomes_random_filter.txt --make-bed --out all_1000_genomes_GBR_processed
plink --bfile all_1000_genomes_GIH_filtered_biallelic --extract all_1000_genomes_random_filter.txt --make-bed --out all_1000_genomes_GIH_processed
plink --bfile all_1000_genomes_GWD_filtered_biallelic --extract all_1000_genomes_random_filter.txt --make-bed --out all_1000_genomes_GWD_processed
plink --bfile all_1000_genomes_IBS_filtered_biallelic --extract all_1000_genomes_random_filter.txt --make-bed --out all_1000_genomes_IBS_processed
plink --bfile all_1000_genomes_ITU_filtered_biallelic --extract all_1000_genomes_random_filter.txt --make-bed --out all_1000_genomes_ITU_processed
plink --bfile all_1000_genomes_JPT_filtered_biallelic --extract all_1000_genomes_random_filter.txt --make-bed --out all_1000_genomes_JPT_processed
plink --bfile all_1000_genomes_KHV_filtered_biallelic --extract all_1000_genomes_random_filter.txt --make-bed --out all_1000_genomes_KHV_processed
plink --bfile all_1000_genomes_LWK_filtered_biallelic --extract all_1000_genomes_random_filter.txt --make-bed --out all_1000_genomes_LWK_processed
plink --bfile all_1000_genomes_MSL_filtered_biallelic --extract all_1000_genomes_random_filter.txt --make-bed --out all_1000_genomes_MSL_processed
plink --bfile all_1000_genomes_MXL_filtered_biallelic --extract all_1000_genomes_random_filter.txt --make-bed --out all_1000_genomes_MXL_processed
plink --bfile all_1000_genomes_PEL_filtered_biallelic --extract all_1000_genomes_random_filter.txt --make-bed --out all_1000_genomes_PEL_processed
plink --bfile all_1000_genomes_PJL_filtered_biallelic --extract all_1000_genomes_random_filter.txt --make-bed --out all_1000_genomes_PJL_processed
plink --bfile all_1000_genomes_PUR_filtered_biallelic --extract all_1000_genomes_random_filter.txt --make-bed --out all_1000_genomes_PUR_processed
plink --bfile all_1000_genomes_STU_filtered_biallelic --extract all_1000_genomes_random_filter.txt --make-bed --out all_1000_genomes_STU_processed
plink --bfile all_1000_genomes_TSI_filtered_biallelic --extract all_1000_genomes_random_filter.txt --make-bed --out all_1000_genomes_TSI_processed
plink --bfile all_1000_genomes_YRI_filtered_biallelic --extract all_1000_genomes_random_filter.txt --make-bed --out all_1000_genomes_YRI_processed
rm all_1000_genomes_ACB_filtered_biallelic.bed
rm all_1000_genomes_ACB_filtered_biallelic.bim
rm all_1000_genomes_ACB_filtered_biallelic.fam
rm all_1000_genomes_ACB_processed.log
rm all_1000_genomes_ASW_filtered_biallelic.bed
rm all_1000_genomes_ASW_filtered_biallelic.bim
rm all_1000_genomes_ASW_filtered_biallelic.fam
rm all_1000_genomes_ASW_processed.log
rm all_1000_genomes_BEB_filtered_biallelic.bed
rm all_1000_genomes_BEB_filtered_biallelic.bim
rm all_1000_genomes_BEB_filtered_biallelic.fam
rm all_1000_genomes_BEB_processed.log
rm all_1000_genomes_CDX_filtered_biallelic.bed
rm all_1000_genomes_CDX_filtered_biallelic.bim
rm all_1000_genomes_CDX_filtered_biallelic.fam
rm all_1000_genomes_CDX_processed.log
rm all_1000_genomes_CEU_filtered_biallelic.bed
rm all_1000_genomes_CEU_filtered_biallelic.bim
rm all_1000_genomes_CEU_filtered_biallelic.fam
rm all_1000_genomes_CEU_processed.log
rm all_1000_genomes_CHB_filtered_biallelic.bed
rm all_1000_genomes_CHB_filtered_biallelic.bim
rm all_1000_genomes_CHB_filtered_biallelic.fam
rm all_1000_genomes_CHB_processed.log
rm all_1000_genomes_CHS_filtered_biallelic.bed
rm all_1000_genomes_CHS_filtered_biallelic.bim
rm all_1000_genomes_CHS_filtered_biallelic.fam
rm all_1000_genomes_CHS_processed.log
rm all_1000_genomes_CLM_filtered_biallelic.bed
rm all_1000_genomes_CLM_filtered_biallelic.bim
rm all_1000_genomes_CLM_filtered_biallelic.fam
rm all_1000_genomes_CLM_processed.log
rm all_1000_genomes_ESN_filtered_biallelic.bed
rm all_1000_genomes_ESN_filtered_biallelic.bim
rm all_1000_genomes_ESN_filtered_biallelic.fam
rm all_1000_genomes_ESN_processed.log
rm all_1000_genomes_FIN_filtered_biallelic.bed
rm all_1000_genomes_FIN_filtered_biallelic.bim
rm all_1000_genomes_FIN_filtered_biallelic.fam
rm all_1000_genomes_FIN_processed.log
rm all_1000_genomes_GBR_filtered_biallelic.bed
rm all_1000_genomes_GBR_filtered_biallelic.bim
rm all_1000_genomes_GBR_filtered_biallelic.fam
rm all_1000_genomes_GBR_processed.log
rm all_1000_genomes_GIH_filtered_biallelic.bed
rm all_1000_genomes_GIH_filtered_biallelic.bim
rm all_1000_genomes_GIH_filtered_biallelic.fam
rm all_1000_genomes_GIH_processed.log
rm all_1000_genomes_GWD_filtered_biallelic.bed
rm all_1000_genomes_GWD_filtered_biallelic.bim
rm all_1000_genomes_GWD_filtered_biallelic.fam
rm all_1000_genomes_GWD_processed.log
rm all_1000_genomes_IBS_filtered_biallelic.bed
rm all_1000_genomes_IBS_filtered_biallelic.bim
rm all_1000_genomes_IBS_filtered_biallelic.fam
rm all_1000_genomes_IBS_processed.log
rm all_1000_genomes_ITU_filtered_biallelic.bed
rm all_1000_genomes_ITU_filtered_biallelic.bim
rm all_1000_genomes_ITU_filtered_biallelic.fam
rm all_1000_genomes_ITU_processed.log
rm all_1000_genomes_JPT_filtered_biallelic.bed
rm all_1000_genomes_JPT_filtered_biallelic.bim
rm all_1000_genomes_JPT_filtered_biallelic.fam
rm all_1000_genomes_JPT_processed.log
rm all_1000_genomes_KHV_filtered_biallelic.bed
rm all_1000_genomes_KHV_filtered_biallelic.bim
rm all_1000_genomes_KHV_filtered_biallelic.fam
rm all_1000_genomes_KHV_processed.log
rm all_1000_genomes_LWK_filtered_biallelic.bed
rm all_1000_genomes_LWK_filtered_biallelic.bim
rm all_1000_genomes_LWK_filtered_biallelic.fam
rm all_1000_genomes_LWK_processed.log
rm all_1000_genomes_MSL_filtered_biallelic.bed
rm all_1000_genomes_MSL_filtered_biallelic.bim
rm all_1000_genomes_MSL_filtered_biallelic.fam
rm all_1000_genomes_MSL_processed.log
rm all_1000_genomes_MXL_filtered_biallelic.bed
rm all_1000_genomes_MXL_filtered_biallelic.bim
rm all_1000_genomes_MXL_filtered_biallelic.fam
rm all_1000_genomes_MXL_processed.log
rm all_1000_genomes_PEL_filtered_biallelic.bed
rm all_1000_genomes_PEL_filtered_biallelic.bim
rm all_1000_genomes_PEL_filtered_biallelic.fam
rm all_1000_genomes_PEL_processed.log
rm all_1000_genomes_PJL_filtered_biallelic.bed
rm all_1000_genomes_PJL_filtered_biallelic.bim
rm all_1000_genomes_PJL_filtered_biallelic.fam
rm all_1000_genomes_PJL_processed.log
rm all_1000_genomes_PUR_filtered_biallelic.bed
rm all_1000_genomes_PUR_filtered_biallelic.bim
rm all_1000_genomes_PUR_filtered_biallelic.fam
rm all_1000_genomes_PUR_processed.log
rm all_1000_genomes_STU_filtered_biallelic.bed
rm all_1000_genomes_STU_filtered_biallelic.bim
rm all_1000_genomes_STU_filtered_biallelic.fam
rm all_1000_genomes_STU_processed.log
rm all_1000_genomes_TSI_filtered_biallelic.bed
rm all_1000_genomes_TSI_filtered_biallelic.bim
rm all_1000_genomes_TSI_filtered_biallelic.fam
rm all_1000_genomes_TSI_processed.log
rm all_1000_genomes_YRI_filtered_biallelic.bed
rm all_1000_genomes_YRI_filtered_biallelic.bim
rm all_1000_genomes_YRI_filtered_biallelic.fam
rm all_1000_genomes_YRI_processed.log
rm all_1000_genomes_ACB.log
rm all_1000_genomes_ASW.log
rm all_1000_genomes_BEB.log
rm all_1000_genomes_CDX.log
rm all_1000_genomes_CEU.log
rm all_1000_genomes_CHB.log
rm all_1000_genomes_CHS.log
rm all_1000_genomes_CLM.log
rm all_1000_genomes_ESN.log
rm all_1000_genomes_FIN.log
rm all_1000_genomes_GBR.log
rm all_1000_genomes_GIH.log
rm all_1000_genomes_GWD.log
rm all_1000_genomes_IBS.log
rm all_1000_genomes_ITU.log
rm all_1000_genomes_JPT.log
rm all_1000_genomes_KHV.log
rm all_1000_genomes_LWK.log
rm all_1000_genomes_MSL.log
rm all_1000_genomes_MXL.log
rm all_1000_genomes_PEL.log
rm all_1000_genomes_PJL.log
rm all_1000_genomes_PUR.log
rm all_1000_genomes_STU.log
rm all_1000_genomes_TSI.log
rm all_1000_genomes_YRI.log

