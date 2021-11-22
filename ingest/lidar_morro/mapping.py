import re

from typing import AnyStr, Dict
from utils import IngestSpec, expand
from . import Pipeline


mapping: Dict["AnyStr@compile", IngestSpec] = {
    # Mapping for Raw Data -> Ingest
    re.compile(r".*/lidar\.z06\.00\.\d{8}\.\d{6}\.sta\.7z"): IngestSpec(
        pipeline=Pipeline,
        pipeline_config=expand("config/pipeline_config_lidar_morro.yml", __file__),
        storage_config=expand("config/storage_config_lidar_morro.yml", __file__),
        name="lidar_morro",
    ),
    # Mapping for Processed Data -> Ingest (so we can reprocess plots)
    re.compile(r"lidar\.z06\.a0\.\d{8}\.\d{6}\.sta\.a2e\.nc"): IngestSpec(
        pipeline=Pipeline,
        pipeline_config=expand("config/pipeline_config_lidar_morro.yml", __file__),
        storage_config=expand("config/storage_config_lidar_morro.yml", __file__),
        name="plot_lidar_morro",
    ),
}
