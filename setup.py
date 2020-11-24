from setuptools import setup
from setuptools import find_packages

regens_summary = "REGENS (REcombinatory Genome ENumeration of Subpopulations) is an open "
regens_summary += "source Python package that simulates whole genomes from real genomic "
regens_summary += "segments. REGENS recombines these segments in a way that simulates "
regens_summary += "completely new individuals while simultaneously preserving the input "
regens_summary += "genomes' linkage disequilibrium (LD) pattern with extremely high fedility. "
regens_summary += "REGENS can also simulate mono-allelic and epistatic single nucleotide variant "
regens_summary += "(SNV) effects on a continuous or binary phenotype without perturbing the simulated LD pattern."
regens_summary += "\n\nplease visit our [github page](https://github.com/EpistasisLab/regens) for more information"

setup(
    long_description = regens_summary,
    long_description_content_type = 'text/markdown',
    packages = find_packages(),
    version='0.2.0',
    python_requires = "==3.7.*",
    name = 'regens',
    entry_points = {'console_scripts': ['regens = regens:main']},
    py_modules = ['regens', 'regens_library', 'regens_testers'],
    setup_requires=["numpy"],
    install_requires = ["bed-reader==0.1.1",
                        "numpy==1.16.2",
                        "pandas==1.1.2",
                        "matplotlib==3.0.3",
                        "scipy==1.2.1",
                        "scikit-learn==0.20.3"]
)
