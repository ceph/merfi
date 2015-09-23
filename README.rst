`merfi`
=======
A helper tool to quickly crawl a file system and sign commonly used files for
repositories, with gpg, rpm-sign, and any other similar tool.

*"a tool called "merfi" ... what could possibly go wrong?"*

rpm-sign
--------
For `rpm-sign`, the default operation will just crawl the filesystem and
look for `Release` files. When that file is found, then it will proceed to sign
the file like::

    $ merfi rpm-sign --key "mykey"
    --> signing: /Users/alfredo/repos/debian/Release
    --> signed: /Users/alfredo/repos/debian/Release.gpg
    --> signed: /Users/alfredo/repos/debian/InRelease

Like all the other supported backends, it will crawl from the current working
directory unless a path is specified::

    $ merfi rpm-sign --key "mykey" /opt/packages

What is really doing behind the scenes is using ``rpm-sign`` like this::

    rpm-sign --key "mykey" --detachsign Release --output Release.gpg
    rpm-sign --key "mykey" --clearsign Release > InRelease


gpg
---
GPG support is similar to ``rpm-sign`` in that it will crawl a path (defaults
to the current working directory) and sign the ``Release`` file::

    $ merfi gpg
    --> signing: /Users/alfredo/repos/debian/Release
    --> signed: /Users/alfredo/repos/debian/Release.gpg
    --> signed: /Users/alfredo/repos/debian/InRelease

Behind the scenes the tool is running ``gpg`` like::

    gpg --armor --detach-sig --output Release.gpg Release
    gpg --clearsign --output InRelease Release

About the name
--------------
*"Firme"* is the Spanish word for "sign" and *"merfi"* is the Peruvian slang
for it.
