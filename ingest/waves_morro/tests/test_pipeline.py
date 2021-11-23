import os
import xarray as xr
from utils import expand, set_dev_env
from ingest.waves_morro import Pipeline

parent = os.path.dirname(__file__)


def test_waves_morro_pipeline():
    set_dev_env()
    pipeline = Pipeline(
        expand("config/pipeline_config_waves_morro.yml", parent),
        expand("config/storage_config_waves_morro.yml", parent),
    )
    output = pipeline.run(
        expand("tests/data/input/buoy.z06.00.20201201.000000.waves.csv", parent)
    )
    expected = xr.open_dataset(
        expand(
            "tests/data/expected/morro.buoy_z06-waves-20m.a1.20201201.000000.nc", parent
        )
    )
    xr.testing.assert_allclose(output, expected)
