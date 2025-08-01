import math
import numpy as np
import pandas as pd
import datetime
import scipy.stats as stats
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr

class asian:
    """
    A class to price Asian options with an arithmetic average price using the Monte Carlo simulation method.

    This implementation simulates stock price paths using Geometric Brownian Motion
    to estimate the option's value, where the payoff is determined by the average stock price over the path.
    """

    def __init__(self, S, K, vol, r, T, option_type, N=1000, M=10000, distribution=stats.norm):
        """
        Initializes the Monte Carlo pricer with option and simulation parameters.

        Parameters:
        ----------
        S : float
            Current stock price (e.g., 100).
        K : float
            Strike price of the option (e.g., 105).
        vol : float
            Annualized volatility of the underlying stock (e.g., 0.2 for 20%).
        r : float
            Annualized risk-free interest rate (e.g., 0.05 for 5%).
        T : float
            Time to maturity in years (e.g., 1 for one year).
        option_type : str
            Type of the option, must be either 'call' or 'put'.
        N : int, optional
            Number of time steps in each simulation path (default is 1000).
            More steps lead to a more accurate path simulation.
        M : int, optional
            Number of simulation paths to generate (default is 10000).
            More paths lead to a more accurate price estimate and lower standard error.
        distribution : scipy.stats distribution object, optional
            The distribution for generating random shocks (default is stats.norm for a standard normal distribution).
        """
        self.S = S  
        self.K = K
        self.vol = vol
        self.r = r
        self.T = T
        self.option_type = option_type
        self.N = N
        self.M = M
        self.distribution = distribution


    def simulate(self):
        """
        Calculates the Asian option price and its standard error using Monte Carlo simulation.

        The method follows the standard procedure for risk-neutral simulation of
        Geometric Brownian Motion (GBM). The payoff is based on the arithmetic
        average of the stock prices at discrete time steps, including the initial price.

        Returns:
        -------
        tuple[float, float]
            A tuple containing:
            - The estimated option price.
            - The standard error of the estimated price, which quantifies the
              precision of the Monte Carlo estimate.
        
        Raises:
        ------
        ValueError
            If the `option_type` is not 'call' or 'put'.
        """
        # --- 1. Set up Simulation Parameters for Geometric Brownian Motion ---
        # Time step size
        dt = self.T / self.N
        # Risk-neutral drift component for the log-price process
        drift = (self.r - 0.5 * self.vol**2) * dt
        # Diffusion (random) component for the log-price process
        diffusion = self.vol * np.sqrt(dt)

        # --- 2. Generate Random Shocks ---
        # Create a matrix of random numbers from the specified distribution.
        # Dimensions are (N steps) x (M simulations).
        Z = self.distribution.rvs(size=(self.N, self.M))

        # --- 3. Simulate Stock Price Paths ---
        # Calculate the change in log price at each step for every simulation path.
        delta_ln_S = drift + diffusion * Z
        # Cumulatively sum the log changes to get the log-price path for N steps.
        ln_S_paths = np.log(self.S) + np.cumsum(delta_ln_S, axis=0)
        # Prepend the initial log price to each path to include it in the average.
        ln_S_paths = np.vstack([np.full(self.M, np.log(self.S)), ln_S_paths])
        # Convert log-price paths to price paths.
        price_paths = np.exp(ln_S_paths)
        # Calculate the arithmetic average price for each simulation path.
        average_prices = np.mean(price_paths, axis=0)

        # --- 4. Calculate Option Payoff for Each Path ---
        if self.option_type.lower() == 'call':
            payoffs = np.maximum(0, average_prices - self.K)
        elif self.option_type.lower() == 'put':
            payoffs = np.maximum(0, self.K - average_prices)
        else:
            raise ValueError("option_type must be 'call' or 'put'")

        # --- 5. Discount Payoffs and Calculate Final Price and Standard Error ---
        # Discount each individual payoff back to its present value.
        discounted_payoffs = np.exp(-self.r * self.T) * payoffs

        # The final option price is the average (mean) of all discounted payoffs.
        option_price = np.mean(discounted_payoffs)

        # Calculate the standard error of the mean to measure the estimate's accuracy.
        # Use ddof=1 for the sample standard deviation (dividing by M-1).
        std_dev = np.std(discounted_payoffs, ddof=1)
        standard_error = std_dev / np.sqrt(self.M)

        return option_price, standard_error