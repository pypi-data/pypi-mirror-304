from typing import Union, Tuple
import os
import datetime
import json
import requests


def _version_to_component(mcversion) -> Union[Tuple[str, int], Tuple[None, None]]:
    res = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
    if res.status_code != 200:
        return None, None
    manifest = res.json()
    for version in manifest["versions"]:
        if version["id"] == mcversion:
            res = requests.get(version["url"])
            if res.status_code != 200:
                return None, None
            package = res.json()
            return (
                package["javaVersion"]["component"],
                package["javaVersion"]["majorVersion"],
            )
    return None, None


def _get_latest_profile(fp) -> Union[str, None]:
    if os.path.exists(fp):
        with open(fp) as fd:
            profiles = json.load(fd)
        latest = None
        for profile in profiles.get("profiles", {}).values():
            timestamp = datetime.datetime.strptime(
                profile.get("lastUsed"), "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            if latest is None or timestamp > latest.get("timestamp"):
                profile["timestamp"] = timestamp
                latest = profile
        if latest and "gameDir" in latest:
            return str(latest["gameDir"])
    return None
