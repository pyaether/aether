import shutil
import warnings
from pathlib import Path

import click


def create_dir_if_not_exists(directory: Path, debug: bool = False) -> None:
    if not directory.exists():
        if debug:
            click.echo(f"Creating directory: {directory}")
        directory.mkdir(parents=True)


def copy_dir(src: Path, dest: Path, directory_name: str, debug: bool = False) -> None:
    if src and src.exists():
        if debug:
            click.echo(f"Copying {directory_name} from {src} to {dest}")
        shutil.copytree(src, dest, dirs_exist_ok=True)
    else:
        warnings.warn(
            f"Project doesn't have a '{src}' directory.",
            UserWarning,
            stacklevel=1,
        )
