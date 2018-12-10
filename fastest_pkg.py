#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author   : Emanuel Haupt <ehaupt@FreeBSD.org>
Purpose  : Find the fastest pkg mirror
Requires : curl
License  : BSD3CLAUSE
"""

from __future__ import print_function  # Imports print_function from python 3

import shlex
import subprocess
import re
import sys
import dns.resolver

def speedtest(url):
    """ Returns bytes per second value """
    cmd = 'curl -Lo /dev/null -skw "%%{speed_download}" %s' % (url)
    proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, err = proc.communicate()

    if err:
        raise Exception("curl returned an error")

    if out:
        return float(out)

    return None

class PkgMirror(object):
    """ class to handle pkg mirrors """
    def __init__(self, mirror):
        self.benchmark_files = (
            'http://%%SERVER%%/%%ABI%%/latest/packagesite.txz',
            'http://%%SERVER%%/%%ABI%%/latest/meta.txz',
            'http://%%SERVER%%/%%ABI%%/latest/digests.txz',
            'http://%%SERVER%%/%%ABI%%/latest/Latest/pkg.txz'
        )
        self.mirror = mirror
        self.abi = self.get_abi()

    @classmethod
    def get_abi(cls):
        """ get ABI string from pkg -vv """
        cmd = '/usr/local/sbin/pkg-static -vv'
        proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        out, err = proc.communicate()

        if err:
            raise Exception("pkg-static returned an error")

        match = re.search(r"\nABI\s+=\s+\"([^\"]*)\"", out)
        if match:
            return match.group(1)

        return None

    def get_urls(self):
        """ returns a list of possible files to download from a mirror """
        self.get_abi()
        urls = []
        for rfile in self.benchmark_files:
            rfile = re.sub('%%SERVER%%', self.mirror, rfile)
            rfile = re.sub('%%ABI%%', self.abi, rfile)
            urls.append(rfile)

        return urls


def get_mirrors():
    """ returns a list of all mirrors for pkg.freebsd.org """
    resolver = dns.resolver.Resolver()
    pkg_mirrors = resolver.query("_http._tcp.pkg.freebsd.org", "SRV")
    return pkg_mirrors


def main():
    """ script starts here """
    stats = []
    mirrors = get_mirrors()
    for mirror in mirrors:
        if mirror.priority > 10:
            pkg = PkgMirror(mirror.target.to_text(omit_final_dot=True))
            for url in pkg.get_urls():
                bytes_per_second = speedtest(url)
                if bytes_per_second:
                    mirror_name = mirror.target.to_text(omit_final_dot=True)
                    print("%s: %s KB/s" % (mirror_name, (bytes_per_second/1000)))
                    stats.append((mirror_name, bytes_per_second))
                    break

    stats.sort(key=lambda x: float(x[1]), reverse=True)
    print("\nFastest:\n%s: %s KB/s" % (stats[0][0], (stats[0][1]/1000)))


# Main section of the script
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:  # Catch Ctrl-C
        sys.exit(0)
    except SystemExit as sysexit:
        if sysexit.code != 0:
            raise
        else:
            sys.exit(0)
    except:
        raise
