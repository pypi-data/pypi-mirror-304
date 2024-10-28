import pkgutil
from rocker.extensions import RockerExtension


class CargoRocker(RockerExtension):
    @staticmethod
    def get_name():
        return "cargo_rocker"

    def __init__(self):
        self.name = CargoRocker.get_name()

    def get_snippet(self, cliargs):
        return pkgutil.get_data(
            "cargo_rocker", "templates/{}_snippet.Dockerfile".format(self.name)
        ).decode("utf-8")

    @staticmethod
    def register_arguments(parser, defaults=None):
        if defaults is None:
            defaults = {}
        parser.add_argument(
            f"--{CargoRocker.get_name()}",
            action="store_true",
            default=defaults.get("cargo_rocker"),
            help="add cargo_rocker to your docker image",
        )
