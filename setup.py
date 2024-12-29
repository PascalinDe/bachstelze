#    Bachstelze
#    Copyright (C) 2024  Carine Dengler
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


# standard library imports
# third party imports
import setuptools

# library specific imports


METADATA = {
    "name": "bachstelze",
    "version": "v0.1",
    "description": "Command-line RSS feed reader.",
    "author": "Carine Dengler",
    "author_email": "bachstelze@pascalin.de",
    "url": "https://github.com/PascalinDe/bachstelze",
    "classifiers": [
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.12",
    ],
}


setuptools.setup(
    **METADATA,
    packages=["bachstelze"],
    entry_points={
        "console_scripts": [f"{METADATA['name']}=bachstelze.__main__:main",],
    }
)