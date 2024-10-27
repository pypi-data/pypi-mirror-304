import abc
from pathlib import Path
from typing import Optional

from package_schemes.interfaces.packages import PackageMeta


class BasePyproject(abc.ABC):
    file: Path

    def __init__(self, file: Path) -> None:
        self.file = file

    @abc.abstractmethod
    def get_root_packages_names(self) -> list[str]:
        pass

    @abc.abstractmethod
    def get_package_meta(self, name: str) -> Optional[PackageMeta]:
        pass


class BaseLock(abc.ABC):
    file: Path

    def __init__(self, file: Path) -> None:
        self.file = file

    @abc.abstractmethod
    def get_package_meta(self, name: str) -> Optional[PackageMeta]:
        pass
