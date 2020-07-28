import logging

from digiformatter import styles

__all__ = ["debug", "info", "warn", "error", "critical", "log"]

styles.create("debug", fg="blue", prefix="DBG", showprefix=True, showtime=True)                               # DEBUG
styles.create("info", prefix="INF", showprefix=True, showtime=True)                                           # INFO
styles.create("warning", fg="yellow", prefix="WRN", showprefix=True, showtime=True)                           # WARNING
styles.create("warn", fg="yellow", prefix="WRN", showprefix=True, showtime=True)                              # WARN
styles.create("error", fg="red", attr="bold", prefix="ERR", showprefix=True, showtime=True)                   # ERROR
styles.create("critical", fg="yellow", bg="red", attr="bold", prefix="CRT", showprefix=True, showtime=True)   # CRITICAL
styles.create("fatal", fg="yellow", bg="red", attr="bold", prefix="CRT", showprefix=True, showtime=True)      # FATAL


def debug(message, **kwargs):
    log(message, level="debug", **kwargs)


def info(message, **kwargs):
    log(message, level="info", **kwargs)


def warn(message, **kwargs):
    log(message, level="warning", **kwargs)


def error(message, **kwargs):
    log(message, level="error", **kwargs)


def critical(message, **kwargs):
    log(message, level="critical", **kwargs)


def log(message, level="info", showtime=None, showprefix=None):
    styles.print(message, style=level, showtime=showtime, showprefix=showprefix)


class DigiFormatterHandler(logging.Handler):
    def init(self, *args, showsource=False, **kwargs):
        self.showsource = showsource
        super().__init__(*args, **kwargs)

    def emit(self, record):
        message = record.getMessage()
        if self.showsource:
            message = f"{record.name}: {message}"
        log(message, level=record.levelname.lower())


# Get the next unassigned log level, higher than the base level specified (default to 20: INFO)
def getFreeLevel(base=None):
    baselevel = logging._nameToLevel.get(base, 20)
    level = baselevel
    while level in logging._levelToName:
        level += 1
    return level


def addLogLevel(name, *args, base=None, showprefix=True, showtime=True, **kwargs):
    styles.create(name, *args, **kwargs)
    freelevel = getFreeLevel(base)
    logging.addLevelName(name, freelevel)
    return freelevel
