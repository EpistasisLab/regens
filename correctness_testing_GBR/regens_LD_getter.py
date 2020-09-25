import pdb 
import numpy as np
import pandas as pd
import argparse
from matplotlib import pyplot as plt
from tqdm import tqdm
from pysnptools.snpreader import SnpData
from regens_LD_cgetter import open_LD_file
from regens_LD_cgetter import binner
from scipy.stats import pearsonr

parser = argparse.ArgumentParser()
parser.add_argument('--ref', nargs = "?", type = str, action = "store", dest = "ref_fname")
parser.add_argument('--sim', nargs = "?", type = str, action = "store", dest = "sim_fname")
# python triadsim_LD_getter.py --ref GBR --sim GBR_simulated

args = parser.parse_args()
reference_ld_files = [args.ref_fname + "_chr" + str(i) + ".ld" for i in range(1, 23)]
simulation_ld_files = [args.sim_fname + "_chr" + str(i) + ".ld" for i in range(1, 23)]


r_reference_chr = []
SNP2_mafs_reference_chr = []
SNP2_ID_reference_chr = []
SNP2_position_reference_chr = []
chromosome_reference_chr = []
SNP1_maf_reference_chr = []
SNP1_ID_reference_chr = []
SNP1_position_reference_chr = []

r_simulated_chr = []
SNP2_mafs_simulated_chr = []
SNP2_ID_simulated_chr = []
SNP2_position_simulated_chr = []
chromosome_simulated_chr = []
SNP1_maf_simulated_chr = []
SNP1_ID_simulated_chr = []
SNP1_position_simulated_chr = []


for i in range(22):
    a, b, c, d, e, f, g, h = open_LD_file(reference_ld_files[i])
    r_reference = a
    SNP2_mafs_reference = b
    SNP2_ID_reference = c
    SNP2_position_reference = d
    chromosome_reference = e
    SNP1_maf_reference = f
    SNP1_ID_reference = g
    SNP1_position_reference = h
    float_indices_reference = np.isnan(r_reference) == False

    a2, b2, c2, d2, e2, f2, g2, h2 = open_LD_file(simulation_ld_files[i])
    r_simulated = a2
    SNP2_mafs_simulated = b2
    SNP2_ID_simulated = c2
    SNP2_position_simulated = d2
    chromosome_simulated = e2
    SNP1_maf_simulated = f2
    SNP1_ID_simulated = g2
    SNP1_position_simulated = h2
    float_indices_simulated = np.isnan(r_simulated) == False

    float_indices = np.logical_and(float_indices_reference, float_indices_simulated)

    r_reference_chr.append(r_reference[float_indices])
    SNP2_mafs_reference_chr.append(SNP2_mafs_reference[float_indices])
    SNP2_ID_reference_chr.append(SNP2_ID_reference[float_indices])
    SNP2_position_reference_chr.append(SNP2_position_reference[float_indices])
    chromosome_reference_chr.append(chromosome_reference[float_indices])
    SNP1_maf_reference_chr.append(SNP1_maf_reference[float_indices])
    SNP1_ID_reference_chr.append(SNP1_ID_reference[float_indices])
    SNP1_position_reference_chr.append(SNP1_position_reference[float_indices])

    r_simulated_chr.append(r_simulated[float_indices])
    SNP2_mafs_simulated_chr.append(SNP2_mafs_simulated[float_indices])
    SNP2_ID_simulated_chr.append(SNP2_ID_simulated[float_indices])
    SNP2_position_simulated_chr.append(SNP2_position_simulated[float_indices])
    chromosome_simulated_chr.append(chromosome_simulated[float_indices])
    SNP1_maf_simulated_chr.append(SNP1_maf_simulated[float_indices])
    SNP1_ID_simulated_chr.append(SNP1_ID_simulated[float_indices])
    SNP1_position_simulated_chr.append(SNP1_position_simulated[float_indices])

r_reference = np.concatenate(r_reference_chr, axis = 0)
SNP2_mafs_reference = np.concatenate(SNP2_mafs_reference_chr, axis = 0)
SNP2_ID_reference = np.concatenate(SNP2_ID_reference_chr, axis = 0)
SNP2_position_reference = np.concatenate(SNP2_position_reference_chr, axis = 0)
chromosome_reference = np.concatenate(chromosome_reference_chr, axis = 0)
SNP1_maf_reference = np.concatenate(SNP1_maf_reference_chr, axis = 0)
SNP1_ID_reference = np.concatenate(SNP1_ID_reference_chr, axis = 0)
SNP1_position_reference = np.concatenate(SNP1_position_reference_chr, axis = 0)

r_simulated = np.concatenate(r_simulated_chr, axis = 0)
SNP2_mafs_simulated = np.concatenate(SNP2_mafs_simulated_chr, axis = 0)
SNP2_ID_simulated = np.concatenate(SNP2_ID_simulated_chr, axis = 0)
SNP2_position_simulated = np.concatenate(SNP2_position_simulated_chr, axis = 0)
chromosome_simulated = np.concatenate(chromosome_simulated_chr, axis = 0)
SNP1_maf_simulated = np.concatenate(SNP1_maf_simulated_chr, axis = 0)
SNP1_ID_simulated = np.concatenate(SNP1_ID_simulated_chr, axis = 0)
SNP1_position_simulated = np.concatenate(SNP1_position_simulated_chr, axis = 0)

all_SNP_indices = np.concatenate([SNP2_ID_reference, SNP1_ID_reference], axis = 0)
all_mafs_reference = np.concatenate([SNP2_mafs_reference, SNP1_maf_reference], axis = 0)
all_mafs_simulated = np.concatenate([SNP2_mafs_simulated, SNP1_maf_simulated], axis = 0)
void, unique_SNP_indices = np.unique(all_SNP_indices, return_index = True)
unique_mafs_reference = all_mafs_reference[unique_SNP_indices]
unique_mafs_simulated = all_mafs_simulated[unique_SNP_indices]

fig, plots = plt.subplots(1, 2, figsize = (16, 7))
bad_indices = (np.abs(r_reference - r_simulated) > 0.1)
good_indices = (np.abs(r_reference - r_simulated) <= 0.1)
maf_pairs = np.array([SNP2_mafs_reference, SNP1_maf_reference])
median_good_maf = np.median(maf_pairs.T[good_indices])
median_bad_maf = np.median(maf_pairs.T[bad_indices])
plots[0].plot(r_reference[good_indices], r_simulated[good_indices], '.k', label = "real vs simulated r values for\n " + args.ref_fname + " subpopulation\n (n = " + str(np.sum(good_indices)) + ", median maf = " + str(median_good_maf) + ")")
plots[0].plot(r_reference[bad_indices], r_simulated[bad_indices], 'xr', label = "real vs simulated r outliers for\n " + args.ref_fname + " subpopulation\n (n = " + str(np.sum(bad_indices)) + ", median maf = " + str(median_bad_maf) + ")")
plots[1].plot(unique_mafs_reference, unique_mafs_simulated, '.k', label = "real vs simulated mafs for " + args.ref_fname + " subpopulation")
plots[0].legend(loc = "upper left")
plots[1].legend(loc = "upper left")
plots[0].set(xlabel = "real r values", ylabel = "simulated r values")
plots[1].set(xlabel = "real mafs", ylabel = "simulated mafs")
plots[0].set_title("real versus simulated r values \n for " + args.ref_fname + " subpopulation")
plots[1].set_title("real versus simulated mafs \n for " + args.ref_fname + " subpopulation")
fig.savefig(args.ref_fname + "_real_vs_sim_r_val_maf_comparision.png")
fig.clf()

distances = SNP2_position_reference - SNP1_position_reference
distances[np.where(distances == 0)] = 1

sorted_distance_indices = np.argsort(distances)
sorted_distances = distances[sorted_distance_indices]
sorted_r_vals_reference = np.abs(r_reference[sorted_distance_indices])
sorted_r_vals_simulated = np.abs(r_simulated[sorted_distance_indices])
unique_distances = np.unique(sorted_distances)
equal_distance_indices  = binner(sorted_distances, len(unique_distances))
average_LD_per_distance_reference = np.array([np.mean(sorted_r_vals_reference[np.array(set)]) for set in equal_distance_indices])
average_LD_per_distance_simulated = np.array([np.mean(sorted_r_vals_simulated[np.array(set)]) for set in equal_distance_indices])

N = 4000
min_indices = [i*int(len(unique_distances)/N) for i in range(N)]
max_indices = [(i + 1)*int(len(unique_distances)/N) for i in range(N)]
unique_distances2 = [np.mean(unique_distances[min_indices[i]:max_indices[i]]) for i in range(N)]
average_LD_per_distance2_reference = [np.mean(average_LD_per_distance_reference[min_indices[i]:max_indices[i]]) for i in range(N)]
average_LD_per_distance2_simulated = [np.mean(average_LD_per_distance_simulated[min_indices[i]:max_indices[i]]) for i in range(N)]

fig, plots = plt.subplots(1, 2, figsize = (16, 7))
plots[0].plot(unique_distances2, average_LD_per_distance2_reference, '.', label = "average absolute r vs distance for real" + args.ref_fname)
plots[1].plot(unique_distances2, average_LD_per_distance2_simulated, '.', label = "average absolute r vs distance for simulated " + args.ref_fname)
plots[0].legend(loc = "upper right")
plots[1].legend(loc = "upper right")
plots[0].set(xlabel = "distance between SNPs", ylabel = "average absolute r value")
plots[1].set(xlabel = "distance between SNPs", ylabel = "average absolute r value")
plots[0].set_title("absolute r versus distance \n for real " + args.ref_fname + " subpopulation")
plots[1].set_title("absolute r versus distance \n for simulated " + args.ref_fname + " subpopulation")
fig.savefig(args.ref_fname + "_real_vs_sim_r_vs_distance_profile_comparison.png")
fig.clf()