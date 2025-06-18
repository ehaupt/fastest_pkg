import shlex
import subprocess
import re


class PkgMirror:
    """class to handle pkg mirrors"""

    def __init__(self, mirror):
        self.benchmark_files = (
            "http://%%SERVER%%/%%ABI%%/%%RELEASE%%/data.pkg",
            "http://%%SERVER%%/%%ABI%%/%%RELEASE%%/packagesite.pkg",
            "http://%%SERVER%%/%%ABI%%/%%RELEASE%%/Latest/pkg.pkg",
        )
        self.mirror = mirror
        self.abi, self.release = self.get_info()

    @classmethod
    def get_info(cls):
        """get ABI string from pkg -vv"""
        cmd = "/usr/local/sbin/pkg-static -vv"
        proc = subprocess.Popen(
            shlex.split(cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
        )
        out, err = proc.communicate()

        if err:
            raise Exception("pkg-static returned an error")

        abi = None
        release = None

        abi_match = re.search(r"\nABI\s+=\s+\"([^\"]*)\"", out.decode("utf-8"))
        if abi_match:
            abi = abi_match.group(1)

        release_match = re.search(r"\n\s+url\s+:\s+\".*/(.*)\"", out.decode("utf-8"))
        if release_match:
            release = release_match.group(1)

        return (abi, release)

    def get_urls(self):
        """returns a list of possible files to download from a mirror"""
        urls = []
        for rfile in self.benchmark_files:
            rfile = re.sub("%%SERVER%%", self.mirror, rfile)
            rfile = re.sub("%%ABI%%", self.abi, rfile)
            rfile = re.sub("%%RELEASE%%", self.release, rfile)
            urls.append(rfile)

        return urls
