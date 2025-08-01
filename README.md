# FA-006-IITISoC-PS6
This repository contains an extensive python package for pricing options.
📈 Black-Scholes Option Pricing Model
This repository implements the Black-Scholes model to price European call and put options, along with visualizations of various Greeks (Delta, Gamma, Vega, Theta, Rho) and time-based animations. It is designed for interactive use in Google Colab and VS Code with support for Plotly, Matplotlib, and NumPy.

## 🔧 Features

### 📊 European Options Pricing

* Binomial Model

* Black-Scholes Model

* Monte Carlo Simulation

* Heston Model

### 📊 American Options Pricing

* Binomial Model

* Monte Carlo Simulation

### ⚙️ Greeks Calculation

* Delta, Gamma, Theta, Vega, Rho for supported models

### 📉 Visualization Tools

* Greeks vs. volatility, time to maturity, risk-free rate

* Monte Carlo path evolution and histograms

### 📊 Options Strategies

* Bull Call Spread, Bull Put Spread, Straddle, Strangle, Collar, and more

### 📈 Implied Volatility Surface

* Surface generation tools for volatility analysis <br> <br> 




## 🗂️ Package Structure

``` markdown
options_pricer/
│
├── options_pricer_european/
│   ├── __init__.py
│   ├── models/
│   │   ├── binomial.py
│   │   ├── black_scholes.py
│   │   ├── monte_carlo.py
│   │   └── heston.py
│   └── utils/
│       ├── greeks_calculators.py
│       ├── visualisation_tools_black_scholes.py
│       ├── visualisation_tools_monte_carlo.py
│       ├── strategies.py
│       └── implied_vol_surface.py
│
├── options_pricer_american/
│   ├── __init__.py
│   ├── models/
│   │   ├── binomial.py
│   │   └── monte_carlo.py
│   └── utils/
│       ├── greeks_calculators.py
│       ├── visualisation_tools_black_scholes.py
│       ├── visualisation_tools_monte_carlo.py
│       ├── strategies.py
│       └── implied_vol_surface.py
│
├── tests/
│   ├── test_binomial.py
│   ├── test_black_scholes.py
│   ├── test_greeks.py
│   ├── ...
│
├── pyproject.toml
├── LICENSE
└── README.md
```
<br> <br>


## The Black-Scholes Model
The Black-Scholes model is a mathematical model for pricing European-style options. It provides closed-form formulas for calculating the theoretical value of options, assuming the underlying asset follows geometric Brownian motion with constant volatility and interest rates.

### **Formula:**
Black-Scholes for Call and Put:

S: Current stock price\
K: Strike price\
T: Time to maturity (in years)\
r: Risk-free interest rate\
σ: Volatility of the stock\

Then,\
$ 𝑑1=(ln(𝑆/𝐾)+(𝑟+𝜎^2/2)𝑇)/𝜎𝑇,𝑑2=𝑑1−𝜎𝑇\ $

**Call Option Price:**\
$ 𝐶=𝑆⋅𝑁(𝑑1)−𝐾𝑒^(−𝑟𝑇)⋅𝑁(𝑑2)\ $ \
**Put Option Price:**\
$ 𝑃=𝐾𝑒−𝑟𝑇⋅𝑁(−𝑑2)−𝑆⋅𝑁(−𝑑1)\ $ <br> 
where $𝑁(⋅)$ is the cumulative distribution function of the standard normal distribution.

### **Usage:**

#### *class* BlackScholes

- Implements the Black-Scholes model for pricing options, containing methods to calculate option price and greeks.

- *module* : **options_pricer_European.models.Black_Scholes**

#### Usage

```python
# initialize object called myModel of class BlackScholes 
myModel = BlackScholes(S, K, sigma, r, T)
```

#### Parameters

- S : *float*
    - The current underlying price.
- K : *float*
    - The strike price for the option contract.
- sigma : *float*
    - The implied volatility of the underlying (as a decimal).
- r : *float*
    - The risk-free interest rate (annualized, as a decimal).
- T : *float*
    - The time to maturity of the option contract.

#### Returns
- Object of the class BlackScholes

#### Methods

- ##### _compute_d1_d2()
    - Computes the values of d1 and d2 for the given parameters using following formulae:
        - $d_1 = \frac{\ln(\frac{S}{K}) + (r + \frac{\sigma^2}{2})T}{\sigma\sqrt{T}}$
        - $d_2 = d_1 - \sigma\sqrt{T}$
    - Args: ```None```
    - Returns: ```None```

- ##### price(option_type)
    - Computes theoretical price of option using Black-Scholes model, the closed form formulae being:
        - $C = S \cdot N(d1) - K \cdot e^{-rT} \cdot N(d2)$
        - $P = - S \cdot N(-d1) + K \cdot r^{-rT} \cdot N(-d2)$
    - Args: 
        - option_type : *str* - the type of option contract, allowed values are ```"call"``` and ```"put"```.
    - Returns : *float* - The price of option calculated using Black-Scholes model.

- ##### delta(option_type)
    - Computes delta (partial derivative of option price w.r.t. underlying price) using Black-Scholes model, the closed form formulae being:
        - $\delta_{call} = N(d1)$
        - $\delta_{put} = N(d1) - 1$
    - Args: 
        - option_type : *str* - the type of option contract, allowed values are ```"call"``` and ```"put"```.
    - Returns : *float* - The value of delta calculated using Black-Scholes model.

- ##### gamma()
    - Computes gamma (partial second derivative of option price w.r.t. underlying price) using Black-Scholes model, the closed form formula being:
        - $\Gamma = \frac{N'(d_1)}{S \sigma \sqrt{T}}$
    - Args: ```None```
    - Returns : *float* - The value of gamma calculated using Black-Scholes model.

- ##### vega()
    - Computes vega (partial derivative w.r.t. volatility(sigma)), formula used is:
        - $\nu = \frac{S \sqrt{T} N'(d_1)}{100}$
    - Args: ```None```
    - Returns : *float* - The value of vega calculated using Black-Scholes model.

- ##### theta()
    - Computes theta (sensitivity of option price to time of expiration of the option), formula used is:
        - $\Theta_{call} = (-\frac {S \sigma N'(d_1)}{2 \sqrt{T}} - r K e^{-rT} N(d_2) ) \cdot \frac{1}{365}$
        - $\Theta_{put} = (-\frac{S \sigma N'(d_1)}{2 \sqrt{T}} + r K e^{-rT} N(-d_2) ) \cdot \frac{1}{365}$
    - Args: 
        - option_type : *str* - the type of option contract, allowed values are ```"call"``` and ```"put"```.
    - Returns : *float* - The value of theta calculated using Black-Scholes model.

- ##### rho()
    - Computes theta (sensitivity of option price to risk-free interest rate), formula used is:
        - $\rho_{call} = \frac{K T e^{-rT} N(d_2)}{100}$
        - $\rho_{put} = \frac{-K T e^{-rT} N(-d_2)}{100}$
    - Args: 
        - option_type : *str* - the type of option contract, allowed values are ```"call"``` and ```"put"```.
    - Returns : *float* - The value of rho calculated using Black-Scholes model.

## The Binomial Model (European Options)

A simple and intuitive model which can be used for pricing both American and European options, based on breaking down the time until an option's expiration into a series of smaller, distinct time steps.

By asssuming that the stock price can go either up or down at each step, the underlying asset price is modeled as a "binomial tree". The value of the option is then calculated by working backward from the end of the tree. At the final step, the option's value is simply its intrinsic value (its payoff). Then, by discounting these payoffs and their probabilities at each preceding node, the model works its way back to the present to determine the option's fair value today.

### **Usage:**

#### *class* Binomial

- Class to implement the Binomial option pricing model, with methods to compute model constants and price.

- *module* : **option_pricer.models.Binomial**

#### Usage

```python
#create binModel object of class Binomial
binModel = Binomial(S = 200, K = 203, sigma = 0.35, r = 0.03, T = 0.5, option_type = 'put', eps_1 = 0,eps_2 = 0, eps_3 = 0)
```

#### Parameters

- S : *float*
    - Current price of underlying asset.
- K : *float*
    - Strike price for option contract.
- sigma : *float*
    - Volatility for underlying (as a decimal).
- r : *float*
    - Risk-free interest rate (annualized, as a decimal).
- T : *float*
    - Time upto expiration for option contract.
- option_type : *str, optional*
    - Type of option, accepts one of two values : ```call``` or ```put```.
- eps_1 : *float, optional*
    - tolerance in ```S```, such that instance variable for underlying price stores ```S+eps_1```. Defaults to 0.
- eps_2 : *float, optional*
    - tolerance in ```sigma```, such that instance variable for volatility stores ```sigma+eps_1```. Defaults to 0.
- eps_3 : *float, optional*
    - tolerance in ```T```, such that instance variable for expiration time stores ```T+eps_1```. Defaults to 0.

#### Returns
- object of class Binomial

#### Methods

- #### compute_constants()
    - Defines instance variables: ```dt```,,,,```discount``` based on 
        - ```dt``` : duration of one time step
        - ```u``` : factor for upward movement at each step
        - ```d``` : factor for downward movement at each step
        - ```p``` : defined as $p = \frac{e^{r \cdot dt} - d} {u - d}$
        - ```discount``` : total payoff discount defined as $discount = e^{-r \cdot T}$
    - Parameters : ```None```
    - Returns : ```None```

- #### price_options()
    - Calculates the option price using the binomial pricing model.
    - Parameters : ```None```
    - Returns 
        - The option price calculated.

## Monte Carlo Model (European Options)

<!-- ## Visualizations
2D plots: Option price vs stock price\

3D surface: Option price vs stock price and time\

Animated charts: Greeks vs time to maturity\

Dropdowns to toggle between Greeks\
🔧 Parameters You Can Modify\
Parameter	Description\
S	Stock price\
K	Strike price\
r	Risk-free interest rate\
sigma	Volatility\
T	Time to maturity\
option_type	Call or Put\ -->

<!-- ## Applications
Financial modeling and trading simulations\
Sensitivity analysis for hedging strategies\
Educational tool for understanding derivatives\
Comparing models like Binomial Tree or Monte Carlo\ -->


<!-- ## Example Use Case
A trader is considering buying a call option on NIFTY at ₹17,750. Using the Black-Scholes model:\
They estimate a fair price of ₹320.\
The market is asking ₹370 → option is overpriced.\
Delta is 0.65, so for every ₹10 move in NIFTY, the option will move ₹6.5.\
Theta is -5, meaning the option loses ₹5 per day if all else is constant.\
→ This helps the trader decide when to buy, how much to hedge, and when to exit.\ -->


<!-- ## Fair Valuation of Options
Purpose: Determine the theoretical price of a call or put option.\
Why helpful: Helps traders decide whether an option is overpriced or underpriced in the market.\
Example: If the market price is higher than the Black-Scholes price, it may indicate an opportunity to sell.\
## Hedging and Risk Management
Use of Greeks:\
Delta: Helps build Delta-neutral strategies.\
Gamma: Indicates the risk of sudden changes in Delta.\
Vega: Measures exposure to volatility.\
Theta: Shows time decay—crucial for short-term options.\
Rho: Helps adjust strategies in response to interest rate changes.\
Why helpful: Institutions and funds use these sensitivities to hedge positions and manage risk.\ -->




