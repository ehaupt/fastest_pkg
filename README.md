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

However, this method does not choose the fastest mirror. This script can help you to find the fastest pkg mirror near you.

```console
$ ./fastest_pkg.py 
pkg0.bme.freebsd.org: 628.348 KB/s
pkg0.isc.freebsd.org: 867.503 KB/s
pkg0.nyi.freebsd.org: 913.416 KB/s
pkg0.pkt.freebsd.org: 12487.97 KB/s
pkg0.tuk.freebsd.org: 884.393 KB/s

Fastest:
pkg0.pkt.freebsd.org: 12487.97 KB/s


Write configuration:
mkdir -p /usr/local/etc/pkg/repos/
echo 'FreeBSD: { url: "http://pkg0.pkt.freebsd.org/${ABI}/latest" }' \
        > /usr/local/etc/pkg/repos/FreeBSD.conf

```

At the end of the output you'll see a sample configuration to hardcode the fastest pkg mirror leading to much higher pkg performance.
