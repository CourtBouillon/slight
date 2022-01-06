from argparse import ArgumentParser
from pathlib import Path

from . import __version__, app


def main(argv=None):
    parser = ArgumentParser(
        prog='slight', description='A lightweight slideshow editor.')
    parser.add_argument(
        '-v', '--version', action='version',
        version=f'slight version {__version__}',
        help='print slight’s version number and exit')
    parser.add_argument(
        '-s', '--slideshows', action='append',
        help='folder containing slideshows')
    parser.add_argument(
        '-t', '--themes', action='append', help='folder containing themes')
    args = parser.parse_args(argv)
    app.config['slideshows'].extend(
        [Path(folder) for folder in args.slideshows])
    app.config['themes'].extend([Path(folder) for folder in args.themes])
    app.run(debug=True)
