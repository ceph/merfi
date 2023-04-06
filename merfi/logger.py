"""
This logging facility was greatly inspired by Outlook 2003.
"""
import sys

CRITICAL = 5
ERROR = 4
WARNING = 3
INFO = 2
DEBUG = 1

_level_names = {
    CRITICAL: 'critical',
    WARNING: 'warning',
    INFO: 'info',
    ERROR: 'error',
    DEBUG: 'debug'
}

_reverse_level_names = dict((v, k) for (k, v) in _level_names.items())

_level_colors = {
    'remote': 'bold',
    'critical': 'red',
    'warning': 'yellow',
    'info': 'blue',
    'debug': 'blue',
    'error': 'red'
}


class LogMessage(object):

    def __init__(self, level_name, message, writer=None, config_level=None):
        self.level_name = level_name
        self.message = message
        self.writer = writer or sys.stdout
        self.config_level = config_level or self.get_config_level()

    def skip(self):
        if self.level_int >= self.config_level:
            return False
        return True

    def header(self):
        from merfi.util import colorize
        colored = colorize.make(self.base_string)
        return getattr(colored, self.level_color)

    @property
    def base_string(self):
        if self.config_level < 2:
            return "--> [%s]" % self.level_name
        return "-->"

    @property
    def level_int(self):
        if self.level_name == 'remote':
            return 2
        return _reverse_level_names.get(self.level_name, 4)

    @property
    def level_color(self):
        return _level_colors.get(self.level_name, 'info')

    def line(self):
        message = self.message
        if isinstance(message, bytes):
            message = message.decode('utf-8')
        msg = message.rstrip('\n')
        return "%s %s\n" % (self.header(), msg)

    def write(self):
        if not self.skip():
            self.writer.write(self.line())

    def get_config_level(self):
        import merfi
        level = merfi.config.get('verbosity', 'error')
        return _reverse_level_names.get(level, 4)


def error(message):
    return LogMessage('error', message).write()


def debug(message):
    return LogMessage('debug', message).write()


def info(message):
    return LogMessage('info', message).write()


def warning(message):
    return LogMessage('warning', message).write()


def critical(message):
    return LogMessage('critical', message).write()
