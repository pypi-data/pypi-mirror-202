import sys
import argparse

from ._extractor import extract_cookie


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="pulse-cookie",
        description="open SSO/SAML page to retrieve authentication cookie for Pulse Connect Secure VPN",
    )
    parser.add_argument("server", help="URL of the Pulse Connect Secure VPN server", type=str)
    parser.add_argument("-n", "--name", help="name of the cookie", type=str, default="DSID")
    args = parser.parse_args()

    cookie = extract_cookie(url=args.server, cookie_name=args.name)
    sys.stdout.write(cookie)
