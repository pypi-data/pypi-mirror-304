"""
# AutoRunCmd

**autoruncmd** is a Python module that acts like a Makefile for Python projects. 
It allows you to define and execute a set of scripts easily using a configuration file. 
This tool helps in organizing and automating common project commands.

## Features
- **Configuration Management**: Store and organize scripts in a configuration file.
- **Easy Initialization**: Quickly create a default configuration file.
- **Add Scripts**: Append new commands to your configuration.
- **Search**: Find specific commands within the configuration.
- **Execute Scripts**: Run entire sections or individual commands by referencing their headers.

"""
from .run import runScript
from .c_init import createConfig
from .add import addtoScript
from .find import findLine
from .main import cli
from .v_n import __version__, __title__

__all__ = ["runScript", "createConfig", "addtoScript", "findLine", "cli",
    "__version__","__title__"]