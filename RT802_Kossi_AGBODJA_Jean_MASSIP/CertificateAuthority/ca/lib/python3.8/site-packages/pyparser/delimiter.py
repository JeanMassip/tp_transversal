# vi:et:ts=4 sw=4 sts=4

"""
This module contains the DelimiterParser
"""

import abc

from pyparser import Parser


class DelimiterParser(Parser):
    """
    The DelimiterParser will call process_line for each line with the results
    for splitting the line.

    This is useful for comma, tab, or any other separated input.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, delimiter=None, max_splits=-1, strip=False,
                 ignore_blanks=False):
        super(DelimiterParser, self).__init__(
            strip=strip,
            ignore_blanks=ignore_blanks
        )

        self.delimiter = delimiter
        self.max_splits = max_splits

    def process(self, line):
        parts = line.split(self.delimiter, self.max_splits)

        self.process_line(*parts)

    @abc.abstractmethod
    def process_line(self, *splits):
        """
        Called for each line with splits being the result of the split
        """

