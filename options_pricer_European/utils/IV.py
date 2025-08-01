"""Finding immplied volatility using option contract parameters and the market price of option by various two different root finding algorithms:
  - Newton-Raphson method
  - Brent's Method (Using the scipy.optimize module)
"""

from scipy import optimize
from ..models.Black_Scholes import BlackScholes

def IV_NewRaph(S0,K,r,T,market_price,op_type='call',tol=0.00001):
    """
    S0 - current underlying price
    K - strike price
    r - risk-free rate
    T - time to maturity
    market_price - current price of option

    From the BS model, the price of an option V = f(sigma, .), vega = dV/dsigma = f'(sigma, .)
    And we need to find the root for f(sigma, .) - V = 0 [solve for sigma that makes the LHS 0]

    """
    
    max_it = 1000
    vol_init = 0.2 #initial guess for volatility

    for i in range(max_it):
        myOpt = BlackScholes(S0,K,vol_init,r,T)
        bs_price = myOpt.price(op_type)
        Vprime = myOpt.vega() * 100
        
        vol_new = vol_init - (bs_price - market_price)/Vprime

        new_bs_price = BlackScholes(S0,K,vol_new,r,T).price(op_type)
        if(abs(vol_new-vol_init)<tol or abs(bs_price - new_bs_price)<tol):
            break

        vol_init = vol_new

    return max(0,vol_new)

def IV_Brent(S0,K,r,T,market_price,op_type='call'):
    def object_func(sigma):
        model_price = BlackScholes(S0,K,sigma,r,T).price(op_type)
        return model_price - market_price
    try:
        IV = optimize.brentq(object_func,-1.0,5.0)
        return IV
    except ValueError:
        return np.nan
