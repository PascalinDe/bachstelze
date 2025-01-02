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
# third party imports
import tinydb
import feedparser

# library specific imports
import bachstelze.config


def insert_rss_feed(db, feed):
    """Insert RSS feed entries.

    :param tinydb.database.TinyDB db: connection to TinyDB database
    :param feedparser.util.FeedParserDict feed: RSS feed
    """
    entries = feed.pop("entries")
    for entry in entries:
        doc_id = hash(entry.pop("id"))
        entry["feed"] = feed
        db.upsert(tinydb.table.Document(entry, doc_id=doc_id))


def get_rss_feed(db, location):
    """Get RSS feed entries.

    :param tinydb.database.TinyDB db: connection to TinyDB database
    :param str location: RSS feed URL

    :returns: RSS feed entries
    :rtype: list
    """
    entries = db.search(tinydb.Query().feed.location == location)
    if not entries:
        return []
    for entry in entries:
        feed = entry.pop("feed", None)
    feed["entries"] = entries
    return feedparser.util.FeedParserDict(feed)


def import_rss_feeds():
    """Import RSS feed locations from file.

    :returns: RSS feed locations
    :rtype: list
    """
    with bachstelze.config.RSS_FEEDS_PATH.open() as fp:
        return [line.strip() for line in fp.readlines()]


def parse_rss_feed(location):
    """Parse RSS feed.

    :param str location: RSS feed location

    :returns: feed with additional 'location' field
    :rtype: feedparser.util.FeedParserDict
    """
    feed = feedparser.parse(location)
    feed["location"] = location
    return feed
