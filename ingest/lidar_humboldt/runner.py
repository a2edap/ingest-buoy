from ingest.lidar_humboldt import Pipeline
from utils import expand, set_dev_env


if __name__ == "__main__":
    set_dev_env()
    pipeline = Pipeline(
        expand("config/pipeline_config_lidar_humboldt.yml", __file__),
        expand("config/storage_config_lidar_humboldt.yml", __file__),
    )
    pipeline.run(
        expand("tests/data/input/lidar.z05.00.20201201.000000.sta.7z", __file__)
    )
