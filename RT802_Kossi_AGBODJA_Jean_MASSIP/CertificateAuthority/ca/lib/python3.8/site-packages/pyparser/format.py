# vi:et:ts=4 sw=4 sts=4

import parse

from pyparser import Parser


_ATTRIBUTE_NAME = '_pyparser_format_pattern'


class pattern(object):
    def __init__(self, pattern):
        self.pattern = pattern

    def __call__(self, func):
        setattr(func, _ATTRIBUTE_NAME, self.pattern)

        return func


class FormatParser(Parser):
    def __init__(self, strip=False, ignore_blanks=True):
        super(FormatParser, self).__init__(strip, ignore_blanks)

        self.patterns = {}

        for symbol_name in dir(self):
            symbol = getattr(self, symbol_name)
            pattern = getattr(symbol, _ATTRIBUTE_NAME, None)

            if pattern is None:
                continue

            compiled = parse.compile(pattern)

            self.patterns[compiled] = symbol

    def default(self, line):
        """
        This method will be called if no patterns match the line.
        """

    def process(self, line):
        for pattern, func in self.patterns.items():
            result = pattern.parse(line)

            if result is not None:
                func(result)

                return

        self.default(line)

