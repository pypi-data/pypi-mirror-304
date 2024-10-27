from typing import Any, Optional

from pydantic import BaseModel, Field, HttpUrl

from package_schemes.schemes.base import TomlBaseModel


class PyProjectScheme(TomlBaseModel):
    class Project(BaseModel):
        class ProjectLicense(BaseModel):
            file: Optional[str] = None
            text: Optional[str] = None

        class ProjectUrls(BaseModel):
            documentation: Optional[HttpUrl] = None
            repository: Optional[HttpUrl] = None

        name: str
        version: Optional[str] = None
        description: Optional[str] = None
        authors: Optional[list[dict[str, str]]] = Field(default_factory=list)
        maintainers: Optional[list[dict[str, str]]] = Field(default_factory=list)
        license: Optional[ProjectLicense] = None
        keywords: list[str] = Field(default_factory=list)
        classifiers: list[str] = Field(default_factory=list)
        dependencies: list[str] = Field(default_factory=list)
        urls: Optional[ProjectUrls] = None
        optional_dependencies: dict[str, list[str]] = Field(
            alias='optional-dependencies',
            default_factory=dict,
        )
        dependency_groups: dict[str, list[str]] = Field(
            alias='dependency-groups',
            default_factory=dict,
        )

    project: Project
