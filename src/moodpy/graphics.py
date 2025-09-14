# -*- coding: utf-8 -*-
"""
Graphics utilities for MoodPy

This module provides functions for handling images in Moodle questions,
including matplotlib plot encoding and image file management.
"""

import os
import time
import base64

try:
    import matplotlib.pyplot as plt
    _HAS_MATPLOTLIB = True
except ImportError:
    plt = None
    _HAS_MATPLOTLIB = False


def tagImg(nom_graf, alt="imagen", width="600", height="400"):
    code = """<p>
    <img src=\"@@PLUGINFILE@@/{}\" alt=\"{}\" width=\"{}\" height=\"{}\" />
    </p>""".format(nom_graf,alt,width,height)
    return code

def fileImg(nom_graf, cod_graf):
    code = """
    <file name=\"{}\" path=\"/\" encoding=\"base64\">{}</file>
    """.format(nom_graf, cod_graf)
    return code

def encodePlot(*args):
    """
    Create a plot from arguments and return filename and base64 encoding.
    
    Args:
        *args: Arguments to pass to plt.plot()
        
    Returns:
        tuple: (filename, base64_encoded_data)
        
    Raises:
        ImportError: If matplotlib is not available
    """
    if not _HAS_MATPLOTLIB:
        raise ImportError("matplotlib is required for plot encoding. Install with: pip install matplotlib")
    
    plt.plot(*args)
    tiempo = str(time.time()).replace(".", "_")
    filename = tiempo + ".png"
    foldername = "./temp"
    
    if not os.path.isdir(foldername):
        os.makedirs(foldername)
    
    folderFile = os.path.join(foldername, filename)
    plt.savefig(folderFile)
    plt.close()
    
    with open(folderFile, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode('utf-8')
    
    return filename, encoded

def encodeGraf(graf):
    """
    Encode a graphic object (with save method) to base64.
    
    Args:
        graf: Graphic object with a save() method
        
    Returns:
        tuple: (filename, base64_encoded_data)
    """
    tiempo = str(time.time()).replace(".", "_")
    filename = tiempo + ".png"
    foldername = "./temp"
    
    if not os.path.isdir(foldername):
        os.makedirs(foldername)
    
    folderFile = os.path.join(foldername, filename)
    graf.save(folderFile)
    
    with open(folderFile, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode('utf-8')
    
    return filename, encoded


def has_matplotlib():
    """Check if matplotlib is available."""
    return _HAS_MATPLOTLIB
