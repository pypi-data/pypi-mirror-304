```
    2024 @ Sett Sarverott <sett@sarverott.com> (https://sarverott.com)

      █▀▄ ▄▀█ █▀█ █▄▀ █▀█ █▀█ █ █▄░█ ▀█▀   framework of technomantic memory system
      █▄▀ █▀█ █▀▄ █░█ █▀▀ █▄█ █ █░▀█ ░█░   for mnemonic forrest placed in darkness

    published under terms of GNU_GPLv3 license                                  
```
# DarkPoint - implementation in Python 

>  2024 @ [Sett Sarverott](https://sarverott.github.io)

![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/sarverott/darkpoint) 
![GitHub last commit](https://img.shields.io/github/last-commit/sarverott/darkpoint?link=https%3A%2F%2Fgithub.com%2FSarverott%2Fdarkpoint%2Fgraphs%2Fcommit-activity) 
![GitHub License](https://img.shields.io/github/license/sarverott/darkpoint?link=https%3A%2F%2Fraw.githubusercontent.com%2FSarverott%2Fdarkpoint%2Frefs%2Fheads%2Fmaster%2FLICENSE)
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FSarverott%2Fdarkpoint%2Frefs%2Fheads%2Fmaster%2Fpyproject.toml) 
![PyPI - Downloads](https://img.shields.io/pypi/dm/darkpoint?label=PyPi%20downloads%20monthly&link=https%3A%2F%2Fpypi.org%2Fproject%2Fdarkpoint) 
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/darkpoint?label=version%20released%20on%20PyPi&link=https%3A%2F%2Fpypi.org%2Fproject%2Fdarkpoint) 
![Pepy Total Downloads](https://img.shields.io/pepy/dt/darkpoint?label=Total%package%20downloads&link=https%3A%2F%2Fwww.pepy.tech%2Fprojects%2Fdarkpoint) 
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/sarverott/darkpoint/total?label=Total%20downloads%20from%20Github&link=https%3A%2F%2Fgithub.com%2Fsarverott%2Fdarkpoint)


This Python framework aims to process information simply and universally. 
Idea of DarkPoint is based on my personal memorization structure and metaphorical explanation how it works. 

Final version will be included in __Mind Toolkit of Technomancer__ as __Thought Model System__ with definition as __Singular Principles__ that allows to create memory palace with startpoint in darkness.

---

### thought model system overview

This is my personal way of thinking, that as natural mechanism is my default non-verbal thought behaviour. It's automatic and acts as my lowest-level coding method of mindsets. After years in process of clearyfication through trial and error I learned to explain how I'm thinking and why perspective of mine can sometimes terrifyingly stand out from other people. I uses simplifying and metaphores to define in the readers' imagination basic core of things and fundamental rules how it works. This `README.md` document is in my opinion still not enought clear, but i hope that soon I finally figure out how to close full fundations of mechanic's ruleset in human words.

### singular principles

These are basic rules that are essential 

- **Points have hooks:** Each piece of information is represented as a point that has a hook.
- **On the end of hooks are next points:** The hooks lead to additional points, creating a chain of information.
- **Every point is information:** Each point represents a specific piece of information.
- **Informations are related by hooking:** The connections between points are established through hooks.
- **Hooks are one-directional:** The connections only go in one direction, leading from one point to another with evental resulting nature, not dimentional.
- **Points can be extended by templates:** Each point can have additional context or details added through templates.
- **Set starting point:** There is a designated starting point from which the connections begin.
- **For __The PALACE__ there is special starting point:** this is root placed in the middle of memories, every time after reset or starting, the point of focus lands here. For example my palace is: `dark void` and reset for me runs through simply thinking about `darkness`.
- **All templates to work properly have to be accessible from the starting point:** These are declared as points too so all relevant information have be reached from the starting point.

---

## installation
> Install official release by using `pip` python package manager 
```sh
pip install darkpoint
```

---

## Examples

All examples can be tested at once, by using `python ./examples/main.py`  
- [CODE OF ALL-IN-ONE EXAMPLE COLLECTION](https://github.com/sarverott/darkpoint/blob/master/examples/main.py)



#### including package
```python
# using points
from darkpoint.Point import Point
```

#### creating Point object
```python
#creating new mnemonic sanctuary
palace = Point("darkness")
```

#### quick hooking of new information
- [example 1](https://github.com/sarverott/darkpoint/blob/master/examples/_1_quick_hooking.py)
```python
palace["color"]="dark"
```



#### longer hooking path of new data
- [example 2](https://github.com/sarverott/darkpoint/blob/master/examples/_2_hooking_path.py)
- [example 7](https://github.com/sarverott/darkpoint/blob/master/examples/_7_absolute_path_traversal.py)
```python
palace["color"]["time"]="dark time is night"
palace["color"]["time"]["always"]="night is always in space as default constant daytime"
palace["color"]["time"]["always"]["sun"]="local star for humanity"
palace["color"]["time"]["always"]["sun"]["far"]="suns in further space from our sun are simply called stars"
palace["color"]["time"]["always"]["sun"]["far"]["images"]="points created by stars on sky are constelations"
```



#### to print just type
- [example 3](https://github.com/sarverott/darkpoint/blob/master/examples/_1_quick_hooking.py)
- [example 4](https://github.com/sarverott/darkpoint/blob/master/examples/_4_print_hooks.py)
```python
print(palace)
print(palace["color"])
```



#### hooking existing points
- [example 4](https://github.com/sarverott/darkpoint/blob/master/examples/_4_print_hooks.py)
- [example 5](https://github.com/sarverott/darkpoint/blob/master/examples/_5_for_loop_with_hooking_path.py)
- [example 6](https://github.com/sarverott/darkpoint/blob/master/examples/_6_hook_existing_points.py)
- [example 8](https://github.com/sarverott/darkpoint/blob/master/examples/_8_chaining.py)
```python
# some hooking
palace   *"time"   +palace["color"]["time"]
palace   *"space"   +Point("natural state of space is darkness and empty void")
# more hooking
palace["space"]   *"time"   +palace["color"]["time"]["always"]
palace["space"]   *"stars"   +palace["color"]["time"]["always"]["sun"]["far"]
```



#### context change
- [example 9](https://github.com/sarverott/darkpoint/blob/master/examples/_9_context_change.py)
- [example 10](https://github.com/sarverott/darkpoint/blob/master/examples/_10_multiple_context_change.py)
```python
# single
palace/'DARK_VOID'
# this and repeat with every hook until reaches another than old context
palace["space"]//'###_SPACE_CONTEXT_INVASION_###'
```

## Links
- Documentation: https://darkpoint.readthedocs.io
- GitHub repository: https://github.com/sarverott/darkpoint
- Project on PyPi: ~~https://pypi.org/project/darkpoint~~ _(Not yet available - pending project publication)_
- Docker image: _(Not yet available - until PyPi publication container developement suspended)_
- CHANGELOG: https://github.com/Sarverott/darkpoint/blob/master/docs/changelog.md

---

### Copyright (C) 2024   Sett Sarverott <sett@sarverott.com> (https://sarverott.com)


    DarkPoint - technomantic framework for mnemonic toolkit that is in accordance with singular principles of thought model system 
    Copyright (C) 2024   Sett Sarverott <sett@sarverott.com> (https://sarverott.com)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

Copy of License can be found in ["LICENSE"](./LICENSE) file.