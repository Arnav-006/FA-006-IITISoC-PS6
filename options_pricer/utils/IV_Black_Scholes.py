"""
Finding implied volatility using black scholes pricing model implemented in options_pricer/models/Black_Scholes.py
Root finding algorithm used - Newton's method

"""

from ..models.Black_Scholes import BlackScholes

def Imp_Vol(S0,K,r,T,market_price,type='call',tol=0.00001):
    """
    S0 - current underlying price
    K - strike price
    r - risk-free rate
    T - time to maturity
    market_price - current price of option

    From the BS model, the price of an option V = f(sigma, .), vega = dV/dsigma = f'(sigma, .)
    And we need to find the root for f(sigma, .) - V = 0 [solve for sigma that makes the LHS 0]

    """
    
    max_it = 100
    vol_init = 0.2 #initial guess for volatility

    for i in range(max_it):
        myOpt = BlackScholes(S0,K,vol_init,r,T)
        bs_price = myOpt.price(type)
        Vprime = myOpt.vega() * 100
        
        vol_new = vol_init - (bs_price - market_price)/Vprime

        new_bs_price = BlackScholes(S0,K,vol_new,r,T).price(type)
        if(abs(vol_new-vol_init) or abs(bs_price - new_bs_price)<tol):
            break

        vol_init = vol_new

    return max(0,vol_new)

print(f"{Imp_Vol(60,57,0.045,30/365,0.70,'call'):.3f}")