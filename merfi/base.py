from merfi import util


class BaseCommand(object):
    """
    A base backend class that holds common functionality for sub commands.
    """
    help_menu = 'help_menu attribute needs to be defined'
    _help = '_help class attribute needs to be defined'
    executable = 'executable class attribute needs to be defined'
    name = 'name class attribute needs to be defined'

    def __init__(self, argv):
        self.argv = argv

    def dependency_help(self):
        try:
            util.check_dependency(self.executable, silent=True)
            msg = '%s is installed and available in current $PATH'
            return util.colorize.make(msg).blue % self.executable
        except RuntimeError:
            msg = '%s is not installed or available in current $PATH'
            return util.colorize.make(msg).red % self.executable

    def check_dependency(self):
        util.check_dependency(self.executable)

    def help(self):
        return self._help % self.dependency_help()
