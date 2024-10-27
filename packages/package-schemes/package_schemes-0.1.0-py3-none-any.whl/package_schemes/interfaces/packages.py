from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass()
class PackageMeta(object):
    name: str
    version_pattern: str | None
    version: str | None
    dependencies: list[str] = field(default_factory=list)

    @classmethod
    def merge(cls, meta_1: Optional[PackageMeta], meta_2: Optional[PackageMeta]):
        if meta_1 is None:
            return meta_2

        if meta_2 is None:
            return meta_1

        assert meta_1.name == meta_2.name
        name = meta_1.name

        version = None

        for i in [meta_1.version, meta_2.version]:
            if i is not None:
                version = i
                break

        assert version is not None

        version_pattern = None
        for i in [meta_1.version_pattern, meta_2.version_pattern, meta_1.version, meta_2.version]:
            if i is not None:
                version_pattern = i
                break

        assert version_pattern is not None

        deps = meta_1.dependencies + meta_2.dependencies

        return cls(
            name,
            version_pattern,
            version,
            deps,
        )


@dataclass()
class Package(object):
    name: str
    version_pattern: str | None
    version: str
    dependencies: list[Package]

    extra: str | None = None
    is_dev: bool = False

    @classmethod
    def from_meta(cls, meta: PackageMeta, deps: list[Package]):
        assert meta.version is not None

        return cls(meta.name, meta.version_pattern, meta.version, deps)
