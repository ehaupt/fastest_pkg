# fastest_pkg

Script to find the fastest FreeBSD.org pkg mirror. By default this is determined by the output of

```console
$ dig +short _http._tcp.pkg.freebsd.org srv
50 10 80 pkg0.bme.freebsd.org.
50 10 80 pkg0.isc.freebsd.org.
50 10 80 pkg0.nyi.freebsd.org.
10 10 80 pkgmir.geo.freebsd.org.
```

However, the used pkg mirror is not always the fastest.

# Sample

```console
$ ./fastest_pkg.py 
pkg0.bme.freebsd.org: 1826.263 KB/s
pkg0.isc.freebsd.org: 501.545 KB/s
pkg0.nyi.freebsd.org: 800.193 KB/s

Fastest:
pkg0.bme.freebsd.org: 1826.263 KB/s
```
