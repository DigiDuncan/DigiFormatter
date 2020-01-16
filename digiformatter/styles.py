from time import strftime, localtime

import colored

__all__ = ["styles"]


class Styles:
    __slots__ = ["_styles", "default", "timestring", "timestampCodes"]

    def __init__(self):
        self._styles = {}
        self.default = colored.fg("cyan_1")
        self.timestring = "%d %b %H:%M:%S"
        self.timestampCodes = colored.fg("magenta")

    def create(self, name, *, fg = None, bg = None, attr = None):
        """Create a custom style"""
        codes = ""
        if fg is not None:
            codes += colored.fg(fg)
        if bg is not None:
            codes += colored.bg(bg)
        if attr is not None:
            codes += colored.attr(attr)
        self._styles[name] = codes

    def format(self, message, *, style="default", showtime=False):
        """Format a message in the requested style"""
        formatted = ""
        if showtime:
            formatted += self._timestamp()
        formatted = self._styles.get(style, self.default) + message + colored.attr("reset")
        return formatted

    def print(self, *args, **kwargs):
        """Print a message in the requested style"""
        print(self.format(*args, **kwargs))

    def _timestamp(self):
        """Color styling for terminal messages"""
        t = localtime()
        return self.timestampCodes + strftime(f"{self._timestring} | ", t) + colored.attr("reset")

    def __getattr__(self, name):
        if name not in self._styles:
            raise AttributeError
        return lambda message: self.print(message, style="name")

    def __str__(self):
        return "styles: " + (" ".join(self.format(level, style=level) for level in self._styles.keys()))


styles = Styles()
