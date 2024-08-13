import click

from .cli import build, run, version


@click.group()
def main() -> None:
    pass


main.add_command(build, name="build")
main.add_command(run, name="run")
main.add_command(version, name="version")

if __name__ == "__main__":
    main()
