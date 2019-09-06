import argparse
import sys

from .exceptions import BaseLensDBError
from .utils import exception_exit
from .core import Lens
from .scanner import scan


def get_options(args=None):
    parser = argparse.ArgumentParser('lens-db')
    parser.add_argument('-now', '-today', action='store_true', help='open lens today')
    parser.add_argument('-days', type=int, help='days after lens were opened', metavar='days')
    parser.add_argument('-scan', action='store_true', help='scan and send email report if needed')
    parser.add_argument('-last', action='store_true', help='get timestamp of last ')
    parser.add_argument('-from-str', type=str, help='load date from str', metavar='str')
    parser.add_argument('-list', action='store_true', help='list database')

    return parser.parse_args(args)

def main():
    try:
        return _main()
    except BaseLensDBError as exc:
        exception_exit(exc)

def _main():
    if len(sys.argv) == 1:
        sys.argv.append('-h')

    options = get_options()

    if options.scan:
        return scan()

    if options.days:
        return Lens.add(delta_days=options.days)

    if options.now:
        return Lens.add(delta_days=0)

    if options.from_str:
        return Lens.add_custom(options.from_str)

    if options.list:
        exit(Lens.list())

    if options.last:
        last = Lens.get_last()
        exit('Last lens opened on %r' % last.strftime('%Y-%m-%d'))
