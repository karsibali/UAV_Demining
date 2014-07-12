__author__ = 'sarslan'
import numpy as np
from scipy.stats import rv_discrete
from scipy.io import savemat


if __name__ == '__main__':
    sample_size = 1000

    C = np.arange(2)
    C_CPT = (0.5, 0.5)
    Ran = rv_discrete(values=(C, C_CPT))
    cloudy = Ran.rvs(size=sample_size)

    S = np.arange(2)
    S_CPT = (0.5, 0.5)
    Ran = rv_discrete(values=(S, S_CPT))
    n_cl = cloudy==0
    cl = cloudy==1
    spr0 = Ran.rvs(size=cloudy[n_cl].size)
    S_CPT = (0.9, 0.1)
    Ran = rv_discrete(values=(S, S_CPT))
    spr1 = Ran.rvs(size=cloudy[cl].size)
    spr = np.zeros(sample_size, dtype=int)
    spr[n_cl] = spr0
    spr[cl] = spr1

    R = np.arange(2)
    R_CPT = (0.8, 0.2)
    Ran = rv_discrete(values=(R, R_CPT))
    rain0 = Ran.rvs(size=cloudy[n_cl].size)
    R_CPT = (0.2, 0.8)
    Ran = rv_discrete(values=(R, R_CPT))
    rain1 = Ran.rvs(size=cloudy[cl].size)
    rain = np.zeros(sample_size, dtype=int)
    rain[n_cl] = rain0
    rain[cl] = rain1

    w_idx = np.zeros((sample_size, 4), dtype=bool)
    w_idx[:,0] = np.logical_and(spr==0, rain==0)
    w_idx[:,1] = np.logical_and(spr==1, rain==0)
    w_idx[:,2] = np.logical_and(spr==0, rain==1)
    w_idx[:,3] = np.logical_and(spr==1, rain==1)

    W = np.arange(2)
    W_CPT = (1, 0)
    Ran = rv_discrete(values=(W, W_CPT))
    wet0 = Ran.rvs(size=np.sum(w_idx[:,0]))
    W_CPT = (0.1, 0.9)
    Ran = rv_discrete(values=(W, W_CPT))
    wet1 = Ran.rvs(size=np.sum(w_idx[:,1]))
    W_CPT = (0.1, 0.9)
    Ran = rv_discrete(values=(W, W_CPT))
    wet2 = Ran.rvs(size=np.sum(w_idx[:,2]))
    W_CPT = (0.01, 0.99)
    Ran = rv_discrete(values=(W, W_CPT))
    wet3 = Ran.rvs(size=np.sum(w_idx[:,3]))
    wet = np.zeros(sample_size, dtype=int)
    wet[w_idx[:,0]] = wet0
    wet[w_idx[:,1]] = wet1
    wet[w_idx[:,2]] = wet2
    wet[w_idx[:,3]] = wet3

    samples = np.column_stack((cloudy, spr, rain, wet))
    savemat('weather-samples', {'samples': samples})
    pass