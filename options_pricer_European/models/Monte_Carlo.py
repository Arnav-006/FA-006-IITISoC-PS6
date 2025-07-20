"""
The code given below has errors in the Control Variates (no error with delta_calc() or delta function in BlackScholes class) - the
obtained standard error is exceptionally high.
"""

import math
import numpy as np
import pandas as pd
import datetime
import scipy.stats as stats
import matplotlib.pyplot as plt
# from pandas_datareader import data as pdr
from Black_Scholes import BlackScholes

class MonteCarlo:
    N=100
    M=100
    """
        N: number of time steps
        M: number of simulations
    """

    """
    In order to implement theta option Greek we need to accept a deviation parameter 'dev' for time to maturiy.
    """

    def __init__(self, S, K, vol, r, T, option_type, dev_0=0, dev_1=0, dev_2=0):
        self.S = S+dev_0
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
        self.erdt = np.exp(self.r*self.dt)
        self.cv = 0
        self.beta1 = -1

    """
    Calculating delta:
    """

    def delta_calc(self):
        "Calculate delta of an option"
        d1 = (np.log(self.S/self.K) + (self.r + self.vol**2/2)*self.T)/(self.vol*np.sqrt(self.T))
        try:
            if self.option_type == "call":
                delta_calc = stats.norm.cdf(d1, 0, 1)
            elif self.option_type == "put":
                delta_calc = -stats.norm.cdf(-d1, 0, 1)
            return delta_calc
        except:
            print("Please confirm option type, either 'call' for Call or 'put' for Put!")

    """
    Further build-up on the control variates method to reduce variance:
    """

    def calculate_option_price(self, ST, cv):
        if self.option_type == 'call':
            #For call option
            CT = np.maximum(0, ST[-1] - self.K) + self.beta1*cv[-1]
        elif self.option_type == 'put':
            #For put option
            CT = np.maximum(0, self.K - ST[-1]) + self.beta1*cv[-1]

        C0 = np.exp(-self.r*self.T)*np.sum(CT)/MonteCarlo.M

        return C0, CT


    """
    Further build-up on the antithetic variates method to reduce variance:
    """

    # def calculate_option_price(self, lnSt1, lnSt2):
    #     # Compute Expectation and SE
    #     ST1 = np.exp(lnSt1) 
    #     ST2 = np.exp(lnSt2) 

    #     if self.option_type == 'call':
    #         # For call option
    #         CT = (np.maximum(0, ST1[-1] - self.K) + np.maximum(0, ST2[-1] - self.K))*0.5
    #         C0 = np.exp(-self.r*self.T)*np.sum(CT)/MonteCarlo.M
    #     elif self.option_type == 'put':
    #         # For put option
    #         CT = (np.maximum(0, self.K - ST1[-1]) + np.maximum(0, self.K - ST2[-1]))*0.5
    #         C0 = np.exp(-self.r*self.T)*np.sum(CT)/MonteCarlo.M

    #     return C0, CT

    """
    Calculation of stock price using control variates to reduce variance:
    """
    def calculate_stock_price(self):
        self.compute_constants()

        # Monte Carlo Simulation
        Z = np.random.normal(size=(MonteCarlo.N, MonteCarlo.M))
        delta_St=self.nudt + self.volsdt*Z
        ST = self.S*np.cumprod( np.exp(delta_St), axis=0)
        ST = np.concatenate( (np.full(shape=(1, MonteCarlo.M), fill_value=self.S), ST ) )
        # bs=BlackScholes(ST[:-1].T, self.K, self.vol, self.r, np.linspace(self.T,0,MonteCarlo.N))
        # deltaSt = bs.delta('call').T
        deltaSt = self.delta_calc()
        cv = np.cumsum(deltaSt*(ST[1:] - ST[:-1]*self.erdt), axis=0)

        return ST, cv



    """
    Calculation of stock price using antithetic variates to reduce variance:
    """

    # def calculate_stock_price(self):
    #     self.compute_constants()

    #     # Monte Carlo Simulation
    #     Z = np.random.normal(size=(MonteCarlo.N, MonteCarlo.M))
    #     delta_lnSt1 = self.nudt + self.volsdt*Z
    #     delta_lnSt2 = self.nudt - self.volsdt*Z
    #     lnSt1 = self.lnS + np.cumsum(delta_lnSt1, axis=0)
    #     lnSt2 = self.lnS + np.cumsum(delta_lnSt2, axis=0)
    #     lnSt1 = np.concatenate( (np.full(shape=(1, MonteCarlo.M), fill_value=self.lnS), lnSt1 ) )
    #     lnSt2 = np.concatenate( (np.full(shape=(1, MonteCarlo.M), fill_value=self.lnS), lnSt2 ) )

    #     return lnSt1, lnSt2

    def simulate(self):

        C0, CT = self.calculate_option_price(self.calculate_stock_price()[0], self.calculate_stock_price()[1])

        sigma = np.sqrt( np.sum( (CT - C0)**2) / (MonteCarlo.M-1) )
        SE = sigma/np.sqrt(MonteCarlo.M)

        return C0, SE
    
mc=MonteCarlo(S=101.15, K=98.01, vol=0.0991, r=0.015, T=0.164, option_type='call')    
print(f"Option Price: {mc.simulate()[0]}")
print(f"Standard Error: {mc.simulate()[1]}")