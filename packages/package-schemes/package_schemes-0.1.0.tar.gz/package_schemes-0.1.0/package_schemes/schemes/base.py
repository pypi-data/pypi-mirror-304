from typing import Any

import toml
from pydantic import BaseModel


class TomlBaseModel(BaseModel):
    @classmethod
    def model_validate_toml(cls, toml_data: str, *args: Any, **kwargs: Any):
        data = toml.loads(toml_data)
        return cls.model_validate(data, *args, **kwargs)
