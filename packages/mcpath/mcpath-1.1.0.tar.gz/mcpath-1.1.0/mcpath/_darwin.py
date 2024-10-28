"""Darwin (MacOS) paths"""

import os
from .facade import JEPath
from .utils import _get_latest_profile, _version_to_component

__all__ = ["java", "bedrock", "preview", "education", "get_runtime"]


class DarwinJEPath(JEPath):
    platform = "darwin"

    def _get_launcher(self) -> str:
        return os.path.join(
            os.path.expanduser("~"),
            "Library",
            "Application Support",
            "minecraft",
            "launcher",
            "minecraft-launcher",
        )

    def _get_executable(self) -> str:
        return os.path.join(
            os.path.expanduser("~"),
            "Library",
            "Application Support",
            "minecraft",
            "versions",
        )

    def _get_game(self) -> str:
        fp = os.path.join(
            os.path.expanduser("~"),
            "Library",
            "Application Support",
            "minecraft",
            "launcher_profiles.json",
        )
        path = _get_latest_profile(fp)
        if path:
            return path
        # fallback
        return os.path.join(
            os.path.expanduser("~"), "Library", "Application Support", "minecraft"
        )


def get_runtime(version: str) -> str:
    """
    Get the full path to the java runtime environment.

    :param version: The version of Minecraft.
    :type version: str
    :return: The java runtime path.
    :rtype: str
    """
    component, major_version = _version_to_component(version)
    if component is None:
        return "java"
    path = os.path.join(
        os.path.expanduser("~"),
        "Library",
        "Application Support",
        "minecraft",
        "runtime",
        component,
        "mac-os",
        component,
        "jre.bundle",
        "Contents",
        "Home",
        "bin",
        "java",
    )
    if os.path.isfile(path):
        return path
    return "java"


java = DarwinJEPath()
bedrock = None
preview = None
education = None
