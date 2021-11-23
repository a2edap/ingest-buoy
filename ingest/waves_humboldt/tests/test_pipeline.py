import os
import xarray as xr
from utils import expand, set_dev_env
from ingest.waves_humboldt import Pipeline

parent = os.path.dirname(__file__)


def test_waves_humboldt_pipeline():
    set_dev_env()
    pipeline = Pipeline(
        expand("config/pipeline_config_waves_humboldt.yml", parent),
        expand("config/storage_config_waves_humboldt.yml", parent),
    )
    output = pipeline.run(
        expand("tests/data/input/buoy.z05.00.20201201.000000.waves.csv", parent)
    )
    expected = xr.open_dataset(
        expand(
            "tests/data/expected/humboldt.buoy_z05-waves-20m.a1.20201201.000000.nc",
            parent,
        )
    )
    xr.testing.assert_allclose(output, expected)
