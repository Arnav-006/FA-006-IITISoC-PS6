import math
import numpy as np
import pandas as pd
import datetime
import scipy.stats as stats
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr

class MonteCarlo:
    """
    A class to price European options using the Monte Carlo simulation method.

    This implementation simulates stock price paths using Geometric Brownian Motion
    to estimate the option's value and its standard error.
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

    @classmethod
    def from_csv(cls, csv_path, K, r, T, option_type, N=1000, M=10000,
                 date_column='Date', price_column='Close',
                 trading_days=252,
                 distribution=stats.norm):
        """
        Create a MonteCarlo instance from a CSV file of historical stock data.
        
        This method is robust to case-insensitive column names and checks for
        data integrity. It calculates the current stock price (S) and historical
        volatility (vol) from the provided data, while other option parameters
        are provided by the user.
        
        The CSV file is expected to have at least a date column and a closing price column.

        Parameters:
        ----------
        cls : MonteCarlo
            The MonteCarlo class.
        csv_path : str
            The file path to the CSV file.
        K : float
            Strike price.
        r : float
            Annualized risk-free interest rate.
        T : float
            Time to maturity in years.
        option_type : str
            'call' or 'put'.
        N : int, optional
            Number of time steps for the simulation (default is 1000).
        M : int, optional
            Number of simulation paths (default is 10000).
        date_column : str, optional
            The name of the date column in the CSV, by default 'Date'.
        price_column : str, optional
            The name of the closing price column in the CSV, by default 'Close'.
        trading_days : int, optional
            The number of trading days in a year for annualizing volatility,
            by default 252.
        distribution : scipy.stats distribution object, optional
            The distribution for random shocks, by default stats.norm.

        Returns:
        -------
        MonteCarlo
            An instance of the MonteCarlo class.

        Raises
        ------
        FileNotFoundError
            If the csv_path does not exist.
        ValueError
            If the specified date or price columns are not found (case-insensitively),
            if the price column contains missing values (NaNs), if there is
            insufficient data (less than 3 rows) to calculate volatility, or if
            the calculated volatility is zero or NaN.
        TypeError
            If the date column cannot be parsed into datetime objects.
        """
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

        return cls(S=S, K=K, vol=volatility, r=r, T=T, option_type=option_type, 
                   N=N, M=M, distribution=distribution)

    def price(self):
        """
        Calculates the European option price and its standard error using Monte Carlo simulation.

        The method follows the standard procedure for risk-neutral simulation of
        Geometric Brownian Motion (GBM).

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
        delta_lnSt = drift + diffusion * Z
        # Start with the initial log price and cumulatively sum the changes to get the log-price path.
        lnSt = np.log(self.S) + np.cumsum(delta_lnSt, axis=0)
        # The terminal log prices are in the last row of the matrix.
        lnST = lnSt[-1]
        # Convert terminal log prices back to standard stock prices.
        ST = np.exp(lnST)

        # --- 4. Calculate Option Payoff for Each Path ---
        if self.option_type.lower() == 'call':
            payoffs = np.maximum(0, ST - self.K)
        elif self.option_type.lower() == 'put':
            payoffs = np.maximum(0, self.K - ST)
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