from setuptools import setup
from setuptools import find_packages

regens_summary = "REGENS (REcombinatory Genome ENumeration "
regens_summary += "of Subpopulations) is an open source "
regens_summary += "Python package that simulates whole "
regens_summary += "genomes from real genomic segments. "
regens_summary += "REGENS recombines these segments in "
regens_summary += "a way that simulates completely new "
regens_summary += "individuals while simultaneously "
regens_summary += "preserving the input genomes' linkage "
regens_summary += "disequilibrium (LD) pattern with "
regens_summary += "extremely high fedility. REGENS can "
regens_summary += "also simulate mono-allelic and "
regens_summary += "epistatic single nucleotide variant "
regens_summary += "(SNV) effects on a continuous or binary "
regens_summary += "phenotype without perturbing the "
regens_summary += "simulated LD pattern.\n\nplease visit "
regens_summary += "our [github page](https://github.com/Ep"
regens_summary += "istasisLab/regens) for more information."

setup(
    long_description=regens_summary,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    version="0.2.0",
    python_requires="==3.7.*",
    name="regens",
    entry_points={"console_scripts": ["regens = regens:main"]},
    py_modules=["regens", "regens_library", "regens_testers"],
    setup_requires=["numpy"],
    install_requires=[
        "bed-reader==0.1.1",
        "numpy==1.16.2",
        "pandas==1.1.2",
        "matplotlib==3.0.3",
        "scipy==1.2.1",
        "scikit-learn==0.20.3",
    ],
)
