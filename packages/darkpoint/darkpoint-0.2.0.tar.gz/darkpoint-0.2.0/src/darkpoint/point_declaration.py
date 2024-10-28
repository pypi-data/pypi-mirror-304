"""DarkPoint's point class declaration file"""

# DarkPoint: technomantic memories framework for mnemonic forrests in darkness
# Copyright (C) 2024   Sett Sarverott <sett@sarverott.com> (https://sarverott.com)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


# from . import helpers


class Point:
    """DarkPoint's point class"""

    ROOT = None

    def __init__(self, data, context="dark void"):
        if Point.ROOT is None:
            Point.ROOT = self
        self.data = data
        self.context = context
        self.hooks = {}
        self.hook_name_buffer = context

    def __str__(self):
        return self.data

    def __repr__(self):
        return self.__str__()

    ##def __repr__(self):
    ##return f"<\"{helpers.soft_string(self.data)}\"-{self.context};{}

    def __getitem__(self, key=None):
        if key is None:
            key = self.context
        return self.hooks[key]

    def __setitem__(self, key=None, data=None):
        if key is None:
            key = self.context
        if data is None:
            data = f"{Point.ROOT}"
        self.hooks[key] = Point(data, self.context)

    def __mul__(self, hook_name):
        if isinstance(hook_name, Point):
            self.hook_name_buffer = str(hook_name)  # setting hook name
        elif isinstance(hook_name, str):
            self.hook_name_buffer = hook_name  # setting hook name
        else:
            raise ValueError("non-Point adding is forbidden!")

        return self

    def __add__(self, point_to_hook):
        if not isinstance(point_to_hook, Point):
            raise ValueError("non-Point adding is forbidden!")

        self.hooks[self.hook_name_buffer] = point_to_hook  # setting point on hook
        self.hook_name_buffer = self.context  # context as default hook_name_buffer
        return point_to_hook  # Return hooked point for chaining

    def __iter__(self):
        return iter(self.hooks.items())

    def __truediv__(self, new_context):
        self.context = new_context  # Change current context
        return self  # Return self for chaining

    def change_context_recursively(self, new_context, old_context):
        """multiple hooked points can have changed context value with that"""
        # print(f"### POINT // ###")
        # print("\t", self)
        # print(f"\t?-{self.context} == {old_context}")
        if self.context == old_context:
            # tmp = None
            # print(f"\t\tchange context from {old_context} to {new_context}")
            for hook_name, hooked_point in self / new_context:
                if not hook_name == new_context and not hook_name == old_context:
                    # for future developement: this statement should have on/off
                    # switching with filter mechanics
                    hooked_point.change_context_recursively(new_context, old_context)
                # print(f"\t\t...asking point hooked on {hook_name}")
                # if hooked_point.change_context_recursively(new_context, old_context):
                # tmp = hook_name
            # return True
        # else:
        # print("\t\tno context change")
        # return False

    def __floordiv__(self, new_context):
        if self.context != new_context:  # infinite loop check
            self.change_context_recursively(new_context, self.context)  # submethod
        return self
