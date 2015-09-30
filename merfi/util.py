import subprocess
import sys
from select import select
import os
from merfi import logger


def infer_path(arguments):
    """
    Infer the path from a list of potential paths. List might be empty and with
    items that are not paths.

    If arguments is an empty list it defaults to using the current working
    directory.
    """
    try:
        path = arguments[-1]
    except IndexError:
        # we didn't get an explicit path to work with so just return the
        # current working directory
        return os.getcwd()
    if os.path.exists(path):
        return os.path.abspath(path)
    else:
        raise RuntimeError('"%s" is not a valid path' % path)


def which(executable):
    """find the location of an executable"""
    if 'PATH' in os.environ:
        envpath = os.environ['PATH']
    else:
        envpath = os.defpath
    PATH = envpath.split(os.pathsep)

    locations = PATH + [
        '/usr/local/bin',
        '/bin',
        '/usr/bin',
        '/usr/local/sbin',
        '/usr/sbin',
        '/sbin',
    ]

    for location in locations:
        executable_path = os.path.join(location, executable)
        if os.path.isfile(executable_path) and os.access(executable_path, os.X_OK):
            return executable_path


def check_dependency(executable, silent=False):
    """
    Raise a RuntimeError if the dependency is not available in $PATH
    """
    if not which(executable):
        if not silent:
            logger.error('could not find %s' % executable)
        raise RuntimeError('%s needs to be installed and available in $PATH' % executable)


class colorize(str):
    """
    Pretty simple to use::

        colorize.make('foo').bold
        colorize.make('foo').green
        colorize.make('foo').yellow
        colorize.make('foo').red
        colorize.make('foo').blue

    Otherwise you could go the long way (for example if you are
    testing this class)::

        string = colorize('foo')
        string._set_attributes()
        string.red

    """

    def __init__(self, string):
        self.stdout = sys.__stdout__
        self.appends = ''
        self.prepends = ''
        self.isatty = self.stdout.isatty()

    def _set_attributes(self):
        """
        Sets the attributes here because the str class does not
        allow to pass in anything other than a string to the constructor
        so we can't really mess with the other attributes.
        """
        for k, v in self.__colors__.items():
            setattr(self, k, self.make_color(v))

    def make_color(self, color):
        if not self.isatty or self.is_windows:
            return self
        return color + self + '\033[0m' + self.appends

    @property
    def __colors__(self):
        return  dict(
                blue   = '\033[34m',
                green  = '\033[92m',
                yellow = '\033[33m',
                red    = '\033[91m',
                bold   = '\033[1m',
                ends   = '\033[0m'
        )

    @property
    def is_windows(self):
        if sys.platform == 'win32':
            return True
        return False

    @classmethod
    def make(cls, string):
        """
        A helper method to return itself and workaround the fact that
        the str object doesn't allow extra arguments passed in to the
        constructor
        """
        obj = cls(string)
        obj._set_attributes()
        return obj

#
# Common string manipulations
#
red_arrow = colorize.make('-->').red
blue_arrow = colorize.make('-->').blue


def run_output(command, **kw):
    logger.info('Running command: %s' % ' '.join(command))
    return _run_output(command, **kw)


def _run_output(cmd, verbose=False, **kw):
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kw
    )
    stdout = [line.strip('\n') for line in process.stdout.readlines()]
    stderr = [line.strip('\n') for line in process.stderr.readlines()]
    if verbose:
        for line in stdout:
            logger.debug(line)
        for line in stderr:
            logger.warning(stderr)
    return '\n'.join(stdout), '\n'.join(stderr), process.wait()


def run(command, **kw):
    logger.info('Running command: %s' % ' '.join(command))
    _run(command, stop_on_nonzero=True, **kw)


def _run(cmd, **kw):
    stop_on_nonzero = kw.pop('stop_on_nonzero', True)

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        close_fds=True,
        **kw
    )

    while True:
        reads, _, _ = select(
            [process.stdout.fileno(), process.stderr.fileno()],
            [], []
        )

        for descriptor in reads:
            if descriptor == process.stdout.fileno():
                read = process.stdout.readline()
                if read:
                    logger.info(read)
                    sys.stdout.flush()

            if descriptor == process.stderr.fileno():
                read = process.stderr.readline()
                if read:
                    logger.warning(read)
                    sys.stderr.flush()

        if process.poll() is not None:
            while True:
                for descriptor in reads:
                    if descriptor == process.stdout.fileno():
                        read = process.stdout.readline()
                        if read:
                            logger.info(read)
                            sys.stdout.flush()

                    if descriptor == process.stderr.fileno():
                        read = process.stderr.readline()
                        if read:
                            logger.warning(read)
                            sys.stderr.flush()
                # At this point we have gone through all the possible
                # descriptors and `read` was empty, so we now can break out of
                # this since all stdout/stderr has been properly flushed to
                # logging
                if not read:
                    break

            break

    returncode = process.wait()
    if returncode != 0:
        if stop_on_nonzero:
            raise RuntimeError(
                "command returned non-zero exit status: %s" % returncode
            )
        else:
            logger.warning("command returned non-zero exit status: %s" % returncode)

