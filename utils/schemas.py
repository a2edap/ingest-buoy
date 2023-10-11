from pathlib import Path

from pydantic import Extra, Field
from tsdat import (
    DatasetConfig,
    PipelineConfig,
    QualityConfig,
    RetrieverConfig,
    StorageConfig,
)
from tsdat.config.attributes import GlobalAttributes


class A2eGlobalAttrs(GlobalAttributes, extra=Extra.allow):
    z_id: str = Field(
        ...,
        regex=r"[a-z][0-9]{2}",
        description=(
            "The instance code for the instrument, used to differentiate multiple"
            " instances of the same instrument at a given location. Looks like 'z01',"
            " 'z02', etc."
        ),
    )


class A2eDatasetConfig(DatasetConfig, extra=Extra.allow):
    attrs: A2eGlobalAttrs = Field(
        ...,
        description="Attributes that pertain to the dataset as a whole (as opposed to"
        " attributes that are specific to individual variables.",
    )


def generate_schema(dir: Path = Path(".vscode/schema/")):
    dir.mkdir(exist_ok=True)
    cls_mapping = {
        "retriever": RetrieverConfig,
        "dataset": A2eDatasetConfig,
        "quality": QualityConfig,
        "storage": StorageConfig,
        "pipeline": PipelineConfig,
    }
    for key, config_class in cls_mapping.items():
        path = dir / f"{key}-schema.json"
        config_class.generate_schema(path)
        print(f"Wrote {key} schema file to {path}")
    print("Done!")


if __name__ == "__main__":
    generate_schema()
