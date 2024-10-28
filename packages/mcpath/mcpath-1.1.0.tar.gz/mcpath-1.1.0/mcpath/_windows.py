"""Windows (win32) paths"""

import os
from .facade import JEPath, BEPath, PREPath, EDUPath
from .utils import _get_latest_profile, _version_to_component

__all__ = ["java", "bedrock", "preview", "education", "get_runtime"]


class WinJEPath(JEPath):
    platform = "win32"

    def _get_launcher(self) -> str:
        path = os.path.join(
            "C:\\" + "XboxGames", "Minecraft Launcher", "Content", "Minecraft.exe"
        )
        return path

    def _get_executable(self) -> str:
        return os.path.expandvars("%APPDATA%\\.minecraft\\versions")

    def _get_game(self) -> str:
        fp = os.path.expandvars("%APPDATA%\\.minecraft\\launcher_profiles.json")
        path = _get_latest_profile(fp)
        if path:
            return path
        # fallback
        return os.path.expandvars("%APPDATA%\\.minecraft")


class WinBEPath(BEPath):
    platform = "win32"

    def _get_game(self) -> str:
        return os.path.expandvars(
            "%LOCALAPPDATA%\\Packages\\Microsoft.MinecraftUWP_8wekyb3d8bbwe\\LocalState\\games\\com.mojang"
        )


class WinPREPath(PREPath):
    platform = "win32"

    def _get_game(self) -> str:
        return os.path.expandvars(
            "%LOCALAPPDATA%\\Packages\\Microsoft.MinecraftWindowsBeta_8wekyb3d8bbwe\\LocalState\\games\\com.mojang"
        )


class WinEDUPath(EDUPath):
    platform = "win32"

    def _get_game(self) -> str:
        return os.path.expandvars(
            "%LOCALAPPDATA%\\Packages\\Microsoft.MinecraftEducationEdition_8wekyb3d8bbwe\\LocalState\\games\\com.mojang"
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
    path = os.path.expandvars(
        os.path.join(
            "%localappdata%",
            "Packages",
            "Microsoft.4297127D64EC6_8wekyb3d8bbwe",
            "LocalCache",
            "Local",
            "runtime",
            component,
            "windows-x64",
            component,
            "bin",
            "java.exe",
        )
    )
    if os.path.isfile(path):
        return path
    return "java"


java = WinJEPath()
bedrock = WinBEPath()
preview = WinPREPath()
education = WinEDUPath()
