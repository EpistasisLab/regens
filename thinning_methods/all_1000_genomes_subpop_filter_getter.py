import pandas as pd
import numpy as np
import pdb

pop_data = pd.read_csv("all_1000_genomes_filtered.psam", sep = "\t", header = 0)
subpops = np.unique(pop_data["Population"])
for subpop in subpops:
    file = open("all_1000_genomes_" + subpop + "_filter.txt", "w")
    file.write("\n".join(((pop_data[pop_data["Population"] == subpop])["#IID"]).to_list()))
    file.close()
    
