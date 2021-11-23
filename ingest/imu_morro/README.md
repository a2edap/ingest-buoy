# IMU Ingest at Morro Bay, CA

Ingest of IMU data from an AXYS Technologies buoy stationed in Morro Bay, CA.

Writen by [Maxwell Levin](mailto:maxwell.levin@pnnl.gov)

## Ingest Organization

The ingest takes the following layout:

- `runner.py` –– development entry point to run this pipeline on a set of input files.
- `mapping.py` –– Defines a mapping of filepath pattern to ingest specification so that
higher level processes know which ingest and configurations to use given a set of input
files.
- `__init__.py` –– Declares this folder as a Python module and provides a number of
methods / classes that upstream code can import.
upstream code can easily launch this ingest on data with the right parameters.
- `config/` –– Contains `yaml` configuration files for specifying metadata, quality
checks and handling, variable retrieval specifications, and input/output types.
- `pipeline/` –– Contains Python code meant to be modified to implement plotting
capabilities, add derived variables, implement custom `FileHandler` or qc objects, or
support any other custom functionality needed.
- `tests/` –– Contains tests that should be applied to this ingest in order to ensure
it functions as intended. Tests in here will be run any time a change is made to the
remote main branch, so the test(s) should be lightweight if possible.
