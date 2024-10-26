from pathlib import Path

import toml
from package_api.pyproject.base import BasePyproject

from uv_audit.package_api.schemes import PyProjectScheme


class PoetryPyproject(BasePyproject):
    def __init__(self, file: Path) -> None:
        super().__init__(file)
        data = toml.loads(file.read_text())
        self.data = PyProjectScheme.model_validate(data)
