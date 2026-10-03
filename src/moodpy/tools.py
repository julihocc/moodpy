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

import math
import html

counter = 0


def txt2arr(temp, array=True):
    """
    Convert text string to array using exec().

    Supports Python expressions (e.g. "[1, 2, 3]", "np.arange(0, 10, 2)",
    "list(range(5))") as well as legacy space-separated numbers ("1 2 3 4 5").

    Args:
        temp (str): Text representation of array/list or space-separated numbers.
        array (bool): Return numpy array if True, list if False.

    Returns:
        numpy.array or list: Converted data.

    Raises:
        ImportError: If numpy is required but not available.
    """
    if array and not _HAS_NUMPY:
        raise ImportError(
            "numpy is required for array=True. Install with: pip install numpy"
        )
    stripped = temp.strip()
    ns = {"np": np, "numpy": np} if _HAS_NUMPY else {}
    x = {}
    ns["x"] = x
    try:
        exec(f"x[None] = {stripped}", ns)
    except SyntaxError:
        # Legacy: space-separated numbers like "1 2 3 4"
        nums = ",".join(stripped.split())
        exec(f"x[None] = [{nums}]", ns)
    return np.array(x[None]) if array else x[None]


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
        raise ImportError(
            "numpy is required for round_normal. Install with: pip install numpy"
        )

    if a is None:
        a = -np.inf
    if b is None:
        b = np.inf

    while True:
        x = np.around(np.random.normal(loc=m, scale=s, size=size), d)
        if np.all((a <= x) & (x <= b)):
            return x


def int_normal(m=0, s=1, size=1, a=-np.inf, b=np.inf):
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
            row += str(A[i, j]) + ","
        if vector:
            M += row[:-1] + ";"
        else:
            M += row[:-1] + ";\n"
    if vector:
        M = M[:-1] + "]"
    else:
        M = M[:-2] + "]"
    return M


def show_latex(a):
    ax = plt.axes([0, 0, 0.3, 0.3])  # left,bottom,width,height
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis("off")
    plt.text(0.4, 0.4, "$%s$" % a, size=50, color="green")


###to numeric question
def NM(x, entero=False, percent=False, error=0.001, round_zero=False):
    """Format a finite answer with a nonnegative relative tolerance.

    ``percent=True`` converts a decimal proportion to percentage points.
    Integer mode retains the legacy exact-answer syntax.
    """
    x, error = float(x), float(error)
    if not math.isfinite(x) or not math.isfinite(error) or error < 0:
        raise ValueError(
            "answer must be finite and error must be finite and nonnegative"
        )
    if percent:
        x *= 100.0
    if not math.isfinite(x) or not math.isfinite(abs(x) * error):
        raise ValueError("answer or tolerance overflowed")
    if entero:
        return "{1:NM:=" + str(int(x)) + "}"
    if abs(x) <= 1e-8 and round_zero:
        return "{1:NM:=0:0.00001}"
    return "{1:NM:=" + str(x) + ":" + str(abs(x) * error) + "}"


def STxt(text):
    """
    Format text answer for Moodle cloze questions.

    Args:
        text (str): Text answer

    Returns:
        str: Formatted Moodle text answer
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError("short answer must be a nonempty string")
    # Moodle's Cloze decoder HTML-decodes answers, but only removes selected
    # backslash escapes. Entities preserve literal punctuation without leaving
    # stray backslashes in the graded answer. Asterisks need the short-answer
    # grader's own wildcard escape, which must survive the Cloze decoder.
    chunks = []
    for index, ch in enumerate(text):
        if ch == "*":
            chunks.append("\\*")
        elif ch in "\\~=#:{}":
            chunks.append("&#{};".format(ord(ch)))
            # Cloze removes one backslash before '#' or '}' after decoding
            # entities. Compensate when that backslash belongs to the answer.
            if ch == "\\" and index + 1 < len(text) and text[index + 1] in "#}":
                chunks.append("&#92;")
        else:
            chunks.append(html.escape(ch, quote=True))
    escaped = "".join(chunks)
    return "{1:SHORTANSWER:=" + escaped + "}"
