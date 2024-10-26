import importlib.util
from collections.abc import Generator
from pathlib import Path
from typing import Any

import ijson
from packaging.specifiers import SpecifierSet
from packaging.version import Version
from pydantic import BaseModel

from uv_audit.package_api.packages import Package

SAFETY_DB_DIR = Path(importlib.util.find_spec('safety_db').origin).parent  # type: ignore


class PackageVulnerability(BaseModel):
    advisory: str
    cve: str
    id: str
    more_info_path: str
    specs: list[str]
    v: str


class ScanManager(object):
    def __init__(self) -> None:
        self.insecure_path = SAFETY_DB_DIR / 'insecure.json'
        self.insecure_full_path = SAFETY_DB_DIR / 'insecure_full.json'

    def get_record_in_insecure(self, key: str) -> list[str] | None:
        with open(self.insecure_path, encoding='utf-8') as file:
            for package_name, value in ijson.kvitems(file, ''):
                if package_name == key:
                    return list(value)
        return None

    def get_record_in_insecure_full(self, key: str) -> list[dict[str, Any]] | None:
        with open(self.insecure_full_path, encoding='utf-8') as file:
            for package_name, value in ijson.kvitems(file, ''):
                if package_name == key:
                    return value
        return None

    def get_package_vulnerability(self, package: Package) -> Generator[PackageVulnerability, Any, Any]:
        specifier_versions = self.get_record_in_insecure(package.name)

        if specifier_versions is None:
            return

        target_version = Version(package.version)

        founded = False
        for specifier_version in specifier_versions:
            specifier = SpecifierSet(specifier_version)

            if target_version in specifier:
                founded = True
                break

        if not founded:
            return

        v1 = self.get_record_in_insecure_full(package.name)

        if v1 is None:
            return

        for vulnerability_spec in v1:
            for specifier_version in vulnerability_spec['specs']:
                specifier = SpecifierSet(specifier_version)

                if target_version in specifier:
                    yield PackageVulnerability.model_validate(vulnerability_spec)
