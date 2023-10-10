from pathlib import Path

import xarray as xr

from utils.a2e_tsdat import PipelineConfig, assert_close


def test_waves_morro():
    config_path = Path("pipelines/waves/config/pipeline_morro.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "pipelines/waves/test/data/input/buoy.z06.00.20201201.000000.waves.csv"
    expected_file = "pipelines/waves/test/data/expected/morro.buoy_z06-waves-20m.a1.20201201.000000.nc"

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore
    assert_close(dataset, expected, check_attrs=False)


def test_waves_humboldt():
    config_path = Path("pipelines/waves/config/pipeline_humboldt.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "pipelines/waves/test/data/input/buoy.z05.00.20201201.000000.waves.csv"
    expected_file = "pipelines/waves/test/data/expected/humboldt.buoy_z05-waves-20m.a1.20201201.000000.nc"

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore
    assert_close(dataset, expected, check_attrs=False)
