#    This file is part of Bachstelze.
#    Copyright (C) 2025  Carine Dengler
#
#    Bachstelze is free software: you can redistribute it and/or modify
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


"""
:synopsis: Test cases configuration management.
"""


# standard library imports
import pathlib

# third party imports
# library specific imports


_HOME_PATH = pathlib.Path("tests") / "data"
_SHARE_PATH = _HOME_PATH / ".local" / "share"
_CONFIG_PATH = _HOME_PATH / ".config" / "bachstelze"
DATABASE_PATH = _SHARE_PATH / "bachstelze.json"
RSS_FEEDS_PATH = _CONFIG_PATH / "rss_feeds.txt"
