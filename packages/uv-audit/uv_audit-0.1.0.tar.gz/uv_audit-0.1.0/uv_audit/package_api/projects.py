from collections.abc import Generator

from uv_audit.package_api.locks.base import BaseLock
from uv_audit.package_api.packages import Package, PackageMeta
from uv_audit.package_api.pyproject.base import BasePyproject


class Project(object):
    pyproject: BasePyproject
    lock: BaseLock
    packages: dict[str, Package]

    def __init__(self, pyproject: BasePyproject, lock: BaseLock) -> None:
        self.pyproject = pyproject
        self.lock = lock
        self.packages = {}

    def get_root_packages(self) -> list[Package]:
        return [self.get_package(i) for i in self.pyproject.get_root_packages_names()]

    def get_packages(self) -> Generator[Package, None, None]:
        def get_children(parent: Package) -> Generator[Package, None, None]:
            yield parent
            for i in parent.dependencies:
                yield from get_children(i)

        for i in self.get_root_packages():
            yield from get_children(i)

    def get_package(self, name: str) -> Package:
        if name in self.packages:
            return self.packages[name]

        package_meta = PackageMeta.merge(self.pyproject.get_package_meta(name), self.lock.get_package_meta(name))

        deps = []

        for dep_package_name in package_meta.dependencies:
            deps.append(self.get_package(dep_package_name))

        self.packages[name] = Package.from_meta(package_meta, deps)

        return self.packages[name]
