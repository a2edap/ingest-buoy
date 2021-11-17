import numpy as np
from typing import Optional
from tsdat import DSUtil, QualityChecker, QualityHandler


# TODO – Developer: Add your custom quality checker / quality handler. Rename these to
# indicate more clearly what they do. You will need to update the pipeline config file
# with the new class name.


class CustomQualityChecker(QualityChecker):
    def run(self, variable_name: str) -> Optional[np.ndarray]:

        # False values in the results array mean the check passed, True values indicate
        # the check failed. Here we initialize the array to be full of False values as
        # an example. Note the shape of the results array must match the variable data.
        results_array = np.full_like(
            self.ds[variable_name].data,
            fill_value=False,
            dtype=bool,
        )

        return results_array


class CustomQualityHandler(QualityHandler):
    def run(self, variable_name: str, results_array: np.ndarray):

        # Some QualityHandlers only want to run if at least one value failed the check.
        # In this case, we replace all values that failed the check with the variable's
        # _FillValue and (possibly) add an attribute to the variable indicating the
        # correction applied.
        if results_array.any():

            fill_value = DSUtil.get_fill_value(self.ds, variable_name)
            keep_array = np.logical_not(results_array)

            var_values = self.ds[variable_name].data
            replaced_values = np.where(keep_array, var_values, fill_value)
            self.ds[variable_name].data = replaced_values

            self.record_correction(variable_name)
