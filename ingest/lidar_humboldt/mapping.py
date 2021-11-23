import re

from typing import AnyStr, Dict
from utils import IngestSpec, expand
from . import Pipeline


mapping: Dict["AnyStr@compile", IngestSpec] = {
    # Mapping for Raw Data -> Ingest
    re.compile(r".*/lidar\.z05\.00\.\d{8}\.\d{6}\.sta\.7z"): IngestSpec(
        pipeline=Pipeline,
        pipeline_config=expand("config/pipeline_config_lidar_humboldt.yml", __file__),
        storage_config=expand("config/storage_config_lidar_humboldt.yml", __file__),
        name="lidar_humboldt",
    ),
    # Mapping for Processed Data -> Ingest (so we can reprocess plots)
    re.compile(r".*/lidar\.z05\.a0\.\d{8}\.\d{6}\.sta\.a2e\.nc"): IngestSpec(
        pipeline=Pipeline,
        pipeline_config=expand("config/pipeline_config_lidar_humboldt.yml", __file__),
        storage_config=expand("config/storage_config_lidar_humboldt.yml", __file__),
        name="plot_lidar_humboldt",
    ),
    # You can add as many {regex: IngestSpec} entries as you would like. This is useful
    # if you would like to reuse this ingest at other locations or possibly for other
    # similar instruments
}
