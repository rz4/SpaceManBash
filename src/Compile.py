import sys
from cx_Freeze import setup, Executable

addtional_mods = ['numpy.core._methods', 'numpy.lib.format', 'GameFrames']

setup(
    name = "SpaceManBash",
    version = "1.0",
    description = "2-D Platformer written in Python Pygame",
    options = {'build_exe': {'includes': addtional_mods}},
    executables = [Executable("SpaceManBash.py", base = None)])
