"""
The Longstaff-Schwarz model along with Carriere Least Squares Method will be employed to price American options using Monte Carlo
simulation.
"""

from options_pricer_European.models.Monte_Carlo import MonteCarlo   # MonteCarlo class imported to access the stock price simulation
import numpy as np

class MonteCarloAmerican():
    mc = MonteCarlo(98.01, 101.15, 0.0991, 0.01, 0.1644, 'put')

    #calculate_stock_price() is expected to yield - average stock price (using Antithetic Variance Reduction) and cv (control 
    # variate using delta hedging)
    ST, cv = mc.calculate_stock_price()


    



