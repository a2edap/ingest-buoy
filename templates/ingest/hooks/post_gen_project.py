import os
import subprocess
from pathlib import Path
import sys

PROJECT_DIR = Path.cwd()  # cwd changes to the newly-generated project when this runs


def main():
    print("Template created for {{ cookiecutter.ingest_name }}. Checking selections...")

    if "{{ cookiecutter.use_custom_data_reader }}" == "no":  # type: ignore
        os.remove(PROJECT_DIR / "readers.py")

    if "{{ cookiecutter.use_custom_data_converter }}" == "no":  # type: ignore
        os.remove(PROJECT_DIR / "converters.py")

    if "{{ cookiecutter.use_custom_qc }}" == "no":  # type: ignore
        os.remove(PROJECT_DIR / "qc.py")
        os.remove(PROJECT_DIR / "config" / "quality.yaml")

    print("Formatting template code...")

    subprocess.run(["black", PROJECT_DIR])

    print(f"Generated {{ cookiecutter.ingest_name }} in {PROJECT_DIR}")


if __name__ == "__main__":
    main()
    sys.exit(0)
