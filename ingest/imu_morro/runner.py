from ingest.imu_morro import Pipeline
from utils import expand, set_dev_env

if __name__ == "__main__":
    set_dev_env()
    pipeline = Pipeline(
        expand("config/pipeline_config_imu_morro.yml", __file__),
        expand("config/storage_config_imu_morro.yml", __file__),
    )
    pipeline.run(
        expand("tests/data/input/buoy.z06.00.20201201.000000.imu.bin", __file__)
    )
