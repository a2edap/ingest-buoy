from pathlib import Path

import xarray as xr

from utils.a2e_tsdat import PipelineConfig, assert_close


def test_lidar_morro():
    config_path = Path("pipelines/lidar/config/pipeline_morro.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "pipelines/lidar/test/data/input/lidar.z06.00.20201201.000000.sta.7z"
    expected_file = "pipelines/lidar/test/data/expected/morro.buoy_z06-lidar-10m.a1.20201201.001000.nc"

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore
    assert_close(dataset, expected, check_attrs=False)


def test_lidar_humboldt():
    config_path = Path("pipelines/lidar/config/pipeline_humboldt.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "pipelines/lidar/test/data/input/lidar.z05.00.20201201.000000.sta.7z"
    expected_file = "pipelines/lidar/test/data/expected/humboldt.buoy_z05-lidar-10m.a1.20201201.001000.nc"

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore
    assert_close(dataset, expected, check_attrs=False)
