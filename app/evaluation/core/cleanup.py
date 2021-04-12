#!/usr/bin/env python

import os
from HPTLC_insight.settings import MEDIA_ROOT

path = MEDIA_ROOT
files = os.listdir(path)

class CleanUp():
    def run(*args):
        for file in files:
            #if "_" in file:
            try:
                os.remove(path+file)
            except:
                continue