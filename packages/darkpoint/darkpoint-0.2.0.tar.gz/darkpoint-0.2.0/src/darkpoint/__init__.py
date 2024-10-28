"""DarkPoint: technomantic memories framework for mnemonic forrests in darkness"""

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

FLAG = True


__all__ = ["point_declaration"]

if __name__ == "__main__":

    if FLAG:
        print(
            "\n\n\t \33[7m                   ",
            "                 \33[0m",
            "\n\33[0m\t \33[7m █▀▄ ▄▀█ █▀█ █▄▀ █▀█ █▀█ █ █▄░█ ▀█▀ \33[0m",
            "\n\t \33[7m █▄▀ █▀█ █▀▄ █░█ █▀▀ █▄█ █ █░▀█ ░█░ \33[0m",
            "\n\t \33[7m                                    \33[0m\n",
            "\n\tDarkPoint   ",
            "Copyright (C) 2024  Sett Sarverott ",
            "<sett@sarverott.com> (https://sarverott.com)",
            "\n\tThis program comes with ABSOLUTELY NO WARRANTY;",
            ' for details read file "LICENSE".',
            "\n\tThis is free software, and you are welcome to redistribute it",
            "\n\tunder certain conditions of license GNU GPL v3.\n\n",
        )
        FLAG = False

    print("darkpoint lounch")
else:
    print("darkpoint import")
