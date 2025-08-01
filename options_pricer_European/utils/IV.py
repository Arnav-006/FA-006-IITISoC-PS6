"""Finding immplied volatility using option contract parameters and the market price of option by various two different root finding algorithms:
  - Newton-Raphson method
  - Brent's Method (Using the scipy.optimize module)
"""

from scipy import optimize
from ..models.Black_Scholes import BlackScholes

def IV_NewRaph(S0,K,r,T,market_price,op_type='call',tol=0.00001):
    """
    This function uses the classic Newton-Raphson algorithm for finding the implied volatility using the Black-Scholes model.

    Usage:
      IV_NewRaph(S0,K,r,T,market_price,op_type='call',tol=0.00001)

    Parameters:
      - S0 : float - Current underlying price.
      - K : float - Strike price for option contract.
      - r : float - Risk-free rate (annualized, as a decimal).
      - T : float - Time to maturity (in years).
      - market_price : float - Current price of option contract in market.
      - op_type : str, optional - Type of option, accepts one of two values - "call" or "put", defaults to call.
      - tol : float, optional - The tolerance that decides how accurate the returned value will be, defaults to 1e-5.

    Returns:
      - Positive implied volatility if a valid market price is input, else zero.

    Example:
      IV_NewRaph(160,156,0.05,0.25,6.45)    #find IV for call option with default option type "call" and default tolerance 1e-5
      IV_NewRaph(250,245,0.06,30/365,0.65,op_type='put',tol=1e-6)    #IV for option of type "put" and tolerance 1e-6
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
