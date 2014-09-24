# -*- coding: utf-8 -*-

"""Tests for TinyCsv"""

from __future__ import absolute_import, print_function, unicode_literals

import logging

from unittest import TestCase

import tinycsv

log = logging.getLogger(__name__)

# Some possible dialects for testing
dialect_configurations = [
    # separator # quote     # escape    # newline
    (',',       "'",        "\\",       "\n"), # 0
    (',',       '"',        "\\",       "\n"), # 1
    (',',       "",         "\\",       "\n"), # 2
    ('\t',      "'",        "\\",       "\n"), # 3
]


def tests_for_dialect(separator, quote, escape, newline):
    """Create test csv data for the specified dialect. This specifies a series
    of csv lines and expected results.
    """
    formatting_data = {'s': separator, 'q': quote, 'e': escape, 'n': newline}

    test_templates = []

    # A basic line
    test_templates += [{
        'test': "{q}field1{q}{s}{q}field2{q}{s}{q}field3{q}{n}",
        'expect': ["field1", "field2", "field3"],
    }, ]

    if quote:  # These tests only make sense when csv format is quoted
        test_templates += [{
            # Test separator characters in quoted fields
            'test': "{q}{s}field1{q}{s}{q}fie{s}ld2{q}{s}{q}field3{s}{q}{n}",
            'expect': ("{s}field1", "fie{s}ld2", "field3{s}"),
        }]

    if escape and quote:  # Test escaped quotes in the fields
        test_templates += [{
            'test': "{q}{e}{q}field1{q}{s}"
                    "{q}fie{e}{q}ld2{q}{s}"
                    "{q}field3{e}{q}{q}{n}",
            'expect': ("{q}field1", "fie{q}ld2", "field3{q}"),
        }]

    if not quote:  # Test escaped separators in the fields
        test_templates += [{
            'test': "{q}{e}{s}field1{q}{s}"
                    "{q}fie{e}{s}ld2{q}{s}"
                    "{q}field3{e}{s}{q}{n}",
            'expect': ("{q}field1", "fie{q}ld2", "field3{q}"),
        }]

    tests = []
    for test_template in test_templates:
        tests += [{
            'test': test_template['test'].format(**formatting_data),
            'expect': tuple([v.format(**formatting_data)
                       for v in test_template['expect']])
        }]
    return tests


# Generate a test for each dialect listed.
_test_template = '''
class TestDialect{ix}(TestCase):
    def test_dialects(self):
        dialect_configuration = dialect_configurations[{ix}]
        dialect = tinycsv.Dialect(*dialect_configuration)
        tests = tests_for_dialect(*dialect_configuration)
        for test in tests:
            result = dialect.parse_line(test['test'])
            self.assertEqual(result, test['expect'])
'''

for ix, dialects_configuration in enumerate(dialect_configurations):
    exec(_test_template.format(ix=ix), globals(), locals())


class TestTinyCsv(TestCase):
    def test_blank_lines_skipped(self):
        self.assertEqual(
            list(tinycsv.CsvReader('''"item1"\n\n"item2"''')),
            [('item1', ), ('item2',), ])

