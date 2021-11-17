import os

from .logger import logger


# TODO: Use a file to set default environment variables
def set_prod_env():
    """----------------------------------------------------------------------------
    Sets environment variables used by the pipeline's storage_config.yml file. Many
    of these environment variables will already be set if running in a deployed
    lambda environment, based on the lambda deployment template. This method makes
    sure that all values are set if they had not been set otherwise.

    ----------------------------------------------------------------------------"""

    # Name of storage bucket where output files are written
    bucket_name = os.environ["STORAGE_BUCKET"]
    assert bucket_name

    # Logging level to use
    logging_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    os.environ["LOG_LEVEL"] = logging_level

    # Whether or not original input files should be kept after they are done processing
    retain_input_files = os.environ.get("RETAIN_INPUT_FILES", "False")
    os.environ["RETAIN_INPUT_FILES"] = retain_input_files

    # Storage class to use
    storage_classname = os.environ.get("STORAGE_CLASSNAME", "tsdat.io.AwsStorage")
    os.environ["STORAGE_CLASSNAME"] = storage_classname

    # Configure the root logger
    logger.setLevel(os.environ["LOG_LEVEL"])


def set_dev_env(**kwargs):
    """----------------------------------------------------------------------------
    Sets environment variables used by the pipeline's storage_config.yml file. Sets
    reasonable defaults and allows for those environment variables to be overridden
    by keyword arguments passed to this function.

    ----------------------------------------------------------------------------"""

    os.environ["LOG_LEVEL"] = "DEBUG"
    os.environ["RETAIN_INPUT_FILES"] = "True"
    os.environ["STORAGE_CLASSNAME"] = "tsdat.io.FilesystemStorage"
    os.environ["STORAGE_BUCKET"] = "N/A"
    os.environ["ROOT_DIR"] = "storage"

    os.environ.update(kwargs)

    logger.setLevel(os.environ["LOG_LEVEL"])
