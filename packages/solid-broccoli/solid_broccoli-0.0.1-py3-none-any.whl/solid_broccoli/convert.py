import argparse
from datetime import datetime
from typing import Optional

from dateutil.parser import parse


def string_to_unix(string_date: str) -> Optional[str]:
    try:
        dt_result = parse(
            string_date, dayfirst=True, ignoretz=True, fuzzy=True
        )
        ts_result = datetime.timestamp(dt_result)
        return str(int(ts_result))
    except Exception:
        return None


def unix_to_string(ts_string: str) -> Optional[str]:
    try:
        number = float(ts_string) if "." in ts_string else int(ts_string)
    except Exception:
        return None

    string_length = len(ts_string.split(".")[0])

    if string_length <= 10:
        return datetime.fromtimestamp(number).strftime("%d-%m-%Y, %H:%M:%S")
    else:
        number = number / 1000
        return datetime.fromtimestamp(number).strftime("%d-%m-%Y, %H:%M:%S")


def unix_to_human_and_versa() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--unix", help="Unix timestamp input s/ms.")
    parser.add_argument(
        "-d",
        "--date",
        help="""
            Date preferable format - days first (example MM-DD-YYYY).\n
            Timezone - ignored.
        """,
    )
    args = parser.parse_args()

    to_return = """
        Wrong input format.\n
        For unix timestamp - only float or integer.\n
        For date preferable format - days first (example MM-DD-YYYY).
    """

    if args.unix:
        converted_input = unix_to_string(args.unix)
        to_return = (
            "Date: " + converted_input if converted_input else to_return
        )
    elif args.date:
        converted_input = string_to_unix(args.date)
        to_return = (
            "Unix timestamp: " + converted_input
            if converted_input
            else to_return
        )
    print(to_return, flush=True)
