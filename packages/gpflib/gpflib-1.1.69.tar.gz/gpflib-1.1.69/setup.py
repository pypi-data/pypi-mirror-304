#!/usr/bin/env python
from setuptools import setup

# See setup.cfg for configuration.
setup(
    package_data={
        'gpflib': ['Graph/*.*','Graph/config6','gpflib.dll','bcclib.dll', 'libgpflib.so','libbcclib.so', 'GPFconfig.txt','BCCconfig.txt', 'Parser.lua','gpflib.py','Segment.dat','idxPOS.dat'],
    }
)

