import traceback

import json
import logging
import sys

logger = logging.getLogger(__name__)


def log_exception(error_message=""):
    exception_type, exception_value, exception_traceback = sys.exc_info()
    traceback_string = traceback.format_exception(
        exception_type, exception_value, exception_traceback
    )
    err_msg = json.dumps(
        {
            "Error_Message": error_message,
            "Error_Type": exception_type.__name__,
            "Exception_Message": str(exception_value),
            "Stack_Trace": traceback_string,
        }
    )
    logger.error(err_msg)


def get_log_message(
    pipeline_state, pipeline_name, location, input_files, exception=False
):

    log_msg = {
        "Pipeline_Name": pipeline_name,
        "State": pipeline_state,
        "Location": location,
        "Input_Files": input_files,
    }

    if exception:
        exception_type, exception_value, exception_traceback = sys.exc_info()
        traceback_string = traceback.format_exception(
            exception_type, exception_value, exception_traceback
        )
        log_msg["Error_Type"] = exception_type.__name__
        log_msg["Exception_Message"] = str(exception_value)
        log_msg["Stack_Trace"] = traceback_string

    return json.dumps(log_msg)
