import os
import xarray as xr
from utils import expand, set_dev_env
from ingest.imu_humboldt import Pipeline

parent = os.path.dirname(__file__)


def test_imu_humboldt_pipeline():
    set_dev_env()
    pipeline = Pipeline(
        expand("config/pipeline_config_imu_humboldt.yml", parent),
        expand("config/storage_config_imu_humboldt.yml", parent),
    )
    output = pipeline.run(
        expand("tests/data/input/buoy.z05.00.20201201.000000.imu.bin", parent)
    )
    expected = xr.open_dataset(
        expand(
            "tests/data/expected/humboldt.buoy_z05-imu.a1.20201201.000008.nc", parent
        )
    )
    xr.testing.assert_allclose(output, expected)
