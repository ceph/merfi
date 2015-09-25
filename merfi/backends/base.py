from merfi import base, util
from tambo import Transport


class BaseBackend(base.BaseCommand):

    options = []
    parser = None

    def parse_args(self):
        self.parser = Transport(self.argv, options=self.options)
        self.parser.catch_help = self.help()
        self.parser.parse_args()
        self.path = util.infer_path(self.parser.unknown_commands)
        self.check_dependency()
        self.sign()

    def sign(self):
        raise NotImplemented()
