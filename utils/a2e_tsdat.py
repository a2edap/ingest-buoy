"""
Thin wrapper around tsdat to change how tsdat stores data to meet A2e filename standards
"""

import tsdat
from tsdat.tstring import Template

# Note: qualifier and temporal are part of the filename, not the datastream for A2e
tsdat.utils.DATASTREAM_TEMPLATE = Template(
    "{location_id}.{dataset_name}.{z_id}.{data_level}"
)

from tsdat import *
