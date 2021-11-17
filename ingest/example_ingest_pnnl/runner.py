from ingest.example_ingest_pnnl import Pipeline
from utils import expand, set_dev_env


if __name__ == "__main__":
    set_dev_env()
    pipeline = Pipeline(
        expand("config/pipeline_config_example_ingest_pnnl.yml", __file__),
        expand("config/storage_config_example_ingest_pnnl.yml", __file__),
    )
    pipeline.run(expand("tests/data/input/data.csv", __file__))
