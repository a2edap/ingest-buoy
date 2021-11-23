from ingest.waves_humboldt import Pipeline
from utils import expand, set_dev_env

if __name__ == "__main__":
    set_dev_env()
    pipeline = Pipeline(
        expand("config/pipeline_config_waves_humboldt.yml", __file__),
        expand("config/storage_config_waves_humboldt.yml", __file__),
    )
    pipeline.run(
        expand("tests/data/input/buoy.z05.00.20201201.000000.waves.csv", __file__)
    )
