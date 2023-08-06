import argparse

from pdm.cli.commands.base import BaseCommand
from pdm.project import Project
from tomlkit import parse
from packaging.version import parse, Version

class VersionCommand(BaseCommand):
    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("version", default="", nargs='?')

    def handle(self, project: Project, options: argparse.Namespace) -> None:
        metadata = project.pyproject.metadata
        current_version = metadata['version']

        if not options.version:
            print(current_version)
            return

        parsed_version = parse(current_version)
        next_version = None

        if options.version == 'major':
            next_version = Version(f"{parsed_version.major + 1}.0.0")
        elif options.version == 'minor':
            next_version = Version(f"{parsed_version.major}.{parsed_version.minor + 1}.0")
        elif (options.version == 'patch' or options.version == 'micro'):
            next_version = Version(f"{parsed_version.major}.{parsed_version.minor}.{parsed_version.micro + 1}")
        else:
            next_version = Version(options.version)

        project.pyproject.metadata["version"] = str(next_version)
        project.pyproject.write(show_message=False)
        print(next_version)


def version(core):
    core.register_command(VersionCommand, "version")
