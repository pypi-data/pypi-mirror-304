from pathlib import Path

from uv_audit.package_api.packages import PackageMeta


class BasePyproject(object):
    file: Path

    def __init__(self, file: Path) -> None:
        self.file = file

    def get_root_packages_names(self) -> list[str]: ...  # type: ignore

    def get_package_meta(self, name: str) -> PackageMeta | None: ...  # type: ignore
