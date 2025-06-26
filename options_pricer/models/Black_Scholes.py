from scipy.stats import norm
import numpy as np

class BlackScholes:
    def __init__(self, S, K, sigma, r, T):
        self.S = S
        self.K = K
        self.r = r
        self.T = T
        self.sigma = sigma

        self.d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        self.d2 = self.d1 - sigma * np.sqrt(T)

    def call_price(self):
        return self.S * norm.cdf(self.d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2)

    def put_price(self):
        return self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2) - self.S * norm.cdf(-self.d1)

    def delta(self, option_type='call'):
        if option_type == 'call':
            return norm.cdf(self.d1)
        else:
            return norm.cdf(self.d1) - 1

    def gamma(self):
        return norm.pdf(self.d1) / (self.S * self.sigma * np.sqrt(self.T))

    def vega(self):
        return (self.S * np.sqrt(self.T) * norm.pdf(self.d1)) / 100

    def theta(self, option_type='call'):
        first_term = -self.S * norm.pdf(self.d1) * self.sigma / (2 * np.sqrt(self.T))
        if option_type == 'call':
            second_term = -self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2)
        else:
            second_term = self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2)
        return (first_term + second_term) / 365

    def rho(self, option_type='call'):
        if option_type == 'call':
            return self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(self.d2) / 100
        else:
            return -self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(-self.d2) / 100


    
