from setuptools import setup

setup(
    python_requires = ">=3.6"
    name = 'regens',
    entry_points = {'console_scripts': ['regens = regens:main']},
    install_requires = ["bed-reader==0.1.1",
                        "numpy==1.16.2",
                        "pandas==1.1.2",
                        "matplotlib==3.0.3",
                        "scipy==1.2.1",
                        "scikit-learn==0.20.3"]
)
