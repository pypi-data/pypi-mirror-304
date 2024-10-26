from pathlib import Path

import toml

from uv_audit.package_api.locks.base import BaseLock
from uv_audit.package_api.packages import PackageMeta
from uv_audit.package_api.schemes import UvLockV1Scheme


class UvLockV1(BaseLock):
    def __init__(self, file: Path) -> None:
        super().__init__(file)
        data = toml.loads(file.read_text())
        self.data = UvLockV1Scheme.model_validate(data)

    def get_package_meta(self, name: str) -> PackageMeta | None:
        for package in self.data.packages:
            if package.name == name:
                return PackageMeta(
                    package.name,
                    None,
                    package.version,
                    [i.name for i in package.dependencies],
                )
        return None
