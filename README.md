## About REGENS

REGENS (REcombinatory Genome ENumeration of Subpopulations) is an open source Python package that simulates whole genomes from real genomic segments. 
REGENS recombining these segments in a way that preserves their linkage disequilibrium (LD) such that the simulated genomes closely resemble the realistic input population \cite{source:1}
Given a biological trait (phenotype), REGENS can also simulate mono-allelic and epistatic single nucleotide variant (SNV) effects of any order without perturbing the simulated LD pattern.

## Input
REGENS requires the following inputs:
- real genotype data formatted as a standard (bed, bim, fam) plink _fileset_, ideally contains a minimum of 80 unrelated individuals
- a folder with one dataframe per chromosome containing genomic position intervals and recombination rates [formatted as such](https://raw.githubusercontent.com/EpistasisLab/REGENS/master/hg19/ACB/ACB_recombination_map_hapmap_format_hg19_chr_1.txt?token=AKJ677MJLXQBVU243VENRWS7NY4XC)

### IMPORTANT NOTICE (PLEASE READ)

**REGENS's simulated genomes are comprised entirely of concatenated segments from the input dataset's real genomes. If your input genomes are not available for public use, then you may not be allowed to publicly release the simulated dataset. Please consult the institutions that provide you access to your input genotype dataset for more information about this matter.**

## Output
Standard output is a standard (bed, bim, fam) plink fileset with the simulated genotype data (and optional phenotype information). 
If plink is not available to you, please consider [bed-reader](https://pypi.org/project/bed-reader/0.1.1/), which reads (bed, bim, fam) plink filesets into the python environment quickly and efficiently. 
 
We provide the second input for all twenty-six 1000 genomes populations created by the [pyrho algorithm](https://github.com/popgenmethods/pyrho).

In phenotype simulation, REGENS also outputs a distribution of phenotypes (see [example](https://github.com/EpistasisLab/REGENS/blob/master/images/example1_all_1000_genomes_ACB_simulated_phenotype_profile.png)) and a file containing the R<sup>2</sup> value of the phenotype/genotype correlation and the *inferred* beta coefficients (see [example](https://github.com/EpistasisLab/REGENS/blob/master/images/example1_all_1000_genomes_ACB_simulated_phenotype_profile.png)), which will most likely be close to but not equal to the input beta coefficients.

## Installing REGENS 

REGENS and its dependencies can be installed with pip as follows: 
```bash
pip install bed-reader
pip install numpy
pip install pandas
pip install matplotlib
pip install scipy
pip install scikit-learn
```
After the installation, please clone this repository to download the neccessary data files to REGENS to run.
On your command line, change working directory to the `regens` directory. 

## Simulate genotype data

The following command uses `ACB.bed`, `ACB.bim`, and `ACB.fam` to simulate 10000 individuals.

```bash
python REGENS.py --in ACB \
    --out CB_simulated \
    --simulate_nsamples 10000 \
    --simulate_nbreakpoints 4 \
    --population_code ACB \
    --human_genome_version hg19
```

## Simulate genotype data with phenotype associations

Given at least one set of one or more SNPs, REGENS can simulate a correlation between each set of SNPs and a binary or continuous phenotype.
Different genotype encoding can be applied:

- Normally, if A is the major allele and a is the minor allele, then (AA = 0, Aa = 1, and aa = 2). However, you can _swap_ the genotype values so that (AA = 2, Aa = 1, and aa = 0).
- You can further transform the values so that they reflect no effect (I), a dominance effect (D), a recessive effect (R), a heterozygous only effect (He), or a homozygous only effect (Ho).

The table below shows how each combination of one step 1 function (columns) and one step 2 function (rows) transforms the original (AA = 0, Aa = 1, and aa = 2) values.

| Input = {0, 1, 2} | Identity  | Swap      |
|-------------------|-----------|-----------|
| Identity          | {0, 1, 2} | {2, 1, 0} |
| Dominance         | {0, 2, 2} | {2, 2, 0} |
| Recessive         | {0, 0, 2} | {2, 0, 0} |
| Heterozygous only | {0, 2, 0} | {0, 2, 0} |
| Homozygous only   | {2, 0, 2} | {2, 0, 2} |

### Example 1: a simple additive model

A full command for REGENS to simulate genomic data with correlated phenotypes would be formatted as follows:

```bash
python REGENS.py --in ACB --out ACB_simulated \
    --simulate_nsamples 10000 --simulate_nbreakpoints 4 \
    --phenotype continuous --mean_phenotype 5.75 \
    --population_code ACB --human_genome_version hg19 \
    --noise 0.5 --causal_SNP_IDs_path causal_SNP_IDs.txt \
    --betas_path betas.txt
```

This command simulates genotype-phenotype correlations according to the following model.
If we let _y_ be an individual's phenotype, s<sub>i</sub> be the i<sup>th</sup> to influence the value of _y_ such that (AA = 0, Aa = 1, and aa = 2), and _B_ be the bias term. The goal is to simulate the following relationship between genotype and phenotype:

y = 0.2s<sub>1</sub> + 0.2s<sub>2</sub> + 0.5s<sub>3</sub> + B + &epsilon;

where &epsilon; ~ N(&mu; = 0, &sigma;<sub>&epsilon;</sub> = 0.5E[y] and E[y] = 5.75.

<!-- h<sub>&theta;</sub>(x) = &theta;<sub>o</sub> x + &theta;<sub>1</sub>x -->
<!-- <img src="https://render.githubusercontent.com/render/math?math=y = 0.2s_1 %2B 0.2s_2 %2B 0.2s_3 %2B B %2B \epsilon"> -->
<!-- <img src="https://render.githubusercontent.com/render/math?math=\epsilon ~ N(\mu = 0, \sigma_{\epsilon} = 0.5E[y])"> -->
<!-- <img src="https://render.githubusercontent.com/render/math?math=E[y] = 5.75"> -->

The following files, formatted as displayed below, must exist in your working directory.
`causal_SNP_IDs.txt` contains specified SNP IDs from the input bim file `ACB.bim` separated by newline characters:
```
rs113633859
rs6757623
rs5836360
```
`betas.txt` contains one (real numbered) beta coefficient for each row in `causal_SNP_IDs.txt`:
```
0.2
0.2
0.5
```

### Example 2: inclusion of nonlinear single-SNP effects

```bash
python REGENS.py --in ACB --out ACB_simulated 
    --simulate_nbreakpoints 4 --simulate_nsamples 10000 \
    --phenotype continuous --mean_phenotype 5.75 \
    --population_code ACB --human_genome_version hg19 \
    --noise 0.5 --causal_SNP_IDs_path causal_SNP_IDs.txt \
    --major_minor_assign_path major_minor_assign.txt \
    --SNP_phenotype_map_path SNP_phenotype_map.txt \
    --betas_path betas.txt
```

* --major_minor_assign_path: the name of the file formatted as `major_minor_assign.txt` or the full path if its not in the working directory
* --SNP_phenotype_map_path: the name of the file formatted as `SNP_phenotype_map.txt` or the full path if its not in the working directory

In addition to the notation from the first example, let S<sub>i</sub> = _swap_(s<sub>i</sub>) be the i<sup>th</sup> genotype to influence the value of _y_ such that (AA = 2, Aa = 1, and aa = 0).
Also, we recall the definitions for the four nontrivial mapping functions (R, D, He, Ho) defined prior to the first example. The second example models phenotypes as follows:

y = 0.2R(s<sub>2</sub>)+ 0.2D(s<sub>3</sub>) + 0.5S<sub>6</sub> + B + &epsilon;

where &epsilon; ~ N(&mu; = 0, &sigma;<sub>&epsilon;</sub> = 0.5E[y] and E[y] = 5.75.

<!-- <img src="https://render.githubusercontent.com/render/math?math=y = 0.2R(s_2) %2B 0.2D(s_3) %2B 0.2S_6 %2B B %2B \epsilon"> -->
<!-- <img src="https://render.githubusercontent.com/render/math?math=\epsilon ~ N(\mu = 0, \sigma_{\epsilon} = 0.5E[y])">
<img src="https://render.githubusercontent.com/render/math?math=E[y] = 5.75"> -->

Specifying that (AA = 2, Aa = 1, and aa = 0) for one or more alleles is optional and requires `major_minor_assign.txt`.

```
0
0
1
```

Specifying the first genotype's dominance (AA = 0, Aa = 2, and aa = 2) and second genotype's heterozygosity only (AA = 0, Aa = 2, and aa = 0) is optional and requires `SNP_phenotype_map.txt`. 

```
dominant
heterozygous_only
regular
```

Note that _R_ indicates `recessive` and _Ho_ indicates `homozygous_only`.

### Example 3: inclusion of epistatic effects

REGENS models epistasis between an arbitrary number of SNPs as the product of transformed SNP values in an individual.
Same command as in Example 2 simulates genotype-phenotype relationships for a different model if the input files were modified.

```bash
python REGENS.py --in ACB --out ACB_simulated \
    --simulate_nbreakpoints 4 --simulate_nsamples 10000 \
    --phenotype continuous --mean_phenotype 5.75 \
    --population_code ACB --human_genome_version hg19 \
    --noise 0.5 --causal_SNP_IDs_path causal_SNP_IDs.txt \
    --major_minor_assign_path major_minor_assign.txt \
    --SNP_phenotype_map_path SNP_phenotype_map.txt \
    --betas_path betas.txt
```

y = 0.2s<sub>1</sub> + 0.2s<sub>2</sub>R(s<sub>3</sub>)+ 0.2Ho(s<sub>4</sub>)s<sub>5</sub>s<sub>5</sub> + B + &epsilon;

where &epsilon; ~ N(&mu; = 0, &sigma;<sub>&epsilon;</sub> = 0.5E[y] and E[y] = 5.75.

<!-- <img src="https://render.githubusercontent.com/render/math?math=y = 0.2s_1 %2B 0.2s_2R(s_3) %2B 0.2Ho(S_4)s_5s_5 %2B B %2B \epsilon"> -->
<!-- <img src="https://render.githubusercontent.com/render/math?math=\epsilon ~ N(\mu = 0, \sigma_{\epsilon} = 0.5E[y])">
<img src="https://render.githubusercontent.com/render/math?math=E[y] = 5.75"> -->

Specifying that multiple SNPs interact (or that rs62240045 has a polynomic effect) requires placing all participating SNPs in the same tab seperated line of causal_SNP_IDs.txt

```
rs11852537
rs1867634	rs545673871
rs2066224	rs62240045	rs62240045
```

For each row containing one or more SNP IDs, `betas.txt` contains a corresponding beta coefficient. (Giving each SNP that participates in a multiplicative interaction its own beta coefficient would be pointless).

```
0.2
0.2
0.2
```

As before, both `major_minor_assign.txt` and `SNP_phenotype_map.txt` are both optional.
If they are not specified, then all SNPs will have the minor allele equal 1 so that the homozygous minor genotype equals 2, and all SNP_phenotype maps will be regular.

For each SNP ID, `major_minor_assign.txt` specifies whether the minor allele or the major allele equals 1, and correspondingly, whether homozygous minor or homozygous major equals 2.
CAUTION: In general, if a SNP appears in two different effects, then it may safely have different major/minor assignments in different effects.
However, if a SNP appears twice in the same effect, then make sure it has the same major/minor assignment within that effect, or that effect may equal 0 depending on the map functions that are used on the SNP. 

```
0	
0	0
1	0	0
```
For each SNP ID, `SNP_phenotype_map.txt` specifies whether the SNP's effect is regular, recessive, dominant, heterozygous_only, or homozygous_only.
In context to an epistatic interaction, first the map functions are applied to their respective SNPs, and then the resulting mapped SNP values are multiplied together as specified by `causal_SNP_IDs.txt`.

```
regular
regular	recessive
homozygous_only regular	regular
```

## License
MIT + file LICENSE

# Technical details

Each genome that REGENS simulates starts out as an empty template of SNP positions without SNP values, which is divided into empty segments that are demarcated by breakpoints. The probability of drawing any genomic position for a given breakpoint is equal to the probability that this position would demarcate a given real recombination event. Once an empty simulated genome is segmented by breakpoints, the row indices of whole genome bed file rows from a real dataset are duplicated so that 1) there is one real individual for each empty segment and 2) every real individual is selected an equal number of times (minus 1 for each remainder sample if the number of segments is not divisible by the number of individuals). Then, for each empty segment, a whole genome is randomly selected without replacement from the set of genomes that correspond to the duplicated indices, and the empty simulated segment is filled with the the homologous segment from the sampled real genome. These steps are repeated for every empty simulated segment so that all of the empty simulated genomes are filled with real SNP values. This quasirandom selection minimizes maf variation between the simulated and real datasets and also maintains normal population level genetic variability by randomizing segment selection. Even though the randomly selected segments are independent from one-another, the simulated dataset will contain the input dataset's LD pattern because each breakpoint location is selected with the same probability that they would demarcate a given real recombination event (i.e. a real biological concatenation of two independent genomic segment).

The Triadsim algorithm has used this method to simulate LD patterns that are almost indistinguishable from those of the input Dataset. REGENS simulates equally realistic data, and it was measured to be 88 times faster and require 8 times lower peak RAM than Triadsim. REGENS is designed to easily simulate GWAS data from any of the 26 populations in the [1000 genomes project](https://www.cog-genomics.org/plink/2.0/resources), and a filtered subset of these subpopulations' genotype data is provided in the github in corresponding plink filesets. In summary, I kept every biallelic SNP such that every subpopulation contains at least two instances of the minor allele. [Exact thinning methods are here](https://github.com/EpistasisLab/REGENS/blob/master/get_1000_genomes_files.sh). REGENS converts output recombination rate maps from [pyrho](https://github.com/popgenmethods/pyrho) (which correspond to the twenty-six 1000 Genome populations on a one to one basis) into probabilities of drawing each simulated breakpoint at a specific genomic location. It is also possible to simulate GWAS data from a custom plink (bed, bim, bam) fileset or a custom recombination rate map (or both files can be custom). Note that recombination rate maps between populations within a superpopulation (i.e. british and italian) have pearson correlation coefficients of roughly 0.9 [(see figure 2B of the pyrho paper)](https://advances.sciencemag.org/content/advances/5/10/eaaw9206.full.pdf), so if a genotype dataset has no recombination rate map for the exact population, then map for a closely relatrf population should suffice. 

We use 500000 SNPs filtered from the 1000 genomes dataset as an example. 
REGENS can select the population that matches most closely to the input dataset with the`--population_code` argument. `pyrho` paper's [Figure 2B](https://advances.sciencemag.org/content/advances/5/10/eaaw9206.full.pdf) shows that closely related populations' recombination rates have high pearson correlation coefficients (roughly 0.9), so using a pyrho recombination rate dataframe for a slightly different population's genotype dataset is acceptable.

## Optional input
- a newline seperated list of rsID sets, where rsIDs within a set are tab seperated and occupy one row.  
- a newline seperated list of real numbers (beta coefficients). Each row has one beta coefficient that corresponds to the product of genotype values in the same row of (3). 
- a newline seperated list of 0s and 1s in the same formation as the rsIDs in (3). If A/a are the major/minor alleles, then 0 specifies that (AA = 0, Aa = 1, and aa = 2), while 1 specifies that (AA = 2, Aa = 1, and aa = 0)
- a newline seperated list of genotype value transformation functions (i.e. is the effect dominant or recessive) in the same formation as the rsIDs in (3).

## REGENS simulates nearly flawless GWAS data

The Triadsim algorithm simulates LD patterns that are almost indistinguishable from those of the input Dataset. REGENS uses triadsim's method of recombining genomic segments to simulate equally realistic data, and we measured it to be 88 times faster and require 8 times lower peak RAM than Triadsim. The following three figures show that REGENS nearly perfectly replicates the input dataset's LD pattern. 

1. For the 1000 genome project's ACB population, this figure compares (right) every SNP's real maf against it's simulated maf and (left) every SNP pair's real genotype pearson correlation coefficient against its simulated genotype pearson correlation coefficient for SNP pairs less than  200 kilobases apart.<img src="https://github.com/EpistasisLab/REGENS/blob/master/images/real_vs_sim_r_val_maf_comparison_ACB.png" width=1000/>

2. For the 1000 genome project's ACB and GBR populations, these figures plot SNP pairs' absolute r values against their distance apart (up to 200 kilobases apart) for both real and simulated populations. More specifically, SNP pairs were sorted by their distance apart and seperated into 4000 adjacent bins, so each datapoint plots one bin's average absolute r value against its average position. Notice that the GBR population has an average |r| value above 0.3 at the distance of 25000, while the ACB population has an average |r| value below 0.3 at the same distance. REGENS precisely reconstructs the trend between LD and distance. <img src="https://github.com/EpistasisLab/REGENS/blob/master/images/real_vs_sim_r_vs_distance_profile_comparison_ACB.png" width=1000/>
<img src="https://github.com/EpistasisLab/REGENS/blob/master/images/real_vs_sim_r_vs_distance_profile_comparison_GBR.png" width=1000/>

3. These figures compare TSNE plots of the first 10 principal components for real and simulated 1000 genomes subpopulations. Principal components were computed from the 1000 genomes population datasets, and the loadings were used to project the simulated individuals onto the PC space. These results demonstrate that REGENS replicates the the input data's overall population structure in simulated datasets. Note that CEU samples, despite being considered European by the 1000 Genomes project, are plotted with other Americans because they are from Utah.<img src="https://github.com/EpistasisLab/REGENS/blob/master/images/TSNE1_vs_TSNE2_for_1000_genome_African_subpopulations.png" width=1000/>
