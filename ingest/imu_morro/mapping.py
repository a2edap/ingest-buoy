import re

from typing import AnyStr, Dict
from utils import IngestSpec, expand
from . import Pipeline


mapping: Dict["AnyStr@compile", IngestSpec] = {
    # Mapping for Raw Data -> Ingest
    re.compile(r".*/buoy\.z06\.00\.\d{8}\.\d{6}\.imu\.bin"): IngestSpec(
        pipeline=Pipeline,
        pipeline_config=expand("config/pipeline_config_imu_morro.yml", __file__),
        storage_config=expand("config/storage_config_imu_morro.yml", __file__),
        name="imu_morro",
    ),
    # Mapping for Processed Data -> Ingest (so we can reprocess plots)
    re.compile(r".*/buoy\.z06\.a0\.\d{8}\.\d{6}\.imu\.a2e\.nc"): IngestSpec(
        pipeline=Pipeline,
        pipeline_config=expand("config/pipeline_config_imu_morro.yml", __file__),
        storage_config=expand("config/storage_config_imu_morro.yml", __file__),
        name="plot_imu_morro",
    ),
}
