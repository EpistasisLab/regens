import numpy as np
import pandas as pd
import pdb
from copy import deepcopy as COPY

def reduce_recomb_rate_info(rcmb_rate_info, bim_SNP_positions):
    
    rcmb_rate_intervals = rcmb_rate_info["Position(bp)"].to_numpy()

    # INDEXING NOTE: Not subtracting one from "SNP_pos_rcmb_interval_map" returns the closest indices of "rcmb_rate_intervals"
    #                boundaries at genomic positions to the RIGHT of each SNP's genomic position in bim_SNP_positions.
    #                The only row still needed is the closest boundary to the LEFT of the first SNP. This is aquired by
    #                implementing "occupied_rcmb_intervals[np.min(np.where(occupied_rcmb_intervals == True)) - 1] = True".

    SNP_pos_rcmb_interval_map = SNP_positions_to_rcmb_intervals(rcmb_rate_intervals, COPY(bim_SNP_positions))
    all_rcmb_intervals = np.arange(len(rcmb_rate_intervals))
    occupied_rcmb_intervals = np.isin(all_rcmb_intervals, SNP_pos_rcmb_interval_map)
    occupied_rcmb_intervals[np.min(np.where(occupied_rcmb_intervals == True)) - 1] = True
    reduced_rcmb_rate_info = rcmb_rate_info[occupied_rcmb_intervals]

    return(reduced_rcmb_rate_info)

def SNP_positions_to_rcmb_intervals(rcmb_interval_boundaries, bim_SNP_positions):

    prev_start_pos = 0
    SNP_rcmb_interval_indices = np.zeros(len(bim_SNP_positions), dtype = np.int64) 
    too_large_indices = bim_SNP_positions >= np.max(rcmb_interval_boundaries)
    too_small_indices = bim_SNP_positions <= np.min(rcmb_interval_boundaries)
    bim_SNP_positions[too_large_indices] = np.max(rcmb_interval_boundaries) - 1
    bim_SNP_positions[too_small_indices] = np.min(rcmb_interval_boundaries) + 1
    num_outer_SNPs = np.sum(too_large_indices) + np.sum(too_small_indices) 
    if num_outer_SNPs > 0:
        print("\nCAUTION: " + str(num_outer_SNPs) + " SNP(s) in the bim file are outside of the positional range considered by the recombination rate info file.\n")
        print("This is unlikely to be an issue if the number of such SNPs is small. Otherwise, remove those SNPs from the input plink files\n")
        print("bim file SNPs earlier than the first recombination interval are assumed to be inside of the first recombination interval.\n")
        print("bim file SNPs farther than the last recombination interval are assumed to be inside of the last recombination interval.\n")
    for i in range(len(bim_SNP_positions)):
        for k in range(len(rcmb_interval_boundaries) - prev_start_pos):
            if rcmb_interval_boundaries[prev_start_pos + k] >= bim_SNP_positions[i]:
                SNP_rcmb_interval_indices[i] = prev_start_pos + k
                prev_start_pos += k
                break
    
    return(SNP_rcmb_interval_indices)

def draw_breakpoints(rcmb_info, bim_info):

    interval_bounds = rcmb_info["Position(bp)"].to_numpy()
    interval_rcmb_rates = (rcmb_info["Map(cM)"].to_numpy())[1:] - (rcmb_info["Map(cM)"].to_numpy())[:-1]
    next_interval_index = 0
    SNP_pos_rcmb_rates = []
    for i, SNP_pos in enumerate(bim_info[3].to_numpy()):
        if SNP_pos <=  interval_bounds[next_interval_index + 1]:
            SNP_pos_rcmb_rates.append(interval_rcmb_rates[next_interval_index])
        else:
            next_interval_index += 1
            if SNP_pos <=  interval_bounds[next_interval_index + 1]:
                SNP_pos_rcmb_rates.append(interval_rcmb_rates[next_interval_index])
            else:
                print("There was a problem")
                pdb.set_trace()
            
    return(np.array(SNP_pos_rcmb_rates))


main_path = "/home/greggj/GxE/REALGenomeSIM/regens/"

bim_info = pd.read_csv(main_path + "input_files/ACB.bim", sep = "\t", header = None)
bim_info_chr = [bim_info[bim_info[0] == i] for i in range(1, 23)]

rcmb_info_paths = [main_path + "hg19/ACB/ACB_recombination_map_hapmap_format_hg19_chr_" + str(i) + ".txt.gz" for i in range(1, 23)]
rcmb_info_chr = [pd.read_csv(path, delim_whitespace = True, header = 0, compression = "gzip") for path in rcmb_info_paths]
rcmb_info_chr = [reduce_recomb_rate_info(rcmb_info_chr[i], bim_info_chr[i][3].to_numpy()) for i in range(22)]

SNP_pos_rcmb_rate_sets = [draw_breakpoints(rcmb_info_chr[i], bim_info_chr[i]) for i in range(22)]
for i in range(22):
    bim_info_chr[i][2] = SNP_pos_rcmb_rate_sets[i]
    bim_info_chr[i] = bim_info_chr[i][[0,1,3,2]]
triadsim_rcmb_rates = pd.concat(bim_info_chr)
triadsim_rcmb_rates.columns = ["CHR", "RS", "POS", "RATE"]
triadsim_rcmb_rates.to_csv("triadsim_rcmb_rate_df.tab", sep = "\t", header = True, index = False)
