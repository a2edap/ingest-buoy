import os
import xarray as xr
from utils import expand, set_env
from ingest.{{ cookiecutter.ingest_slug }} import Pipeline

parent = os.path.dirname(__file__)


# TODO – Developer: Update paths to your input files here. Please add tests if needed.
def test_{{ cookiecutter.ingest_slug }}_pipeline():
    set_env()
    pipeline = Pipeline(
        expand("config/pipeline_config_{{ cookiecutter.ingest_slug }}.yml", parent),
        expand("config/storage_config_{{ cookiecutter.ingest_slug }}.yml", parent),
    )
    output = pipeline.run(expand("tests/data/input/data.csv", parent))
    expected = xr.open_dataset(expand("tests/data/expected/data.csv", parent))
    xr.testing.assert_allclose(output, expected)
