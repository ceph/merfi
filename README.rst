`merfi`
=======
A helper tool to quickly crawl a file system and sign commonly used files for
repositories, with gpg, rpm-sign, and any other similar tool.

*"a tool called "merfi" ... what could possibly go wrong?"*

rpm-sign
--------
For ``rpm-sign``, the default operation will just crawl the filesystem looking
for Debian repositories containing  ``Release`` files. When the proper
``Release`` file is found, merfi will proceed to sign the file like::

    $ merfi rpm-sign --key "mykey"
    --> signing: /Users/alfredo/repos/debian/dists/trusty/Release
    --> signed: /Users/alfredo/repos/debian/dists/trusty/Release.gpg
    --> signed: /Users/alfredo/repos/debian/dists/trusty/InRelease

Like all the other supported backends, it will crawl from the current working
directory unless a path is specified::

    $ merfi rpm-sign --key "mykey" /opt/packages

What is really doing behind the scenes is using ``rpm-sign`` like this::

    rpm-sign --key "mykey" --detachsign Release --output Release.gpg
    rpm-sign --key "mykey" --clearsign Release > InRelease

gpg
---
GPG support is similar to ``rpm-sign`` in that merfi will crawl a path
(defaults to the current working directory) looking for Debian repositories,
and sign the appropriate ``Release`` files:

    $ merfi gpg
    --> signing: /Users/alfredo/repos/debian/dists/trusty/Release
    --> signed: /Users/alfredo/repos/debian/dists/trusty/Release.gpg
    --> signed: /Users/alfredo/repos/debian/dists/trusty/InRelease

Behind the scenes the tool is running ``gpg`` like::

    gpg --armor --detach-sig --output Release.gpg Release
    gpg --clearsign --output InRelease Release

iso
---
merfi can generate an ISO from a tree of package repositories::

    $ merfi iso /opt/packages --output my-dvd.iso

This will generate two files, ``my-dvd.iso`` and ``my-dvd.iso.SHA256SUM``. You
can verify the ISO file's integrity by passing the checksum file to the
``sha256sum -c`` command::

    $ sha256sum -c my-dvd.iso.SHA256SUM
    my-dvd.iso: OK

About the name
--------------
*"Firme"* is the Spanish word for "sign" and *"merfi"* is the Peruvian slang
for it.
