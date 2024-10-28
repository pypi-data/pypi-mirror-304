"""Linux paths"""

import os
import configparser

from .facade import BEPath, JEPath
from .utils import _get_latest_profile, _version_to_component

__all__ = ["java", "bedrock", "preview", "education", "get_runtime"]


class LinuxJEPath(JEPath):
    platform = "linux"

    def _get_launcher(self) -> str:
        return os.path.join(
            os.path.expanduser("~"), ".minecraft", "launcher", "minecraft-launcher"
        )

    def _get_executable(self) -> str:
        return os.path.join(os.path.expanduser("~"), ".minecraft", "versions")

    def _get_game(self) -> str:
        fp = os.path.join(
            os.path.expanduser("~"), ".minecraft", "launcher_profiles.json"
        )
        path = _get_latest_profile(fp)
        if path:
            return path
        # fallback
        return os.path.join(os.path.expanduser("~"), ".minecraft")


class LinuxBEPath(BEPath):
    platform = "linux"

    def _get_executable(self) -> str:
        return ""

    def _get_game(self) -> str:
        fp = os.path.join(
            os.path.expanduser("~"),
            ".var",
            "app",
            "io.mrarm.mcpelauncher",
            "data",
            "mcpelauncher",
            "profiles",
            "profiles.ini",
        )
        if os.path.exists(fp):
            try:
                config = configparser.ConfigParser()
                config.read(fp)
                if config.has_section("General"):
                    general = config["General"]
                    profile = config[general.get("selected")]
                    return os.path.join(profile.get("dataDir"), "games", "com.mojang")
            except KeyError:
                ...

        # Fallback
        return os.path.join(
            os.path.expanduser("~"),
            ".var",
            "app",
            "io.mrarm.mcpelauncher",
            "data",
            "mcpelauncher",
            "games",
            "com.mojang",
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
        ".minecraft",
        "runtime",
        component,
        "linux",
        component,
        "bin",
        "java",
    )
    if os.path.isfile(path):
        return path
    return "java"


java = LinuxJEPath()
bedrock = LinuxBEPath()
preview = None
education = None
