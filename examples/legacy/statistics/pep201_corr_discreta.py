"""
PEP201_corr_discreta

Migrated from legacy generator: PEP201_corr_discreta.ipynb
Subject Area: statistics

This module contains educational content generators for MoodPy v3.0.0.
"""

import moodpy
from moodpy import Generator, Cloze
import numpy as np
import numpy.random as rnd

# Disable Sage HTML warnings if present
try:
    import sage.misc.html
    sage.misc.html._old_and_deprecated_behavior = False
except ImportError:
    pass

{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 29,
   "metadata": {},
   "outputs": [],
   "source": [
    "import moodpy as me\n",
    "import numpy as np\n",
    "import numpy.random as rnd\n",
#     "sage.misc.html._old_and_deprecated_behavior = False"  # TODO: Replace Sage functionality
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 30,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<h1>PEP201_corr_discreta</h1>\n",
      "<h1> Cálculo de estadísticos para variables aleatorias discretas </h1>\n"
     ]
    }
   ],
   "source": [
    "label = \"PEP201_corr_discreta\"\n",
    "miCabecera = \"<h1> Cálculo de estadísticos para variables aleatorias discretas </h1>\"\n",
#     "print(html(\"<h1>\"+label+\"</h1>\"))\n",  # TODO: Convert HTML output for MoodPy
#     "print(html(miCabecera))"  # TODO: Convert HTML output for MoodPy
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<h1>PEP201_corr_discreta</h1>"
      ],
      "text/plain": [
       "<h1>PEP201_corr_discreta</h1>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "text/html": [
       "PGgxPiBDw6FsY3VsbyBkZSBlc3RhZMOtc3RpY29zIHBhcmEgdmFyaWFibGVzIGFsZWF0b3JpYXMgZGlzY3JldGFzIDwvaDE+\n"
      ],
      "text/plain": [
       "PGgxPiBDw6FsY3VsbyBkZSBlc3RhZMOtc3RpY29zIHBhcmEgdmFyaWFibGVzIGFsZWF0b3JpYXMgZGlzY3JldGFzIDwvaDE+\n"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "text/html": [
       "PGgxPiBDw6FsY3VsbyBkZSBlc3RhZMOtc3RpY29zIHBhcmEgdmFyaWFibGVzIGFsZWF0b3JpYXMgZGlzY3JldGFzIDwvaDE+CiAgICA8cD4KICAgIFN1cG9uZ2Ftb3MgcXVlIFwoWCxZXCkgc29uIHZhcmlhYmxlcyBhbGVhdG9yaWFzIGRpc2NyZXRhcywgCiAgICBjb24gdW5hIGZ1bmNpw7NuIGRlIGRlbnNpZGFkIFwoZih4LHkpXCkgdGFsIHF1ZSAKICAgIDxzY3JpcHQgdHlwZT0ibWF0aC90ZXg7IG1vZGU9ZGlzcGxheSI+Zih4LHkpPWMqKDUgXCwgeF57Mn0gKyA3IFwsIHggeSArIDcgXCwgeV57Mn0gKyA3IFwsIHggKyAyIFwsIHkgKyA0KTwvc2NyaXB0PiBzaQogICAgXCh4IFxpbiBbNSwxM10sIHkgXGluIFsxMCwyNF1cKSB5IFwoMFwpIGVuIGN1YWxlc3F1aWVyYQogICAgb3Ryb3MgcHVudG9zLiAKICAgIDwvcD4KICAgIAogICAgPHA+IENhbGN1bGUgbGEgY29udGFudGVzIGRlIG5vcm1hbGl6YWNpw7NuIDxicj4KICAgIFwoYz1cKXsxOk5NOj0xLjk2Nzk2MTU4NTM4OTg1ZS02OjUuOTAzODg0NzU2MTY5NTZlLTh9IDwvcD4KICAgIAogICAgPHA+IENhbGN1bGUgbG9zIHNpZ3VpZW50ZXMgZXN0YWTDrXN0aWNvcwogICAgPGRpdiBjbGFzcz0ibm90cnVuY2F0ZSI+Cjx0YWJsZSBib3JkZXI9IjEiIGNsYXNzPSJ0YWJsZV9mb3JtIj4KPHRib2R5Pgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD4tLS1Fc3RhZMOtc3RpY28tLS08L3RkPgo8dGQ+VmFsb3I8L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYiI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cbXVfWDwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9OS4zODI1NzE3MzIyOjAuMjgxNDc3MTUxOTY2fTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1hIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPlxtdV9ZPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj0xOC41MDI2NTY3NDgxOjAuNTU1MDc5NzAyNDQ0fTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1iIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPkUoWFkpPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj0xNzMuMjU5MDYyNDYzOjUuMTk3NzcxODczODl9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWEiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+RShYXjIpPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj05NC41OTg0MTc3NTg5OjIuODM3OTUyNTMyNzd9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWIiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+RShZXjIpPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj0zNTkuMjY4NDYxNDQ4OjEwLjc3ODA1Mzg0MzR9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWEiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XHNpZ21hXjJfWDwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9Ni41NjU3NjU0NDkwMTowLjE5Njk3Mjk2MzQ3fTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1iIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPlxzaWdtYV4yX1k8L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PTE2LjkyMDE1NDcwODE6MC41MDc2MDQ2NDEyNDR9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWEiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XHNpZ21hX3tYWX08L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PS0wLjM0MzQ0MTcxMjU5NjotMC4wMTAzMDMyNTEzNzc5fTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1iIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPlxzaWdtYV9YPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj0yLjU2MjM3NDk2MjYxOjAuMDc2ODcxMjQ4ODc4M308L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cc2lnbWFfWTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9NC4xMTM0MTE1NjU2MTowLjEyMzQwMjM0Njk2OH08L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYiI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5ccmhvPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj0tMC4wMzI1ODQyODQ4ODc2Oi0wLjAwMDk3NzUyODU0NjYyN308L3RkPgo8L3RyPgo8L3Rib2R5Pgo8L3RhYmxlPgo8L2Rpdj4gPC9wPgogICAgCgogICAg\n"
      ],
      "text/plain": [
       "PGgxPiBDw6FsY3VsbyBkZSBlc3RhZMOtc3RpY29zIHBhcmEgdmFyaWFibGVzIGFsZWF0b3JpYXMgZGlzY3JldGFzIDwvaDE+CiAgICA8cD4KICAgIFN1cG9uZ2Ftb3MgcXVlIFwoWCxZXCkgc29uIHZhcmlhYmxlcyBhbGVhdG9yaWFzIGRpc2NyZXRhcywgCiAgICBjb24gdW5hIGZ1bmNpw7NuIGRlIGRlbnNpZGFkIFwoZih4LHkpXCkgdGFsIHF1ZSAKICAgIDxzY3JpcHQgdHlwZT0ibWF0aC90ZXg7IG1vZGU9ZGlzcGxheSI+Zih4LHkpPWMqKDUgXCwgeF57Mn0gKyA3IFwsIHggeSArIDcgXCwgeV57Mn0gKyA3IFwsIHggKyAyIFwsIHkgKyA0KTwvc2NyaXB0PiBzaQogICAgXCh4IFxpbiBbNSwxM10sIHkgXGluIFsxMCwyNF1cKSB5IFwoMFwpIGVuIGN1YWxlc3F1aWVyYQogICAgb3Ryb3MgcHVudG9zLiAKICAgIDwvcD4KICAgIAogICAgPHA+IENhbGN1bGUgbGEgY29udGFudGVzIGRlIG5vcm1hbGl6YWNpw7NuIDxicj4KICAgIFwoYz1cKXsxOk5NOj0xLjk2Nzk2MTU4NTM4OTg1ZS02OjUuOTAzODg0NzU2MTY5NTZlLTh9IDwvcD4KICAgIAogICAgPHA+IENhbGN1bGUgbG9zIHNpZ3VpZW50ZXMgZXN0YWTDrXN0aWNvcwogICAgPGRpdiBjbGFzcz0ibm90cnVuY2F0ZSI+Cjx0YWJsZSBib3JkZXI9IjEiIGNsYXNzPSJ0YWJsZV9mb3JtIj4KPHRib2R5Pgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD4tLS1Fc3RhZMOtc3RpY28tLS08L3RkPgo8dGQ+VmFsb3I8L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYiI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cbXVfWDwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9OS4zODI1NzE3MzIyOjAuMjgxNDc3MTUxOTY2fTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1hIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPlxtdV9ZPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj0xOC41MDI2NTY3NDgxOjAuNTU1MDc5NzAyNDQ0fTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1iIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPkUoWFkpPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj0xNzMuMjU5MDYyNDYzOjUuMTk3NzcxODczODl9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWEiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+RShYXjIpPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj05NC41OTg0MTc3NTg5OjIuODM3OTUyNTMyNzd9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWIiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+RShZXjIpPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj0zNTkuMjY4NDYxNDQ4OjEwLjc3ODA1Mzg0MzR9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWEiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XHNpZ21hXjJfWDwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9Ni41NjU3NjU0NDkwMTowLjE5Njk3Mjk2MzQ3fTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1iIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPlxzaWdtYV4yX1k8L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PTE2LjkyMDE1NDcwODE6MC41MDc2MDQ2NDEyNDR9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWEiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XHNpZ21hX3tYWX08L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PS0wLjM0MzQ0MTcxMjU5NjotMC4wMTAzMDMyNTEzNzc5fTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1iIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPlxzaWdtYV9YPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj0yLjU2MjM3NDk2MjYxOjAuMDc2ODcxMjQ4ODc4M308L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cc2lnbWFfWTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9NC4xMTM0MTE1NjU2MTowLjEyMzQwMjM0Njk2OH08L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYiI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5ccmhvPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj0tMC4wMzI1ODQyODQ4ODc2Oi0wLjAwMDk3NzUyODU0NjYyN308L3RkPgo8L3RyPgo8L3Rib2R5Pgo8L3RhYmxlPgo8L2Rpdj4gPC9wPgogICAgCgogICAg\n"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "    <questiontext format=\"html\">\n",
      "<text>\n",
      "<![CDATA[\n",
      "<h1> Cálculo de estadísticos para variables aleatorias discretas </h1>\n",
      "    <p>\n",
      "    Supongamos que \\(X,Y\\) son variables aleatorias discretas, \n",
      "    con una función de densidad \\(f(x,y)\\) tal que \n",
      "    $$f = lambda x,y: c*(5 \\, x^{2} + 7 \\, x y + 7 \\, y^{2} + 7 \\, x + 2 \\, y + 4)$$ si\n",
      "    \\(x \\in [5,13], y \\in [10,24]\\) y \\(0\\) en cualesquiera\n",
      "    otros puntos. \n",
      "    </p>\n",
      "    \n",
      "    <p> Calcule la contantes de normalización <br>\n",
      "    \\(c=\\){1:NM:=1.96796158538985e-6:5.90388475616956e-8} </p>\n",
      "    \n",
      "    <p> Calcule los siguientes estadísticos\n",
      "    <div class=\"notruncate\">\n",
      "<table border=\"1\" class=\"table_form\">\n",
      "<tbody>\n",
      "<tr class =\"row-a\">\n",
      "<td>---Estadístico---</td>\n",
      "<td>Valor</td>\n",
      "</tr>\n",
      "<tr class =\"row-b\">\n",
      "<td><script type=\"math/tex\">\\mu_X</script></td>\n",
      "<td>{1:NM:=9.3825717322:0.281477151966}</td>\n",
      "</tr>\n",
      "<tr class =\"row-a\">\n",
      "<td><script type=\"math/tex\">\\mu_Y</script></td>\n",
      "<td>{1:NM:=18.5026567481:0.555079702444}</td>\n",
      "</tr>\n",
      "<tr class =\"row-b\">\n",
      "<td><script type=\"math/tex\">E(XY)</script></td>\n",
      "<td>{1:NM:=173.259062463:5.19777187389}</td>\n",
      "</tr>\n",
      "<tr class =\"row-a\">\n",
      "<td><script type=\"math/tex\">E(X^2)</script></td>\n",
      "<td>{1:NM:=94.5984177589:2.83795253277}</td>\n",
      "</tr>\n",
      "<tr class =\"row-b\">\n",
      "<td><script type=\"math/tex\">E(Y^2)</script></td>\n",
      "<td>{1:NM:=359.268461448:10.7780538434}</td>\n",
      "</tr>\n",
      "<tr class =\"row-a\">\n",
      "<td><script type=\"math/tex\">\\sigma^2_X</script></td>\n",
      "<td>{1:NM:=6.56576544901:0.19697296347}</td>\n",
      "</tr>\n",
      "<tr class =\"row-b\">\n",
      "<td><script type=\"math/tex\">\\sigma^2_Y</script></td>\n",
      "<td>{1:NM:=16.9201547081:0.507604641244}</td>\n",
      "</tr>\n",
      "<tr class =\"row-a\">\n",
      "<td><script type=\"math/tex\">\\sigma_{XY}</script></td>\n",
      "<td>{1:NM:=-0.343441712596:-0.0103032513779}</td>\n",
      "</tr>\n",
      "<tr class =\"row-b\">\n",
      "<td><script type=\"math/tex\">\\sigma_X</script></td>\n",
      "<td>{1:NM:=2.56237496261:0.0768712488783}</td>\n",
      "</tr>\n",
      "<tr class =\"row-a\">\n",
      "<td><script type=\"math/tex\">\\sigma_Y</script></td>\n",
      "<td>{1:NM:=4.11341156561:0.123402346968}</td>\n",
      "</tr>\n",
      "<tr class =\"row-b\">\n",
      "<td><script type=\"math/tex\">\\rho</script></td>\n",
      "<td>{1:NM:=-0.0325842848876:-0.000977528546627}</td>\n",
      "</tr>\n",
      "</tbody>\n",
      "</table>\n",
      "</div> </p>\n",
      "    \n",
      "]]>\n",
      "</text></questiontext>\n",
      "\n",
      "    <generalfeedback format=\"html\">\n",
      "<text>\n",
      "<![CDATA[\n",
      "\n",
      "\n",
      "    \n",
      "]]>\n",
      "</text></generalfeedback>\n",
      "\n",
      "    \n"
     ]
    }
   ],
   "source": [
    "def gen(impr, cabecera=\"\"):\n",
    "    \n",
    "    def htable(tab):\n",
#     "        return html(table(tab, frame=True))\n",  # TODO: Convert HTML output for MoodPy
    "    \n",
    "    data = {}\n",
    "    ans = {}\n",
    "    tex = {}\n",
    "    \n",
    "    #x,y = var(\"x,y\")\n",
    "    \n",
    "    par = 2+rnd.poisson(8)\n",
    "    while True:        \n",
    "        a,b,c,d,e,g = rnd.randint(par, size = 6)\n",
    "        if a+b+c+d+e+g>0:\n",
    "            break\n",
    "    \n",
    "    x,y = var(\"x,y\")\n",
    "    \n",
    "    f_ = lambda x,y: a*x**2 + b*y**2 + c*x*y + d*x + e*y + g \n",
    "    \n",
    "    xmin = rnd.randint(1,2+rnd.poisson(par))\n",
    "    delx = 2+rnd.poisson(par)\n",
    "    xmax = xmin + delx\n",
    "    xint = range(xmin, xmax+1)\n",
    "    tex[\"xint\"] = \"[\"+str(xmin)+\",\"+str(xmax)+\"]\"\n",
    "    \n",
    "    ymin = rnd.randint(1,2+rnd.poisson(par))\n",
    "    dely = 2+rnd.poisson(par)\n",
    "    ymax = ymin + dely\n",
    "    yint = range(ymin, ymax+1)\n",
    "    tex[\"yint\"] = \"[\"+str(ymin)+\",\"+str(ymax)+\"]\"\n",
    "        \n",
    "    k = np.sum(np.array([[f_(u,v) for u in xint] for v in yint]))\n",
    "    #print c,type(c)\n",
    "    c = 1./k\n",
    "    ans[\"c\"] = me.NM(c)\n",
    "        \n",
    "    f = lambda x,y: f_(x,y)/k\n",
    "    \n",
    "    tex[\"fep\"] = latex(f_(x,y))\n",
    "    tex[\"f\"] = latex(f(x,y))\n",
    "    #show(tex[\"f_\"])\n",
    "    #print f(x,y)\n",
    "    \n",
    "    #print np.sum(np.array([[f(u,v) for u in xint] for v in yint]))\n",
    "    \n",
    "   \n",
    "    def estat(g, dig = 5):\n",
    "        es = np.sum(np.array([[g(u,v)*f(u,v).n() for u in xint] \n",
    "                                for v in yint]))\n",
    "        return es\n",
    "    \n",
    "    respuestas = [[\"---Estadístico---\", \"Valor\"]]\n",
    "    \n",
    "    mx = estat(lambda x,y:x)#; print mx\n",
    "    my = estat(lambda x,y:y)#; print my\n",
    "    sx = sqrt(estat(lambda x,y:(x-mx)**2))\n",
    "    sy = sqrt(estat(lambda x,y:(y-my)**2))\n",
    "    sxy = estat(lambda x,y: (x-mx)*(y-my))\n",
    "    r = sxy/(sx*sy)\n",
    "    \n",
    "    midict = {0:[\"a\",\"b\"]}\n",
    "\n",
    "    func = {0: [\"$\\mu_X$\", lambda x,y: x] }\n",
    "    func[1] = [\"$\\mu_Y$\", lambda x,y:y]\n",
    "    func[2] = [\"$E(XY)$\", lambda x,y: x*y]\n",
    "    func[3] = [\"$E(X^2)$\", lambda x,y: x*x]\n",
    "    func[4] = [\"$E(Y^2)$\", lambda x,y: y*y]\n",
    "    func[5] = [\"$\\sigma^2_X\", lambda x,y: (x-mx)**2]\n",
    "    func[6] = [\"$\\sigma^2_Y\", lambda x,y: (y-my)**2]\n",
    "    func[7] = [\"$\\sigma_{XY}\", lambda x,y: (x-mx)*(y-my)]\n",
    "    func[8] = [\"$\\sigma_X\", sx]\n",
    "    func[9] = [\"$\\sigma_Y\", sy]\n",
    "    func[10] = [\"$\\\\rho$\", r]\n",
    "    \n",
    "    for k in range(8):\n",
    "        respuestas.append([func[k][0], me.NM(estat(func[k][1]))])\n",
    "        \n",
    "    for k in [8,9,10]:\n",
    "        respuestas.append([func[k][0], me.NM(func[k][1])])\n",
    "        \n",
    "    ans[\"res\"] = htable(respuestas)\n",
    "    \n",
    "    ejercicio = cabecera + \"\"\"\n",
    "    <p>\n",
    "    Supongamos que \\(X,Y\\) son variables aleatorias discretas, \n",
    "    con una función de densidad \\(f(x,y)\\) tal que \n",
    "    $$f = lambda x,y: c*({tex[fep]})$$ si\n",
    "    \\(x \\in {tex[xint]}, y \\in {tex[yint]}\\) y \\(0\\) en cualesquiera\n",
    "    otros puntos. \n",
    "    </p>\n",
    "    \n",
    "    <p> Calcule la contantes de normalización <br>\n",
    "    \\(c=\\){ans[c]} </p>\n",
    "    \n",
    "    <p> Calcule los siguientes estadísticos\n",
    "    {ans[res]} </p>\n",
    "    \"\"\".format(tex=tex, data=data, ans=ans)\n",
    "\n",
    "    retroalimentacion = \"\"\"\n",
    "\n",
    "    \"\"\".format(tex=tex)\n",
    "    \n",
    "    if impr:\n",
#     "        show(html(ejercicio+retroalimentacion))\n",  # TODO: Convert HTML output for MoodPy
    "    return me.pretty(ejercicio, retroalimentacion)\n",
    "\n",
    "np.random.seed(2)\n",
#     "show(html(\"<h1>\"+label+\"</h1>\"))\n",  # TODO: Convert HTML output for MoodPy
#     "show(html(miCabecera))\n",  # TODO: Convert HTML output for MoodPy
    "me.quick(gen, label, 0, impr=True, cabecera=miCabecera)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "PGgxPiBDw6FsY3VsbyBkZSBlc3RhZMOtc3RpY29zIHBhcmEgdmFyaWFibGVzIGFsZWF0b3JpYXMgZGlzY3JldGFzIDwvaDE+CiAgICA8cD4KICAgIFN1cG9uZ2Ftb3MgcXVlIFwoWCxZXCkgc29uIHZhcmlhYmxlcyBhbGVhdG9yaWFzIGRpc2NyZXRhcywgCiAgICBjb24gdW5hIGZ1bmNpw7NuIGRlIGRlbnNpZGFkIFwoZih4LHkpXCkgdGFsIHF1ZSAKICAgIDxzY3JpcHQgdHlwZT0ibWF0aC90ZXg7IG1vZGU9ZGlzcGxheSI+Zih4LHkpPWMqKHheezJ9ICsgNSBcLCB4IHkgKyA0IFwsIHleezJ9ICsgNSBcLCB4ICsgeSArIDIpPC9zY3JpcHQ+IHNpCiAgICBcKHggXGluIFs4LDE0XSwgeSBcaW4gWzEsNl1cKSB5IFwoMFwpIGVuIGN1YWxlc3F1aWVyYQogICAgb3Ryb3MgcHVudG9zLiAKICAgIDwvcD4KICAgIAogICAgPHA+IENhbGN1bGUgbGEgY29udGFudGVzIGRlIG5vcm1hbGl6YWNpw7NuIDxicj4KICAgIFwoYz1cKXsxOk5NOj0wLjAwMDA1NDI3NzAyOTk2MDkyMDU6MS42MjgzMTA4OTg4Mjc2MmUtNn0gPC9wPgogICAgCiAgICA8cD4gQ2FsY3VsZSBsb3Mgc2lndWllbnRlcyBlc3RhZMOtc3RpY29zCiAgICA8ZGl2IGNsYXNzPSJub3RydW5jYXRlIj4KPHRhYmxlIGJvcmRlcj0iMSIgY2xhc3M9InRhYmxlX2Zvcm0iPgo8dGJvZHk+Cjx0ciBjbGFzcyA9InJvdy1hIj4KPHRkPi0tLUVzdGFkw61zdGljby0tLTwvdGQ+Cjx0ZD5WYWxvcjwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1iIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPlxtdV9YPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj0xMS40MDU3NzUwNzY6MC4zNDIxNzMyNTIyOH08L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cbXVfWTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9NC4wNTg1MTA2MzgzOjAuMTIxNzU1MzE5MTQ5fTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1iIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPkUoWFkpPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj00Ni4xOTY4MDg1MTA2OjEuMzg1OTA0MjU1MzJ9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWEiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+RShYXjIpPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj0xMzMuOTU0NDA3Mjk1OjQuMDE4NjMyMjE4ODR9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWIiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+RShZXjIpPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj0xOS4xMzI5Nzg3MjM0OjAuNTczOTg5MzYxNzAyfTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1hIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPlxzaWdtYV4yX1g8L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PTMuODYyNzAyMjEwODE6MC4xMTU4ODEwNjYzMjR9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWIiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XHNpZ21hXjJfWTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9Mi42NjE0NzAxMjIyMzowLjA3OTg0NDEwMzY2Njh9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWEiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XHNpZ21hX3tYWX08L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PS0wLjA5MzY1MDk3MzI5MTE6LTAuMDAyODA5NTI5MTk4NzN9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWIiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XHNpZ21hX1g8L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PTEuOTY1Mzc1ODQ0Njc6MC4wNTg5NjEyNzUzNDAxfTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1hIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPlxzaWdtYV9ZPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj0xLjYzMTQwMTI3NTY2OjAuMDQ4OTQyMDM4MjY5OH08L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYiI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5ccmhvPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj0tMC4wMjkyMDgyNzMyOTg1Oi0wLjAwMDg3NjI0ODE5ODk1NX08L3RkPgo8L3RyPgo8L3Rib2R5Pgo8L3RhYmxlPgo8L2Rpdj4gPC9wPgogICAgCgogICAg\n"
      ],
      "text/plain": [
       "PGgxPiBDw6FsY3VsbyBkZSBlc3RhZMOtc3RpY29zIHBhcmEgdmFyaWFibGVzIGFsZWF0b3JpYXMgZGlzY3JldGFzIDwvaDE+CiAgICA8cD4KICAgIFN1cG9uZ2Ftb3MgcXVlIFwoWCxZXCkgc29uIHZhcmlhYmxlcyBhbGVhdG9yaWFzIGRpc2NyZXRhcywgCiAgICBjb24gdW5hIGZ1bmNpw7NuIGRlIGRlbnNpZGFkIFwoZih4LHkpXCkgdGFsIHF1ZSAKICAgIDxzY3JpcHQgdHlwZT0ibWF0aC90ZXg7IG1vZGU9ZGlzcGxheSI+Zih4LHkpPWMqKHheezJ9ICsgNSBcLCB4IHkgKyA0IFwsIHleezJ9ICsgNSBcLCB4ICsgeSArIDIpPC9zY3JpcHQ+IHNpCiAgICBcKHggXGluIFs4LDE0XSwgeSBcaW4gWzEsNl1cKSB5IFwoMFwpIGVuIGN1YWxlc3F1aWVyYQogICAgb3Ryb3MgcHVudG9zLiAKICAgIDwvcD4KICAgIAogICAgPHA+IENhbGN1bGUgbGEgY29udGFudGVzIGRlIG5vcm1hbGl6YWNpw7NuIDxicj4KICAgIFwoYz1cKXsxOk5NOj0wLjAwMDA1NDI3NzAyOTk2MDkyMDU6MS42MjgzMTA4OTg4Mjc2MmUtNn0gPC9wPgogICAgCiAgICA8cD4gQ2FsY3VsZSBsb3Mgc2lndWllbnRlcyBlc3RhZMOtc3RpY29zCiAgICA8ZGl2IGNsYXNzPSJub3RydW5jYXRlIj4KPHRhYmxlIGJvcmRlcj0iMSIgY2xhc3M9InRhYmxlX2Zvcm0iPgo8dGJvZHk+Cjx0ciBjbGFzcyA9InJvdy1hIj4KPHRkPi0tLUVzdGFkw61zdGljby0tLTwvdGQ+Cjx0ZD5WYWxvcjwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1iIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPlxtdV9YPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj0xMS40MDU3NzUwNzY6MC4zNDIxNzMyNTIyOH08L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cbXVfWTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9NC4wNTg1MTA2MzgzOjAuMTIxNzU1MzE5MTQ5fTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1iIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPkUoWFkpPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj00Ni4xOTY4MDg1MTA2OjEuMzg1OTA0MjU1MzJ9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWEiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+RShYXjIpPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj0xMzMuOTU0NDA3Mjk1OjQuMDE4NjMyMjE4ODR9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWIiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+RShZXjIpPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj0xOS4xMzI5Nzg3MjM0OjAuNTczOTg5MzYxNzAyfTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1hIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPlxzaWdtYV4yX1g8L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PTMuODYyNzAyMjEwODE6MC4xMTU4ODEwNjYzMjR9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWIiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XHNpZ21hXjJfWTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9Mi42NjE0NzAxMjIyMzowLjA3OTg0NDEwMzY2Njh9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWEiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XHNpZ21hX3tYWX08L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PS0wLjA5MzY1MDk3MzI5MTE6LTAuMDAyODA5NTI5MTk4NzN9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWIiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XHNpZ21hX1g8L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PTEuOTY1Mzc1ODQ0Njc6MC4wNTg5NjEyNzUzNDAxfTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1hIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPlxzaWdtYV9ZPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj0xLjYzMTQwMTI3NTY2OjAuMDQ4OTQyMDM4MjY5OH08L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYiI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5ccmhvPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj0tMC4wMjkyMDgyNzMyOTg1Oi0wLjAwMDg3NjI0ODE5ODk1NX08L3RkPgo8L3RyPgo8L3Rib2R5Pgo8L3RhYmxlPgo8L2Rpdj4gPC9wPgogICAgCgogICAg\n"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "text/html": [
       "PGgxPiBDw6FsY3VsbyBkZSBlc3RhZMOtc3RpY29zIHBhcmEgdmFyaWFibGVzIGFsZWF0b3JpYXMgZGlzY3JldGFzIDwvaDE+CiAgICA8cD4KICAgIFN1cG9uZ2Ftb3MgcXVlIFwoWCxZXCkgc29uIHZhcmlhYmxlcyBhbGVhdG9yaWFzIGRpc2NyZXRhcywgCiAgICBjb24gdW5hIGZ1bmNpw7NuIGRlIGRlbnNpZGFkIFwoZih4LHkpXCkgdGFsIHF1ZSAKICAgIDxzY3JpcHQgdHlwZT0ibWF0aC90ZXg7IG1vZGU9ZGlzcGxheSI+Zih4LHkpPWMqKDQgXCwgeF57Mn0gKyAyIFwsIHggeSArIDYgXCwgeCArIDYgXCwgeSArIDUpPC9zY3JpcHQ+IHNpCiAgICBcKHggXGluIFs2LDEzXSwgeSBcaW4gWzQsMTddXCkgeSBcKDBcKSBlbiBjdWFsZXNxdWllcmEKICAgIG90cm9zIHB1bnRvcy4gCiAgICA8L3A+CiAgICAKICAgIDxwPiBDYWxjdWxlIGxhIGNvbnRhbnRlcyBkZSBub3JtYWxpemFjacOzbiA8YnI+CiAgICBcKGM9XCl7MTpOTTo9MC4wMDAwMTI2Mzc3NTE0OTEyNTQ3OjMuNzkxMzI1NDQ3Mzc2NDBlLTd9IDwvcD4KICAgIAogICAgPHA+IENhbGN1bGUgbG9zIHNpZ3VpZW50ZXMgZXN0YWTDrXN0aWNvcwogICAgPGRpdiBjbGFzcz0ibm90cnVuY2F0ZSI+Cjx0YWJsZSBib3JkZXI9IjEiIGNsYXNzPSJ0YWJsZV9mb3JtIj4KPHRib2R5Pgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD4tLS1Fc3RhZMOtc3RpY28tLS08L3RkPgo8dGQ+VmFsb3I8L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYiI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cbXVfWDwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTAuMjY1MzkyNzgxMzowLjMwNzk2MTc4MzQzOX08L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cbXVfWTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTEuMDc1MDE3NjkyOTowLjMzMjI1MDUzMDc4Nn08L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYiI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5FKFhZKTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTEzLjQ5MDc5OTcxNzozLjQwNDcyMzk5MTUxfTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1hIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPkUoWF4yKTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTEwLjE2MTM1ODgxMTozLjMwNDg0MDc2NDMzfTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1iIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPkUoWV4yKTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTM4LjU3NTM3MTU1OjQuMTU3MjYxMTQ2NX08L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cc2lnbWFeMl9YPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj00Ljc4MzA2OTg1NjM0OjAuMTQzNDkyMDk1Njl9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWIiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XHNpZ21hXjJfWTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTUuOTE5MzU0NjUyOTowLjQ3NzU4MDYzOTU4N308L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cc2lnbWFfe1hZfTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9LTAuMTk4NjA2OTYwMjQ6LTAuMDA1OTU4MjA4ODA3MjF9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWIiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XHNpZ21hX1g8L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PTIuMTg3MDIzMDU4MDM6MC4wNjU2MTA2OTE3NDA4fTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1hIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPlxzaWdtYV9ZPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj0zLjk4OTkwNjU5NzAyOjAuMTE5Njk3MTk3OTF9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWIiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XHJobzwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9LTAuMDIyNzYwMzIwNTA5NjotMC4wMDA2ODI4MDk2MTUyODl9PC90ZD4KPC90cj4KPC90Ym9keT4KPC90YWJsZT4KPC9kaXY+IDwvcD4KICAgIAoKICAgIA==\n"
      ],
      "text/plain": [
       "PGgxPiBDw6FsY3VsbyBkZSBlc3RhZMOtc3RpY29zIHBhcmEgdmFyaWFibGVzIGFsZWF0b3JpYXMgZGlzY3JldGFzIDwvaDE+CiAgICA8cD4KICAgIFN1cG9uZ2Ftb3MgcXVlIFwoWCxZXCkgc29uIHZhcmlhYmxlcyBhbGVhdG9yaWFzIGRpc2NyZXRhcywgCiAgICBjb24gdW5hIGZ1bmNpw7NuIGRlIGRlbnNpZGFkIFwoZih4LHkpXCkgdGFsIHF1ZSAKICAgIDxzY3JpcHQgdHlwZT0ibWF0aC90ZXg7IG1vZGU9ZGlzcGxheSI+Zih4LHkpPWMqKDQgXCwgeF57Mn0gKyAyIFwsIHggeSArIDYgXCwgeCArIDYgXCwgeSArIDUpPC9zY3JpcHQ+IHNpCiAgICBcKHggXGluIFs2LDEzXSwgeSBcaW4gWzQsMTddXCkgeSBcKDBcKSBlbiBjdWFsZXNxdWllcmEKICAgIG90cm9zIHB1bnRvcy4gCiAgICA8L3A+CiAgICAKICAgIDxwPiBDYWxjdWxlIGxhIGNvbnRhbnRlcyBkZSBub3JtYWxpemFjacOzbiA8YnI+CiAgICBcKGM9XCl7MTpOTTo9MC4wMDAwMTI2Mzc3NTE0OTEyNTQ3OjMuNzkxMzI1NDQ3Mzc2NDBlLTd9IDwvcD4KICAgIAogICAgPHA+IENhbGN1bGUgbG9zIHNpZ3VpZW50ZXMgZXN0YWTDrXN0aWNvcwogICAgPGRpdiBjbGFzcz0ibm90cnVuY2F0ZSI+Cjx0YWJsZSBib3JkZXI9IjEiIGNsYXNzPSJ0YWJsZV9mb3JtIj4KPHRib2R5Pgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD4tLS1Fc3RhZMOtc3RpY28tLS08L3RkPgo8dGQ+VmFsb3I8L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYiI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cbXVfWDwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTAuMjY1MzkyNzgxMzowLjMwNzk2MTc4MzQzOX08L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cbXVfWTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTEuMDc1MDE3NjkyOTowLjMzMjI1MDUzMDc4Nn08L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYiI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5FKFhZKTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTEzLjQ5MDc5OTcxNzozLjQwNDcyMzk5MTUxfTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1hIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPkUoWF4yKTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTEwLjE2MTM1ODgxMTozLjMwNDg0MDc2NDMzfTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1iIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPkUoWV4yKTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTM4LjU3NTM3MTU1OjQuMTU3MjYxMTQ2NX08L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cc2lnbWFeMl9YPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj00Ljc4MzA2OTg1NjM0OjAuMTQzNDkyMDk1Njl9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWIiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XHNpZ21hXjJfWTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTUuOTE5MzU0NjUyOTowLjQ3NzU4MDYzOTU4N308L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cc2lnbWFfe1hZfTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9LTAuMTk4NjA2OTYwMjQ6LTAuMDA1OTU4MjA4ODA3MjF9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWIiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XHNpZ21hX1g8L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PTIuMTg3MDIzMDU4MDM6MC4wNjU2MTA2OTE3NDA4fTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1hIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPlxzaWdtYV9ZPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj0zLjk4OTkwNjU5NzAyOjAuMTE5Njk3MTk3OTF9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWIiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XHJobzwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9LTAuMDIyNzYwMzIwNTA5NjotMC4wMDA2ODI4MDk2MTUyODl9PC90ZD4KPC90cj4KPC90Ym9keT4KPC90YWJsZT4KPC9kaXY+IDwvcD4KICAgIAoKICAgIA==\n"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "text/html": [
       "PGgxPiBDw6FsY3VsbyBkZSBlc3RhZMOtc3RpY29zIHBhcmEgdmFyaWFibGVzIGFsZWF0b3JpYXMgZGlzY3JldGFzIDwvaDE+CiAgICA8cD4KICAgIFN1cG9uZ2Ftb3MgcXVlIFwoWCxZXCkgc29uIHZhcmlhYmxlcyBhbGVhdG9yaWFzIGRpc2NyZXRhcywgCiAgICBjb24gdW5hIGZ1bmNpw7NuIGRlIGRlbnNpZGFkIFwoZih4LHkpXCkgdGFsIHF1ZSAKICAgIDxzY3JpcHQgdHlwZT0ibWF0aC90ZXg7IG1vZGU9ZGlzcGxheSI+Zih4LHkpPWMqKDggXCwgeF57Mn0gKyA0IFwsIHggeSArIDQgXCwgeV57Mn0gKyB4ICsgNCBcLCB5ICsgMSk8L3NjcmlwdD4gc2kKICAgIFwoeCBcaW4gWzMsMTVdLCB5IFxpbiBbNiwxNV1cKSB5IFwoMFwpIGVuIGN1YWxlc3F1aWVyYQogICAgb3Ryb3MgcHVudG9zLiAKICAgIDwvcD4KICAgIAogICAgPHA+IENhbGN1bGUgbGEgY29udGFudGVzIGRlIG5vcm1hbGl6YWNpw7NuIDxicj4KICAgIFwoYz1cKXsxOk5NOj00LjYyMjc4MTA2NTA4ODc2ZS02OjEuMzg2ODM0MzE5NTI2NjNlLTd9IDwvcD4KICAgIAogICAgPHA+IENhbGN1bGUgbG9zIHNpZ3VpZW50ZXMgZXN0YWTDrXN0aWNvcwogICAgPGRpdiBjbGFzcz0ibm90cnVuY2F0ZSI+Cjx0YWJsZSBib3JkZXI9IjEiIGNsYXNzPSJ0YWJsZV9mb3JtIj4KPHRib2R5Pgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD4tLS1Fc3RhZMOtc3RpY28tLS08L3RkPgo8dGQ+VmFsb3I8L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYiI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cbXVfWDwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTAuNTczMzE3MzA3NzowLjMxNzE5OTUxOTIzMX08L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cbXVfWTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTEuMTE0NzgzNjUzODowLjMzMzQ0MzUwOTYxNX08L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYiI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5FKFhZKTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTE2LjgzMDUyODg0NjozLjUwNDkxNTg2NTM4fTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1hIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPkUoWF4yKTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTI0LjA2MDA5NjE1NDozLjcyMTgwMjg4NDYyfTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1iIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPkUoWV4yKTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTMxLjUzNzM3OTgwODozLjk0NjEyMTM5NDIzfTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1hIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPlxzaWdtYV4yX1g8L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PTEyLjI2NTA1NzI2NDc6MC4zNjc5NTE3MTc5NDF9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWIiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XHNpZ21hXjJfWTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9Ny45OTg5NjQxMzU4OTowLjIzOTk2ODkyNDA3N308L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cc2lnbWFfe1hZfTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9LTAuNjg5NjA1NTMyMzEzOi0wLjAyMDY4ODE2NTk2OTR9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWIiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XHNpZ21hX1g8L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PTMuNTAyMTUwMzc3MjM6MC4xMDUwNjQ1MTEzMTd9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWEiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XHNpZ21hX1k8L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PTIuODI4MjQ0MDAyMTg6MC4wODQ4NDczMjAwNjU1fTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1iIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPlxyaG88L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PS0wLjA2OTYyMjQxMzEzODE6LTAuMDAyMDg4NjcyMzk0MTR9PC90ZD4KPC90cj4KPC90Ym9keT4KPC90YWJsZT4KPC9kaXY+IDwvcD4KICAgIAoKICAgIA==\n"
      ],
      "text/plain": [
       "PGgxPiBDw6FsY3VsbyBkZSBlc3RhZMOtc3RpY29zIHBhcmEgdmFyaWFibGVzIGFsZWF0b3JpYXMgZGlzY3JldGFzIDwvaDE+CiAgICA8cD4KICAgIFN1cG9uZ2Ftb3MgcXVlIFwoWCxZXCkgc29uIHZhcmlhYmxlcyBhbGVhdG9yaWFzIGRpc2NyZXRhcywgCiAgICBjb24gdW5hIGZ1bmNpw7NuIGRlIGRlbnNpZGFkIFwoZih4LHkpXCkgdGFsIHF1ZSAKICAgIDxzY3JpcHQgdHlwZT0ibWF0aC90ZXg7IG1vZGU9ZGlzcGxheSI+Zih4LHkpPWMqKDggXCwgeF57Mn0gKyA0IFwsIHggeSArIDQgXCwgeV57Mn0gKyB4ICsgNCBcLCB5ICsgMSk8L3NjcmlwdD4gc2kKICAgIFwoeCBcaW4gWzMsMTVdLCB5IFxpbiBbNiwxNV1cKSB5IFwoMFwpIGVuIGN1YWxlc3F1aWVyYQogICAgb3Ryb3MgcHVudG9zLiAKICAgIDwvcD4KICAgIAogICAgPHA+IENhbGN1bGUgbGEgY29udGFudGVzIGRlIG5vcm1hbGl6YWNpw7NuIDxicj4KICAgIFwoYz1cKXsxOk5NOj00LjYyMjc4MTA2NTA4ODc2ZS02OjEuMzg2ODM0MzE5NTI2NjNlLTd9IDwvcD4KICAgIAogICAgPHA+IENhbGN1bGUgbG9zIHNpZ3VpZW50ZXMgZXN0YWTDrXN0aWNvcwogICAgPGRpdiBjbGFzcz0ibm90cnVuY2F0ZSI+Cjx0YWJsZSBib3JkZXI9IjEiIGNsYXNzPSJ0YWJsZV9mb3JtIj4KPHRib2R5Pgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD4tLS1Fc3RhZMOtc3RpY28tLS08L3RkPgo8dGQ+VmFsb3I8L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYiI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cbXVfWDwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTAuNTczMzE3MzA3NzowLjMxNzE5OTUxOTIzMX08L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cbXVfWTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTEuMTE0NzgzNjUzODowLjMzMzQ0MzUwOTYxNX08L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYiI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5FKFhZKTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTE2LjgzMDUyODg0NjozLjUwNDkxNTg2NTM4fTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1hIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPkUoWF4yKTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTI0LjA2MDA5NjE1NDozLjcyMTgwMjg4NDYyfTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1iIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPkUoWV4yKTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTMxLjUzNzM3OTgwODozLjk0NjEyMTM5NDIzfTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1hIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPlxzaWdtYV4yX1g8L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PTEyLjI2NTA1NzI2NDc6MC4zNjc5NTE3MTc5NDF9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWIiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XHNpZ21hXjJfWTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9Ny45OTg5NjQxMzU4OTowLjIzOTk2ODkyNDA3N308L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cc2lnbWFfe1hZfTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9LTAuNjg5NjA1NTMyMzEzOi0wLjAyMDY4ODE2NTk2OTR9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWIiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XHNpZ21hX1g8L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PTMuNTAyMTUwMzc3MjM6MC4xMDUwNjQ1MTEzMTd9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWEiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XHNpZ21hX1k8L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PTIuODI4MjQ0MDAyMTg6MC4wODQ4NDczMjAwNjU1fTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1iIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPlxyaG88L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PS0wLjA2OTYyMjQxMzEzODE6LTAuMDAyMDg4NjcyMzk0MTR9PC90ZD4KPC90cj4KPC90Ym9keT4KPC90YWJsZT4KPC9kaXY+IDwvcD4KICAgIAoKICAgIA==\n"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "text/html": [
       "PGgxPiBDw6FsY3VsbyBkZSBlc3RhZMOtc3RpY29zIHBhcmEgdmFyaWFibGVzIGFsZWF0b3JpYXMgZGlzY3JldGFzIDwvaDE+CiAgICA8cD4KICAgIFN1cG9uZ2Ftb3MgcXVlIFwoWCxZXCkgc29uIHZhcmlhYmxlcyBhbGVhdG9yaWFzIGRpc2NyZXRhcywgCiAgICBjb24gdW5hIGZ1bmNpw7NuIGRlIGRlbnNpZGFkIFwoZih4LHkpXCkgdGFsIHF1ZSAKICAgIDxzY3JpcHQgdHlwZT0ibWF0aC90ZXg7IG1vZGU9ZGlzcGxheSI+Zih4LHkpPWMqKHggeSArIDMgXCwgeV57Mn0gKyA0IFwsIHggKyAyIFwsIHkgKyA3KTwvc2NyaXB0PiBzaQogICAgXCh4IFxpbiBbMywxM10sIHkgXGluIFs2LDExXVwpIHkgXCgwXCkgZW4gY3VhbGVzcXVpZXJhCiAgICBvdHJvcyBwdW50b3MuIAogICAgPC9wPgogICAgCiAgICA8cD4gQ2FsY3VsZSBsYSBjb250YW50ZXMgZGUgbm9ybWFsaXphY2nDs24gPGJyPgogICAgXChjPVwpezE6Tk06PTAuMDAwMDQzMzUxOTc0NjgyNDQ2ODoxLjMwMDU1OTI0MDQ3MzQwZS02fSA8L3A+CiAgICAKICAgIDxwPiBDYWxjdWxlIGxvcyBzaWd1aWVudGVzIGVzdGFkw61zdGljb3MKICAgIDxkaXYgY2xhc3M9Im5vdHJ1bmNhdGUiPgo8dGFibGUgYm9yZGVyPSIxIiBjbGFzcz0idGFibGVfZm9ybSI+Cjx0Ym9keT4KPHRyIGNsYXNzID0icm93LWEiPgo8dGQ+LS0tRXN0YWTDrXN0aWNvLS0tPC90ZD4KPHRkPlZhbG9yPC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWIiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XG11X1g8L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PTguMzU3NjUzNzkxMTM6MC4yNTA3Mjk2MTM3MzR9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWEiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XG11X1k8L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PTkuMDA5MDYwNTYyNzE6MC4yNzAyNzE4MTY4ODF9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWIiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+RShYWSk8L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PTc1LjE5NTk5NDI3NzU6Mi4yNTU4Nzk4MjgzM308L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5FKFheMik8L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PTc5LjcyMjQ2MDY1ODE6Mi4zOTE2NzM4MTk3NH08L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYiI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5FKFleMik8L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PTgzLjg3NDEwNTg2NTU6Mi41MTYyMjMxNzU5N308L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cc2lnbWFeMl9YPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj05Ljg3MjA4Mzc2NTY5OjAuMjk2MTYyNTEyOTcxfTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1iIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPlxzaWdtYV4yX1k8L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PTIuNzEwOTMzNjQyOTc6MC4wODEzMjgwMDkyODkxfTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1hIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPlxzaWdtYV97WFl9PC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj0tMC4wOTg2MTQ4ODg5MDM5Oi0wLjAwMjk1ODQ0NjY2NzEyfTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1iIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPlxzaWdtYV9YPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj0zLjE0MTk4NzIzMTk0OjAuMDk0MjU5NjE2OTU4M308L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cc2lnbWFfWTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MS42NDY0OTEzMTI3NTowLjA0OTM5NDczOTM4MjZ9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWIiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XHJobzwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9LTAuMDE5MDYyNDQ2MTcwMjotMC4wMDA1NzE4NzMzODUxMDd9PC90ZD4KPC90cj4KPC90Ym9keT4KPC90YWJsZT4KPC9kaXY+IDwvcD4KICAgIAoKICAgIA==\n"
      ],
      "text/plain": [
       "PGgxPiBDw6FsY3VsbyBkZSBlc3RhZMOtc3RpY29zIHBhcmEgdmFyaWFibGVzIGFsZWF0b3JpYXMgZGlzY3JldGFzIDwvaDE+CiAgICA8cD4KICAgIFN1cG9uZ2Ftb3MgcXVlIFwoWCxZXCkgc29uIHZhcmlhYmxlcyBhbGVhdG9yaWFzIGRpc2NyZXRhcywgCiAgICBjb24gdW5hIGZ1bmNpw7NuIGRlIGRlbnNpZGFkIFwoZih4LHkpXCkgdGFsIHF1ZSAKICAgIDxzY3JpcHQgdHlwZT0ibWF0aC90ZXg7IG1vZGU9ZGlzcGxheSI+Zih4LHkpPWMqKHggeSArIDMgXCwgeV57Mn0gKyA0IFwsIHggKyAyIFwsIHkgKyA3KTwvc2NyaXB0PiBzaQogICAgXCh4IFxpbiBbMywxM10sIHkgXGluIFs2LDExXVwpIHkgXCgwXCkgZW4gY3VhbGVzcXVpZXJhCiAgICBvdHJvcyBwdW50b3MuIAogICAgPC9wPgogICAgCiAgICA8cD4gQ2FsY3VsZSBsYSBjb250YW50ZXMgZGUgbm9ybWFsaXphY2nDs24gPGJyPgogICAgXChjPVwpezE6Tk06PTAuMDAwMDQzMzUxOTc0NjgyNDQ2ODoxLjMwMDU1OTI0MDQ3MzQwZS02fSA8L3A+CiAgICAKICAgIDxwPiBDYWxjdWxlIGxvcyBzaWd1aWVudGVzIGVzdGFkw61zdGljb3MKICAgIDxkaXYgY2xhc3M9Im5vdHJ1bmNhdGUiPgo8dGFibGUgYm9yZGVyPSIxIiBjbGFzcz0idGFibGVfZm9ybSI+Cjx0Ym9keT4KPHRyIGNsYXNzID0icm93LWEiPgo8dGQ+LS0tRXN0YWTDrXN0aWNvLS0tPC90ZD4KPHRkPlZhbG9yPC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWIiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XG11X1g8L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PTguMzU3NjUzNzkxMTM6MC4yNTA3Mjk2MTM3MzR9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWEiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XG11X1k8L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PTkuMDA5MDYwNTYyNzE6MC4yNzAyNzE4MTY4ODF9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWIiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+RShYWSk8L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PTc1LjE5NTk5NDI3NzU6Mi4yNTU4Nzk4MjgzM308L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5FKFheMik8L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PTc5LjcyMjQ2MDY1ODE6Mi4zOTE2NzM4MTk3NH08L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYiI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5FKFleMik8L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PTgzLjg3NDEwNTg2NTU6Mi41MTYyMjMxNzU5N308L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cc2lnbWFeMl9YPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj05Ljg3MjA4Mzc2NTY5OjAuMjk2MTYyNTEyOTcxfTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1iIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPlxzaWdtYV4yX1k8L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PTIuNzEwOTMzNjQyOTc6MC4wODEzMjgwMDkyODkxfTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1hIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPlxzaWdtYV97WFl9PC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj0tMC4wOTg2MTQ4ODg5MDM5Oi0wLjAwMjk1ODQ0NjY2NzEyfTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1iIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPlxzaWdtYV9YPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj0zLjE0MTk4NzIzMTk0OjAuMDk0MjU5NjE2OTU4M308L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cc2lnbWFfWTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MS42NDY0OTEzMTI3NTowLjA0OTM5NDczOTM4MjZ9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWIiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XHJobzwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9LTAuMDE5MDYyNDQ2MTcwMjotMC4wMDA1NzE4NzMzODUxMDd9PC90ZD4KPC90cj4KPC90Ym9keT4KPC90YWJsZT4KPC9kaXY+IDwvcD4KICAgIAoKICAgIA==\n"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "text/html": [
       "PGgxPiBDw6FsY3VsbyBkZSBlc3RhZMOtc3RpY29zIHBhcmEgdmFyaWFibGVzIGFsZWF0b3JpYXMgZGlzY3JldGFzIDwvaDE+CiAgICA8cD4KICAgIFN1cG9uZ2Ftb3MgcXVlIFwoWCxZXCkgc29uIHZhcmlhYmxlcyBhbGVhdG9yaWFzIGRpc2NyZXRhcywgCiAgICBjb24gdW5hIGZ1bmNpw7NuIGRlIGRlbnNpZGFkIFwoZih4LHkpXCkgdGFsIHF1ZSAKICAgIDxzY3JpcHQgdHlwZT0ibWF0aC90ZXg7IG1vZGU9ZGlzcGxheSI+Zih4LHkpPWMqKDQgXCwgeF57Mn0gKyA2IFwsIHggeSArIHleezJ9ICsgNSBcLCB4ICsgMiBcLCB5ICsgMik8L3NjcmlwdD4gc2kKICAgIFwoeCBcaW4gWzgsMTddLCB5IFxpbiBbNiwxNF1cKSB5IFwoMFwpIGVuIGN1YWxlc3F1aWVyYQogICAgb3Ryb3MgcHVudG9zLiAKICAgIDwvcD4KICAgIAogICAgPHA+IENhbGN1bGUgbGEgY29udGFudGVzIGRlIG5vcm1hbGl6YWNpw7NuIDxicj4KICAgIFwoYz1cKXsxOk5NOj02Ljk0ODA2MzIyNzM3NTM3ZS02OjIuMDg0NDE4OTY4MjEyNjFlLTd9IDwvcD4KICAgIAogICAgPHA+IENhbGN1bGUgbG9zIHNpZ3VpZW50ZXMgZXN0YWTDrXN0aWNvcwogICAgPGRpdiBjbGFzcz0ibm90cnVuY2F0ZSI+Cjx0YWJsZSBib3JkZXI9IjEiIGNsYXNzPSJ0YWJsZV9mb3JtIj4KPHRib2R5Pgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD4tLS1Fc3RhZMOtc3RpY28tLS08L3RkPgo8dGQ+VmFsb3I8L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYiI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cbXVfWDwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTMuMzUxMjI0NTk2MTowLjQwMDUzNjczNzg4NH08L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cbXVfWTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTAuNDA0Mzc3Mjc5ODowLjMxMjEzMTMxODM5NX08L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYiI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5FKFhZKTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTM4Ljc3MzMxOTQzNzo0LjE2MzE5OTU4MzEyfTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1hIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPkUoWF4yKTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTg1LjkxMjY4MzY4OTo1LjU3NzM4MDUxMDY4fTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1iIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPkUoWV4yKTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTE0Ljc3NTYxMjI5ODozLjQ0MzI2ODM2ODk0fTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1hIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPlxzaWdtYV4yX1g8L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PTcuNjU3NDg1NDcyNzU6MC4yMjk3MjQ1NjQxODJ9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWIiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XHNpZ21hXjJfWTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9Ni41MjQ1NDU3MTY5NjowLjE5NTczNjM3MTUwOX08L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cc2lnbWFfe1hZfTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9LTAuMTM3ODU4NDA4ODYzOi0wLjAwNDEzNTc1MjI2NTg4fTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1iIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPlxzaWdtYV9YPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj0yLjc2NzIxNjE5NTUyOjAuMDgzMDE2NDg1ODY1Nn08L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cc2lnbWFfWTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9Mi41NTQzMTkwMzE5NTowLjA3NjYyOTU3MDk1ODR9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWIiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XHJobzwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9LTAuMDE5NTAzNjExMjM1MjotMC4wMDA1ODUxMDgzMzcwNTZ9PC90ZD4KPC90cj4KPC90Ym9keT4KPC90YWJsZT4KPC9kaXY+IDwvcD4KICAgIAoKICAgIA==\n"
      ],
      "text/plain": [
       "PGgxPiBDw6FsY3VsbyBkZSBlc3RhZMOtc3RpY29zIHBhcmEgdmFyaWFibGVzIGFsZWF0b3JpYXMgZGlzY3JldGFzIDwvaDE+CiAgICA8cD4KICAgIFN1cG9uZ2Ftb3MgcXVlIFwoWCxZXCkgc29uIHZhcmlhYmxlcyBhbGVhdG9yaWFzIGRpc2NyZXRhcywgCiAgICBjb24gdW5hIGZ1bmNpw7NuIGRlIGRlbnNpZGFkIFwoZih4LHkpXCkgdGFsIHF1ZSAKICAgIDxzY3JpcHQgdHlwZT0ibWF0aC90ZXg7IG1vZGU9ZGlzcGxheSI+Zih4LHkpPWMqKDQgXCwgeF57Mn0gKyA2IFwsIHggeSArIHleezJ9ICsgNSBcLCB4ICsgMiBcLCB5ICsgMik8L3NjcmlwdD4gc2kKICAgIFwoeCBcaW4gWzgsMTddLCB5IFxpbiBbNiwxNF1cKSB5IFwoMFwpIGVuIGN1YWxlc3F1aWVyYQogICAgb3Ryb3MgcHVudG9zLiAKICAgIDwvcD4KICAgIAogICAgPHA+IENhbGN1bGUgbGEgY29udGFudGVzIGRlIG5vcm1hbGl6YWNpw7NuIDxicj4KICAgIFwoYz1cKXsxOk5NOj02Ljk0ODA2MzIyNzM3NTM3ZS02OjIuMDg0NDE4OTY4MjEyNjFlLTd9IDwvcD4KICAgIAogICAgPHA+IENhbGN1bGUgbG9zIHNpZ3VpZW50ZXMgZXN0YWTDrXN0aWNvcwogICAgPGRpdiBjbGFzcz0ibm90cnVuY2F0ZSI+Cjx0YWJsZSBib3JkZXI9IjEiIGNsYXNzPSJ0YWJsZV9mb3JtIj4KPHRib2R5Pgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD4tLS1Fc3RhZMOtc3RpY28tLS08L3RkPgo8dGQ+VmFsb3I8L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYiI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cbXVfWDwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTMuMzUxMjI0NTk2MTowLjQwMDUzNjczNzg4NH08L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cbXVfWTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTAuNDA0Mzc3Mjc5ODowLjMxMjEzMTMxODM5NX08L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYiI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5FKFhZKTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTM4Ljc3MzMxOTQzNzo0LjE2MzE5OTU4MzEyfTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1hIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPkUoWF4yKTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTg1LjkxMjY4MzY4OTo1LjU3NzM4MDUxMDY4fTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1iIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPkUoWV4yKTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9MTE0Ljc3NTYxMjI5ODozLjQ0MzI2ODM2ODk0fTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1hIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPlxzaWdtYV4yX1g8L3NjcmlwdD48L3RkPgo8dGQ+ezE6Tk06PTcuNjU3NDg1NDcyNzU6MC4yMjk3MjQ1NjQxODJ9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWIiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XHNpZ21hXjJfWTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9Ni41MjQ1NDU3MTY5NjowLjE5NTczNjM3MTUwOX08L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cc2lnbWFfe1hZfTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9LTAuMTM3ODU4NDA4ODYzOi0wLjAwNDEzNTc1MjI2NTg4fTwvdGQ+CjwvdHI+Cjx0ciBjbGFzcyA9InJvdy1iIj4KPHRkPjxzY3JpcHQgdHlwZT0ibWF0aC90ZXgiPlxzaWdtYV9YPC9zY3JpcHQ+PC90ZD4KPHRkPnsxOk5NOj0yLjc2NzIxNjE5NTUyOjAuMDgzMDE2NDg1ODY1Nn08L3RkPgo8L3RyPgo8dHIgY2xhc3MgPSJyb3ctYSI+Cjx0ZD48c2NyaXB0IHR5cGU9Im1hdGgvdGV4Ij5cc2lnbWFfWTwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9Mi41NTQzMTkwMzE5NTowLjA3NjYyOTU3MDk1ODR9PC90ZD4KPC90cj4KPHRyIGNsYXNzID0icm93LWIiPgo8dGQ+PHNjcmlwdCB0eXBlPSJtYXRoL3RleCI+XHJobzwvc2NyaXB0PjwvdGQ+Cjx0ZD57MTpOTTo9LTAuMDE5NTAzNjExMjM1MjotMC4wMDA1ODUxMDgzMzcwNTZ9PC90ZD4KPC90cj4KPC90Ym9keT4KPC90YWJsZT4KPC9kaXY+IDwvcD4KICAgIAoKICAgIA==\n"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "--------------------------------\n",
      "Done: 2019-09-02 15:28:31.228764\n",
      "Folder: PEP201_corr_discreta\n",
      "Filename: PEP201_corr_discreta-1567456111.23.xml\n",
      "#exes: 5\n"
     ]
    }
   ],
   "source": [
    "np.random.seed(12)\n",
    "me.quick(gen, label, 5, impr=True, cabecera=miCabecera)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "--------------------------------\n",
      "Done: 2019-09-02 15:29:33.732087\n",
      "Folder: PEP201_corr_discreta\n",
      "Filename: PEP201_corr_discreta-1567456173.73.xml\n",
      "#exes: 225\n"
     ]
    }
   ],
   "source": [
    "np.random.seed(123)\n",
    "me.quick(gen, label, 15*15, impr=False, cabecera=miCabecera)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "SageMath 8.1",
   "language": "",
   "name": "sagemath"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 2
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython2",
   "version": "2.7.15+"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 1
}
