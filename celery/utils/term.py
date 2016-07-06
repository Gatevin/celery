# -*- coding: utf-8 -*-
"""
    celery.utils.term
    ~~~~~~~~~~~~~~~~~

    Terminals and colors.

"""
import platform

from functools import reduce
from typing import Any, Mapping, Tuple

__all__ = ['colored']

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
OP_SEQ = '\033[%dm'
RESET_SEQ = '\033[0m'
COLOR_SEQ = '\033[1;%dm'

IS_WINDOWS = platform.system() == 'Windows'


def fg(s: str) -> str:
    return COLOR_SEQ % s


class colored:
    """Terminal colored text.

    Example::
        >>> c = colored(enabled=True)
        >>> print(str(c.red('the quick '), c.blue('brown ', c.bold('fox ')),
        ...       c.magenta(c.underline('jumps over')),
        ...       c.yellow(' the lazy '),
        ...       c.green('dog ')))

    """

    def __init__(self, *s: Tuple[str],
                 enabled: bool=True, op: str='', **kwargs) -> None:
        self.s = s
        self.enabled = not IS_WINDOWS and enabled
        self.op = op

        # type: Mapping[str, str]
        self.names = {
            'black': self.black,
            'red': self.red,
            'green': self.green,
            'yellow': self.yellow,
            'blue': self.blue,
            'magenta': self.magenta,
            'cyan': self.cyan,
            'white': self.white,
        }

    def _add(self, a: str, b: str) -> str:
        return str(a) + str(b)

    def _fold_no_color(self, a: Any, b: Any) -> str:
        try:
            A = a.no_color()
        except AttributeError:
            A = str(a)
        try:
            B = b.no_color()
        except AttributeError:
            B = str(b)

        return ''.join((str(A), str(B)))

    def no_color(self) -> str:
        if self.s:
            return str(reduce(self._fold_no_color, self.s))
        return ''

    def embed(self) -> str:
        prefix = ''
        if self.enabled:
            prefix = self.op
        return ''.join((str(prefix), str(reduce(self._add, self.s))))

    def node(self, s: Any, op: str) -> Any:
        return self.__class__(enabled=self.enabled, op=op, *s)

    def black(self, *s: Tuple[str]) -> Any:
        return self.node(s, fg(30 + BLACK))

    def red(self, *s: Tuple[str]) -> Any:
        return self.node(s, fg(30 + RED))

    def green(self, *s: Tuple[str]) -> Any:
        return self.node(s, fg(30 + GREEN))

    def yellow(self, *s: Tuple[str]) -> Any:
        return self.node(s, fg(30 + YELLOW))

    def blue(self, *s: Tuple[str]) -> Any:
        return self.node(s, fg(30 + BLUE))

    def magenta(self, *s: Tuple[str]) -> Any:
        return self.node(s, fg(30 + MAGENTA))

    def cyan(self, *s: Tuple[str]) -> Any:
        return self.node(s, fg(30 + CYAN))

    def white(self, *s: Tuple[str]) -> Any:
        return self.node(s, fg(30 + WHITE))

    def bold(self, *s: Tuple[str]) -> Any:
        return self.node(s, OP_SEQ % 1)

    def underline(self, *s: Tuple[str]) -> Any:
        return self.node(s, OP_SEQ % 4)

    def blink(self, *s: Tuple[str]) -> Any:
        return self.node(s, OP_SEQ % 5)

    def reverse(self, *s: Tuple[str]) -> Any:
        return self.node(s, OP_SEQ % 7)

    def bright(self, *s: Tuple[str]) -> Any:
        return self.node(s, OP_SEQ % 8)

    def ired(self, *s: Tuple[str]) -> Any:
        return self.node(s, fg(40 + RED))

    def igreen(self, *s: Tuple[str]) -> Any:
        return self.node(s, fg(40 + GREEN))

    def iyellow(self, *s: Tuple[str]) -> Any:
        return self.node(s, fg(40 + YELLOW))

    def iblue(self, *s: Tuple[str]) -> Any:
        return self.node(s, fg(40 + BLUE))

    def imagenta(self, *s: Tuple[str]) -> Any:
        return self.node(s, fg(40 + MAGENTA))

    def icyan(self, *s: Tuple[str]) -> any:
        return self.node(s, fg(40 + CYAN))

    def iwhite(self, *s: Tuple[str]) -> any:
        return self.node(s, fg(40 + WHITE))

    def reset(self, *s: Tuple[str]) -> any:
        return self.node(s or [''], RESET_SEQ)

    def __add__(self, other: Any) -> str:
        return str(self) + str(other)

    def __repr__(self) -> str:
        return repr(self.no_color())

    def __str__(self) -> str:
        suffix = ''
        if self.enabled:
            suffix = RESET_SEQ
        return str(''.join((self.embed(), str(suffix))))
