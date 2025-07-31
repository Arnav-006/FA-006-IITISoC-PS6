import math
import numpy as np
import pandas as pd
import datetime
import scipy.stats as stats
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr

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
    def __init__(self, S, K, vol, r, T, option_type, dev_0=0, dev_1=0, dev_2=0, distribution=stats.norm):
        self.S = S+dev_0
        self.K = K
        self.vol = vol+dev_2
        self.r = r
        self.T = T+dev_1
        self.option_type = option_type
        self.distribution = distribution
        """
        S: stock price
        K: strike price
        vol: volatility
        r: risk-free interest rate
        T: time to maturity in years
        type: 'call' or 'put'
        distribution: distribution for generating random shocks, default is standard normal
        """

    """
    Parses data from the CSV file, to get the value of the volatility.
    This requires a CSV file path to be passed from the user as an argument of this function implemented on the class while creating
    an instance of the class.
    """
    @classmethod
    def from_csv_simulate(self, cls, csv_path, K, r, T, option_type, N=1000, M=10000,
                 date_column='Date', price_column='Close',
                 trading_days=252,
                 distribution=stats.norm):
        try:
            data = pd.read_csv(csv_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: The file at path '{csv_path}' was not found.")

        # --- Column Name Robustness (Case-Insensitive) ---
        col_map = {c.lower(): c for c in data.columns}
        lower_date_col, lower_price_col = date_column.lower(), price_column.lower()

        if lower_date_col not in col_map:
            raise ValueError(f"Date column '{date_column}' not found. Available columns: {list(data.columns)}")
        if lower_price_col not in col_map:
            raise ValueError(f"Price column '{price_column}' not found. Available columns: {list(data.columns)}")
            
        actual_date_col, actual_price_col = col_map[lower_date_col], col_map[lower_price_col]

        # --- Data Processing and Integrity Checks ---
        try:
            data[actual_date_col] = pd.to_datetime(data[actual_date_col])
        except Exception as e:
            raise TypeError(f"Could not parse date column '{actual_date_col}'. Ensure it contains valid date formats. Error: {e}")

        data.set_index(actual_date_col, inplace=True)
        data.sort_index(inplace=True)

        if data[actual_price_col].isnull().any():
            raise ValueError(f"Price column '{actual_price_col}' contains missing (NaN) values. Please clean the data.")

        if len(data) < 3:
            raise ValueError(f"Insufficient data to calculate volatility. Need at least 3 data points, but found {len(data)}.")

        # --- Parameter Calculation ---
        S = data[actual_price_col].iloc[-1]
        log_returns = np.log(data[actual_price_col] / data[actual_price_col].shift(1))
        volatility = log_returns.std() * np.sqrt(trading_days)

        if pd.isna(volatility) or volatility == 0:
            raise ValueError("Calculated volatility is zero or NaN. Check for constant prices in the data.")
        
        instance = cls(S=S, K=K, vol=volatility, r=r, T=T, option_type=option_type, N=N, M=M, distribution=distribution)   
        instance.data = data  
        C0, CT = self.calculate_option_price(data)
        sigma = np.sqrt( np.sum( (CT[-1] - C0)**2) / (MonteCarlo.M-1) )
        SE = sigma/np.sqrt(MonteCarlo.M)

        return C0, SE


    def compute_constants(self):
        self.dt = self.T/MonteCarlo.N
        self.nudt = (self.r - 0.5*self.vol**2)*self.dt
        self.volsdt = self.vol*np.sqrt(self.dt)
        self.lnS = np.log(self.S)

    def calculate_option_price(self, ST):
        # Compute Expectation and SE

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

        return np.exp(lnSt)

    def simulate(self):

        C0, CT = self.calculate_option_price(self.calculate_stock_price())

        sigma = np.sqrt( np.sum( (CT[-1] - C0)**2) / (MonteCarlo.M-1) )
        SE = sigma/np.sqrt(MonteCarlo.M)

        return C0, SE