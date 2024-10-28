# mcpath

![Tests](https://github.com/legopitstop/mcpath/actions/workflows/tests.yml/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/mcpath)](https://pypi.org/project/mcpath/)
[![Python](https://img.shields.io/pypi/pyversions/mcpath)](https://www.python.org/downloads//)
![Downloads](https://img.shields.io/pypi/dm/mcpath)
![Status](https://img.shields.io/pypi/status/mcpath)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Issues](https://img.shields.io/github/issues/legopitstop/mcpath)](https://github.com/legopitstop/mcpath/issues)

Get paths to Minecraft Java, Bedrock, Preview, and Education Edition folders.

## Supported Platforms

|                   | Java     | Bedrock  | Preview/Beta | Education | Runtime  |
| ----------------- | -------- | -------- | ------------ | --------- | -------- |
| **Android** _[1]_ | ❌       | ✅       | ❌           | ❌        | ❌       |
| **Darwin**        | ✅ _[3]_ | ❌       | ❌           | ❌        | ✅ _[3]_ |
| **iOS** _[2]_     | ❌       | ✅       | ❌           | ❌        | ❌       |
| **Linux**         | ✅       | ✅ _[4]_ | ❌           | ❌        | ✅       |
| **Windows**       | ✅       | ✅       | ✅           | ✅        | ✅       |

1. With [Pydroid 3](https://play.google.com/store/apps/details?id=ru.iiec.pydroid3&hl=en_US)
2. With [Pyto](https://apps.apple.com/us/app/pyto-ide/id1436650069)
3. Has not been tested.
4. With [mcpelauncher](https://mcpelauncher.readthedocs.io/en/latest/).

## Paths

| Argument Name              | Example                                                                                                                            |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| root                       | `C:\Users\USER\AppData\Roaming\.minecraft`                                                                                         |
| launcher                   | `C:\XboxGames\Minecraft Launcher\Content\Minecraft.exe`                                                                            |
| executable                 | `minecraft://`                                                                                                                     |
| worlds                     | `C:\Users\USER\AppData\Roaming\.minecraft\saves`                                                                                   |
| resource_packs             | `C:\Users\USER\AppData\Roaming\.minecraft\resourcepacks`                                                                           |
| behavior_packs             | `C:\Users\USER\AppData\Local\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalState\games\com.mojang\behavior_packs`             |
| development_resource_packs | `C:\Users\USER\AppData\Local\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalState\games\com.mojang\development_resource_packs` |
| development_behavior_packs | `C:\Users\USER\AppData\Local\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalState\games\com.mojang\development_behavior_packs` |
| screenshots                | `C:\Users\USER\AppData\Roaming\.minecraft\screenshots`                                                                             |

## Installation

Install the module with pip:

```bat
pip3 install mcpath
```

Update existing installation: `pip3 install mcpath --upgrade`

## Requirements

| Name                                             | Usage                                                |
| ------------------------------------------------ | ---------------------------------------------------- |
| [`requests`](https://pypi.org/project/requests/) | Get runtime component and version using mojang's API |

## Examples

```Python
from mcpath import java

print(java.worlds)
# C:\Users\USER\AppData\Roaming\.minecraft\saves
```

```Python
import mcpath

print(mcpath.get_runtime('1.21.3'))
# C:\Users\USER\AppData\Local\Packages\Microsoft.4297127D64EC6_8wekyb3d8bbwe\LocalCache\Local\runtime\java-runtime-delta\windows-x64\java-runtime-delta\bin\java.exe
```
