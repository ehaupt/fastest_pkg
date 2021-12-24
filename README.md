# fastest_pkg

## Synopsis

Script to find the fastest FreeBSD.org pkg mirror near you.

## Description

By default FreeBSD pkg uses DNS-based load balancing. This is achieved a SRV query:

```console
$ dig +short _http._tcp.pkg.freebsd.org srv
10 10 80 pkgmir.geo.freebsd.org.
50 10 80 pkg0.bme.freebsd.org.
50 10 80 pkg0.isc.freebsd.org.
50 10 80 pkg0.nyi.freebsd.org.
50 10 80 pkg0.pkt.freebsd.org.
50 10 80 pkg0.tuk.freebsd.org.
```

However, this method does not choose the fastest mirror. This script can help you to find the fastest pkg mirror near you. At the end of the output you'll see a sample configuration to hardcode the fastest pkg mirror leading to much higher pkg performance.


```console
$ ./fastest_pkg.py 
pkg0.bme.freebsd.org: 16.1 MB/s
pkg0.isc.freebsd.org: 0.0 B/s
pkg0.nyi.freebsd.org: 4.7 MB/s
pkg0.pkt.freebsd.org: 11.9 MB/s
pkg0.tuk.freebsd.org: 2.2 MB/s

Fastest:
pkg0.bme.freebsd.org: 16.1 MB/s


Write configuration:
mkdir -p /usr/local/etc/pkg/repos/
echo 'FreeBSD: { url: "http://pkg0.bme.freebsd.org/${ABI}/latest" }' \
        > /usr/local/etc/pkg/repos/FreeBSD.conf

```

The following cli options are available:

```console
$ fastest_pkg --help
usage: fastest_pkg [-h] [-j] [-v] [-t TIMEOUT]

Script for finding and configuring fastest FreeBSD pkg mirror

optional arguments:
  -h, --help            show this help message and exit
  -j, --json            only show basic information in JSON format
  -v, --verbose         be more verbose
  -t TIMEOUT, --timeout TIMEOUT
                        timeout in ms
```
