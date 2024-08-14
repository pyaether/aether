from pathlib import Path

import click
from bs4 import BeautifulSoup
from pytempl import render

import pytempl_cli

from .loader import load_build_function_instance, load_configs
from .utils import copy_dir, create_dir_if_not_exists


@click.command()
@click.option("--debug", is_flag=True, help="Enable debug mode to echo steps.")
def build(debug: bool) -> None:
    pytempl_config = load_configs()

    create_dir_if_not_exists(pytempl_config.build_output_dir, debug)

    build_static_dir = pytempl_config.build_output_dir / "static"
    create_dir_if_not_exists(build_static_dir, debug)

    build_static_css_dir = build_static_dir / "css"
    create_dir_if_not_exists(build_static_css_dir, debug)

    build_static_js_dir = build_static_dir / "js"
    create_dir_if_not_exists(build_static_js_dir, debug)

    build_static_assets_dir = build_static_dir / "assets"
    create_dir_if_not_exists(build_static_assets_dir, debug)

    copy_dir(pytempl_config.styles_dir, build_static_css_dir, "styles", debug)
    copy_dir(pytempl_config.js_scripts_dir, build_static_js_dir, "js_scripts", debug)
    copy_dir(pytempl_config.assets_dir, build_static_assets_dir, "assets", debug)
    copy_dir(
        pytempl_config.public_dir, pytempl_config.build_output_dir, "public", debug
    )

    if debug:
        click.echo("Loading build function instance...")
    instance = load_build_function_instance(
        pytempl_config.file_target, pytempl_config.function_target
    )

    if debug:
        click.echo("Rendering HTML...")
    rendered_html = render(instance())
    soup = BeautifulSoup(rendered_html, "lxml")

    def update_paths(tag_name: str, attribute: str) -> None:
        for tag in soup.find_all(tag_name):
            if attribute in tag.attrs:
                if not tag[attribute].startswith(("http://", "https://", "/")):
                    old_path = Path(tag[attribute])
                    if Path("styles") in old_path.parents:
                        new_path = build_static_css_dir / old_path.relative_to("styles")
                    elif Path("js_scripts") in old_path.parents:
                        new_path = build_static_js_dir / old_path.relative_to(
                            "js_scripts"
                        )
                    elif Path("assets") in old_path.parents:
                        new_path = build_static_assets_dir / old_path.relative_to(
                            "assets"
                        )
                    elif Path("public") in old_path.parents:
                        new_path = (
                            pytempl_config.build_output_dir
                            / old_path.relative_to("public")
                        )
                    else:
                        new_path = pytempl_config.build_output_dir / old_path.name

                    new_path = new_path.relative_to(pytempl_config.build_output_dir)

                    if debug:
                        click.echo(f"Updating {attribute}: {old_path} -> /{new_path}")
                    tag[attribute] = f"/{new_path}"

    if debug:
        click.echo("Updating paths in HTML...")
    # Update link, img, and script tags
    for tag, attr in [("link", "href"), ("img", "src"), ("script", "src")]:
        update_paths(tag, attr)

    if debug:
        click.echo("Writing final HTML to file...")
    with open(
        pytempl_config.build_output_dir / "index.html", "w", encoding="utf-8"
    ) as file:
        file.write(soup.decode(formatter="html5"))

    click.echo("Built successfully")


@click.command()
def run() -> None:
    click.echo("Running Application")


@click.command()
def version() -> None:
    click.echo(f"Pytempl CLI version {pytempl_cli.__version__}")
