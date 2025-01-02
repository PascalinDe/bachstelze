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
:synopsis: RSS feed handling test cases.
"""


# standard library imports
import copy

# third party imports
import tinydb
import tinydb.storages
import unittest
import unittest.mock
import feedparser

# library specific imports
import bachstelze.rss
import bachstelze.config

from tests import RSS_FEEDS_PATH


@unittest.mock.patch(
    "bachstelze.config",
    RSS_FEEDS_PATH=RSS_FEEDS_PATH,
)
class RSSTestCase(unittest.TestCase):
    """RSS feed handling test cases."""

    def test_import_rss_feeds(self, *args):
        """Test importing RSS feed locations from file.


        Trying: import RSS feed locations from file
        Expecting: list of RSS feed locations
        """
        with RSS_FEEDS_PATH.open() as fp:
            self.assertEqual(
                bachstelze.rss.import_rss_feeds(),
                [location.strip() for location in fp.readlines()],
            )

    def test_parse_rss_feeds(self, *args):
        """Test parsing RSS feeds.

        Trying: parse RSS feeds
        Expecting: list of FeedParserDict objects
        with additional 'location' field
        """
        locations = bachstelze.rss.import_rss_feeds()
        for location in locations:
            feed = bachstelze.rss.parse_rss_feed(location)
            self.assertIsInstance(feed, feedparser.util.FeedParserDict)
            self.assertIn(feed["location"], locations)

    def test_insert_rss_feed(self, *args):
        """Test inserting RSS feed entries.

        Trying: insert RSS feed entries
        Expecting: RSS feed entries (with an additional 'feed' entry
        and without 'id' field) have been inserted
        """
        db = tinydb.TinyDB(storage=tinydb.storages.MemoryStorage)
        location = bachstelze.rss.import_rss_feeds().pop()
        feed = bachstelze.rss.parse_rss_feed(location)
        actual = copy.deepcopy(feed)
        bachstelze.rss.insert_rss_feed(db, feed)
        documents = db.all()
        self.assertEqual(len(documents), len(actual["entries"]))
        entries = actual.pop("entries")
        for entry in entries:
            entry.pop("id", None)
        for document in documents:
            feed = document.pop("feed")
            self.assertEqual(feed, actual)
            self.assertIn(document, entries)
        db.close()

    def test_get_rss_feed(self, *args):
        """Test getting RSS feed entries.

        Trying: inserting and getting RSS feed entries
        Expecting: FeedParserDict object
        """
        db = tinydb.TinyDB(storage=tinydb.storages.MemoryStorage)
        location = bachstelze.rss.import_rss_feeds().pop()
        feed = bachstelze.rss.parse_rss_feed(location)
        actual = copy.deepcopy(feed)
        bachstelze.rss.insert_rss_feed(db, feed)
        feed = bachstelze.rss.get_rss_feed(db, location)
        for key_0, values_0 in actual.items():
            if key_0 != "entries":
                self.assertEqual(values_0, feed[key_0])
            else:
                for entry in values_0:
                    entry.pop("id", None)
                self.assertEqual(values_0, feed[key_0])
        db.close()

    def test_get_rss_feed_inexistent_location(self, *args):
        """Test getting RSS feed entries.

        Trying: getting inexistent RSS feed entries
        Expecting: empty list
        """
        db = tinydb.TinyDB(storage=tinydb.storages.MemoryStorage)
        self.assertEqual(
            bachstelze.rss.get_rss_feed(db, "https://www.example.com/"),
            []
        )
        db.close()
