import argparse
import sys

from .core import Lens
from .credentials import save_credentials
from .exceptions import BaseLensDBError
from .scanner import disable, enable, scan, show_status
from .utils import exception_exit

__all__ = ["main", "get_options"]

HELPS = {
    "now": "Open lens today",
    "days": "Days after lens were opened",
    "scan": "Scan and send email report if needed",
    "last": "Get timestamp of last entry",
    "from-str": "Load date from str in format YYYY-MM-DD",
    "list": "List database",
    "credentials": "Sets the credentials for sending emails",
    "username": "Username to send the email from",
    "password": "Password associated to the username",
    "disable": "disable scan (if it was enabled)",
    "enable": "enable scan (if it was disabled)",
    "status": "show if scan is enabled or not",
}


def get_help(x):
    return HELPS.get(x, "ERROR (%r)" % x)


def get_options(args=None):
    """Returns the CLI arguments parsed."""
    parser = argparse.ArgumentParser("lens-db")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("now", help=get_help("now"))

    days_subparser = subparsers.add_parser("days", help=get_help("days"))
    days_subparser.add_argument("days", type=int, help=get_help("days"), metavar="days")

    subparsers.add_parser("scan", help=get_help("scan"))

    subparsers.add_parser("last", help=get_help("last"))

    from_str_subparser = subparsers.add_parser("from-str", help=get_help("from-str"))
    from_str_subparser.add_argument(
        "string", type=str, help=get_help("from-str"), metavar="str",
    )

    subparsers.add_parser("list", help=get_help("list"))

    credentials_parser = subparsers.add_parser(
        "credentials", help=get_help("credentials")
    )
    credentials_parser.add_argument("username", help=get_help("username"))
    credentials_parser.add_argument("password", help=get_help("password"))

    subparsers.add_parser("disable", help=get_help("disable"))
    subparsers.add_parser("enable", help=get_help("enable"))

    subparsers.add_parser("status", help=get_help("status"))

    return parser.parse_args(args)


def main():
    """Main function of the program."""
    try:
        return _main()
    except BaseLensDBError as exc:
        exception_exit(exc)


def _main():
    """Secondary function of the program."""
    if len(sys.argv) == 1:
        sys.argv.append("-h")

    options = get_options()

    if options.command == "scan":
        return scan()

    if options.command == "days":
        return Lens.add(delta_days=options.days)

    if options.command == "now":
        return Lens.add(delta_days=0)

    if options.command == "from-str":
        return Lens.add_custom(options.string)

    if options.command == "list":
        exit(Lens.list())

    if options.command == "last":
        last = Lens.get_last()
        if last is None:
            exit("No lens in database")
        exit("Last lens opened on %r" % last.strftime("%Y-%m-%d"))

    if options.command == "credentials":
        save_credentials(username=options.username, password=options.password)
        return

    if options.command == "enable":
        enable()
        return

    if options.command == "disable":
        disable()
        return

    if options.command == "status":
        show_status()
        return
