import argparse

from .core import Lens
from .scanner import scan


def get_options(args=None):
    parser = argparse.ArgumentParser('lens-db')
    parser.add_argument('-now', '-today', action='store_true', help='open lens today')
    parser.add_argument('-days', type=int, help='days after lens were opened')
    parser.add_argument('-scan', action='store_true', help='scan and send email report if needed')
    parser.add_argument('-last', action='store_true', help='get timestamp of last ')

    return parser.parse_args(args)


def main():
    options = get_options()

    if options.scan:
        return scan()

    if options.days:
        return Lens.add(delta_days=options.days)

    if options.now:
        return Lens.add(delta_days=0)

    if options.last:
        last = Lens.get_last()
        exit('Last lens opened on %r' % last)
