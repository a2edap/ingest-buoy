# INGEST-TEMPLATE

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![tests](https://github.com/tsdat/ingest-template/actions/workflows/tests.yml/badge.svg)](https://github.com/tsdat/ingest-template/actions/workflows/tests.yml)

This repository helps provide a way to group similar `tsdat` ingest scripts in the same
repository so that they can be more easily maintained and deployed on input files. 


## How it works

- **`runner.py`**: Top-level CLI to run the appropriate ingest on one or more files.
Run `python runner.py --help` to see the full list of commands it offers.
- **`ingest/*`**: collection of python modules, each of which is a self-describing and
self-contained ingest. Every ingest module exports the necessary information for the
`runner` or higher-level processes to instantiate and run the ingest.
- **`tests/*`**: tests performed on all ingests. Note that individual ingests also define
their own tests, so this folder is primarily used for high-level sanity checks.
- **`utils/*`**: utility methods and classes used throughout the project. This folder
will be updated as needed to allow ingests to leverage common project-specific tools.
- **`.devcontainer/*`, `.vscode/*`, `*docker*`**: Configurations to simplify and
development environment setup.
- **`.github/*`**: Workflows and templates to ensure code is well-tested and issues are
tracked appropriately.


## Adding a new pipeline

Developers should follow the following five-step process to create a new ingest
pipeline.

1. Clone or fork this repository to your development area
2. Set up your development environment according to the instructions below.
3. Run `> pytest` to ensure that tests pass (validate your setup)
4. Run `> cookiecutter templates/ingest -o ingest/` to generate your own ingest.
5. Follow the steps outlined in the generated ingest README to modify the generated ingest code.
6. Test your changes, then push back up to your remote repository.

This repository supports adding as many ingests as you want. Just follow steps 3-6 for
each new ingest you want to add.


## Development environment setup

This section outlines how to set up the recommended development environment for this
project.


1. Download and install [VS Code](https://code.visualstudio.com). Make sure to add 
`code` to your path if prompted.

    We chose VS Code because of its clean user interface, quick startup time, extremely
    powerful capabilities out-of-box, and its rich library of open source extensions.

2. Clone your fork of this repository to your laptop and open it up in VS Code

3. The first time you open this project in VS Code you will be prompted to install the
recommended extensions. Please do so now.

4. **Windows users**: We recommend using
[Docker](https://www.docker.com/products/docker-desktop) to manage dependencies for
this project. If you choose to use Docker follow the steps below:
    - Press `F1` (or `ctrl-shift-p`) to bring up the command pane in VS Code
    - In the command pane, type: `Remote-Containers: Open Folder in Container...` and
    hit `return`
    - You will be prompted to specify which folder should be opened. Select the folder
    containing this `README` file
    - Several dialog boxes may appear while the VS Code window is refreshing. Please
    install the recommended extensions via the dialog box. An additional dialog box
    should appear asking you to reload the window so Pylance can take effect. Please do
    this as well.
    - After the window refreshes your development environment will be set up correctly.
    You may skip steps 5. and 6.

    You can find more information about VS Code and docker containers
    [here](https://code.visualstudio.com/docs/remote/containers).

5. We highly recommend using [conda](https://docs.anaconda.com/anaconda/install/) to
manage dependencies in your development environment. Please install this using the link
above if you haven't already done so. Then run the following commands to create your
environment:
    
    ```bash
    $ conda create --name ingest python=3.8
    $ conda activate ingest
    (ingest) $ pip install -r requirements-dev.txt
    ```

6. Tell VS Code to use your new `conda` environment:
    - Press `F1` (or `ctrl-shift-p`) to bring up the command pane in VS Code
    - In the command pane, type: `Python: Select Interpreter` and hit `return`
    - Select the newly-created `ingest` conda environment from the list. Note
    that you may need to refresh the list (cycle icon in the top right) for it to show
    up.
    - Reload the VS Code window to ensure that this setting propagates correctly.
    This is probably not needed, but doesn't hurt. To do this, press `F1` to open
    the control pane again and type `Developer: Reload Window`.

## Additional resources

- Learn more about `tsdat`:
    - GitHub: https://github.com/tsdat/tsdat
    - Documentation: https://tsdat.readthedocs.io
    - Data standards: https://github.com/tsdat/data_standards
- Learn more about `xarray`: 
    - GitHub: https://github.com/pydata/xarray
    - Documentation: https://xarray.pydata.org
- Other useful tools:
    - VS Code: https://code.visualstudio.com/docs
    - Docker: https://docs.docker.com/get-started/
    - `pytest`: https://github.com/pytest-dev/pytest
    - `black`: https://github.com/psf/black
    - `matplotlib` guide: https://realpython.com/python-matplotlib-guide/