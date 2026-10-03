"""
matrizDeCorrelacion-Copy1

Migrated from legacy generator: matrizDeCorrelacion-Copy1.ipynb
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
   "execution_count": 1,
   "metadata": {
    "collapsed": false,
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "import toMoodle as me\n",
    "import random as rd\n",
    "import numpy as np\n",
    "import sympy as spy\n",
    "import datetime as dt\n",
    "#import base64\n",
    "import matplotlib.pyplot as plt\n",
    "from scipy import stats\n",
    "#import sys"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "def corr(x, y):\n",
    "    xm = np.mean(x, axis=None)\n",
    "    ym = np.mean(y, axis=None)\n",
    "    cxy = np.sum((x-xm)*(y-ym))\n",
    "    cxx = np.sum((x-xm)**2)\n",
    "    cyy = np.sum((y-ym)**2)\n",
    "    return cxy/np.sqrt(cxx*cyy)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "NaN\n"
     ]
    }
   ],
   "source": [
    "rechazos = 0\n",
    "totalPruebas = 0\n",
    "imprimir = False\n",
    "betas = [.01,0.05,0.10]\n",
    "for test in range(totalPruebas):\n",
    "    if imprimir: print \"test:\",str(test+1),16*\"-\"\n",
    "    \"\"\"\n",
    "    l = len(betas)\n",
    "    i = np.random.randint(l)\n",
    "    beta = betas[i].n(digits=3)\n",
    "    #\"\"\"\n",
    "    mu = np.random.poisson(100, size = 4)\n",
    "    x = np.empty([1,1])\n",
    "    for m in mu:\n",
    "        x=np.append(x, 1.*np.random.poisson(m,size=15))\n",
    "    print(x)\n",
    "    #np.resize(M, (2,3))\n",
    "    if imprimir: print(M)\n",
    "    sesgo = 1.*np.random.poisson(15,size=(2,3))\n",
    "    sesgo[0][1] = 0\n",
    "    sesgo[1][0] = 0\n",
    "    if imprimir: print(sesgo)\n",
    "    M+= sesgo \n",
    "    if imprimir: print(M)\n",
    "    if imprimir: print(beta)\n",
    "    T = M[0]+M[1]\n",
    "    if imprimir: print(T)\n",
    "    totalFila = np.sum(M, axis=1)\n",
    "\n",
    "    xx = totalFila[0]\n",
    "    xy = totalFila[1]\n",
    "    total = np.sum(T)\n",
    "\n",
    "    E = [T*xx/total, T*xy/total]\n",
    "    if imprimir: print(\"E=\",E)\n",
    "    O = [M[0],M[1]]\n",
    "    if imprimir: print(\"O=\",O)\n",
    "\n",
    "    if imprimir: print = lambda \"desv(E,O: \",desv(E,O))\n",
    "    chi2 = np.sum(desv(E,O), axis=None)\n",
    "\n",
    "    if imprimir: print(\"chi2 %.4f\" % (chi2))\n",
    "\n",
    "    nu = 6-1\n",
    "\n",
    "    def F(x):\n",
    "        return stats.chi2(nu).cdf(x)\n",
    "    def iF(p):\n",
    "        return stats.chi2(nu).ppf(p)\n",
    "\n",
    "\n",
    "    valorp = 1 - F(chi2)\n",
    "    if imprimir: print(\"valor p =\", valorp)\n",
    "\n",
    "    b = 0.05\n",
    "\n",
    "    if valorp <= b:\n",
    "        rechazos=rechazos+1\n",
    "print 1.*rechazos/totalPruebas"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "def generoVsMaterias(lista=[], prueba=False, betas = [.01, 0.05, .10]): \n",
    "    l = len(betas)\n",
    "    i = np.random.randint(l)\n",
    "    beta = betas[i].n(digits=3)\n",
    "    \n",
    "    M = 1.*np.random.poisson(15,size=(2,3))\n",
    "    #np.resize(M, (2,3))\n",
    "    if imprimir: print(M)\n",
    "    sesgo = 1.*np.random.poisson(15,size=(2,3))\n",
    "    sesgo[0][1] = 0\n",
    "    sesgo[1][0] = 0\n",
    "    if imprimir: print(sesgo)\n",
    "    M+= sesgo \n",
    "    if imprimir: print(M)\n",
    "    T = M[0]+M[1]\n",
    "    if imprimir: print(T)\n",
    "    totalFila = np.sum(M, axis=1)\n",
    "\n",
    "    xx = totalFila[0]\n",
    "    xy = totalFila[1]\n",
    "    total = np.sum(T)\n",
    "\n",
    "    E = [T*xx/total, T*xy/total]\n",
    "    if imprimir: print(\"E=\",E)\n",
    "    O = [M[0],M[1]]\n",
    "    if imprimir: print(\"O=\",O)\n",
    "\n",
    "    if imprimir: print = lambda \"desv(E,O: \",desv(E,O))\n",
    "    chi2 = np.sum(desv(E,O), axis=None)\n",
    "\n",
    "    if imprimir: print(\"chi2 %.4f\" % (chi2))\n",
    "\n",
    "    nu = 6-1\n",
    "\n",
    "    def F(x):\n",
    "        return stats.chi2(nu).cdf(x)\n",
    "    def iF(p):\n",
    "        return stats.chi2(nu).ppf(p)\n",
    "\n",
    "\n",
    "    valorp = 1 - F(chi2)\n",
    "    if imprimir: print(\"valor p =\", valorp)\n",
    "\n",
    "    if imprimir: print(\"Con un nivel de significación: \"+str(b))\n",
    "    if valorp > beta:\n",
    "        myMC = \"{1:MC:=acepta~rechaza}\"\n",
    "    else:\n",
    "        myMC = \"{1:MC:acepta~=rechaza}\"\n",
    "    \n",
    "    linea=[]    \n",
    "    ejercicio = \"<p> Supongamos que un grupo de estudiantes, la siguiente tabla\"\n",
    "    ejercicio += \"representa el número de hombres y mujeres que toman\"\n",
    "    ejercicio += \"ingenierías, humanidades y negocios como sus materias principales.</p>\"\n",
    "    \n",
    "    htmlTable = [\"<p> <table style=\\\"width:100%\\\" border=\\\"1\\\" >\",\n",
    "                 \"<tr>\",\n",
    "                 \"<th>\",\" \",\"</th>\",\n",
    "                 \"<th>\",\"Ingenierías\",\"</th>\",\n",
    "                 \"<th>\",\"Humanidades\",\"</th>\",\n",
    "                 \"<th>\",\"Negocios\",\"</th>\",\n",
    "                 \"</tr>\",\n",
    "                 \"<tr>\",\n",
    "                 \"<th>\",\"Hombres\",\"</th>\",\n",
    "                 \"<td>\",str(M[0][0]),\"</td>\",\n",
    "                 \"<td>\",str(M[0][1]),\"</td>\",\n",
    "                 \"<td>\",str(M[0][2]),\"</td>\",\n",
    "                 \"</tr>\",\n",
    "                 \"<tr>\",\n",
    "                 \"<th>\",\"Mujeres\",\"</th>\",\n",
    "                 \"<td>\",str(M[1][0]),\"</td>\",\n",
    "                 \"<td>\",str(M[1][1]),\"</td>\",\n",
    "                 \"<td>\",str(M[1][2]),\"</td>\",\n",
    "                 \"</tr>\",\n",
    "                 \"</table> </p>\"\n",
    "                ]\n",
    "    \n",
    "    for cel in htmlTable:\n",
    "        ejercicio = ejercicio + cel\n",
    "    \n",
    "    ejercicio += \"<p> Nuestra hipótesis (nula) es que la elección de materias es independiente del género.\"\n",
    "    ejercicio += \"Determine si esta se acepta o rechaza a un nivel de significación de \"+str(beta)+\"</p>\"\n",
    "    \n",
    "    linea.append(ejercicio)\n",
    "    \n",
    "    MC = \"<p> Estadístico chi-cuadrado =\"+me.NM(chi2)+\"</p>\"\n",
    "    MC = MC+\"<p> valor-p=\"+me.NM(valorp)+\"</p>\"\n",
    "    MC = MC+\"<p> La hipótesis nula Ho se \"+myMC+\"</p>\"\n",
    "\n",
    "    #print MC\n",
    "    linea.append(MC)\n",
    "\n",
    "    #print linea\n",
    "    lista.append(linea)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "bloques=17*5\n",
    "ejercicios=[]\n",
    "\n",
    "for k in range(bloques):\n",
    "    generoVsMaterias(ejercicios)\n",
    "mil_exes=[]; mil_sol=[]\n",
    "for elemento in ejercicios:\n",
    "    #print elemento\n",
    "    mil_exes.append(elemento[0])\n",
    "    mil_sol.append(elemento[1])\n",
    "me.ExeToMoodle(\"generoVsMateriasSesgado\", mil_exes, mil_sol)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "SageMath 7.5.1",
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
   "version": "2.7.13"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 0
}
