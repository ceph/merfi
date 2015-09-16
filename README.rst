`merfi`
=======
A helper tool to quickly crawl a file system and sign commonly used files for
repositories, with gpg, rpm-sign, and any other similar tool.

rpm-sign
--------
For `rpm-sign`, the default operation will just crawl the filesystem and
look for `Release` files. When that file is found, then it will proceed to sign
the file like::

    $ merfi rpm-sign --key "mykey"
    --> signing: /Users/alfredo/repos/debian/Release
    --> signed: /Users/alfredo/repos/debian/Release.gpg
    --> signed: /Users/alfredo/repos/debian/InRelease


What is really doing behind the scenes is using ``rpm-sign`` like this::

    rpm-sign --key "mykey" --detachsign Release --output Release.gpg
    rpm-sign --key "mykey" --clearsign Release > InRelease


About the name
--------------
*"Firme"* is the Spanish word for "sign" and *"merfi"* is the Peruvian slang
for it.
