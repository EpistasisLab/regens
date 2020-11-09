Thank you for contributing to REGENS! :thumbsup: 

We welcome you to check the [existing issues](https://github.com/EpistasisLab/regens/issues) for bugs or enhancements to work on. 
If you find any bugs or have any questions/ideas for an extension to REGENS, please submit a [new issue](https://github.com/EpistasisLab/regens/issues/new) so we can discuss it.
More detailed guidelines below!

## How to report a bug

When submitting an issue, please make sure to answer these questions:

1. What version of REGENS are you using?
2. What operating system and processor architecture are you using?
3. What did you do?
4. What did you expect to see?
5. What did you see instead?

## How to submit a contribution

1. Create your own fork of this repository
2. Make the changes in your fork on a branch that is NOT master or main branch.
3. If you think the project would benefit from these changes:
    * Make sure you have followed the guidelines above.
    * Submit a pull request.

## Repository structure
Please be sure to familiarize yourself with the repository structure before making any major contributions.

### Folders :file_cabinet:

  * `correctness_testing_ACB`: A directory containing bash scripts to test code correctness on the ACB subpopulation, as well as the output for those tests. Correctness testing part 2 is optional and requires plink version 1.90Beta.
  * `correctness_testing_GBR`: A directory containing bash scripts to test code correctness on the GBR subpopulation, as well as the output for those tests. Correctness testing part 2 is optional and requires plink version 1.90Beta.
  * `examples`: A directory containing bash scripts that run the data simulation examples in the README.
  * `hg19`: for each 1000 genomes project population, contains a folder with one gzipped recombination rate dataframe per hg19 reference human autosome.
  * `hg38`: for each 1000 genomes project population, contains a folder with one gzipped recombination rate dataframe per hg38 reference human autosome.
  * `images`: contains figures that are either displayed or linked to in this github README
  * `input_files`: contains examples of regens input that is meant to be provided by the user. The example custom recombination rate information is copied from that of the hg19 mapped ACB population. Also contains input for the Triadsim algorithm. The genetic input labeled as "not_trio" for Triadsim is comprised of ACB population duplicates and is only meant to compare Triadsim's runtime. 
  * `paper`: A directory containing the paper's md file, bib file, and figure. 
  * `runtime_testing_files`: A directory containing files that were used to compute runtimes, max memory usage values, and improvement ratio bootstrapped confidence intervals.
  * `unit_testing_files`: A directory containing bash scripts to unit test code correctness on the ACB subpopulation, as well as the output for those tests.

### Files :file_folder:

  * `regens.py`: the main file that runs the regens algorithm
  * `regens_library.py`: functions that the regens algorithm uses repeatedly. 
  * `regens_testers.py`: functions used exclusively for correctness testing and unit testing

## Your first contribution

If you haven't contributed to open source code before, check out these friendly tutorials:

 * http://makeapullrequest.com/
 
 * http://www.firsttimersonly.com/
 
 * [How to contribute to an open source project on GitHub](https://egghead.io/series/how-to-contribute-to-an-open-source-project-on-github).

These guides should provide you with everything you need to start out!
