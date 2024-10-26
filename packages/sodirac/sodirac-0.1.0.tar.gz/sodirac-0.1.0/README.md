# DIRAC (Domain Invariant Respresentation through Adversatial Calibration)

[![stars-badge](https://img.shields.io/github/stars/boxiangliulab/DIRAC?logo=GitHub&color=yellow)](https://github.com/boxiangliulab/DIRAC/stargazers)
[![pypi-badge](https://img.shields.io/pypi/v/scglue)](https://pypi.org/project/dirac)
[![conda-badge](https://anaconda.org/bioconda/scglue/badges/version.svg)](https://anaconda.org/bioconda/scglue)
[![docs-badge](https://readthedocs.org/projects/scglue/badge/?version=latest)](https://scglue.readthedocs.io/en/latest/?badge=latest)
[![build-badge](https://github.com/gao-lab/GLUE/actions/workflows/build.yml/badge.svg)](https://github.com/gao-lab/GLUE/actions/workflows/build.yml)
[![coverage-badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/Jeff1995/e704b2f886ff6a37477311b90fdf7efa/raw/coverage.json)](https://github.com/gao-lab/GLUE/actions/workflows/build.yml)
[![license-badge](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


### Spatially resolved integration of multi-omics with DIRAC highlights cell-specific remodeling

![Model architecture](docs/Figs/Workflow.png)

For more details, please check out our [publication](https://doi.org/10.1038/s41587-022-01284-4).

## Directory structure

```
.
├── dirac                  # Main Python package
├── data                    # Data files
├── evaluation              # Method evaluation pipelines
├── experiments             # Experiments and case studies
├── tests                   # Unit tests for the Python package
├── docs                    # Documentation files
├── custom                  # Customized third-party packages
├── packrat                 # Reproducible R environment via packrat
├── env.yaml                # Reproducible Python environment via conda
├── pyproject.toml          # Python package metadata
├── LICENSE
└── README.md
```

## Installation

The `spagnns` package can be installed via conda using one of the following commands:

```sh
conda install -c conda-forge -c bioconda dirac  # CPU only
conda install -c conda-forge -c bioconda dirac pytorch-gpu  # With GPU support
```

Or, it can also be installed via pip:

```sh
pip install spagnns
```

> Installing within a
> [conda environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
> is recommended.

## Usage

Please checkout the documentations and tutorials at
[dirac.readthedocs.io](https://rundirac.readthedocs.io/en/latest/).
