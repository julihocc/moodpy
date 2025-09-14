# -*- coding: utf-8 -*-
"""
MoodPy Tools Module

Common utilities for developing MoodPy question generators.
This module provides helper functions for:
- Random number generation with constraints
- Array manipulation and conversion
- Moodle numerical question formatting
- Mathematical utilities

Functions:
    txt2arr: Convert text strings to numpy arrays
    round_normal: Generate bounded normal random numbers with rounding
    int_normal: Generate bounded integer normal random numbers  
    NM: Format numerical answers for Moodle cloze questions
"""

# Required imports with graceful error handling
try:
    import numpy as np
    _HAS_NUMPY = True
except ImportError:
    np = None
    _HAS_NUMPY = False

# Optional matplotlib import
try:
    import matplotlib.pyplot as plt
    _HAS_MATPLOTLIB = True
except ImportError:
    plt = None
    _HAS_MATPLOTLIB = False

counter = 0

def txt2arr(temp, array=True):
    """
    Convert text string to array using exec().
    
    Args:
        temp (str): Text representation of array/list
        array (bool): Return numpy array if True, list if False
        
    Returns:
        numpy.array or list: Converted data
        
    Raises:
        ImportError: If numpy is required but not available
    """
    arr = ' '.join(temp.split()).replace(" ",",")
    x = {}
    exec("x[None] = {}".format(arr))    
    if array:
        if not _HAS_NUMPY:
            raise ImportError("numpy is required for array=True. Install with: pip install numpy")
        return np.array(x[None])
    else: 
        return x[None]

def round_normal(m=0, s=1, size=1, a=None, b=None, d=0):
    """
    Generate bounded normal random numbers with rounding.
    
    Args:
        m (float): mean
        s (float): standard deviation  
        size (int): size of the array
        a (float): lower bound (default: -infinity)
        b (float): upper bound (default: +infinity)
        d (int): round to d decimals
        
    Returns:
        numpy.array: Random numbers within bounds
        
    Raises:
        ImportError: If numpy is not available
    """
    if not _HAS_NUMPY:
        raise ImportError("numpy is required for round_normal. Install with: pip install numpy")
    
    if a is None:
        a = -np.inf
    if b is None:
        b = np.inf
        
    while True:
        x = np.around(np.random.normal(loc=m, scale=s, size=size), d)
        if np.all( (a<=x) & (x<=b) ):
            return x
        
def int_normal(m=0,s=1,size=1,a=-np.inf, b=np.inf):
    """
    m: mean
    s: standart deviation
    n: size of the array
    a: lower bound
    b: upper bound    
    """
    x = round_normal(m=m, s=s, size=size, a=a, b=b)
    return x.astype("int")

def matlabfy(A, vector=False):
    M = "["
    for i in range(A.nrows()):
        row = ""
        for j in range(A.ncols()):
            row+=str(A[i,j])+","
        if vector:
            M+=row[:-1]+";"
        else:
            M+=row[:-1]+";\n"
    if vector:
        M = M[:-1]+"]"
    else:
        M = M[:-2]+"]"
    return M

def show_latex(a):
    ax = plt.axes([0,0,0.3,0.3]) #left,bottom,width,height
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')
    plt.text(0.4,0.4,'$%s$' %a,size=50,color="green")

###to numeric question
def NM(x, entero=False, percent=False, error=0.001, round_zero=False):
    if entero:
        x = int(x)
        sx = str(x)
        stol = str(0)
        return "{1:NM:=" + sx + "}"
    if percent:
        x += x * 100.0
    else:
        sx = str(1.0 * x)
        tol = x * error
        if tol<0:
            tol = -tol
        stol = str(tol)
        # print sx, type(sx)
        #
        # print(x,type(x))
        if np.isclose(0, x) and round_zero:
            return "{1:NM:=0:0.00001}"
        else:
            return "{1:NM:=" + sx + ":" + stol + "}"


    
