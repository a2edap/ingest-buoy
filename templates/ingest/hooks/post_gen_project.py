import os
import shutil
import subprocess

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def copy_file(filepath, target):
    shutil.copy(filepath, os.path.join(PROJECT_DIRECTORY, target))


if __name__ == "__main__":

    print("Template created for {{ cookiecutter.ingest_slug }}")

    if "{{ cookiecutter.use_custom_filehandler }}" == "no":
        remove_file("pipeline/filehandler.py")

    if "{{ cookiecutter.use_custom_qc }}" == "no":
        remove_file("pipeline/qc.py")

    print("Linting template code...")

    subprocess.run(["black", PROJECT_DIRECTORY])

    print(f"Generated {{ cookiecutter.ingest_slug }} at {PROJECT_DIRECTORY}")
