#    This file is part of Bachstelze.
#    Copyright (C) 2024  Carine Dengler
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
:synopsis: RSS feed handling.
"""


# standard library imports
import os
import json

# third party imports
import bs4
import feedparser

# library specific imports
import config


def _import_rss_feeds():
    """Import RSS feeds from JSON file.

    :returns: RSS feeds
    :rtype: list
    """
    with config.RSS_FEEDS_PATH.open() as fp:
        return [item["location"] for item in json.load(fp)]


def parse_rss_feeds():
    """Parse RSS feeds.

    :returns: feed
    :rtype: feedparser.util.FeedParserDict
    """
    for location in _import_rss_feeds():
        yield feedparser.parse(location)


def pprint_feed(feed):
    """Pretty-print RSS feed.

    :param feedparser.util.FeedParserDict feed: RSS feed

    :returns: pretty-printed RSS feed
    :rtype: str
    """
    for entry in feed["entries"]:
        yield os.linesep.join(
            (
                entry["title"],
                bs4.BeautifulSoup(entry["summary"], "html.parser").text,
            )
        )
