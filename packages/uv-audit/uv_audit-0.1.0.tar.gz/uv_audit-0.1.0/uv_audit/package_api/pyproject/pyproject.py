from pathlib import Path

import toml

from uv_audit.package_api.packages import PackageMeta
from uv_audit.package_api.pyproject.base import BasePyproject
from uv_audit.package_api.schemes import PyProjectScheme
from uv_audit.patterns import PACKAGE_AND_VERSION_PATTERN


class Pyproject(BasePyproject):
    def __init__(self, file: Path) -> None:
        super().__init__(file)
        data = toml.loads(file.read_text())
        self.data = PyProjectScheme.model_validate(data)

    def get_root_packages_names(self) -> list[str]:
        packages: list[str] = []
        for dep in self.data.project.dependencies:
            match = PACKAGE_AND_VERSION_PATTERN.match(dep)
            if match:
                packages.append(match.group('name'))

        return packages

    def get_package_meta(self, name: str) -> PackageMeta | None:
        for dep in self.data.project.dependencies:
            if not dep.startswith(name):
                continue

            match = PACKAGE_AND_VERSION_PATTERN.match(dep)

            if not match:
                continue

            return PackageMeta(
                match.group('name'),
                match.group('version'),
                None,
                [],
            )

        return None
