from collections import UserDict
from pathlib import Path
from typing import Any

import rtoml

DIR_BASE = Path(__file__).parent.parent
DIR_ASSET = DIR_BASE / "assets"
DIR_IMG = DIR_ASSET / "images"
DIR_FONT = DIR_ASSET / "fonts"
DIR_MAP = DIR_ASSET / "maps"


class Config(UserDict):
    """配置文件"""

    def __init__(self, config_file: str) -> None:
        try:
            with open(config_file, "r", encoding="utf8") as f:
                self.config = rtoml.load(f)
        except IOError as e:
            print(e)

        super().__init__(self)

    def __getitem__(self, key: Any) -> Any:
        return self.config[key]
