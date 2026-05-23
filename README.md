# Automation for Lattice Generation and FEM Simulation

This repository contains a reproducible workflow for generating lattice-based nose cone, preparing Ansys LS-DYNA input decks, running impact simulations, and post-processing the results.

The codebase was organized to support publication sharing: each stage of the workflow is separated into a small set of notebooks and data folders so that the modeling pipeline can be inspected and adapted for related studies.

## Repository Overview

- [CAD_files](CAD_files): source CAD geometry used as the basis for the lattice structure.
- [nTop_files](nTop_files): nTop templates and related files used to generate lattice structures and finite-element meshes.
- [DYNA_files](DYNA_files): LS-DYNA keyword files used for simulation.
- [scripts](scripts): Jupyter notebooks and Python utilities for generation, setup, simulation, and post-processing.

## Python Requirements

Install the Python dependencies with:

```bash
pip install -r requirements.txt
```

## Software Requirements

- nTop for lattice generation and mesh export
- Ansys LS-DYNA for impact simulation

## Workflow

1. Generate or update the lattice finite-element model from the nTop template. Log in nTop before running notebook.
   [scripts/generate_k_file_from_nTop.ipynb](scripts/generate_k_file_from_nTop.ipynb)

2. Build the LS-DYNA keyword decks for the lattice and the assembled impact system, then launch the simulation.
   Notebook: [scripts/setup_k_file_and_run.ipynb](scripts/setup_k_file_and_run.ipynb)

3. Post-process the LS-DYNA results and extract metrics such as HIC from the generated `d3plot`.
   Notebook: [scripts/get_HIC.ipynb](scripts/get_HIC.ipynb)

Because some paths in the notebooks point to local software installations, users should review solver and application paths before running the workflow on a new machine.

## Reproducibility Notes

- Generated keyword files in [DYNA_files](DYNA_files) can be used as reference examples for expected deck structure.
- Some notebooks assume that prerequisite files already exist from an earlier step in the workflow.
- Local executable paths for LS-DYNA, nTop, or related tools may need to be updated before execution.

## Suggested Citation Use

If this repository is shared alongside a publication, it is best described as:

"A workflow for automated lattice generation, LS-DYNA deck construction, impact simulation, and post-processing for lattice nose-cone studies."
