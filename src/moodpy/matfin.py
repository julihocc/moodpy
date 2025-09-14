#!/usr/bin/env python
# coding: utf-8

# Required dependencies with graceful error handling
try:
    import numpy as np
    _HAS_NUMPY = True
except ImportError:
    np = None
    _HAS_NUMPY = False

try:
    from tabulate import tabulate
    _HAS_TABULATE = True
except ImportError:
    tabulate = None
    _HAS_TABULATE = False

from . import tools

frec = {1:"anualmente", 2:"semestralmente", 3:"cuatrimestral", 4:"trimestralmente",
        6:"bimestralmente", 12: "mensualmente"}

per ={1:"año", 2:"semestre", 3:"cuatrimestre", 4:"trimestre", 6:"bimestre", 
      12:"mes"}

tempo = per ={1:"anual", 2:"semestral", 3:"cuatrimestral", 4:"trimestral", 6:"bimestral", 12:"mensual"}

def get_frec():
    f = np.random.choice(list(frec.keys()))
    return {"f":f, "frecuencia":frec[f], "periodo":per[f], "temporalidad":tempo[f]}

def gen_T(f,_N, min_N=5):
    while True:
        N = np.random.poisson(_N)
        T = np.around(_N/f).astype(int)
        if T!=0 and T*f>min_N:
            return {"T":T}
        
def alpha(j,N):
    return (1-(1+j)**(-N))/j

def gen_rates(r_mean, f):
    while True:
        r_pct = np.random.poisson(r_mean*100)
        r = np.around(1.*r_pct/100,2)
        j = np.around(r/f,4)
        r = j*f
        j_pct = np.around(j*100, 2)
        r_pct = np.around(r*100, 2)
        if j>0:
            return {"j":j, "r":r, "j_pct":j_pct, "r_pct":r_pct}

def gen_flux(f, N_mean, j, scale = 0.5, lower=-np.inf, upper=np.inf, sim="normal"):
    X = {}
    while True:
        X.update(gen_T(f, N_mean))
        X["F0"] = -np.random.poisson(1000)*1000
        X["N"] = np.int(f*X["T"])
        R = -X["F0"]/alpha(j, X["N"])//1000
        if sim=="normal":
            future =  1000*tools.int_normal(m=R, s=scale*R, n=X["N"], a = lower, b=upper)
        elif sim=="poisson":
            future = 1000*np.random.poisson(R, size=X["N"])
        X["F"] = np.concatenate([[X["F0"]],future])
        return X
    
def VPN(F, j):
    vpn = 0
    for k,Fk in enumerate(F):
        vpn+= Fk*(1+j)**(-k)
    return {"VPN": vpn}

def tab_flux(F, f= None):
    header = []
    values = []
    for k, Fk in enumerate(F):
        if f is None:
            header.append("Periodo {}".format(k))
        else:
            periodo = per[f].title()
            header.append("{} {}".format(periodo, k))
        values.append(r"\${}".format(Fk))
    tab =[header, values]
    tab[0][0] = "Inversión"
    tab[1][0] = r"-\${}".format(-F[0])
    html_tab = tabulate(tab, headers="firstrow", tablefmt="html")
    return html_tab

def tab_flux_vertical(F, f=None, fmt="html"):
    tab = []
    for k, Fk in enumerate(F):
        row = []
        if f is None:
            idx = "Periodo {}".format(k)
        else:
            periodo = per[f].title()
            idx = "{} {}".format(periodo, k)
        row.append(r"{}".format(idx))
        row.append(r"${}".format(Fk))
        tab.append(row)
    #print(tab)
    tab[0][0] = r"Inversión"
    tab[0][1] = r"-${}".format(-F[0])
    html_tab = tabulate(tab, tablefmt=fmt)
    return {"tab": html_tab}
    
def TIR(F):
    output = {}
    try:
        rc = np.real_if_close(np.roots(F))
        #print(rc)
        r = np.array([np.real(r0) for r0 in rc if np.isclose(np.imag(r0),0)])
        idxs = 1<r
        r0 = np.sort(r[idxs])[0]
        v0 = np.polyval(F,r0)
        if np.abs(v0)<1e-3:
            output["TIR"] = float(r0-1)
            #return r0-1
    except Exception as e:
        # Handle any errors in TIR calculation
        output["TIR"] = None
    return output
