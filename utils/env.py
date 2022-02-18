import os

from .logger import logger


def set_env(**kwargs):
    """----------------------------------------------------------------------------
    Ensures that environment variables used by the pipeline are set. If there are
    not already set, this method will set them to good defaults for running in a
    local filesystem environment in development mode. Keyword arguments are
    accepted to override the default values, but environment variables will take
    precedence over defaults or keyword arguments.
    ----------------------------------------------------------------------------"""

    defaults = {
        "LOG_LEVEL": "DEBUG",
        "RETAIN_INPUT_FILES": "True",
        "STORAGE_CLASSNAME": "tsdat.io.FilesystemStorage",
        "STORAGE_BUCKET": "N/A",
        "ROOT_DIR": "storage",
    }
    defaults.update(kwargs)

    for key, default in defaults.items():
        if key not in os.environ:
            os.environ[key] = default

    logger.setLevel(os.environ["LOG_LEVEL"])
