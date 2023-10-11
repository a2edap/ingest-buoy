from pathlib import Path

import xarray as xr

from utils.a2e_tsdat import PipelineConfig, assert_close


def test_imu_morro():
    config_path = Path("pipelines/imu/config/pipeline_morro.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "pipelines/imu/test/data/input/buoy.z06.00.20201201.000000.imu.bin"
    expected_file = (
        "pipelines/imu/test/data/expected/morro.buoy_z06-imu.a1.20201201.000011.nc"
    )

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore
    assert_close(dataset, expected, check_attrs=False)


def test_imu_humboldt():
    config_path = Path("pipelines/imu/config/pipeline_humboldt.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "pipelines/imu/test/data/input/buoy.z05.00.20201201.000000.imu.bin"
    expected_file = (
        "pipelines/imu/test/data/expected/humboldt.buoy_z05-imu.a1.20201201.000008.nc"
    )

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore
    assert_close(dataset, expected, check_attrs=False)


def test_imu_oahu():
    config_path = Path("pipelines/imu/config/pipeline_oahu.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "pipelines/imu/test/data/input/buoy.z07.00.20221123.213000.imu.bin"
    expected_file = (
        "pipelines/imu/test/data/expected/oahu.buoy_z07-imu.a1.20221123.213037.nc"
    )

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore
    assert_close(dataset, expected, check_attrs=False)
