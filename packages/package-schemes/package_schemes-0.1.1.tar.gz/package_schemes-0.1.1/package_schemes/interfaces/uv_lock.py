from pathlib import Path
from typing import Optional

import toml

from package_schemes.interfaces.base import BaseLock
from package_schemes.interfaces.packages import PackageMeta
from package_schemes.schemes.uv_lock import UvLockV1Scheme


class UvLockV1(BaseLock):
    def __init__(self, file: Path) -> None:
        super().__init__(file)
        data = toml.loads(file.read_text())
        self.data = UvLockV1Scheme.model_validate(data)

    def get_package_meta(self, name: str) -> Optional[PackageMeta]:
        for package in self.data.packages:
            if package.name == name:
                return PackageMeta(
                    package.name,
                    None,
                    package.version,
                    [i.name for i in package.dependencies],
                )
        return None
