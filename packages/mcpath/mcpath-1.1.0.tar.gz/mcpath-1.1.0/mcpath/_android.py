"""Android paths"""

import os
from .facade import BEPath

__all__ = ["java", "bedrock", "preview", "education", "get_runtime"]


class AndroidBEPath(BEPath):
    platform = "android"

    def _get_game(self) -> str:
        internal = os.path.join(
            "data", "user", "0", "com.mojang.minecraftpe", "games", "com.mojang"
        )
        external = os.path.join(
            "storage",
            "emulated",
            "0",
            "Android",
            "data",
            "com.mojang.minecraftpe",
            "files",
            "games",
            "com.mojang",
        )
        return internal if os.path.exists(internal) else external


def get_runtime(version: str) -> None:
    return None


java = None
bedrock = AndroidBEPath()
preview = None
education = None
