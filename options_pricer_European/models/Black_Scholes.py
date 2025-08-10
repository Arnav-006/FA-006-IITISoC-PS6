import numpy as np
import pandas as pd
from scipy.stats import norm


class BlackScholes:
    def __init__(self, S, K, sigma, r, T):
        self.S = S
        self.K = K
        self.sigma = sigma
        self.r = r
        self.T = T
        self._compute_d1_d2()

    def _compute_d1_d2(self):
        self.d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
        self.d2 = self.d1 - self.sigma * np.sqrt(self.T)

    def price(self, option_type):
        if option_type == 'call':
            return round(self.S * norm.cdf(self.d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2),3)
        else:
            return round(self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2) - self.S * norm.cdf(-self.d1),3)

    def delta(self, option_type):
        return norm.cdf(self.d1) if option_type == 'call' else norm.cdf(self.d1) - 1

    def gamma(self):
        return norm.pdf(self.d1) / (self.S * self.sigma * np.sqrt(self.T))

    def vega(self):
        return self.S * norm.pdf(self.d1) * np.sqrt(self.T) / 100

    def theta(self, option_type):
        term1 = -self.S * norm.pdf(self.d1) * self.sigma / (2 * np.sqrt(self.T))
        term2 = self.r * self.K * np.exp(-self.r * self.T)
        return (term1 - term2 * norm.cdf(self.d2)) / 365 if option_type == 'call' else (term1 + term2 * norm.cdf(-self.d2)) / 365

    def rho(self, option_type):
        rho_val = self.K * self.T * np.exp(-self.r * self.T)
        return rho_val * norm.cdf(self.d2) / 100 if option_type == 'call' else -rho_val * norm.cdf(-self.d2) / 100
