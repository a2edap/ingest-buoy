# Ingest Pipeline Cookiecutter

This cookiecutter template is intended to be used to generate boilerplate pipeline code
to accelerate the development of ingest pipelines.

To use it, make sure you have `cookiecutter` installed (This should already be
installed if you set up your development environment according to
[the instructions](../../README.md#development-environment-setup))
```
pip install cookiecutter
```

Then run the following command from the top-level directory of the repository:
```
cookiecutter templates/ingest -o ingest/
```

This will bring up a commandline interface which will go through some options. Consult
the documentation below for more information regarding these prompts.


| Field                    | Default               | Description                                                                                                                         |
|--------------------------|-----------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| `author`                 | `First Last`          | Main author of this ingest.                                                                                                         |
| `email`                  |                       | Contact email of the author.                                                                                                        |
| `location`               | `Location`            | The name of the location where the instrument or ingest is located.                                                                 |
| `location_slug`          | `location`            | Location used to name files and attributes. Lowercase alphanumeric and '_' characters allowed.                                      |
| `ingest`                 | `Ingest Name`         | Verbose name of the ingest. Used in README.md                                                                                       |
| `ingest_slug`            | `ingest_name`         | Name used for the ingest module. Should take the format: `type_make_model_loc` (e.g., `lidar_halo_xrp_nwtc`)                        |
| `description`            | `description`         | A brief description of the ingest. Used in README.md                                                                                |
| `use_custom_filehandler` | `yes`                 | Flag to generate a custom FileHandler template. Use this if data cannot be read in using out-of-box FileHandlers provided by tsdat. |
| `use_custom_qc`          | `yes`                 | Flag to generate a custom QC template module. Use this if you want to apply custom quality checks or handlers.                      |
