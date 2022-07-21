#!/usr/bin/env python3

import tarfile
import os
import shutil
TD = 'test-data'
with tarfile.open('test-data.tgz', 'r:gz') as tar:
    if os.path.isdir(TD):
        shutil.rmtree(TD)
    os.mkdir(TD)
    tar.extractall(path=TD)
