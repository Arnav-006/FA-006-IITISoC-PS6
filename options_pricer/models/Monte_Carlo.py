import math
import numpy as np
import pandas as pd
import datetime
import scipy.stats as stats
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr

class MonteCarlo:
    N=1000
    M=10000
    """
        N: number of time steps
        M: number of simulations
    """

    """
    In order to implement theta option Greek we need to accept a deviation parameter 'dev' for time to maturiy.
    """

    def __init__(self, S, K, vol, r, T, option_type, dev_1=0, dev_2=0):
        self.S = S  
        self.K = K
        self.vol = vol+dev_2
        self.r = r
        self.T = T+dev_1
        self.option_type = option_type
        """
        S: stock price
        K: strike price
        vol: volatility
        r: risk-free interest rate
        T: time to maturity in years
        type: 'call' or 'put'
        """

    def compute_constants(self):
        self.dt = self.T/MonteCarlo.N
        self.nudt = (self.r - 0.5*self.vol**2)*self.dt
        self.volsdt = self.vol*np.sqrt(self.dt)
        self.lnS = np.log(self.S)

    def calculate_option_price(self, lnSt, dev=0):
        # Compute Expectation and SE
        ST = np.exp(lnSt) + dev

        if self.option_type == 'call':
            # For call option
            CT = np.maximum(0, ST - self.K)
            C0 = np.exp(-self.r*self.T)*np.sum(CT[-1])/MonteCarlo.M
        elif self.option_type == 'put':
            # For put option
            CT = np.maximum(0, self.K - ST)
            C0 = np.exp(-self.r*self.T)*np.sum(CT[-1])/MonteCarlo.M

        return C0, CT

    def calculate_stock_price(self):
        self.compute_constants()

        # Monte Carlo Simulation
        Z = np.random.normal(size=(MonteCarlo.N, MonteCarlo.M))
        delta_lnSt = self.nudt + self.volsdt*Z
        lnSt = self.lnS + np.cumsum(delta_lnSt, axis=0)
        lnSt = np.concatenate( (np.full(shape=(1, MonteCarlo.M), fill_value=self.lnS), lnSt ) )

        return lnSt

    def simulate(self):

        C0, CT = self.calculate_option_price(self.calculate_stock_price())

        sigma = np.sqrt( np.sum( (CT[-1] - C0)**2) / (MonteCarlo.M-1) )
        SE = sigma/np.sqrt(MonteCarlo.M)

        return C0, SE