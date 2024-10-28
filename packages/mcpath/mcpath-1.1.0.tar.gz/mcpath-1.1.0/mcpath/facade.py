import os

__all__ = ["MCPath", "JEPath", "BEPath", "PREPath", "EDUPath"]


class MCPath:
    @property
    def game(self) -> str:
        """
        Get the path to the main Minecraft folder.
        """
        return self._get_game()

    @property
    def launcher(self) -> str:
        """
        Get the path to the Minecraft launcher.
        """
        return self._get_launcher()

    @property
    def executable(self) -> str:
        """
        Get the path of the executable file.
        """
        return self._get_executable()

    @property
    def worlds(self) -> str:
        """
        Get the path of the directory holding world files.
        """
        return self._get_worlds()

    @property
    def resource_packs(self) -> str:
        """
        Get the path of the directory holding resource pack files.
        """
        return self._get_resource_packs()

    @property
    def behavior_packs(self) -> str:
        """
        Get the path of the directory holding behavior pack files.
        """
        return self._get_behavior_packs()

    @property
    def development_resource_packs(self) -> str:
        """
        Get the path of the directory holding development resource pack files.
        """
        return self._get_development_resource_packs()

    @property
    def development_behavior_packs(self) -> str:
        """
        Get the path of the directory holding development behavior pack files.
        """
        return self._get_development_behavior_packs()

    @property
    def screenshots(self) -> str:
        """
        Get the path of the directory holding screenshot files.
        """
        return self._get_screenshots()

    # private

    def _get_launcher(self) -> str:
        raise NotImplementedError()

    def _get_game(self) -> str:
        raise NotImplementedError()

    def _get_executable(self) -> str:
        raise NotImplementedError()

    def _get_worlds(self) -> str:
        raise NotImplementedError()

    def _get_resource_packs(self) -> str:
        raise NotImplementedError()

    def _get_behavior_packs(self) -> str:
        raise NotImplementedError()

    def _get_development_resource_packs(self) -> str:
        raise NotImplementedError()

    def _get_development_behavior_packs(self) -> str:
        raise NotImplementedError()

    def _get_screenshots(self) -> str:
        raise NotImplementedError()


class JEPath(MCPath):
    edition = "java"

    def _get_worlds(self) -> str:
        return os.path.join(self._get_game(), "saves")

    def _get_resource_packs(self) -> str:
        return os.path.join(self._get_game(), "resourcepacks")

    def _get_behavior_packs(self) -> str:
        return ""

    def _get_development_resource_packs(self) -> str:
        return ""

    def _get_development_behavior_packs(self) -> str:
        return ""

    def _get_screenshots(self) -> str:
        return os.path.join(self._get_game(), "screenshots")


class BEPath(MCPath):
    edition = "bedrock"

    def _get_executable(self) -> str:
        return "minecraft://"

    def _get_worlds(self) -> str:
        return os.path.join(self._get_game(), "minecraftWorlds")

    def _get_resource_packs(self) -> str:
        return os.path.join(self._get_game(), "resource_packs")

    def _get_behavior_packs(self) -> str:
        return os.path.join(self._get_game(), "behavior_packs")

    def _get_development_resource_packs(self) -> str:
        return os.path.join(self._get_game(), "development_resource_packs")

    def _get_development_behavior_packs(self) -> str:
        return os.path.join(self._get_game(), "development_behavior_packs")

    def _get_screenshots(self) -> str:
        return os.path.join(self._get_game(), "Screenshots")


class PREPath(BEPath):
    edition = "preview"

    def _get_executable(self) -> str:
        return "minecraft-preview://"


class EDUPath(BEPath):
    edition = "education"

    def _get_executable(self) -> str:
        return "minecraftEdu://"
