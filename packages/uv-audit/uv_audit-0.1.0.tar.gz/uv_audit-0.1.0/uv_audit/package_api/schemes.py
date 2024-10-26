from pydantic import BaseModel, Field, HttpUrl


class PyProjectScheme(BaseModel):
    class Project(BaseModel):
        class ProjectLicense(BaseModel):
            file: str | None = None
            text: str | None = None

        class ProjectUrls(BaseModel):
            documentation: HttpUrl | None = None
            repository: HttpUrl | None = None

        name: str
        version: str | None = None
        description: str | None = None
        authors: list[dict[str, str]] | None = Field(default_factory=list)
        maintainers: list[dict[str, str]] | None = Field(default_factory=list)
        license: ProjectLicense | None = None
        keywords: list[str] = Field(default_factory=list)
        classifiers: list[str] = Field(default_factory=list)
        dependencies: list[str] = Field(default_factory=list)
        optional_dependencies: dict[str, list[str]] | None = Field(alias='optional-dependencies', default_factory=dict)
        urls: ProjectUrls | None = None

    project: Project


class UvLockV1Scheme(BaseModel):
    class ResolutionMarker(BaseModel):
        marker: str

    class Package(BaseModel):
        class Source(BaseModel):
            registry: HttpUrl | None = None
            editable: str | None = None

        class Wheel(BaseModel):
            url: HttpUrl
            hash: str
            size: int

        class Sdist(BaseModel):
            url: HttpUrl
            hash: str
            size: int

        class Dependency(BaseModel):
            name: str
            specifier: str | None = None

        name: str
        version: str
        source: Source | None
        sdist: Sdist | None = None
        wheels: list[Wheel] = Field(default_factory=list)
        dependencies: list[Dependency] = Field(default_factory=list)
        metadata_requires_dist: list[Dependency] = Field(default_factory=list)
        metadata_requires_dev: list[Dependency] = Field(default_factory=list)

        dev_dependencies: dict[str, list[dict[str, str]]] = Field(
            alias='dev-dependencies',
            default_factory=list,
        )
        optional_dependencies: dict[str, list[dict[str, str]]] = Field(
            alias='optional-dependencies',
            default_factory=dict,
        )

    version: int
    requires_python: str | None = None
    resolution_markers: list[ResolutionMarker] = Field(default_factory=list)
    packages: list[Package] = Field(alias='package', default_factory=list)
