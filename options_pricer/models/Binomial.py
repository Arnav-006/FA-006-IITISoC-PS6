import math

"""
    European style binomial option pricing model.

    Parameters:
    S : float
        Current stock price
    K : float
        Strike price
    T : float
        Time to maturity (in years)
    r : float
        Risk-free interest rate (annualized, as a decimal)
    sigma : float
        Volatility of the underlying stock (annualized, as a decimal)
    N : int
        Number of binomial steps
    option_type : str
        'call' for call option, 'put' for put option

    Returns:
    float
        The option price
"""

class Binomial:

    N = 100     #Number of time steps

    def __init__(self, S, K, sigma, r, T, option_type='call', eps_1=0, eps_2=0, eps_3=0):
        self.S = S+eps_1  
        self.K = K
        self.sigma = sigma+eps_3
        self.r = r
        self.T = T+eps_2
        """
        S: stock price
        K: strike price
        sigma: volatility
        r: risk-free interest rate
        T: time to maturity in years
        """

    def compute_constants(self):
        dt = self.T / Binomial.N
        self.u = math.exp(self.sigma * math.sqrt(dt))
        self.d = 1 / self.u
        self.p = (math.exp(self.r * dt) - self.d) / (self.u - self.d)
        self.discount = math.exp(-self.r * self.T)
        
    def price_options(self):
        self.compute_constants()

        # Handling edge cases
        if S <= 0 or K <= 0 or T < 0 or sigma < 0 or N < 1:
        raise ValueError("Invalid input values.")

        # Initialize asset prices at maturity
        ST = [0] * (Binomial.N + 1)
        for i in range(Binomial.N + 1):
            ST[i] = self.S * (self.u ** (Binomial.N - i)) * (self.d ** i)

        # Initialize option values at maturity
        option_values = [0] * (Binomial.N + 1)
        for i in range(Binomial.N + 1):
            if self.option_type == 'call':
                option_values[i] = max(0, ST[i] - self.K)
            else:
                option_values[i] = max(0, self.K - ST[i])

        # Step back through the tree
        for j in range(Binomial.N - 1, -1, -1):
            for i in range(j + 1):
                option_values[i] = math.exp(-self.r * self.dt) * (self.p * option_values[i] + (1 - self.p) * option_values[i + 1])

        return option_values[0]
