from options_pricer_European.models.Binomial import Binomial

def implied_volatility_binomial_bisection(S, K, r, T, market_price, option_type='call', N=100, tol=1e-5, max_iter=100):
    """
    Implied volatility using bisection method and your Binomial model.
    
    Parameters:
    - S: Spot price
    - K: Strike price
    - r: Risk-free rate
    - T: Time to maturity
    - market_price: Observed market option price
    - option_type: 'call' or 'put'
    - N: number of binomial steps
    - tol: convergence tolerance
    - max_iter: maximum iterations
    
    Returns:
    - Implied volatility (float) or None if not found
    """
    Binomial.N = N

    low_vol = 1e-5
    high_vol = 5.0

    for _ in range(max_iter):
        mid_vol = (low_vol + high_vol) / 2
        model = Binomial(S, K, mid_vol, r, T, option_type)
        try:
            price = model.price_options()
        except:
            return None  # In case of model failure
        
        diff = price - market_price

        if abs(diff) < tol:
            return mid_vol
        if diff > 0:
            high_vol = mid_vol
        else:
            low_vol = mid_vol

    return None  # did not converge within max_iter
