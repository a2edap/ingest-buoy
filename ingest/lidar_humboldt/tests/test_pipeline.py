import os
import xarray as xr
from utils import expand, set_dev_env
from ingest.lidar_humboldt import Pipeline

parent = os.path.dirname(__file__)


def test_lidar_humboldt_pipeline():
    set_dev_env()
    pipeline = Pipeline(
        expand("config/pipeline_config_lidar_humboldt.yml", parent),
        expand("config/storage_config_lidar_humboldt.yml", parent),
    )
    output = pipeline.run(
        expand("tests/data/input/lidar.z05.00.20201201.000000.sta.7z", parent)
    )
    expected = xr.open_dataset(expand("tests/data/expected/data.csv", parent))
    xr.testing.assert_allclose(output, expected)
