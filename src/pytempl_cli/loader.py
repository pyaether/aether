import importlib
import importlib.util
import sys
from pathlib import Path
from typing import Any

import tomli
from pydantic import BaseModel, Field


class ImportFromStringError(Exception):
    pass


def load_build_function_instance(file_target: str, function_target: str) -> Any:
    working_dir = Path.cwd()
    working_file = Path(file_target)

    if not working_file.exists():
        raise FileNotFoundError(f"File '{file_target}' not found.")

    module_path = working_dir / file_target
    module_name = Path(file_target).stem

    sys.path.append(str(working_dir))

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    else:
        raise ImportFromStringError(
            f"Could not import module from path '{module_path}'"
        )

    try:
        instance = getattr(module, function_target)
    except AttributeError:
        message = f'Attribute "{function_target}" not found in module "{module_name}".'
        raise ImportFromStringError(message)

    return instance


class PytemplConfig(BaseModel):
    file_target: Path = Field(default=Path("main.py"))
    function_target: str = Field(default="main")
    assets_dir: Path = None
    public_dir: Path = None
    styles_dir: Path = None
    js_scripts_dir: Path = None
    build_output_dir: Path = Field(default=Path("build/"))
    run_host: str = Field(default="localhost")
    run_port: int = Field(default=8080)


def load_configs() -> PytemplConfig:
    pyproject_file = Path("pyproject.toml")
    if not pyproject_file.exists():
        raise FileNotFoundError("Unable to locate configuration file.")

    with open(pyproject_file, "rb") as file:
        pyproject_tools: dict = tomli.load(file).get("tool", {})
        config: dict = pyproject_tools.get("pytempl", {})
        output_dir = config.get("build", {}).get("output_dir", "build")
        host = config.get("run", {}).get("host")
        port = config.get("run", {}).get("port")

    pytempl_config = PytemplConfig(**config)

    if host:
        pytempl_config.run_host = host

    if port:
        pytempl_config.run_port = port

    if output_dir:
        pytempl_config.build_output_dir = Path(output_dir)

    return pytempl_config
