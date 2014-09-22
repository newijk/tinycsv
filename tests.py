# -*- coding: utf-8 -*-

"""Tests for TinyCsv"""

from __future__ import absolute_import, print_function, unicode_literals

import logging

from unittest import TestCase

import tinycsv

log = logging.getLogger(__name__)

# Some possible dialects for testing
dialects = [
    # separator # quote     # escape
    (',',       "'",        "\\"),
]


def csv_for_dialect(separator, quote, escape, newline):
    """Create test csv data for the specified dialect"""
    formatting_data = {'s': separator, 'q': quote, 'e': escape, 'n': newline}
    return "".join([
        # A basic line
        "{q}field1{q}{s}{q}field2{q}{s}{q}field3{q}{n}",

        # A line with separator characters in quoted fields
        # TODO: This should ofcourse not be included for unquoted csv
        "{q}{s}field1{q}{s}{q}fie{s}ld2{q}{s}{q}field{s}3{q}{n}"

        # A line with escaped quotes in the quoted fields
        # TODO: Not to be included in unquoted csv
        "{q}{e}{q}field1{q}{s}{q}fie{e}{q}ld2{q}{e}{q}field3{e}{q}{q}{n}",
    ]).format(**formatting_data)


class TestDialect(TestCase):

    def test_basic_read(self):
        print(csv_for_dialect(',', "'", '\\', '\n'))
        dialect = tinycsv.Dialect()
        self.assertEqual(
            dialect.parse_line('"field1","field2"'),
            ('field1', 'field2'),
        )

    def test_read_with_escaped_quote(self):
        dialect = tinycsv.Dialect()
        self.assertEqual(
            dialect.parse_line(r'"item\"1","item2"'),
            ('item"1', 'item2'),
        )

    def test_read_with_quoted_separator(self):
        dialect = tinycsv.Dialect()
        self.assertEqual(
            dialect.parse_line('",item0","item,1","item2,"'),
            (',item0', 'item,1', 'item2,')
        )


class TestTinyCsv(TestCase):
    def test_blank_lines_skipped(self):
        self.assertEqual(
            list(tinycsv.CsvReader('''"item1"\n\n"item2"''')),
            [('item1', ), ('item2',), ])

