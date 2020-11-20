import pandas as pd
import numpy as np
import pdb

processed_bim_SNPs = (pd.read_csv("all_1000_genomes_ACB_processed.bim", sep = "\t", header = None))
file = open("all_1000_genomes_random_filter.txt", "w")
file.write("\n".join(processed_bim_SNPs[1].to_list()))
file.close()
    
