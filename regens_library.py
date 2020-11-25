import numpy as np
import pandas as pd
import pdb
from time import time
from bed_reader import open_bed
from bed_reader import to_bed
from scipy.optimize import root
from copy import deepcopy as COPY
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from regens_testers import unit_tester

pd.options.mode.chained_assignment = None

# TODO: double check that the modified recombination_rate_to_probabilities function works as expected.
# TODO: double check why you don't subtract 1 from the first "SNP_positions_to_rcmb_intervals" use but you do from the second.
# IMPORTANT DEFINITION: a breakpoint refers to the genomic position of the boundary between segments.
# from two sampled whole genomes. It does not refer to the programming definition of breakpoint.


def reduce_recomb_rate_info(rcmb_rate_info, bim_SNP_positions, test_functionality):

    """

    Purpose
    -------
    To reduce the number of rows in rcmb_rate_info so that every resulting genomic interval contains at least one SNP.

    Parameters
    ----------
    rcmb_rate_info: a pandas dataframe with two columns. "Position(bp)" is the genomic position of the ith interval's left
                    boundary. The ith row is both the left boundry of the ith interval and the right boundary of the (i-1)th
                    interval. "Map(cM)" is the cumulative recombination rate in centiMorgans, which is 0 in the first row.

    bim_SNP_positions: the genomic positions of every SNP directly from the input bim file.

    Returns
    -------
    reduced_rcmb_rate_info: "rcmb_rate_info" with rows removed to ensure that at least one
                            SNP position from "bim_SNP_positions" resides in every interval.

    """

    rcmb_rate_intervals = rcmb_rate_info["Position(bp)"].to_numpy()

    # INDEXING NOTE: Not subtracting one from "SNP_pos_rcmb_interval_map" returns the closest indices of "rcmb_rate_intervals"
    #                boundaries at genomic positions to the RIGHT of each SNP's genomic position in bim_SNP_positions.
    #                The only row still needed is the closest boundary to the LEFT of the first SNP. This is aquired by
    #                implementing "occupied_rcmb_intervals[np.min(np.where(occupied_rcmb_intervals == True)) - 1] = True".

    SNP_pos_rcmb_interval_map = SNP_positions_to_rcmb_intervals(
        rcmb_rate_intervals, COPY(bim_SNP_positions), test_functionality, context=1
    )
    all_rcmb_intervals = np.arange(len(rcmb_rate_intervals))
    occupied_rcmb_intervals = np.isin(all_rcmb_intervals, SNP_pos_rcmb_interval_map)
    occupied_rcmb_intervals[
        np.min(np.where(occupied_rcmb_intervals == True)) - 1
    ] = True
    reduced_rcmb_rate_info = rcmb_rate_info[occupied_rcmb_intervals]

    # reduced_rcmb_rate_info.to_csv("correct_reduce_recomb_rate_info_output.txt", sep = "\t", header = True, index = False)
    if test_functionality == "test_units":
        unit_tester(
            reduced_rcmb_rate_info, "correct_reduce_recomb_rate_info_output.txt", 0
        )
    return reduced_rcmb_rate_info


def SNP_positions_to_rcmb_intervals(
    rcmb_interval_boundaries, bim_SNP_positions, test_functionality, context
):

    """

    Purpose
    -------
    To produce a list with indices that correspond to "bim_SNP_positions" indices
    and values that correspond to "rcmb_rate_intervals" indices. This is an intermediate
    step in converting sampled breakpoint intervals to SNPs from the input dataset.

    Parameters
    ----------
    rcmb_interval_boundaries: The "Position(bp)" column from "rcmb_rate_info". The ith element is the genomic position of
                              both the left boundry of the ith interval and the right boundary of the (i-1)th interval.

    bim_SNP_positions: the genomic positions of every SNP directly from the input bim file.

    Returns
    -------
    SNP_rcmb_interval_indices: a list with indices that correspond to "rcmb_rate_intervals"
    indices and values that correspond to "bim_SNP_positions" indices

    """

    prev_start_pos = 0
    SNP_rcmb_interval_indices = np.zeros(len(bim_SNP_positions), dtype=np.int64)
    too_large_indices = bim_SNP_positions >= np.max(rcmb_interval_boundaries)
    too_small_indices = bim_SNP_positions <= np.min(rcmb_interval_boundaries)
    bim_SNP_positions[too_large_indices] = np.max(rcmb_interval_boundaries) - 1
    bim_SNP_positions[too_small_indices] = np.min(rcmb_interval_boundaries) + 1
    num_outer_SNPs = np.sum(too_large_indices) + np.sum(too_small_indices)
    if num_outer_SNPs > 0:
        print(
            "\nCAUTION: "
            + str(num_outer_SNPs)
            + " SNP(s) in the bim file are outside of the positional range considered by the recombination rate info file.\n"
        )
        print(
            "This is unlikely to be an issue if the number of such SNPs is small. Otherwise, remove those SNPs from the input plink files\n"
        )
        print(
            "bim file SNPs earlier than the first recombination interval are assumed to be inside of the first recombination interval.\n"
        )
        print(
            "bim file SNPs farther than the last recombination interval are assumed to be inside of the last recombination interval.\n"
        )
    for i in range(len(bim_SNP_positions)):
        for k in range(len(rcmb_interval_boundaries) - prev_start_pos):
            if rcmb_interval_boundaries[prev_start_pos + k] >= bim_SNP_positions[i]:
                SNP_rcmb_interval_indices[i] = prev_start_pos + k
                prev_start_pos += k
                break

    if test_functionality == "test_units":
        unit_tester(
            SNP_rcmb_interval_indices,
            "correct_SNP_positions_to_rcmb_intervals_output" + str(context) + ".txt",
            None,
        )

    return SNP_rcmb_interval_indices


def choice_with_periodic_replacement(length, width, probabilities, test_functionality):

    """

    Purpose
    -------
    This function's operations are equivalent to the following procedure:
        1) Sample B indices from a probability vector without replacement.
        2) Replace the sampled indices.
        3) Repeat Steps 1 and 2 N times.
    Here, B is the number of breakpoints per chromosome, and N is the number of individuals to be simulated.

    Parameters
    ----------
    length: The (int) number of individuals to be simulated (N)
    width: the (int) number of breakpoints per chromosome (B)
    probabilities: A numpy array, where the ith element is the probability of sampling the ith
                   recombination interval from "reduced_rcmb_rate_info" to contain a breakpoint

    Returns
    -------
    an NxB numpy array containing N sets of B recombination interval indices. All indices
    have 1 subtracted from them because a [0] element is appended onto the beginning of
    the cumulative probability distribution for technical convenience, which increases
    all of the indices by one higher than rest of the code expects them to be.

    """

    samples = np.zeros((width, length)).astype(int)
    cumulative_probabilities = np.repeat(
        [np.cumsum(np.append([0], probabilities))], length, axis=0
    )
    max_cumulative_vals = cumulative_probabilities[:, -1]
    for i in range(width):
        adjusted_uniform_sample = max_cumulative_vals * np.random.rand(length)
        samples[i] = np.array(
            [
                np.searchsorted(probs, sample)
                for probs, sample in zip(
                    cumulative_probabilities, adjusted_uniform_sample
                )
            ]
        )
        if i < (width - 1):
            for j, pos in enumerate(samples[i]):
                cumulative_probabilities[j][pos:] -= (
                    cumulative_probabilities[j][pos]
                    - cumulative_probabilities[j][pos - 1]
                )
            max_cumulative_vals = cumulative_probabilities[:, -1]

    if test_functionality == "test_units":
        unit_tester(
            samples.T - 1, "correct_choice_with_periodic_replacement_output.txt", None
        )

    return samples.T - 1


def centimorgans_to_probabilities(recomb_rate_info, test_functionality):

    """

    Purpose
    -------
    Convert recombination rates (in cM) to the probability that a recombination event exists at the
    corresponding interval given that one recombination event exists in the chromosome. This is used
    as the probability of drawing that interval's genomic position to be the site of a breakpoint.

    Parameters
    ----------
    recomb_rate_info: Output from the "reduce_recomb_rate_info" function.

    Returns
    -------
    a numpy array of probabilities that sum to 1. The ith probability is the probability
    of drawing the ith recombination interval to use as the location of a breakpoint.

    """

    new_cumulative_cM = recomb_rate_info["Map(cM)"].to_numpy()
    rcmb_rates = new_cumulative_cM[1:] - new_cumulative_cM[0:-1]
    expected_Ri = (1 - np.exp(-rcmb_rates / 50)) / 2
    expected_R = np.sum(expected_Ri)
    p_Ri_true_given_R_one = expected_Ri / expected_R

    if test_functionality == "test_units":
        unit_tester(
            p_Ri_true_given_R_one,
            "correct_centimorgans_to_probabilities_output.txt",
            None,
        )

    return p_Ri_true_given_R_one


def draw_breakpoints(
    rcmb_rate_info,
    bim_SNP_positions,
    num_breakpoints,
    simulation_sample_size,
    test_functionality,
    chromosome_number,
    output_plink_filename_prefix,
):

    """

    Purpose
    -------
    Computes breakpoint sampling probabilities with "centimorgans_to_probabilities", Draws breakpoints
    with "choice_with_periodic_replacement", and converts the breakpoints' corresponding recombination
    interval indices into the indices of input SNPs that reside inside of the recombination interval.

    Parameters
    ----------
    rcmb_rate_info:  Output from the "reduce_recomb_rate_info" function.
    bim_SNP_positions: the genomic positions of every SNP directly from the input bim file.
    num_breakpoints: user-specified (int) number of breakpoints per chromosome.
    simulation_sample_size: user-specified number of samples to be simulated.
    test_functionality: an argument which, if equal to "yes", tests regens' functionality. It substantially increases runtime.
    chromosome_number: the chromosome that is currently being simulated.
    output_plink_filename_prefix: plink prefix of the (bed, bim, fam) fileset that will contain simulated individuals.

    Returns
    -------
    an NxB numpy array containing N sets of B recombination interval indices.
    Each index is an input SNP's bim row index (also it's bed column index).

    """

    if test_functionality == "test_correctness":
        from regens_testers import test_drawn_breakpoints
        from regens_testers import test_breakpoint_SNP_mapping

    SNP_count = len(bim_SNP_positions)
    probabilities = centimorgans_to_probabilities(rcmb_rate_info, test_functionality)
    rcmb_rate_intervals = rcmb_rate_info["Position(bp)"].to_numpy()
    breakpoints = choice_with_periodic_replacement(
        simulation_sample_size, num_breakpoints, probabilities, test_functionality
    )

    if test_functionality == "test_correctness":
        test_drawn_breakpoints(
            breakpoints, probabilities, chromosome_number, output_plink_filename_prefix
        )
        old_breakpoints = COPY(breakpoints)

    # INDEXING NOTE: Subtracting one from "SNP_pos_rcmb_interval_map" returns the closest indices of "rcmb_rate_intervals"
    #                boundaries at genomic positions to the LEFT of each SNP's genomic position in bim_SNP_positions.
    #                This is because all SNPs up to the SNP immediately to the left of the ith breakpoint comprise the ith
    #                segment, noting that the (B+1)th includes all SNPs after the Bth breakpoint (there are B breakpoints).

    SNP_pos_rcmb_interval_map = (
        SNP_positions_to_rcmb_intervals(
            rcmb_rate_intervals, COPY(bim_SNP_positions), test_functionality, context=2
        )
        - 1
    )

    rcmb_interval_SNP_pos_map = {}
    for rcmb_interval in np.unique(SNP_pos_rcmb_interval_map):
        rcmb_interval_SNP_pos_map[rcmb_interval] = np.where(
            SNP_pos_rcmb_interval_map == rcmb_interval
        )[0]

    for jj in range(len(breakpoints)):
        for k in range(num_breakpoints):
            interval_index = breakpoints[jj][k]
            SNP_indices = rcmb_interval_SNP_pos_map[interval_index]
            if len(SNP_indices) == 1:
                breakpoints[jj][k] = SNP_indices[0]
            else:
                breakpoints[jj][k] = SNP_indices[
                    int(len(SNP_indices) * np.random.rand() - 0.5)
                ]

    if test_functionality == "test_correctness":
        test_breakpoint_SNP_mapping(
            old_breakpoints, rcmb_rate_intervals, breakpoints, bim_SNP_positions
        )
    if test_functionality == "test_units":
        unit_tester(breakpoints, "correct_draw_breakpoints_output.txt", None)

    return breakpoints


def get_samples_fast(
    simulation_sample_size,
    bed_col_bounds,
    plink_file_name_prefix,
    num_breakpoints,
    test_functionality,
):

    """

    Purpose
    -------
    Imports real whole genomes from the input bed file in proportions as close as possible to that of the bed file's population and
    randomly assigns every breakpoint seperated segment to be copied from one of the imported whole genomes without replacement.

    Parameters
    ----------
    simulation_sample_size: the (int) number of samples to be simulated (N)
    bed_col_bounds: first and last column indices of all SNP indices that comprise the chromosome being simulated
    num_breakpoints: user-specified (int) number of breakpoints per chromosome (B).
    plink_file_name_prefix: plink prefix of the (bed, bim, fam) fileset that contains real whole genomes.

    Returns
    -------
    an Nx(B+1)xS numpy array containing N sets of B whole chromosomes, each of which have S snps.
    Each row in the ith (B+1)xS subset will contribute one genomic segment. Those (B+1) genomic
    segments will be concatenated to comprise the ith simulated individual.

    """

    bed_file_path = plink_file_name_prefix + ".bed"
    bed_reader = open_bed(bed_file_path, count_A1=True, num_threads=1)
    num_repeats = int(
        simulation_sample_size * (num_breakpoints + 1) / int(bed_reader.iid_count) + 1
    )
    bed_row_indices = np.repeat(range(bed_reader.iid_count), num_repeats)
    np.random.shuffle(bed_row_indices)
    bed_row_indices = bed_row_indices[: simulation_sample_size * (num_breakpoints + 1)]
    bed_file_samples = bed_reader.read(
        (bed_row_indices, slice(bed_col_bounds[0], bed_col_bounds[1])), dtype="int8"
    )
    bed_file_samples_dimensions = (
        int(len(bed_row_indices) / (num_breakpoints + 1)),
        num_breakpoints + 1,
        len(bed_file_samples[0]),
    )
    reshaped_output = bed_file_samples.reshape(bed_file_samples_dimensions)

    if test_functionality == "test_units":
        # gives 3 different counts of how many times each minor allele is drawn. They're small and vanishingly unlikely to all be made correctly by chance.
        SNP_minor_allele_counts = np.sum(reshaped_output, axis=(0, 1))
        simulated_individual_minor_allele_counts = np.sum(reshaped_output, axis=(1, 2))
        breakpoint_interval_minor_allele_counts = np.sum(reshaped_output, axis=(0, 2))
        unit_tester(
            SNP_minor_allele_counts,
            "correct_get_samples_fast_SNP_minor_allele_counts_output.txt",
            None,
        )
        unit_tester(
            simulated_individual_minor_allele_counts,
            "correct_get_samples_fast_simulated_individual_minor_allele_counts_output.txt",
            None,
        )
        unit_tester(
            breakpoint_interval_minor_allele_counts,
            "correct_get_samples_fast_breakpoint_interval_minor_allele_counts_output.txt",
            None,
        )

    return reshaped_output


def breakpoints_to_simulated_individuals(
    breakpoints, SNP_count, sampled_individuals, test_functionality
):

    """

    Purpose
    -------
    Imports real whole genomes from the input bed file in proportions as close as possible to that of the bed file's population and
    randomly assigns every breakpoint seperated segment to be copied from one of the imported whole genomes without replacement.

    Parameters
    ----------
    sampled_individuals: an Nx(B+1)xS numpy array containing N sets of B whole chromosomes, each of which have S snps.
                         Each row in the ith (B+1)xS subset will contribute one genomic segment. Those (B+1) genomic
                         segments will be concatenated to comprise the ith simulated individual.
    breakpoints: an Nx(B+1) numpy array, where N is the number of simulated individuals, and B is the number of breakpoints
                 per chromosome in each individual. Each breakpoint is the row number of a SNP in the input bim file,
                 which directly corresponds to a specific genomic location.
    SNP_count: The number of input SNPs in the chromosome currently being simulated

    Returns
    -------
    an NxS numpy array containing N simulated chromosomes, each of which has segments from B+1 individuals and S total SNPs.
    """

    breakpoints = np.append(
        breakpoints, SNP_count * np.ones((len(breakpoints), 1), dtype=np.int64), axis=1
    )
    breakpoints_masks = np.zeros(
        (len(breakpoints), len(breakpoints[0]), SNP_count), dtype=bool
    )
    for j, breakpoint_vec in enumerate(breakpoints):
        startpoint = 0
        for k, breakpoint in enumerate(np.sort(breakpoint_vec)):
            breakpoints_masks[j][k][startpoint:breakpoint] = True
            startpoint = breakpoint
    simulated_individuals = sampled_individuals[breakpoints_masks].reshape(
        -1, SNP_count
    )

    if test_functionality == "test_correctness":
        from regens_testers import test_simulated_individuals

        test_simulated_individuals(
            breakpoints, sampled_individuals, simulated_individuals
        )

    return simulated_individuals


def write_bed_file(
    simulated_individuals,
    bim_SNP_names,
    output_name,
    bim_SNP_complete_pos,
    bim_SNP_nucleotides,
    population_ID,
    test_functionality,
):

    """

    Purpose
    -------
    to write the simulated data into realistic (bed, bim, fam) filesets. Does not include phenotypes at this point.

    Parameters
    ----------
    sampled_individuals: an Nx(B+1)xS numpy array containing N sets of B whole chromosomes, each of which have S snps.
                         Each row in the ith (B+1)xS subset will contribute one genomic segment. Those (B+1) genomic
                         segments will be concatenated to comprise the ith simulated individual.
    bim_SNP_names: a list of SNP's rsIDs from the input bed file.
    output_name: name of the output bed file, which annotates the chromosome that it belongs to.
    bim_SNP_complete_pos: Sx3 numpy array. Columns comprise the first, third, and fourth columns from the input bim file.
    bim_SNP_nucleotides: Sx2 numpy array. Columns comprise the fifth and sixth columns from the input bim file (i.e. major and minor alleles).
                         CAUTION: minor alleles with frequencies near 50% may become the major allele after the simulation
                         because the simulated allele frequency always deviates from the real allele frequency by a small ammout.
                         This makes plink flip the sign of r values for simulated SNP pairs relative to real SNP pairs
                         if plink's --keep-allele-order flag is not used when computing the r values with plink.
    population_ID: An input argument that is concatenated to each sample's row index to comprise columns 1 and 2 for the output fam file.
                   If no input argument is selected, then it includes the popilation ID from the 1000 genomes input plink fileset. If
                   the input plink files are custom, then it includes an empty string as the population_ID.

    Returns
    -------
    It returns nothing. It only writes the simulated data into plink files.

    """

    simulated_IDs = np.array(
        [population_ID + "_" + str(i) for i in range(1, len(simulated_individuals) + 1)]
    )
    metadata = {
        "fid": simulated_IDs,
        "iid": simulated_IDs,
        "sex": np.array([2] * len(simulated_IDs)),
        "pheno": np.array([-9] * len(simulated_IDs)),
        "chromosome": bim_SNP_complete_pos.T[0],
        "sid": bim_SNP_names,
        "cm_position": bim_SNP_complete_pos.T[1],
        "bp_position": bim_SNP_complete_pos.T[2],
        "allele_1": bim_SNP_nucleotides.T[0],
        "allele_2": bim_SNP_nucleotides.T[1],
    }

    to_bed(output_name, simulated_individuals, properties=metadata, count_A1=True)

    if test_functionality == "test_units":
        bed_reader = open_bed(output_name, count_A1=True, num_threads=1)
        output_bed_file = bed_reader.read(dtype="int8")
        output_bim_file = (
            pd.read_csv(
                output_name[:-4] + ".bim", delimiter="\t", header=None, dtype=str
            )
            .to_numpy()
            .astype("str")
        )
        output_fam_file = (
            pd.read_csv(
                output_name[:-4] + ".fam", delimiter=" ", header=None, dtype=str
            )
            .to_numpy()
            .astype("str")
        )
        unit_tester(output_bed_file, "correct_write_bed_file_output.bed", None)
        unit_tester(output_bim_file, "correct_write_bed_file_output.bim", None)
        unit_tester(output_fam_file, "correct_write_bed_file_output.fam", None)


def get_feature_SNPs(
    feature_SNP_IDs,
    cumulative_SNP_counts,
    output_file_names,
    sample_size,
    bim_SNP_names,
):

    """

    Purpose
    -------
    Each row in the causal_SNP_IDs contains one or more SNPs that transform to compute a single genetic feature.
    The purpose of this function is to return all of those SNPs' genotypes for one row in the causal_SNP_IDs file.

    Parameters
    ----------
    feature_SNP_IDs: A list of rsIDs from the input plink file (same as the output bim file) that comprise a single feature.
    cumulative_SNP_counts: the cumulative number of SNPs summed from chromosome 1 to chromosome 22 in ascending order.
    output_file_names: the names of the output bed files for all chromosomes.
    sample_size: the number of samples that have been simulated.
    bim_SNP_names: a list of SNPs from the output bim file (same as the input bim file).

    Returns
    -------
    It returns a 2D numpy array where each column is the column contains the causal genotypes for one SNP.
    """

    feature_SNPs = np.zeros((sample_size, len(feature_SNP_IDs)))
    for i, SNP_ID in enumerate(feature_SNP_IDs):
        index = np.where(SNP_ID == bim_SNP_names)[0][0]
        output_file_index = np.min(np.where(index <= cumulative_SNP_counts)) - 1
        output_file_reader = open_bed(
            output_file_names[output_file_index], count_A1=True, num_threads=1
        )
        adjusted_SNP_index = index - cumulative_SNP_counts[output_file_index]
        feature_SNPs[:, [i]] += output_file_reader.read(
            index=adjusted_SNP_index, dtype="float32"
        )

    return feature_SNPs


def simulate_phenotypes(
    output_file_names,
    causal_SNP_IDs_path,
    cumulative_SNP_counts,
    major_minor_assignments_path,
    betas_path,
    mean_phenotype,
    sample_size,
    bim_SNP_names,
    phenotype,
    SNP_phenotype_map_path,
    noise=0,
):

    """

    Purpose
    -------
    to simulate correlations between the genotypes of selected SNPs and a continuous or binary phenotype.

    Parameters
    ----------
    output_file_names: the names of the output bed files for all chromosomes.
    causal_SNP_IDs_path: the path to the file containing causal rsIDs from which phenotype values are simulated.
    cumulative_SNP_counts: the cumulative number of SNPs summed from chromosome 1 to chromosome 22 in ascending order.
    major_minor_assignments_path: the path to the file specifying whether the major
                                  or minor allele in each causal SNP adds 1 to the genotype.
    betas_path: the path to the file containing one beta coefficient per row.
    sample_size: the number of samples that have been simulated.
    bim_SNP_names: a list of SNPs from the output bim file (same as the input bim file).
    phenotype: an input argument specifying whether to simulate a continuous or binary phenotype.
    output_name: name of the output bed file, which annotates the chromosome that it belongs to.
    mean_phenotype: an input argument (float). It can be any number for continuous phenotypes,
                    and it must be in between 0 and 1 for binary phenotypes.
    SNP_phenotype_map_path: the path to the file specifying whether each causal SNP's phenotype map
                            is additive, dominant, recessive, heterozygous_only, or homozygous_only.
    noise: a percentage of the mean phenotype that is the standard deviation of the
           random gaussian noise that contributes to the simulated phenotype's values.

    Returns
    -------
    It returns a numpy array of one simulated phenotype per simulated whole genome. It only writes
    the simulated data into plink files. It also writes the values of the inferred beta coefficients
    and overall R^2 between the causal genotypes and the phenotype into a text file.

    """

    # imports required model components (SNPs and beta values).
    github_link = "https://github.com/EpistasisLab/regens"
    causal_SNP_IDs = open(causal_SNP_IDs_path, "r").readlines()
    try:
        betas = np.array(open(betas_path, "r").readlines()).astype(np.float64)
    except:
        print(
            "\nerror: The beta coefficients file at "
            + betas_path
            + " is incorrectly formatted. Visit "
            + github_link
            + " for examples of correct formatting.\n"
        )
        exit()
    if len(betas) != len(causal_SNP_IDs):
        print(
            "\nerror: The causal_SNP_IDs and betas files must have the same number of rows. Visit "
            + github_link
            + " for examples of correct formatting.\n"
        )
        exit()

    # imports optional model components (major/minor assignments and SNP_phenotype_maps).
    if major_minor_assignments_path != "standard":
        major_minor_assignments = open(major_minor_assignments_path, "r").readlines()
        if len(major_minor_assignments) != len(causal_SNP_IDs):
            print(
                "\nerror: The causal_SNP_IDs and major_minor_assignments files must have the same number of rows. Visit "
                + github_link
                + " for examples of correct formatting.\n"
            )
            exit()
    if SNP_phenotype_map_path != "standard":
        SNP_phenotype_map = open(SNP_phenotype_map_path, "r").readlines()
        if len(SNP_phenotype_map) != len(causal_SNP_IDs):
            print(
                "\nerror: The causal_SNP_IDs and SNP_phenotype_map files must have the same number of rows. Visit "
                + github_link
                + " for examples of correct formatting.\n"
            )
            exit()

    # simulates phenotypes based on model specifications
    feature_size = len(betas)
    features = np.zeros((sample_size, feature_size))
    for p in range(feature_size):
        feature_SNP_IDs = causal_SNP_IDs[p].strip().split("\t")
        try:
            feature_SNPs = get_feature_SNPs(
                feature_SNP_IDs,
                cumulative_SNP_counts,
                output_file_names,
                sample_size,
                bim_SNP_names,
            )
        except:
            print(
                "\nerror: The causal SNP IDs on row "
                + str(p + 1)
                + " are either incorrectly formatted or they do not exist in the input bim file:\n"
            )
            print("Visit " + github_link + " for examples of correct formatting.\n")
        if major_minor_assignments_path != "standard":
            if np.all(
                np.isin(major_minor_assignments[p].strip().split("\t"), ["0", "1"])
            ):
                feature_major_minor_assignments = np.array(
                    major_minor_assignments[p].strip().split("\t")
                ).astype(np.int64)
                feature_major_minor_assignments_alt = COPY(
                    feature_major_minor_assignments
                )
                feature_major_minor_assignments_alt[
                    feature_major_minor_assignments_alt == 0
                ] = -1
                feature_SNPs_with_assignments = (
                    feature_SNPs - 2 * feature_major_minor_assignments
                ) * (-1 * feature_major_minor_assignments_alt)
            else:
                print(
                    "\nerror: The major minor assignments on row "
                    + str(p + 1)
                    + " are either incorrectly formatted or they do not exist in the input bim file:\n"
                )
                print("Visit " + github_link + " for examples of correct formatting.\n")
        if major_minor_assignments_path == "standard":
            feature_SNPs_with_assignments = feature_SNPs

        if SNP_phenotype_map_path != "standard":
            feature_SNP_phenotype_map = SNP_phenotype_map[p].strip().split("\t")
            if feature_SNPs_with_assignments.shape[1] > 1:
                for m in range(len(feature_SNP_phenotype_map)):
                    if feature_SNP_phenotype_map[m] == "recessive":
                        feature_SNPs_with_assignments[:, m][
                            feature_SNPs_with_assignments[:, m] == 1
                        ] = 0
                    elif feature_SNP_phenotype_map[m] == "dominant":
                        feature_SNPs_with_assignments[:, m][
                            feature_SNPs_with_assignments[:, m] == 1
                        ] = 2
                    elif feature_SNP_phenotype_map[m] == "heterozygous_only":
                        feature_SNPs_with_assignments[:, m][
                            feature_SNPs_with_assignments[:, m] == 2
                        ] = 0
                        feature_SNPs_with_assignments[:, m][
                            feature_SNPs_with_assignments[:, m] == 1
                        ] = 2
                    elif feature_SNP_phenotype_map[m] == "homozygous_only":
                        feature_SNPs_with_assignments[:, m][
                            feature_SNPs_with_assignments[:, m] == 0
                        ] = 2
                        feature_SNPs_with_assignments[:, m][
                            feature_SNPs_with_assignments[:, m] == 1
                        ] = 0
                    elif feature_SNP_phenotype_map[m] == "regular":
                        pass
                    else:
                        print(
                            "\nerror: all SNP_phenotype labels must be 'regular', 'recessive', 'dominant', 'heterozygous_only', or 'homozygous_only'.\n"
                        )
                        print(
                            "Visit "
                            + github_link
                            + " for examples of correct formatting.\n"
                        )
                        exit()
            if feature_SNPs_with_assignments.shape[1] == 1:
                for m in range(len(feature_SNP_phenotype_map)):
                    if feature_SNP_phenotype_map[m] == "recessive":
                        feature_SNPs_with_assignments[
                            feature_SNPs_with_assignments == 1
                        ] = 0
                    elif feature_SNP_phenotype_map[m] == "dominant":
                        feature_SNPs_with_assignments[
                            feature_SNPs_with_assignments == 1
                        ] = 2
                    elif feature_SNP_phenotype_map[m] == "heterozygous_only":
                        feature_SNPs_with_assignments[
                            feature_SNPs_with_assignments == 2
                        ] = 0
                        feature_SNPs_with_assignments[
                            feature_SNPs_with_assignments == 1
                        ] = 2
                    elif feature_SNP_phenotype_map[m] == "homozygous_only":
                        feature_SNPs_with_assignments[
                            feature_SNPs_with_assignments == 0
                        ] = 2
                        feature_SNPs_with_assignments[
                            feature_SNPs_with_assignments == 1
                        ] = 0
                    elif feature_SNP_phenotype_map[m] == "regular":
                        pass
                    else:
                        print(
                            "\nerror: all SNP_phenotype labels must be 'regular', 'recessive', 'dominant', 'heterozygous_only', or 'homozygous_only'.\n"
                        )
                        print(
                            "Visit "
                            + github_link
                            + " for examples of correct formatting.\n"
                        )
                        exit()

        features[:, p] = np.product(feature_SNPs_with_assignments, axis=1)
    weighted_feature_sums = np.sum(betas * features, axis=1, keepdims=True)
    weighted_feature_sums += np.random.normal(
        loc=0,
        scale=noise * np.mean(weighted_feature_sums),
        size=weighted_feature_sums.shape,
    )

    if phenotype == "binary":

        def logistic_with_unknown_intercept(
            intercept, weighted_feature_sums, mean_phenotype
        ):
            disease_probabilities = 1 / (
                1 + np.exp(-1 * (weighted_feature_sums + intercept))
            )
            return np.mean(disease_probabilities) - mean_phenotype

        intercept = root(
            fun=logistic_with_unknown_intercept,
            x0=np.array([0]),
            args=(weighted_feature_sums, mean_phenotype),
        ).x[0]
        disease_probabilities = 1 / (
            1 + np.exp(-1 * (weighted_feature_sums + intercept))
        )
        simulated_phenotypes = (
            np.random.rand(len(disease_probabilities))
            <= disease_probabilities.reshape(-1)
        ).astype(np.int8)
        model = LogisticRegression(
            C=1e100, tol=1e-100, max_iter=1000000, solver="lbfgs"
        ).fit(features, simulated_phenotypes)

    elif phenotype == "continuous":

        def linear_with_unknown_intercept(
            intercept, weighted_feature_sums, mean_phenotype
        ):
            return np.mean(weighted_feature_sums + intercept) - mean_phenotype

        intercept = root(
            fun=linear_with_unknown_intercept,
            x0=np.array([0]),
            args=(weighted_feature_sums, mean_phenotype),
        ).x[0]
        simulated_phenotypes = weighted_feature_sums + intercept
        model = LinearRegression().fit(features, simulated_phenotypes)

    else:
        print("error: phenotype must be either 'binary' or 'continuous'.")
        exit()

    model_profile = open(output_file_names[0][:-8] + "model_profile.txt", "w")
    model_profile.write(
        "measured R^2 of model fit: "
        + str(model.score(features, simulated_phenotypes))
        + "\n"
    )
    for i, b in enumerate(model.coef_[0]):
        model_profile.write(
            "measured beta value of feature" + str(i + 1) + ": " + str(b) + "\n"
        )
    model_profile.write("measured beta value of intercept: " + str(model.intercept_[0]))
    model_profile.close()
    return simulated_phenotypes
