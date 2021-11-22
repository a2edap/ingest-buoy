import os
import xarray as xr
from utils import expand, set_dev_env
from ingest.lidar_morro import Pipeline

parent = os.path.dirname(__file__)


def test_lidar_morro_pipeline():
    set_dev_env()
    pipeline = Pipeline(
        expand("config/pipeline_config_lidar_morro.yml", parent),
        expand("config/storage_config_lidar_morro.yml", parent),
    )
    output = pipeline.run(
        expand("tests/data/input/lidar.z06.00.20201201.000000.sta.7z", parent)
    )
    expected = xr.open_dataset(
        expand(
            "tests/data/expected/morro.buoy_z06-lidar-10m.a1.20201201.001000.nc", parent
        )
    )
    xr.testing.assert_allclose(output, expected)
