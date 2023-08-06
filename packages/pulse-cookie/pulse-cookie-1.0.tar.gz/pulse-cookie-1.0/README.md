# Pulse Cookie

Pulse Cookie is a minimal web GUI that helps you connect to Pulse Connect Secure VPN servers that require Web-based multi-factor authentication (SSO/SAML). This script is intended to be used in conjunction with the [OpenConnect VPN CLI client](https://www.infradead.org/openconnect/) using the `--protocol=nc` option.

You might want to use this script if:

- your organization uses the [Pulse Connect Secure VPN](https://www.pulsesecure.net/) with multi-factor authentication (MFA) that requires you to enter credentials into a web GUI
- you want to avoid using the official (proprietary) Pulse Connect Secure VPN client application

## Usage

1. Run the provided script: `get-pulse-cookie [-n <cookie-name>] <server-url>`.
2. The URL will open in a new Qt WebEngine browser window.
3. Log on using your organization's SSO/SAML procedure. This should store the authentication cookie `<cookie-name>` (you need to know this name in advance!)
4. When the cookie is stored, the Web UI closes and the value of the cookie is printed to `stdout`.
5. You can then use the value of the cookie to connect to the server using OpenConnect: `sudo openconnect --protocol nc -C <cookie-name>=<cookie-value> <server-url>`

## Example

If my organization's Pulse Connect Secure VPN server is `https://vpn.jh.edu/Linux` and the name of the authentication cookie it stores is `DSID`, I can run `get-pulse-cookie -n DSID "https://vpn.jh.edu/Linux"`, which will print the cookie to `stdout`.

## Installation

### External dependency

You will need to install [Qt WebEngine](https://doc.qt.io/qt-6/qtwebengine-index.html), which provides the web GUI for the authentication workflow. On Arch Linux, this is provided by the [`qt6-webengine`](https://archlinux.org/packages/extra/x86_64/qt6-webengine/) package.

### This script

This is a standard Python package that can be installed using `pip`, perhaps directly from this repository as `pip install <url-of-this-repo>`.
