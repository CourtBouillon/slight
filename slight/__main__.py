from argparse import ArgumentParser
from pathlib import Path

from . import __version__, app


def main(argv=None):
    """The ``slight`` programs can take multiple options.

    .. option:: -s <folder>, --slideshows <folder>

        Add a folder where slideshows are stored. Can be set mutliple times.

    .. option:: -t <folder>, --themes <folder>

        Add a folder where themes are stored. Can be set mutliple times.

    .. option:: -v, --version

        Show the version number. Other options and arguments are ignored.

    .. option:: -h, --help

        Show the command-line usage. Other options and arguments are ignored.

    """
    parser = ArgumentParser(
        prog='slight', description='A lightweight slideshow editor.')
    parser.add_argument(
        '-v', '--version', action='version',
        version=f'Slight version {__version__}',
        help='print Slight’s version number and exit')
    parser.add_argument(
        '-s', '--slideshows', action='append',
        help='folder containing slideshows')
    parser.add_argument(
        '-t', '--themes', action='append', help='folder containing themes')
    args = parser.parse_args(argv)
    if args.slideshows:
        app.config['slideshows'].extend(
            [Path(folder) for folder in args.slideshows])
    if args.themes:
        app.config['themes'].extend([Path(folder) for folder in args.themes])
    app.run(debug=True)
