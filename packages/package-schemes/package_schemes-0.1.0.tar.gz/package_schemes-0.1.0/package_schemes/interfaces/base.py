from pathlib import Path
from typing import Optional

from package_schemes.interfaces.packages import PackageMeta


class BasePyproject(object):
    file: Path

    def __init__(self, file: Path) -> None:
        self.file = file

    def get_root_packages_names(self) -> list[str]: ...  # type: ignore

    def get_package_meta(self, name: str) -> Optional[PackageMeta]: ...  # type: ignore


class BaseLock(object):
    file: Path

    def __init__(self, file: Path) -> None:
        self.file = file

    def get_version(self): ...

    def get_package_meta(self, name: str) -> Optional[PackageMeta]: ...
