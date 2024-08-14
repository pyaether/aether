import argparse
import os
import re
import subprocess
from pathlib import Path

import tomli


def load_config():
    working_dir = os.getcwd()
    if os.path.isfile(working_dir + "/pyproject.toml"):
        with open(working_dir + "/pyproject.toml", "rb") as f:
            pyproject_tools: dict = tomli.load(f).get("tool")
            version = pyproject_tools.get("poetry").get("version")
            config = pyproject_tools.get("versioning").get("files")
            return version, config
    else:
        raise Exception("Unable to locate configuration file.")


def find_substring_index(strings, substring):
    return next(i for i, string in enumerate(strings) if substring in string)


def sync_version_in_different_files(version, config):
    if "version_variable" in config:
        for value in config.get("version_variable"):
            file_name = value.split(":")[0]
            variable_name = value.split(":")[1]

            file = Path(os.getcwd() + "/" + file_name)
            text = file.read_text().splitlines(keepends=True)
            line_index = find_substring_index(text, variable_name)
            text[line_index] = text[line_index].replace(
                re.search(f"{variable_name}.*$", text[line_index]).group(0),
                variable_name + " = " + f'"{version}"',
            )
            file.write_text("".join(text))


def versioning(level):
    subprocess.run(["poetry", "version", level])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--version-level",
        "-v",
        choices=[
            "patch",
            "minor",
            "major",
            "prepatch",
            "preminor",
            "premajor",
            "prerelease",
            "repack",
            "",
        ],
        type=str,
        required=True,
    )
    args = ap.parse_args()

    if args.version_level:
        if args.version_level == "repack":
            versioning("")
        else:
            versioning(args.version_level)
        version, config = load_config()
        sync_version_in_different_files(version, config)
    else:
        versioning(args.version_level)
