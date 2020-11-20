import pandas as pd
import numpy as np
# python all_1000_genomes_get_duplicated_SNPs.py

SNPs = (pd.read_csv("all_1000_genomes_GBR_filtered.bim", delimiter = "\t", header = None))[1]
unique_SNPs, counts  = np.unique(SNPs, return_counts=True)
SNPs_to_remove = unique_SNPs[counts > 1]
SNPs_to_remove_file = open("all_1000_genomes_SNP_filter_multiallelic.txt", "w")
SNPs_to_remove_file.write("\n".join(SNPs_to_remove.tolist()))
SNPs_to_remove_file.close()