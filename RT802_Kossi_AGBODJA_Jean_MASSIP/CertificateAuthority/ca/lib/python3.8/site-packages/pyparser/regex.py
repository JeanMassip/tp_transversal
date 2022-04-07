# vi:et:ts=4 sw=4 sts=4

"""
This module contains the RegexParser and Pattern decorator
"""

import logging
import re

from pyparser import Parser


_ATTRIBUTE_NAME = '_pyparser_re_pattern'


class pattern(object):
    """
    This class is a decorator that'll attach a regular expression attribute
    to a function that the RegexParser class will use to call that function if
    the regular expression matches.
    """

    def __init__(self, regex):
        self.pattern = regex

    def __call__(self, func):
        setattr(func, _ATTRIBUTE_NAME, self.pattern)

        return func


class RegexParser(Parser):
    """
    RegexParser is an implemention of a Parser that uses the Pattern decorator
    to connect a regular expression to a method.  If the line that's being
    parsed matches the regular expression, then that method will be called and
    the parser will move on to the next line.

    If no regular expressions match the given line, the default method will be
    called.

    The kwargs argument will have the parser call your methods with the match
    object's groupdict as keyword args.

    The handle_errors argument if True, will catch and log any exceptions
    caused by the Pattern decorator instead of passing on the exception.

    Here is an example subclass without using keywords that will count how many
    lines contain the string 'foo'.

        class NoKWArgs(RegexParser):
            def __init__(self):
                RegexParser.__init__(self)

                self.data = 0

            @pattern('^$')
            def blank(self, match):
                pass # ignore blank lines

            @pattern('.+foo.+')
            def foo(self, match):
                self.data += 1

    Here is another example that will parse /proc/cpuinfo from a UNIX like
    system, using the kwargs argument and named groups:

        class CPUInfoParser(RegexParser):
            def __init__(self):
                RegexParser.__init__(self)

                self.data = {}
                self.processor = None

            @pattern('^(?P<attribute>.+)\\s+:\\s+(?P<value>.+)$')
            def attribute(self, match, attribute, value):
                if attribute == 'processor':
                    self.processor = {}
                    self.data[value] = self.processor
                else:
                    if self.processor is not None:
                        self.processor[attribute] = value
    """

    def __init__(self, strip=False, named_groups=False, handle_errors=True,
                 ignore_blanks=False):
        super(RegexParser, self).__init__(
            strip=strip,
            ignore_blanks=ignore_blanks
        )

        self.kwargs = named_groups
        self.regexes = {}

        for symbol_name in dir(self):
            symbol = getattr(self, symbol_name)
            regex = getattr(symbol, _ATTRIBUTE_NAME, None)

            if regex is None:
                continue

            try:
                self.regexes[re.compile(regex)] = symbol
            except Exception as exp:
                if handle_errors:
                    logging.exception(exp)
                else:
                    raise exp

    def default(self, line):
        """
        This method will be called if no regular expressions match line.
        """

        pass

    def process(self, line):
        for regex, func in self.regexes.items():
            match = regex.match(line)
            if match is not None:
                if self.kwargs:
                    func(match, **match.groupdict())
                else:
                    func(match)

                return

        self.default(line)

