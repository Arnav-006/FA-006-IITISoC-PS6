import numpy as np

class BinomialAmerican:
    N = 100  # Number of time steps

    def __init__(self, S, K, sigma, r, T, option_type='call', eps_1=0, eps_2=0, eps_3=0):
        self.S = S + eps_1
        self.K = K
        self.sigma = sigma + eps_3
        self.r = r
        self.T = T + eps_2
        self.option_type = option_type

    def compute_constants(self):
        self.dt = self.T / BinomialAmerican.N
        self.u = np.exp(self.sigma * np.sqrt(self.dt))
        self.d = 1 / self.u
        self.p = (np.exp(self.r * self.dt) - self.d) / (self.u - self.d)
        self.discount = np.exp(-self.r * self.T)

    def price_options(self):
        self.compute_constants()

        if self.S <= 0 or self.K <= 0 or self.T < 0 or self.sigma < 0 or BinomialAmerican.N < 1:
            raise ValueError("Invalid input values.")

        # Vector of indices 0 to N
        i = np.arange(BinomialAmerican.N + 1)

        # Calculate asset prices at maturity
        ST = self.S * (self.u ** (BinomialAmerican.N - i)) * (self.d ** i)

        # Option values at maturity
        if self.option_type == 'call':
            option_values = np.maximum(0, ST - self.K)
        else:
            option_values = np.maximum(0, self.K - ST)

        # Step backward through the tree with early exercise check (American style)
        for j in range(BinomialAmerican.N - 1, -1, -1):
            ST = self.S * (self.u ** (j - i[:j+1])) * (self.d ** i[:j+1])  # Asset prices at time j
            option_values = np.exp(-self.r * self.dt) * (
                self.p * option_values[:-1] + (1 - self.p) * option_values[1:]
            )

            # Immediate exercise value at node
            if self.option_type == 'call':
                option_values = np.maximum(option_values, ST - self.K)
            else:
                option_values = np.maximum(option_values, self.K - ST)

        return option_values[0]
