# pylint: disable=W0622
"""cubicweb-eac application packaging information"""

distname = "cubicweb-eac"
modname = "cubicweb_eac"  # required by apycot

numversion = (0, 10, 0)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = "Implementation of Encoded Archival Context for CubicWeb"
web = "http://www.cubicweb.org/project/%s" % distname

__depends__ = {
    "cubicweb[postgresql]": ">=4.0.0, < 5.0",
    "cubicweb-web": ">= 1.1.0, < 2.0.0",
    "cubicweb-prov": ">= 1.0.0",
    "cubicweb-skos": ">= 3.1.0",
    "cubicweb-addressbook": ">= 2.0.2",
    "cubicweb-compound": ">= 1.0.0",
    "python-dateutil": None,
}
__recommends__ = {}

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python",
    "Programming Language :: JavaScript",
]
