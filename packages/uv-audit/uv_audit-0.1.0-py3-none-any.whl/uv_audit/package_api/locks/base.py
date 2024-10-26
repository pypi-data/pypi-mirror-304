from pathlib import Path

from uv_audit.package_api.packages import PackageMeta


class BaseLock(object):
    file: Path

    def __init__(self, file: Path) -> None:
        self.file = file

    def get_version(self): ...

    def get_package_meta(self, name: str) -> PackageMeta | None: ...
