import math
import numpy as np
import pandas as pd
import datetime
import scipy.stats as stats
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr

class MonteCarlo:
    N=100
    M=10000
    """
        N: number of time steps
        M: number of simulations
    """

    def __init__(self, S, K, vol, r, T):
        self.S = S  
        self.K = K
        self.vol = vol
        self.r = r
        self.T = T
        """
        S: stock price
        K: strike price
        vol: volatility
        r: risk-free interest rate
        T: time to maturity in years
        """

    def compute_constants(self):
        self.dt = self.T/MonteCarlo.N
        self.nudt = (self.r - 0.5*self.vol**2)*self.dt
        self.volsdt = self.vol*np.sqrt(self.dt)
        self.lnS = np.log(self.S)

    def simulate(self):
        self.compute_constants()

        # Monte Carlo Simulation
        Z = np.random.normal(size=(MonteCarlo.N, MonteCarlo.M))
        delta_lnSt = self.nudt + self.volsdt*Z
        lnSt = self.lnS + np.cumsum(delta_lnSt, axis=0)
        lnSt = np.concatenate( (np.full(shape=(1, MonteCarlo.M), fill_value=self.lnS), lnSt ) )

        # Compute Expectation and SE
        ST = np.exp(lnSt)
        CT = np.maximum(0, ST - self.K)
        C0 = np.exp(-self.r*self.T)*np.sum(CT[-1])/MonteCarlo.M

        sigma = np.sqrt( np.sum( (CT[-1] - C0)**2) / (MonteCarlo.M-1) )
        SE = sigma/np.sqrt(MonteCarlo.M)

        return C0, SE