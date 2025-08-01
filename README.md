# FA-006-IITISoC-PS6
This repository contains an extensive python package for pricing options.

## Implied Volatility Calculation Functions

Finding immplied volatility using option contract parameters and the market price of option by various different root finding algorithms.

### 1. Newton-Raphson Method

The Newton-Raphson method is a powerful iterative algorithm used to find the roots (or zeros) of a real-valued function. The method starts with an initial guess, $x_0$, for the root. It then uses the function's value, $f(x_n)$, and its first derivative, $f'(x_n)$, at that point to draw a tangent line. The next, and hopefully better, guess, $x_{n+1}$, is the point where this tangent line intersects the x-axis.

The iterative formula for the method is:
$x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$

*function* IV_NewRaph

*module* - **options_pricer_European.utils.IV**

This function uses the classic Newton-Raphson algorithm(Read more https://www.geeksforgeeks.org/engineering-mathematics/newton-raphson-method/) for finding the implied volatility using the Black-Scholes model.

#### Usage:
```python
IV_NewRaph(S0,K,r,T,market_price,op_type='call',tol=0.00001)
```

#### Parameters:
- S0 : *float* 
    - Current underlying price.
- K : *float* 
    - Strike price for option contract.
- r : *float* 
    - Risk-free rate (annualized, as a decimal).
- T : *float* 
    - Time to maturity (in years).
- market_price : *float* 
    - Current price of option contract in market.
- op_type : *str, optional* 
    - Type of option, accepts one of two values - ```call``` or ```put```, defaults to call.
- tol : float, optional 
    - The tolerance that decides how accurate the returned value will be, defaults to 1e-5.

#### Returns:
- Positive implied volatility if a valid market price is input, else zero.

#### Example:
```python
IV_NewRaph(160,156,0.05,0.25,6.45)    #find IV for call option with default option type "call" and default tolerance 1e-5
IV_NewRaph(250,245,0.06,30/365,0.65,op_type='put',tol=1e-6)    #IV for option of type "put" and tolerance 1e-6
```

### 2. Brent's Method

Brent's method is a root-finding algorithm that combines the speed and guaranteed convergence of several other methods.

It is a hybrid algorithm that intelligently chooses between three techniques at each step:
*  **Bisection:** For guaranteed convergence.
*  **Secant Method:** For faster linear convergence.
*  **Inverse Quadratic Interpolation:** For even faster, super-linear convergence.

*function* IV_Brent

*module* - **options_pricer_European.utils.IV**

This function uses the Brent's algorithm for finding the implied volatility using the Black-Scholes model. The implementation for Brent's method is taken from scipy.optimize (Read more https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.brentq.html#brentq).


#### Usage:
```python
IV_Brent(S0,K,r,T,market_price,op_type='call')
```

#### Parameters:
- S0 : *float* 
    - Current underlying price.
- K : *float*
    - Strike price for option contract.
- r : *float* 
    - Risk-free rate (annualized, as a decimal).
- T : *float* 
    - Time to maturity (in years).
- market_price : *float* 
    - Current price of option contract in market.
- op_type : *str, optional* 
    - Type of option, accepts one of two values - ```call``` or ```put```, defaults to call.

#### Returns:

- Positive implied volatility if a valid market price is input, else ```np.nan```.

#### Example:
```python
IV_Brent(160,156,0.05,0.25,6.45)    #find IV for call option with default option type "call"
IV_Brent(250,245,0.06,30/365,0.65,op_type='put')    #IV for option of type "put"
```

### 3. Bisection Method (for Binomial Model)

The bisection method is a simple and reliable root-finding algorithm.

The method works by repeatedly narrowing down an interval that is known to contain a root. It starts with an interval $[a, b]$ where the function values, $f(a)$ and $f(b)$, have opposite signs.

At each step, it calculates the midpoint, $c = (a+b)/2$, and checks the sign of $f(c)$. It then discards the half of the interval where the function does not cross zero, creating a new, smaller interval. This process continues until the interval is sufficiently small.

*function* IV_Binomial_Bisection

*module* - **options_pricer_European.utils.IV**

Implied volatility using bisection method on Binomial Model.

#### Usage:
```python
IV_Binomial_Bisection(S, K, r, T, market_price, option_type='call', N=100, tol=1e-5, max_iter=100)
```

#### Parameters:
- S : *float*
    - Spot price.
- K : *float*
    - Strike price.
- r : *float*
    - Risk-free rate (annualized, as a decimal).
- T : *float*
    - Time to maturity (in years).
- market_price : *float*
    - Observed market option price.
- option_type : *str, optional*
    - Type of option, accepts either ```call``` or ```put```.
- N : *int*
    - Number of binomial steps.
- tol: *float*
    - Convergence tolerance.
- max_iter: *int*
    - Maximum iterations.

#### Returns:
- Implied volatility (*float*) or ```None``` if not found.

#### Example:
```python
IV_Binomial_Bisection(160,156,0.05,0.25,6.45) #It takes by default option type as call, N=100, tol=1e-5, max iterations=100.
IV_Binomial_Bisection(250,245,0.06,0.50,2.45,option_type='put',N=90,tol=1e-6,max_iter=150) #customized values for N, max iterations, option type.
```
