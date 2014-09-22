# -*- coding: utf-8 -*-

"""A Tiny CSV reader that covers most use cases. Aims to be easy to use,
pure python and usable for most csv files in use today.
"""

from __future__ import absolute_import, print_function, unicode_literals

import logging

from io import StringIO

log = logging.getLogger(__name__)


class LineReader(object):
    def __init__(self, file_obj):
        self.file_obj = file_obj

    def __iter__(self):
        """TODO: Add fancy stuff later,
        like raising exceptions on suspicious stuff.
        """
        return iter(self.file_obj)


class Dialect(object):
    """A CSV dialect, this one also serves as the default. How Pythonic..."""
    quote = '"'
    separator = ","
    escape_char = '\\'

    def parse_line(self, line, line_number=None):
        log.debug("Parsing line: '%s'", line)

        fields = ()
        escaped = False
        in_quote = False
        buffer = []

        if not line.endswith('\n'):
            line = "{}\n".format(line)

        for ix, c in enumerate(line):
            # Quoting
            if c == self.quote and not escaped:
                in_quote = not in_quote

            # Escaping
            elif c == self.escape_char:
                escaped = True if not escaped else False
                continue # prevent escaped from being unset at end of loop

            # Field separation or EOL
            elif c in [self.separator, '\n'] and not in_quote:
                # Field done, push the current buffer onto fields
                fields = fields + (''.join(buffer), )
                buffer = []

            # Optional ignored whitespace
            elif not c.strip() and not in_quote:
                pass

            # An actual character
            else:
                if not in_quote:
                    raise Exception(
                        "Non whitespace or separator found outside quote "
                        "(line={}, col={}, char='{}' (ord={}))".format(
                            line_number or 'unknown', ix, c, ord(c)))
                buffer += [c, ]

            escaped = False

        return fields


class CsvReader(object):
    """Read csv files"""
    chunk_size = 1024
    skip_blank_lines = True

    def __init__(self, file_obj, dialect=None):
        if isinstance(file_obj, str):
            file_obj = StringIO(file_obj)

        self.dialect = dialect if dialect else Dialect()
        self.line_reader = LineReader(file_obj)

    def __iter__(self):
        for line_number, line in enumerate(self.line_reader):
            if self.skip_blank_lines and not line.strip():
                pass  # Empty line
            else:
                yield self.dialect.parse_line(line, line_number=line_number)






