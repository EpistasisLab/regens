import pandas as pd
import numpy as np
from functools import reduce
import pdb 

subpops = ['ACB', 'ASW', 'BEB', 'CDX', 'CEU', 'CHB', 'CHS', 'CLM', 'ESN', 'FIN', 'GBR', 'GIH', 'GWD', 'IBS', 'ITU', 'JPT', 'KHV', 'LWK', 'MSL', 'MXL', 'PEL', 'PJL', 'PUR', 'STU', 'TSI', 'YRI']

print(1)
pop_mafs_list = [pd.read_csv("all_1000_genomes_" + pop + ".afreq", sep = "\t", header = 0, usecols = ["ALT_FREQS"], engine = 'c').to_numpy().reshape(-1) for pop in subpops]
#some freqs are 1 instead of 0, which is horrible, but can be accounted for
pop_low_maf_indices_list = [np.where(np.logical_or(pop_mafs <= np.min(pop_mafs[pop_mafs != 0]), pop_mafs >= np.max(pop_mafs[pop_mafs != 1])))[0] for pop_mafs in pop_mafs_list]
low_maf_indices = reduce(np.union1d, pop_low_maf_indices_list)
SNPs_to_remove = (pd.read_csv("all_1000_genomes_ACB.afreq", sep = "\t", header = 0, usecols = ["ID"], engine = 'c').to_numpy().reshape(-1))[low_maf_indices]

print(2)
pop_hwe_list = [pd.read_csv("all_1000_genomes_" + pop + ".hardy", sep = "\t", header = 0, usecols = ["P"], engine = 'c').to_numpy().reshape(-1) for pop in subpops]
pop_low_hwe_indices_list = [np.where(pop_hwe <= 1E-10)[0] for pop_hwe in pop_hwe_list]
low_hwe_indices = reduce(np.union1d, pop_low_hwe_indices_list)
SNPs_to_remove_hwe = (pd.read_csv("all_1000_genomes_ACB.hardy", sep = "\t", header = 0, usecols = ["ID"], engine = 'c').to_numpy().reshape(-1))[low_hwe_indices]

print(3)
SNPs_to_remove = np.union1d(SNPs_to_remove, SNPs_to_remove_hwe)
SNPs_to_remove = "\n".join(SNPs_to_remove)
SNPs_to_remove_file = open("all_1000_genomes_SNP_filter.txt", "w")
SNPs_to_remove_file.write(SNPs_to_remove)
SNPs_to_remove_file.close()
