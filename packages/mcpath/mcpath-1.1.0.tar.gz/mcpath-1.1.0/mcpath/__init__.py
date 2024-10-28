import sys

__version__ = "1.1.0"

from .facade import MCPath, JEPath, BEPath, PREPath, EDUPath

if sys.platform == "win32":
    from ._windows import java, bedrock, preview, education, get_runtime
elif sys.platform == "darwin":
    from ._darwin import java, bedrock, preview, education, get_runtime
elif sys.platform in ["ios", "iPadOS"]:
    from ._ios import java, bedrock, preview, education, get_runtime
elif sys.platform == "linux" and hasattr(sys, "getandroidapilevel"):
    from ._android import java, bedrock, preview, education, get_runtime
elif sys.platform == "linux":
    from ._linux import java, bedrock, preview, education, get_runtime
else:
    from ._dummy import java, bedrock, preview, education, get_runtime
