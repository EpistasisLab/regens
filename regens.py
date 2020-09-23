import numpy as np
import pandas as pd
import argparse
import os
import pdb
from bed_reader import open_bed
from bed_reader import to_bed
from matplotlib import pyplot as plt
pd.options.mode.chained_assignment = None

from regens_library import SNP_positions_to_rcmb_intervals
from regens_library import reduce_recomb_rate_info
from regens_library import choice_with_periodic_replacement
from regens_library import centimorgans_to_probabilities
from regens_library import draw_breakpoints
from regens_library import get_samples_fast
from regens_library import breakpoints_to_simulated_individuals
from regens_library import write_bed_file
from regens_library import simulate_phenotypes

parser = argparse.ArgumentParser()
parser.add_argument('--in', nargs = "?", type = str, action = "store", dest = "input_plink_filename_prefix", default = "empty", help = 'input plink filename prefix')
parser.add_argument('--out', nargs = "?", type = str, action = "store", dest = "output_plink_filename_prefix", default = "simulated_whole_genomes", help = 'output plink filename prefix')
parser.add_argument('--simulate_nbreakpoints', nargs = "?", type = int, action = "store", dest = "num_breakpoints_simulated", default = 4, help = 'If there are n breakpoints, then each simulated chromosome is comprised of n+1 chunks, where each chunk is from a randomly drawn input sample')
parser.add_argument('--simulate_nsamples', nargs = "?", type = int, action = "store", dest = "num_samples_simulated", default = 1000, help = 'number of simulated')
parser.add_argument('--phenotype', nargs = "?", type = str, action = "store", dest = "phenotype", default = -9)
parser.add_argument('--mean_phenotype', nargs = "?", type = float, action = "store", dest = "mean_phenotype", default = None)
parser.add_argument('--population_code', nargs = "?", type = str, action = "store", dest = "population_code", default = "empty")
parser.add_argument('--human_genome_version', nargs = "?", type = str, action = "store", dest = "human_genome_version", default = "empty")
parser.add_argument('--recombination_file_path_prefix', nargs = "?", type = str, action = "store", dest = "recombination_file_path_prefix", default = "empty")
parser.add_argument('--noise', nargs = "?", type = float, action = "store", dest = "noise", default = 0)
parser.add_argument('--population_ID', nargs = "?", type = str, action = "store", dest = "population_ID", default = '')
parser.add_argument('--causal_SNP_IDs_path', nargs = "?", type = str, action = "store", dest = "causal_SNP_IDs_path", default = "empty", help = 'input plink filename prefix')
parser.add_argument('--major_minor_assignments_path', nargs = "?", type = str, action = "store", dest = "major_minor_assignments_path", default = "standard", help = 'input plink filename prefix')
parser.add_argument('--betas_path', nargs = "?", type = str, action = "store", dest = "betas_path", default = "empty", help = 'input plink filename prefix')
parser.add_argument('--SNP_phenotype_map_path', nargs = "?", type = str, action = "store", dest = "SNP_phenotype_map_path", default = "standard", help = 'input plink filename prefix')
parser.add_argument('--test_functionality', nargs = "?", type = str, action = "store", dest = "test_functionality", default = "no", help = 'input plink filename prefix')

args = parser.parse_args()
test_functionality = args.test_functionality
#imports functions to automatically test various aspects of the code if specified:
if test_functionality == "yes":
    from regens_testers import test_drawn_breakpoints
    from regens_testers import test_breakpoint_SNP_mapping
    from regens_testers import test_simulated_individuals

#checks the input plink filename prefix
input_plink_filename_prefix = args.input_plink_filename_prefix
bim_file_path = input_plink_filename_prefix + ".bim"
if os.path.isfile(input_plink_filename_prefix + ".bim") and os.path.isfile(input_plink_filename_prefix + ".bed") and os.path.isfile(input_plink_filename_prefix + ".fam"):
    bim_file = pd.read_csv(bim_file_path, delim_whitespace = True, header = None)
    if len(bim_file.columns) != 6:
        print("\nerror: bim file must be in standard format (it must have 6 columns).\n")
        exit()
    chromosomes = np.unique(bim_file[0])
    bim_SNP_pos_chr = [((bim_file[bim_file[0] == chr])[3]).to_numpy() for chr in chromosomes]
    bim_SNP_complete_pos_chr = [((bim_file[bim_file[0] == chr])[[0, 2, 3]]).to_numpy() for chr in chromosomes]
    bim_SNP_nucleotides_chr = [((bim_file[bim_file[0] == chr])[[4, 5]]).to_numpy().astype('U') for chr in chromosomes]
    bim_SNP_names = (bim_file[1]).to_numpy().astype('U')
    bim_SNP_names_chr = [((bim_file[bim_file[0] == chr])[1]).to_numpy().astype('U') for chr in chromosomes]
    chr_SNP_counts = [len(bim_SNP_pos_chr[i]) for i in range(len(chromosomes))]
    cumulative_SNP_counts = np.cumsum([0] + chr_SNP_counts)
else:
    print("\nerror: one or more of the three necessary plink files with the filename prefix '" + input_plink_filename_prefix + "' is not present.\n")
    exit()

# The output filename prefix does not need to be checked. 
output_plink_filename_prefix = args.output_plink_filename_prefix

# Checks the number of breakpoints
num_breakpoints = args.num_breakpoints_simulated
if num_breakpoints < 0:
    print("\nerror: the number of breakpoints cannot be negative.\n")
    exit()
if num_breakpoints == 0:
    print("\nwarning: setting 0 breakpoints means that each whole chromosome will be a real individual's whole chromosome from the dataset.\n")
if num_breakpoints > 5:
    print("\nwarning: you have selected " + str(num_breakpoints) + " breakpoints per chromosome, and there is no good reason to choose more than a few breakpoints per chromosome.\n") 
    print("The simulation may become worse if there aren't roughly as many high recombination rate regions as there are breakpoints, and it may require large ammounts of time and memory.\n")

# checks the number of samples to be simulated
simulation_sample_size = args.num_samples_simulated
if simulation_sample_size <= 0:
    print("\nerror: the number of simulated samples cannot be negative or 0.\n")
    exit()
SNP_count = cumulative_SNP_counts[-1]
minutes = str((126/60)*(simulation_sample_size/10000)*(SNP_count/531170))
max_ram = str((4.1)*(simulation_sample_size/10000)*(SNP_count/531170))
print("\nSimulating " + str(simulation_sample_size) + " samples and " + str(SNP_count) + " SNPs will require roughly " + minutes + " minutes and a maximum ram usage of " + max_ram + " GB.\n")

# checks the specified phenotype category
phenotype = args.phenotype
if phenotype not in ["continuous", "binary", -9]:
    print("\nerror: if a phenotype is specified, it must be 'continuous' or 'binary'.\n")
    exit()

# checks that the mean phenotype value makes sense
mean_phenotype = args.mean_phenotype
if phenotype == "binary":
    if mean_phenotype <= 0 or mean_phenotype >= 1:
        print("The mean phenotype value for a binary phenotype must be greater than 0 ort less than 1")
        exit()

# checks path information related to the recombination rate info file
pop_code = args.population_code
hg_version = args.human_genome_version
rcmb_path_prefix = args.recombination_file_path_prefix
hg_pop_codes = ["ACB", "ASW", "BEB", "CDX", "CEU", "CHB", "CHS", "CLM", "ESN", "FIN", "GBR", "GIH", "GWD", "IBS", "ITU", "JPT", "KHV", "LWK", "MSL", "MXL", "PEL", "PJL", "PUR", "STU", "TSI", "YRI"]

if rcmb_path_prefix != "empty":
    rcmb_rate_info_path_prefix = rcmb_path_prefix
elif hg_version in ["hg19", "hg38"]:
    if pop_code in hg_pop_codes:
        rcmb_rate_info_path_prefix = hg_version + "/" + pop_code + "/" + pop_code 
        rcmb_rate_info_path_prefix += "_recombination_map_hapmap_format_" + hg_version + "_chr_"
        try:
            rcmb_rate_info_file_names = np.sort(os.listdir(hg_version + "/" + pop_code))
            correct_info_file_names = np.sort([pop_code + "_recombination_map_hapmap_format_" + hg_version + "_chr_" + str(i) + ".txt.gz" for i in range(1, 23)])
        except:
            print("\nerror, possibility 1: Your working directory needs to be in the same directory as the triadsim_main.py file.\n")
            print("error, possibility 2: the triadsim_main.py file needs to be in the same directory as the hg19 and hg38 folders.\n") 
            exit()
        try: 
            if np.any(rcmb_rate_info_file_names != correct_info_file_names):
                exit()
        except:
            print("\nerror: a recombination rate map file has been deleted or is incorrectly named in" + rcmb_rate_info_path_prefix + ".\n")
            exit()        
else:
    print("\nerror: The human genome version must be 19 or 38, and the population code must be one of the following\n")
    print(hg_pop_codes)
    print("\nAlternatively, you can override the human genome version and population code arguments by adding a path to a custom recombination file with the recombination_file_path_prefix argument\n")
    exit()

# This downloads dataframes containing genomic intervals and recombination rates (in CentiMorgans/Megabase). There is one dataframe per chromosome. 
rcmb_rate_info_paths = [rcmb_rate_info_path_prefix + str(chr) + '.txt.gz' for chr in chromosomes]
rcmb_rate_info_chr = [pd.read_csv(path, delim_whitespace = True, header = 0, compression = "gzip") for path in rcmb_rate_info_paths]
rcmb_rate_info_chr = [reduce_recomb_rate_info(rcmb_rate_info_chr[i], bim_SNP_pos_chr[i]) for i in range(len(chromosomes))]
rcmb_rate_intervals_chr = [((rcmb_rate_info_chr[i])["Position(bp)"]).to_numpy().reshape(-1) for i in range(len(chromosomes))]

# checks that percent noise value makes sense
noise = args.noise
if noise < 0:
    print("The ammount of noise as a percentage of the average signal cannot be negative.")
    exit()

# gets the population ID for file_names. Doesn't need a type check. 
population_ID = args.population_ID
if population_ID == '' and pop_code in hg_pop_codes:
    population_ID = pop_code

# checks to make sure that input phenotype simulation files exist in the working directory
causal_SNP_IDs_path = args.causal_SNP_IDs_path
major_minor_assignments_path = args.major_minor_assignments_path
betas_path = args.betas_path
SNP_phenotype_map_path = args.SNP_phenotype_map_path
if not (os.path.isfile(causal_SNP_IDs_path) or (causal_SNP_IDs_path == "empty" and phenotype == -9)):
    print("\nerror: A causal SNP IDs file named '" + causal_SNP_IDs_path + "' does not exist in your working directory.\n")
    exit()
if not (os.path.isfile(betas_path) or (betas_path == "empty" and phenotype == -9)):
    print("\nerror: A betas file named '" + betas_path + "' does not exist in your working directory.\n")
    exit()
if not (os.path.isfile(major_minor_assignments_path) or (major_minor_assignments_path == "standard")):
    print("\nerror: A major minor assignments file named '" + major_minor_assignments_path + "' does not exist in your working directory.\n")
    exit()
if not (os.path.isfile(SNP_phenotype_map_path) or (SNP_phenotype_map_path == "standard")):
    print("\nerror: A SNP phenotype map file named '" + SNP_phenotype_map_path + "' does not exist in your working directory.\n")
    exit()

# runs the main algorithm. 
for i in range(len(chromosomes)):

    print("simulating chromosome " + str(chromosomes[i]))

    input_sample_column_bounds = [cumulative_SNP_counts[i], cumulative_SNP_counts[i + 1]]
    samples = get_samples_fast(simulation_sample_size,
                               input_sample_column_bounds, 
                               input_plink_filename_prefix, 
                               num_breakpoints)

    breakpoints = draw_breakpoints(rcmb_rate_info_chr[i], 
                                   bim_SNP_pos_chr[i], 
                                   num_breakpoints, 
                                   simulation_sample_size,
                                   test_functionality,
                                   (i + 1),
                                   output_plink_filename_prefix)

    simulated_individuals = breakpoints_to_simulated_individuals(breakpoints, 
                                                                 chr_SNP_counts[i], 
                                                                 samples,
                                                                 test_functionality)

    write_bed_file(simulated_individuals, 
                   bim_SNP_names_chr[i], 
                   output_plink_filename_prefix + "_chr" + str(chromosomes[i]) + ".bed",
                   bim_SNP_complete_pos_chr[i],
                   bim_SNP_nucleotides_chr[i],
                   population_ID)

if phenotype == "binary" or phenotype == "continuous":

    sample_size = len(simulated_individuals)
    output_file_names = [output_plink_filename_prefix + "_chr" + str(chromosomes[i]) + ".bed" for i in range(len(chromosomes))]

    simulated_phenotypes = simulate_phenotypes(output_file_names, causal_SNP_IDs_path, cumulative_SNP_counts,
                                               major_minor_assignments_path, betas_path, mean_phenotype, sample_size,
                                               bim_SNP_names, phenotype, SNP_phenotype_map_path, noise = noise)
    
    if phenotype == "binary":
        legend_label = "phenotype barplot (mean = " + str(np.round(np.mean(simulated_phenotypes), 5))
        legend_label += ", min = " + str(np.round(np.min(simulated_phenotypes), 5)) + ", max = " + str(np.round(np.max(simulated_phenotypes), 5)) + ")"
        plt.bar([0, 1], [np.sum(simulated_phenotypes == 0), np.sum(simulated_phenotypes == 1)], label = legend_label, tick_label = ["0", "1"])
    if phenotype == "continuous":
        legend_label = "phenotype value histogram (mean = " + str(np.round(np.mean(simulated_phenotypes), 5))
        legend_label += ", min = " + str(np.round(np.min(simulated_phenotypes), 5)) + ", max = " + str(np.round(np.max(simulated_phenotypes), 5)) + ")"
        plt.hist(simulated_phenotypes, bins = 30, label = legend_label)
    plt.legend()
    plt.xlabel("phenotype value", fontsize = 12)
    plt.ylabel("number of value instances", fontsize = 12)
    plt.savefig(output_plink_filename_prefix + "_phenotype_profile.png")
    plt.clf()

    for file_name in output_file_names:
        fam_file_name = file_name[:-3] + "fam"
        fam_file = pd.read_csv(fam_file_name, delimiter = " ", header = None)
        fam_file[5] = simulated_phenotypes.reshape(-1,1)
        fam_file[4] = 2
        fam_file.to_csv(fam_file_name, sep = " ", header = False, index = False)


