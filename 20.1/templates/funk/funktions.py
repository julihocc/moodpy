#!/usr/bin/env python
# coding: utf-8

import sys
rutas = [r"D:\Dropbox\Moodpy\Moodpy Package\20.1"]
for ruta in rutas:
    sys.path.append(ruta)

import numpy as np
#np.random.seed(123)

import moodpy
import tools

import os
path = os.getcwd()

from sage.all import * 
sage.misc.html._old_and_deprecated_behavior = False

import datetime as dt
def test():
    print("Ubicación: \n\t",path)
    print("Hora: \n\t",dt.datetime.now())    

if __name__ == "__main__":
    test()
