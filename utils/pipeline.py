import xarray as xr
from tsdat import IngestPipeline, FileHandler, S3Path
from tsdat.qc import QualityManagement
from typing import Union, List, Dict


class IngestPipeline(IngestPipeline):
    def run(self, filepath: Union[str, List[str]]) -> xr.Dataset:
        """----------------------------------------------------------------------------
        Runs the pipeline from start to finish.

        Args:
            filepath (Union[str, List[str]]): The path or list of paths to the file(s)
            to run the pipeline on.

        Returns:
            xr.Dataset: The processed xarray dataset. Note that this is the internal
            representation of the dataset. The final dataset will have already been
            written to disk.

        ----------------------------------------------------------------------------"""
        # If the file is a zip/tar, then we need to extract the individual files
        with self.storage.tmp.extract_files(filepath) as file_paths:

            # Open each raw file into a Dataset, standardize the raw file names and store.
            raw_dataset_mapping: Dict[
                str, xr.Dataset
            ] = self.read_and_persist_raw_files(file_paths)

            # Customize the raw data before it is used as input for standardization
            raw_dataset_mapping: Dict[
                str, xr.Dataset
            ] = self.hook_customize_raw_datasets(raw_dataset_mapping)

            # Standardize the dataset and apply corrections / customizations
            dataset = self.standardize_dataset(raw_dataset_mapping)
            dataset = self.hook_customize_dataset(dataset, raw_dataset_mapping)

            # Apply quality control / quality assurance to the dataset.
            previous_dataset = self.get_previous_dataset(dataset)
            dataset = QualityManagement.run(dataset, self.config, previous_dataset)

            # Apply any final touches to the dataset and persist the dataset
            dataset = self.hook_finalize_dataset(dataset)
            dataset = self.store_and_reopen_dataset(dataset)

            # Hook to generate custom plots
            self.hook_generate_and_persist_plots(dataset)

        return dataset

    def run_plots(self, files: Union[List[S3Path], List[str]]):
        """----------------------------------------------------------------------------
        Runs the `IngestPipeline.hook_generate_and_persist_plots()` function on the
        provided file or list of files. This is useful for re-running plots without the
        need to also reprocess the data.

        Args:
            files (Union[List[S3Path], str]): The file(s) to read in and produce plots
            for. Note that these files will be processed independent of one another.

        ----------------------------------------------------------------------------"""
        for _file in files:
            with self.storage.tmp.fetch(_file) as tmp_file:
                ds = FileHandler.read(tmp_file)
                self.hook_generate_and_persist_plots(ds)
