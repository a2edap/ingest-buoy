import xarray as xr
from pathlib import Path
from tsdat import PipelineConfig, assert_close


def test_metocean_morro():
    config_path = Path("pipelines/metocean/config/pipeline_morro.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "pipelines/metocean/test/data/input/buoy.z06.00.20201201.000000.zip"
    expected_file = "pipelines/metocean/test/data/expected/morro.buoy_z06-metocean-10m.a1.20201201.000000.nc"

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore
    assert_close(dataset, expected, check_attrs=False)


def test_metocean_humboldt():
    config_path = Path("pipelines/metocean/config/pipeline_humboldt.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "pipelines/metocean/test/data/input/buoy.z05.00.20201201.000000.zip"
    expected_file = "pipelines/metocean/test/data/expected/humboldt.buoy_z05-metocean-10m.a1.20201201.000000.nc"

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore
    assert_close(dataset, expected, check_attrs=False)
