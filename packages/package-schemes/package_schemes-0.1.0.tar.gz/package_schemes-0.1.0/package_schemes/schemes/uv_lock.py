from typing import Optional

from pydantic import BaseModel, Field, HttpUrl

from package_schemes.schemes.base import TomlBaseModel


class UvLockV1Scheme(TomlBaseModel):
    class ResolutionMarker(BaseModel):
        marker: str

    class Package(BaseModel):
        class Source(BaseModel):
            registry: Optional[HttpUrl] = None
            editable: Optional[str] = None

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
            specifier: Optional[str] = None

        name: str
        version: str
        source: Optional[Source]
        sdist: Optional[Sdist] = None
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
    requires_python: Optional[str] = None
    resolution_markers: list[ResolutionMarker] = Field(default_factory=list)
    packages: list[Package] = Field(alias='package', default_factory=list)
