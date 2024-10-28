"""iOS paths"""

from .facade import BEPath

import file_system

__all__ = ["java", "bedrock", "preview", "education", "get_runtime"]


class iPhoneBEPath(BEPath):
    platform = "ios"

    def _get_game(self) -> str:
        path = file_system.pick_directory()
        if path.endswith("games/com.mojang"):
            return str(path)
        return ""


def get_runtime(version: str) -> None:
    return None


java = None
bedrock = iPhoneBEPath()
preview = None
education = None
