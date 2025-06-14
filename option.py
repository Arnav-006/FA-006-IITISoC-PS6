"""
Contains a class 'option', under which various models can be implemented.
Objects of class created 'option' can be used to access functions of the class.

Object takes in 5 parameters at time of instantiation:
S - underlying spot price
K - strike price
T - time to maturity(in years)
r - risk-free interest rate
sigma - volatility of underlying
(annual dividend yield assumed 0)

eg:
op1 = option(270, 275, 0.25, 0.06, 0.45)
op1.BlackScholes()
"""

import math
from scipy.stats import norm

class option:
    """
    A class to represent a European option and calculate price and Greeks using the Black-Scholes model.
    """

    def __init__(self, S, K, T, r, sigma):
        self.spot = S
        self.strike = K
        self.maturity = T
        self.rate = r
        self.volatility = sigma

    def BlackScholes(self, optionType):
        try:
            S = self.spot
            K = self.strike
            T = self.maturity
            r = self.rate
            sigma = self.volatility

            d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
            d2 = d1 - sigma * math.sqrt(T)

            if optionType.upper() == 'C':
                price = (S * norm.cdf(d1)) - (K * math.exp(-r * T) * norm.cdf(d2))
                delta = norm.cdf(d1)
                theta = -(S * norm.pdf(d1) * sigma) / (2 * math.sqrt(T)) - r * K * math.exp(-r * T) * norm.cdf(d2)
                rho = K * T * math.exp(-r * T) * norm.cdf(d2)
            elif optionType.upper() == 'P':
                price = -(S * norm.cdf(-d1)) + (K * math.exp(-r * T) * norm.cdf(-d2))
                delta = -norm.cdf(-d1)
                theta = -(S * norm.pdf(d1) * sigma) / (2 * math.sqrt(T)) + r * K * math.exp(-r * T) * norm.cdf(-d2)
                rho = -K * T * math.exp(-r * T) * norm.cdf(-d2)
            else:
                raise ValueError("Invalid option type. Use 'C' for Call or 'P' for Put.")

            gamma = norm.pdf(d1) / (S * sigma * math.sqrt(T))
            vega = S * norm.pdf(d1) * math.sqrt(T)

            print(f"""Option Price = {price:.4f}
GREEKS:
Delta = {delta:.4f}
Gamma = {gamma:.4f}
Vega = {vega:.4f}
Theta = {theta:.4f}
Rho = {rho:.4f}
""")

        except Exception as e:
            print("Error during Black-Scholes calculation:", str(e))
