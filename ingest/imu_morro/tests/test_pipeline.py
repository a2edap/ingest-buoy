import os
import xarray as xr
from utils import expand, set_dev_env
from ingest.imu_morro import Pipeline

parent = os.path.dirname(__file__)


def test_imu_morro_pipeline():
    set_dev_env()
    pipeline = Pipeline(
        expand("config/pipeline_config_imu_morro.yml", parent),
        expand("config/storage_config_imu_morro.yml", parent),
    )
    output = pipeline.run(
        expand("tests/data/input/buoy.z06.00.20201201.000000.imu.bin", parent)
    )
    expected = xr.open_dataset(
        expand("tests/data/expected/morro.buoy_z06-imu.a1.20201201.000011.nc", parent)
    )
    xr.testing.assert_allclose(output, expected)
