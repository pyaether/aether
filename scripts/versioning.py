import re
from enum import StrEnum
from pathlib import Path

import click
import tomli
import tomli_w
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class VersionLevel(StrEnum):
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"
    ALPHA = "alpha"
    BETA = "beta"
    RC = "rc"


class SupportedBackend(StrEnum):
    POETRY = "poetry"
    UV = "uv"


def load_config():
    pyproject_path = Path.cwd() / "pyproject.toml"
    if pyproject_path.exists():
        with open(pyproject_path, "rb") as f:
            pyproject_data = tomli.load(f)
            config = pyproject_data.get("tool", {}).get("versioning", {}).get("files")

            backend = (
                pyproject_data.get("tool", {}).get("versioning", {}).get("backend")
            )
            if backend is None:
                raise RuntimeError(
                    "`pyproject.toml` file doesn't contain `tool.versioning.backend` property."
                )
            match SupportedBackend(backend):
                case SupportedBackend.POETRY:
                    version = (
                        pyproject_data.get("tool", {}).get("poetry", {}).get("version")
                    )
                case SupportedBackend.UV:
                    version = pyproject_data.get("project", {}).get("version")

            if version is None:
                raise RuntimeError(
                    "`pyproject.toml` file doesn't contain `version` property."
                )

            return version, config
    else:
        raise RuntimeError("Unable to locate `pyproject.toml` file.")


def save_config(version):
    pyproject_path = Path.cwd() / "pyproject.toml"
    if pyproject_path.exists():
        with open(pyproject_path, "wb") as f:
            pyproject_data = tomli.load(f)

            backend = pyproject_data["tool"]["versioning"]["backend"]
            match SupportedBackend(backend):
                case SupportedBackend.POETRY:
                    pyproject_data["tool"]["poetry"]["version"] = version
                case SupportedBackend.UV:
                    pyproject_data["project"]["version"] = version

            tomli_w.dump(pyproject_data, f)
    else:
        raise RuntimeError("Unable to locate `pyproject.toml` file.")


def parse_version(version) -> dict:
    VERSION_PATTERN = re.compile(
        r"^"
        r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)"
        r"(?:(?P<pre_type>a|b|rc)(?P<pre_num>\d+))?"
        r"(?:\.post(?P<post>\d+))?"
        r"(?:\.dev(?P<dev>\d+))?"
        r"$"
    )

    pattern_match = VERSION_PATTERN.match(version)
    if pattern_match:
        return pattern_match.groupdict()
    else:
        raise ValueError(
            f"Invalid version format {version}. Expected format: MAJOR.MINOR.PATCH[.preTYPE[.preNUM][.post][.dev]]"
        )


def find_substring_index(strings, substring):
    return next(i for i, string in enumerate(strings) if substring in string)


def sync_version_in_different_files(
    version, config, dry_run: bool
) -> list[dict[str, int | Path]]:
    files_synced = []
    if "version_variable" in config:
        for value in config.get("version_variable"):
            file_name = value.split(":")[0]
            variable_name = value.split(":")[1]

            file = Path.cwd() / file_name
            text = file.read_text().splitlines(keepends=True)
            line_index = find_substring_index(text, variable_name)
            text[line_index] = text[line_index].replace(
                re.search(f"{variable_name}.*$", text[line_index]).group(0),
                variable_name + " = " + f'"{version}"',
            )

            if not dry_run:
                file.write_text("".join(text))

            files_synced.append(
                {
                    "file_path": file.relative_to(Path.cwd()),
                    "line_number": line_index + 1,
                }
            )

    return files_synced


def versioning(level: VersionLevel, current_version: str, dry_run: bool) -> str:
    version_parts = parse_version(current_version)

    match level:
        case VersionLevel.MAJOR:
            new_version = f"{int(version_parts['major']) + 1}.0.0"
        case VersionLevel.MINOR:
            new_version = (
                f"{version_parts['major']}.{int(version_parts['minor']) + 1}.0"
            )
        case VersionLevel.PATCH:
            new_version = f"{version_parts['major']}.{version_parts['minor']}.{int(version_parts['patch']) + 1}"
        case VersionLevel.ALPHA | VersionLevel.BETA | VersionLevel.RC:
            pre_type_map = {
                VersionLevel.ALPHA: "a",
                VersionLevel.BETA: "b",
                VersionLevel.RC: "rc",
            }

            if version_parts["pre_type"] == pre_type_map[level]:
                pre_num = int(version_parts["pre_num"] or 0) + 1
            else:
                pre_num = 1

            new_version = f"{version_parts['major']}.{version_parts['minor']}.{version_parts['patch']}.{pre_type_map[level]}{pre_num}"

    if not dry_run:
        save_config(new_version)

    return new_version


def display_update_summary(
    console: Console,
    files_synced: list[dict[str, int | Path]],
):
    grid = Table.grid()
    grid.add_column(justify="center")

    for sync_infomation in files_synced:
        grid.add_row(
            f"Synced version updates in file [cyan]`{sync_infomation['file_path']}`[/cyan] at line [cyan]{sync_infomation['line_number']}[/cyan]"
        )

    console.print(
        Panel(grid, title="Version Update Summary", border_style="blue", padding=(1, 2))
    )


@click.command()
@click.argument(
    "level", type=click.Choice([vl.value for vl in VersionLevel], case_sensitive=False)
)
@click.option(
    "--show-summary",
    "-s",
    is_flag=True,
    help="Show what files changed",
)
@click.option(
    "--dry-run",
    "-d",
    is_flag=True,
    help="Show what would be done without making changes",
)
def main(level: str, show_summary: bool, dry_run: bool):
    console = Console()

    current_version, versioning_config = load_config()
    new_version = versioning(VersionLevel(level), current_version, dry_run)
    files_synced = sync_version_in_different_files(
        new_version, versioning_config, dry_run
    )

    if dry_run:
        console.print(
            f"[yellow]Dry Run[/yellow]: Bumped version: [bold]{current_version}[/bold] :arrow_right: [bold green]{new_version}[/bold green]"
        )
    else:
        console.print(
            f"Bumped version: [bold]{current_version}[/bold] :arrow_right: [bold green]{new_version}[/bold green]"
        )

    if show_summary:
        display_update_summary(console, files_synced)


if __name__ == "__main__":
    main()
