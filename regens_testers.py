import numpy as np
import pandas as pd
import pdb
from matplotlib import pyplot as plt
pd.options.mode.chained_assignment = None

def test_drawn_breakpoints(breakpoints, probabilities, chromosome_number, output_plink_filename_prefix):

    """
    
    Purpose
    -------
    To show that each breakpoint is, on average, drawn the expected number of times given the "probabilities" 1D array. 
    To confirms that each row in the "breakpoints" 2D array contains 1 or 0 instances of each breakpoint. 

    Parameters
    ----------
    breakpoints: an NxB numpy array, where N is the number of simulated individuals, and B is the number of breakpoints per chromosome in each individual. 
                 each breakpoint is an index in probabilities, which directly corresponds to a specific recombination interval.
    probabilities: a 1D numpy array. The ith element is the probability of drawing a breakpoint at the ith recombination 
                   interval in a single draw, noting that each row in "breakpoints" cannot contain any breakpoint more than once. 
    chromosome_number: the cromosome being analyzed

    Returns
    -------
    It returns nothing. It plots the expected number of times each breakpoint index is drawn against the actual number of times. 
    for each chromosome. It also prints the row numbers of any breakpoint vectors that contain more than one instance of the same breakpoint. 
    
    """
    
    num_breakpoints = len(breakpoints[0])
    num_samples = len(breakpoints)
    breakpoint_indices = list(range(len(probabilities)))
    breakpoint_counts = dict(zip(breakpoint_indices, len(probabilities)*[0]))

    breakpoint_vecs_with_unwanted_replacement = []
    for i, breakpoint_vec in enumerate(breakpoints):
        if len(breakpoint_vec) != len(np.unique(breakpoint_vec)):
            breakpoint_vecs_with_unwanted_replacement.append(i)
        for b in breakpoint_vec:
            breakpoint_counts[b] += 1

    print("The samples in the following list have drawn the same breakpoint more than once:")
    print(breakpoint_vecs_with_unwanted_replacement)
    if len(breakpoint_vecs_with_unwanted_replacement) == 0:
        print("Every sample has successfully drawn breakpoints without replacement")
    if len(breakpoint_vecs_with_unwanted_replacement) > 0:
        print("Some samples have drawn breakpoints with replacement. This is an error, and it should be attended to.")

    expected_num_breakpoint_counts = []
    num_breakpoint_counts = []
    for index in breakpoint_indices:
        p_not_drawing_breakpoint = (1 - probabilities[index])**num_breakpoints
        p_drawing_breakpoint = 1 - p_not_drawing_breakpoint
        expected_num_breakpoint_counts.append(num_samples*p_drawing_breakpoint)
        num_breakpoint_counts.append(breakpoint_counts[index])

    expected_num_breakpoint_counts = np.array(expected_num_breakpoint_counts)
    num_breakpoint_counts = np.array(num_breakpoint_counts)

    plt.plot(expected_num_breakpoint_counts, num_breakpoint_counts, '*', label = "expected vs actual breakpoint index counts")
    plt.plot(expected_num_breakpoint_counts, expected_num_breakpoint_counts, '-', label = "y = x")
    plt.legend(loc = "upper left")
    plt.xlabel("expected number of breakpoints", fontsize = 14)
    plt.ylabel("number of breakpoints", fontsize = 14)
    if "/" in output_plink_filename_prefix:
        prefix = "/".join((output_plink_filename_prefix.split("/"))[:-1]) + "/"
        print(prefix)
    else:
        prefix = ""
    plt.savefig(prefix + "expected_vs_actual_breakpoint_counts_full_range_chr" + str(chromosome_number) + ".png")
    plt.clf()

def test_breakpoint_SNP_mapping(old_breakpoints, rcmb_interval_positions, new_breakpoints, SNP_positions):

    """
    
    Purpose
    -------
    To confirm for every drawn breakpoint that, when each breakpoint's recombination interval is replaced with the genomic position of a SNP,
    that the SNP's genomic position is in-between the genomic positions of the recombination interval's left and right boundaries.     

    Parameters
    ----------
    old_breakpoints: an NxB numpy array, where N is the number of simulated individuals, and B is the number of breakpoints per chromosome in each individual. 
                     each breakpoint is an index in probabilities, which directly corresponds to a specific recombination interval.
    rcmb_interval_positions: a list where ith index contains the genomic position of the left bound of the recombination interbal, which corresponds 
                             to the ith element in "probabilities." Note that the left bound of the ith interval is the right bound of the (i-1)th interval. 
    new_breakpoints: an NxB numpy array, where N is the number of simulated individuals, and B is the number of breakpoints per chromosome in each individual. 
                     each breakpoint is the row number of a SNP in the input bim file, which directly corresponds to a specific genomic location.
    SNP_positions: a list where ith index contains the genomic position of the SNP in the input bim file's ith row. 

    Returns
    -------
    It returns nothing. It prints a list of the (row, column) coordinates of any new breakpoint with a genomic position that
    does not fall in between the genomic positions of the original recombination interval's left and right boundaries.
    
    """

    num_breakpoints = len(old_breakpoints[0])
    erronious_mappings = []
    for i in range(len(old_breakpoints)):
        for k in range(num_breakpoints):
            rcmb_interval_position = rcmb_interval_positions[old_breakpoints[i][k]]
            SNP_position = SNP_positions[new_breakpoints[i][k]]
            next_rcmb_interval = rcmb_interval_positions[old_breakpoints[i][k] + 1]
            if rcmb_interval_position <= SNP_position and SNP_position <= next_rcmb_interval:
                pass
            else:
                erronious_mappings.append((i,k))
    print("The following rcmb interval indices have been incorrectly mapped to SNP indices")
    print(erronious_mappings)
    if len(erronious_mappings) == 0:
        print("Every index has been mapped correctly")
    if len(erronious_mappings) > 0:
        print("Some SNP indices are not contained in the corresponding rcmb interval. This is an error, and it should be attended to.")
                
def test_simulated_individuals(breakpoints, sampled_individuals, simulated_individuals):
    
    """
    
    Purpose
    -------
    To verify that every simulated individual is comprised of the correct segments from the correct real individuals     

    Parameters
    ----------
    breakpoints: an Nx(B+1) numpy array, where N is the number of simulated individuals, and B is the number of breakpoints per chromosome in each individual. 
                 each breakpoint is the row number of a SNP in the input bim file, which directly corresponds to a specific genomic location. Note that the
                 last column in breakpoints has all elements equal to the current chromosomes last SNP index. The other columns are simple breakpoint values. 
    sampled_individuals: an Nx(B+1)xS numpy array, where N is the number of simulated individuals, B is the number of breakpoints per chromosome 
                         (B breakpoints seperate B+1 segments from B+1 real individuals), and S is the number of SNPs per individual in the current chromosome. 
    simulated_individuals: an NxS numpy arrray. Each array of S SNPs contains concatenated segments from B+1 individuals.  

    Returns
    -------
    It returns nothing. It prints a list of the (row, segment index) of any segments within 
    simulated individuals that do not map back to the correct region of the correct real individual    

    """

    incorrect_segment_coordinates = []
    for j, breakpoint_vec in enumerate(breakpoints):
        startpoint = 0
        for k, breakpoint in enumerate(np.sort(breakpoint_vec)):
            if np.any(sampled_individuals[j][k][startpoint:breakpoint] != simulated_individuals[j][startpoint:breakpoint]):
                incorrect_segment_coordinates.append([j, k])
            startpoint = breakpoint
 
    print("\nThe following segments (simulated_individual row number, segment index) are not from the correct regions of the correct real individuals")
    print(incorrect_segment_coordinates)
    if len(incorrect_segment_coordinates) == 0:
        print("Every segment in every simulated individual is from the correct region of the correct real individual")
    else:
        print("\nThis is a technical error that needs to be addressed\n")


             

        
        
        