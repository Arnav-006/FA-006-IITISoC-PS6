import numpy as np
import scipy.stats as stats

class Heston:
    """
    A class for simulating stock price paths using the Heston stochastic volatility model.

    The Heston model is a mathematical model that describes the evolution of the
    volatility of an underlying asset. It assumes that the volatility is not
    constant (as in the Black-Scholes model) but follows a random process.
    Specifically, the variance follows a Cox-Ingersoll-Ross (CIR) mean-reverting process.

    This class uses a Monte Carlo simulation with an Euler-Maruyama discretization
    scheme to generate paths for both the stock price and its variance.
    """
    def __init__(self, S0, v0, r, T, kappa, theta, xi, rho, steps=250, paths=10000):
        """
        Initializes the Heston model parameters.

        Parameters:
        ----------
        S0 : float
            Initial stock price.
        v0 : float
            Initial variance of the stock price.
        r : float
            Annualized risk-free interest rate.
        T : float
            Time to maturity in years.
        kappa : float
            Rate of mean reversion for the variance process. A higher kappa
            means the variance reverts to `theta` more quickly.
        theta : float
            Long-term mean of the variance. The variance process will tend to
            drift towards this level.
        xi : float
            Volatility of volatility (vol-of-vol). It determines the volatility
            of the variance process.
        rho : float
            Correlation coefficient between the Brownian motions of the stock
            price and its variance. A negative rho is common for equities,
            capturing the leverage effect (volatility tends to increase when
            the stock price falls).
        steps : int, optional
            Number of time steps in the simulation (default is 250).
        paths : int, optional
            Number of simulation paths to generate (default is 10000).
        """
        self.S0 = S0
        self.v0 = v0
        self.r = r
        self.T = T
        self.kappa = kappa
        self.theta = theta
        self.xi = xi
        self.rho = rho
        self.steps = steps
        self.paths = paths
        self.dt = T / steps

    def simulate_paths(self):
        """
        Simulates the paths for both the stock price (S) and its variance (v).

        This implementation uses the Euler-Maruyama discretization scheme. A 'full
        truncation' scheme is applied to the variance process to prevent it from
        becoming negative, which is a known issue with this discretization method
        for the CIR process.

        Returns:
        -------
        tuple[np.ndarray, np.ndarray]
            A tuple containing two numpy arrays: (S, v).
            - S: The simulated stock price paths with shape (paths, steps + 1).
            - v: The simulated variance paths with shape (paths, steps + 1).
        """
        # Initialize arrays to store the paths for stock price and variance
        S = np.zeros((self.paths, self.steps + 1))
        v = np.zeros((self.paths, self.steps + 1))

        # Set the initial values for the first time step
        S[:, 0] = self.S0
        v[:, 0] = self.v0

        for t in range(1, self.steps + 1):
            # Generate correlated random shocks for the stock and variance processes
            Z1 = stats.norm.rvs(size=self.paths)
            Z2_indep = stats.norm.rvs(size=self.paths)
            Z2 = self.rho * Z1 + np.sqrt(1 - self.rho ** 2) * Z2_indep

            # Full Truncation Scheme: Ensure the variance used in the calculation is non-negative
            v_t_prev = np.maximum(v[:, t - 1], 0)

            # Update variance using the Euler-Maruyama scheme for the CIR process
            # We apply maximum(..., 0) again to ensure the resulting variance is not negative
            v[:, t] = np.maximum(
                v[:, t - 1]
                + self.kappa * (self.theta - v[:, t - 1]) * self.dt
                + self.xi * np.sqrt(v_t_prev) * np.sqrt(self.dt) * Z2,
                0
            )

            # Update stock price using the Euler-Maruyama scheme for GBM with stochastic volatility
            S[:, t] = S[:, t - 1] * np.exp(
                (self.r - 0.5 * v_t_prev) * self.dt
                + np.sqrt(v_t_prev) * np.sqrt(self.dt) * Z1
            )

        return S, v
