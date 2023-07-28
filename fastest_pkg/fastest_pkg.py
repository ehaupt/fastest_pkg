# -*- coding: utf-8 -*-

"""
Author   : Emanuel Haupt <ehaupt@FreeBSD.org>
Purpose  : Find the fastest pkg mirror
License  : BSD3CLAUSE
"""

import argparse
import json
from operator import itemgetter
from sys import stderr as STREAM
from typing import Dict
from urllib.parse import urlparse
import dns.resolver
import pycurl
from fastest_pkg.utils.human_bytes import HumanBytes
from fastest_pkg.utils.pkg_mirror import PkgMirror


def speedtest(url: str, args: Dict):
    parsed_url = urlparse(url)

    # download location
    path = "/dev/null"

    # callback function for c.XFERINFOFUNCTION
    def status(download_t, download_d, upload_t, upload_d):
        STREAM.write(
            "{}: {}%\r".format(
                parsed_url.netloc,
                str(int(download_d / download_t * 100) if download_t > 0 else 0),
            )
        )
        STREAM.flush()

    # download file using pycurl
    speed_download = 0
    with open(path, "wb") as f:
        curl = pycurl.Curl()
        curl.setopt(curl.URL, url)
        curl.setopt(curl.WRITEDATA, f)
        # display progress
        if args["verbose"]:
            curl.setopt(curl.NOPROGRESS, False)
            curl.setopt(curl.XFERINFOFUNCTION, status)
        else:
            curl.setopt(curl.NOPROGRESS, True)

        curl.setopt(pycurl.CONNECTTIMEOUT, int(args["timeout"] / 1000))
        curl.setopt(pycurl.TIMEOUT_MS, args["timeout"])

        try:
            curl.perform()
        except Exception as error:
            if args["verbose"]:
                # keep progress onscreen after error
                print()

                # print error
                print(error, file=STREAM)

        speed_download = curl.getinfo(pycurl.SPEED_DOWNLOAD)

        curl.close()

    # keeps progress onscreen after download completes
    if args["verbose"] and speed_download > 0:
        print()

    # print download speed
    if not args["json"]:
        print(
            (
                "%s: %s/s"
                % (parsed_url.netloc, (HumanBytes.format(speed_download, metric=True)))
            )
        )

    return speed_download


def get_mirrors():
    """returns a list of all mirrors for pkg.freebsd.org"""
    resolver = dns.resolver.Resolver()
    try:
        pkg_mirrors = resolver.resolve("_http._tcp.pkg.all.freebsd.org", "SRV")
    except AttributeError:
        pkg_mirrors = resolver.query("_http._tcp.pkg.all.freebsd.org", "SRV")

    return pkg_mirrors


def argument_parser():
    """Parsers CLI arguments and displays help text, handles all the Cli stuff"""
    parser = argparse.ArgumentParser(
        description="Script for finding and configuring fastest FreeBSD pkg mirror"
    )

    parser.add_argument(
        "-j",
        "--json",
        action="store_true",
        help="only show basic information in JSON format",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="be more verbose",
    )

    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        default=5000,
        help="timeout in ms",
    )

    argument = vars(parser.parse_args())
    return argument


def main():
    """script starts here"""
    cli_arguments = argument_parser()
    stats = []
    mirrors = get_mirrors()
    for mirror in mirrors:
        if mirror.priority > 10:
            pkg = PkgMirror(mirror.target.to_text(omit_final_dot=True))
            bytes_per_second = speedtest(url=pkg.get_urls()[0], args=cli_arguments)
            mirror_name = mirror.target.to_text(omit_final_dot=True)
            stats.append(
                {
                    "mirror_name": mirror_name,
                    "bytes_per_second": bytes_per_second,
                }
            )

    stats_sorted = sorted(stats, key=itemgetter("bytes_per_second"), reverse=True)

    if cli_arguments["json"]:
        print(json.dumps(stats_sorted))
    else:
        pkg = PkgMirror(stats_sorted[0]["mirror_name"])
        pkg_cfg = 'FreeBSD: { url: "http://%s/${ABI}/%s", mirror_type: "NONE" }' % (
            stats_sorted[0]["mirror_name"],
            pkg.release,
        )
        print(
            "\nFastest:\n%s: %s/s"
            % (
                stats_sorted[0]["mirror_name"],
                HumanBytes.format(stats_sorted[0]["bytes_per_second"], metric=True),
            )
        )
        print("\n")
        print("Write configuration:")
        print("mkdir -p /usr/local/etc/pkg/repos/")
        print("echo '" + pkg_cfg + "' \\\n\t> /usr/local/etc/pkg/repos/FreeBSD.conf")
        print("\n")
