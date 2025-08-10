"""
The Longstaff-Schwarz model along with Carriere Least Squares Method will be employed to price American options using Monte Carlo
simulation.
"""

from options_pricer_European.models.Monte_Carlo import MonteCarlo   # MonteCarlo class imported to access the stock price simulation
import numpy as np
from statsmodels.nonparametric.smoothers_lowess import lowess
from scipy.interpolate import interp1d
import statsmodels.api as sm
import matplotlib.pyplot as plt

class MonteCarloAmerican():
    def __init__(self, S, K, vol, r, T, option_type):
        self.S = S
        self.K = K
        self.vol = vol
        self.r = r
        self.T = T
        self.option_type = option_type
        self.discount = np.exp(-self.r*self.T/MonteCarlo.N)  # Discount factor for each time step
        self.CF=0
        self.S=0
        
        """
        S: stock price
        K: strike price
        vol: volatility
        r: risk-free interest rate
        T: time to maturity in years
        type: 'call' or 'put'
        """

    def calculate_stock_price_ame(self):
        mc = MonteCarlo(self.S, self.K, self.vol, self.r, self.T, 'put')

        """
        calculate_stock_price() is expected to yield - average stock price and cv (control variate using delta hedging)
        """
        ST, cv = mc.calculate_stock_price()     # Stock price and delta hedging control variate

        return ST, cv

    def intrinsic_value(self, ST, cv):
        CF = np.maximum(self.K - ST, 0) + cv
        
        return CF

    def backtrack(self):
        
        self.CF = self.intrinsic_value(*self.calculate_stock_price_ame())  # Cash flow matrix initialized with intrinsic values
        self.S = self.calculate_stock_price_ame()[0]  # Stock price matrix

        for n in range(MonteCarlo.N-1, 0, -1):                 # walk from T-Δt to Δt
            itm = self.CF[:,n] > 0                      # in-the-money mask
            if not itm.any():                      # no ITM path → go to previous step
                self.CF[:,n] = self.CF[:,n+1]*self.discount
                continue

            # --- Carriere: non-parametric regression on ITM paths only ---
            S_itm, Y  = self.S[itm,n], self.CF[itm,n+1]*self.discount
        
            cont_val  = lowess(endog=Y, exog=S_itm, frac=0.3, return_sorted=False)

            # Predict continuation value for *all* paths using nearest-neighbor rule
        
            f = interp1d(S_itm, cont_val, fill_value="extrapolate")
            C_hat = f(self.S[:,n])                       # continuation estimate

            # --- Optimal decision ---
            exercise = self.CF[:,n] > C_hat             # boolean exercise decision
            self.CF[exercise, n]  = self.CF[exercise, n]     # keep immediate payoff
            self.CF[~exercise, n] = self.CF[~exercise,n+1]*self.discount


        # Price estimate (high bias)                
        V0_high = self.CF[:,1].mean()*self.discount


    def plot_data(self):
        """
        Preparing data for plotting
        """

        n_plot = 6
        exercise_flag = (self.CF[:,n_plot] > self.CF[:,n_plot+1]*self.discount)
        stock_n  = self.S[:, n_plot]
        payoff_n = self.CF[:, n_plot]                   # realised cash flow at that step
        cont_n  = self.CF[:, n_plot+1]*self.discount        # continuation value
        ex_flag = payoff_n > cont_n        #exercise flag

        plt.figure(figsize=(7,5))
        plt.scatter(stock_n[ex_flag], payoff_n[ex_flag],  s=8, c='C3', label='exercise')
        plt.scatter(stock_n[~ex_flag], cont_n[~ex_flag], s=8, c='C0', label='continue')

        def linreg(x,y):
            X = sm.add_constant(x)
            return sm.OLS(y, X).fit()

        fit_ex  = linreg(stock_n[exercise_flag], payoff_n[exercise_flag])   # exercised
        fit_con = linreg(stock_n[~exercise_flag], cont_n[~exercise_flag])  # continued

        xgrid = np.linspace(stock_n.min(), stock_n.max(), 100)
        plt.plot(xgrid, fit_ex.predict(sm.add_constant(xgrid)), 'C3--')
        plt.plot(xgrid, fit_con.predict(sm.add_constant(xgrid)), 'C0--')
        plt.xlabel('Stock price $S_{t_6}$');  plt.ylabel('Value')
        plt.title('Payoff vs. price at $t_6$')
        plt.legend();  plt.show()


    def simulate(self):

        if(self.option_type == 'call'):
            # For call option
            CT = np.maximum(0, self.ST - self.K)
            C0 = np.exp(-self.r*self.T)*np.sum(CT[-1])/MonteCarlo.M
        elif(self.option_type == 'put'):
            # For put option 
            self.backtrack()  # Backtracking to find the optimal exercise strategy
            self.plot_data()  # Plotting the results




