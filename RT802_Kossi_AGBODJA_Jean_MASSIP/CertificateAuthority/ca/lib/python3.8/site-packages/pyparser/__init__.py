# vi:et:ts=4 sw=4 sts=4

"""
This module contains the base level parser
"""

import abc


__version__ = '1.0'


class Parser(object):
    """
    Parser is an abstract base class that defines the behavior of a parser.

    Subclass it and implement the process method to parse the text.

    If strip is specified, the line has leading and trailing whitespace
    stripped before it is passed to process.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, strip=False, ignore_blanks=True):
        self.strip = strip
        self.ignore_blanks = ignore_blanks
        self.data = None
        self.parsing = False

    def start(self):
        """
        Override this method to have your parser know when processing has
        started.
        """

    def finish(self):
        """
        Override this method to have your parser know when processing has
        finished.
        """

    @abc.abstractmethod
    def process(self, line):
        """
        The process method will be called for each line of the data being
        parsed.  You must override it and it should drive the rest of your
        parsing.
        """

    def parse(self, iterable):
        """
        This method will do the main parsing.  It will iterate each item in
        iterable calling process on it.

        It returns the value of self.data when processing has completed.
        """

        self.parsing = True

        self.start()

        for line in iterable:
            if self.strip:
                line = line.strip()

                if self.ignore_blanks and line == '':
                    continue
            else:  # remove newlines
                line = line.rstrip('\r\n')

                if self.ignore_blanks and line.strip() == '':
                    continue

            self.process(line)

        self.finish()

        self.parsing = False

        return self.data

    def reset(self):
        """
        This method will reset the data of the object so that you can parse
        another file.

        If you need to reset more, just override and make sure you chain up to
        this method.
        """

        self.data = None
        self.parsing = False

