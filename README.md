
# FA-006-IITISoC-PS6
This repository contains an extensive python package for pricing options.
📈 Black-Scholes Option Pricing Model
This repository implements the Black-Scholes model to price European call and put options, along with visualizations of various Greeks (Delta, Gamma, Vega, Theta, Rho) and time-based animations. It is designed for interactive use in Google Colab and VS Code with support for Plotly, Matplotlib, and NumPy.

# 🔧 Features

## 📊 European Options Pricing

* Binomial Model

* Black-Scholes Model

* Monte Carlo Simulation

* Heston Model

## 📊 American Options Pricing

* Binomial Model

* Monte Carlo Simulation

## ⚙️ Greeks Calculation

* Delta, Gamma, Theta, Vega, Rho for supported models

## 📉 Visualization Tools

* Greeks vs. volatility, time to maturity, risk-free rate

* Monte Carlo path evolution and histograms

## 📊 Options Strategies

* Bull Call Spread, Bull Put Spread, Straddle, Strangle, Collar, and more

## 📈 Implied Volatility Surface

* Surface generation tools for volatility analysis <br> <br> 




# 🗂️ Package Structure

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

# Models for European Options

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

Monte Carlo simulation is extensively used in pricing European, American as well as exotic options. The speciality of this model lies in the fact that it can provide a good estmiate of the parameters of any system that cannot be modelled using analytical approaches like solving differential equations. 

The movement of the price of stock can't be modelled accurately due to its dependence on innumerable factors in complex ways. It thus, lies beyond the scope of any existing analytical method. Monte Carlo solves the problem by approximating the stock prices to follow **Geometric Brownian Motion**. It adopts risk-neutral pricing to derive the value of the option from the future payoff averaged over large enough number of simulations.

### **Usage:**

#### *class* MonteCarlo

- Class to implement the Monte Carlo option pricing model, with methods to compute model constants and price.

- *module* : **option_pricer_European.models.Monte_Carlo**

#### Usage

```python
#create binModel object of class Binomial
mcModel = MonteCarlo(S=101.15, K=98.01, vol=0.90, r=0.02, T=0.14, option_type='c', dev_0=0, dev_1=0, dev_2=0)
```
> **Note**:
    > The time argument accepts the input as a fraction of one year.


#### Parameters

- S : *float*
    - Current price of underlying asset.
- K : *float*
    - Strike price for option contract.
- vol : *float*
    - Volatility for underlying (as a decimal).
- r : *float*
    - Risk-free interest rate (annualized, as a decimal).
- T : *float*
    - Time upto expiration for option contract.
- option_type : *str, optional*
    - Type of option, accepts one of two values : ```call``` or ```put```.
- dev_0 : *float, optional*
    - tolerance in ```S```, such that instance variable for underlying price stores ```S+eps_1```. Defaults to 0.
- dev_1 : *float, optional*
    - tolerance in ```sigma```, such that instance variable for volatility stores ```sigma+eps_1```. Defaults to 0.
- dev_2 : *float, optional*
    - tolerance in ```T```, such that instance variable for expiration time stores ```T+eps_1```. Defaults to 0.

> **Note**:
    > dev_0, dev_1 and dev_2 parameters are defined solely for the calculation of Greeks, they play no role in calculation of option price at maturity.

#### Returns
- object of class MonteCarlo

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


# Strategies
Functions for creating Profit/Loss graphs for classical option trading strategies, that use option pricing models specified by the user to find the option premiums.

### Bull_Call_Spread

Compute and visualize the profit and loss (P&L) of a bull call spread strategy using different pricing models.

The `Bull_Call_Spread` function calculates the payoff and P&L of a bull call spread. This strategy involves **buying a call option with a strike price (K2) and selling a put option with a higher strike price (K1)**. This reduces the upfront investment due to the premium gained on sold call, and improves return for a moderately bullish outcome. The function supports three pricing models: Black-Scholes (`BS`), Binomial (`BIN`), and Monte Carlo (`MC`). It also generates a plot of the P&L across a range of stock prices.

#### Usage

```python
Bull_Call_Spread(S, K1, K2, r, sigma, T, model="BS", S_max=None, num_points=100)
```

#### Parameters

- S : *float* 
    - Current stock price.
- K1 : *float* 
    - Lower strike price for buying call option.
- K2 : *float* 
    - Higher strike price for selling call option(higher strike).
- r : *float* 
    - Risk-free interest rate (annualized, as a decimal).
- sigma : *float*
    - Implied volatility of underlying (annualized, as a decimal).
- T : *float*
    - Time to expiration of the option, in years.
- model : *str, optional*
    - Pricing model to use. Options are:
        - ```"BS"```: Black-Scholes model
        - ```"BIN"```: Binomial model
        - ```"BS"```: Monte Carlo simulation
- S_max : *float, optional*
    - Maximum underlying price to show on x-axis in P&L plot. If ```None``` defaults to ```1.5 * K2```.
- num_points : *int, optional*
    - Number of stock price points to plot P&L. If ```None``` defaults to 100.

#### Returns

- None
    - The function does not return a value but generates a plot of the P&L and prints an error message if ```K2 <= K1```.

#### Examples

```python
# Example using Black-Scholes model
Bull_Call_Spread(S=100, K1=95, K2=105, r=0.05, sigma=0.2, T=1.0, model="BS")

# Example using Binomial model with custom S_max
Bull_Call_Spread(S=50, K1=45, K2=55, r=0.03, sigma=0.25, T=0.5, model="BIN", S_max=80, num_points=200)
```
---

### Bull_Put_Spread

Compute and visualize the profit and loss (P&L) of a bull put spread strategy using different pricing models.

The `Bull_Put_Spread` function calculates the payoff and P&L of a bull put spread. This strategy involves **buying a put option with a lower strike price (K2) and selling a put option with a higher strike price (K1)**. This strategy is useful for limiting potential losses while benefiting from a moderately bullish outlook. The function supports three pricing models: Black-Scholes (`BS`), Binomial (`BIN`), and Monte Carlo (`MC`). It also generates a plot of the P&L across a range of stock prices.

#### Usage

```python
Bull_Put_Spread(S, K1, K2, r, sigma, T, model="BS", S_max=None, num_points=100)
```

#### Parameters

- S : *float* 
    - Current stock price.
- K1 : *float* 
    - Lower strike price for buying put option.
- K2 : *float* 
    - Higher strike price for selling put option(higher strike).
- r : *float* 
    - Risk-free interest rate (annualized, as a decimal).
- sigma : *float*
    - Implied volatility of underlying (annualized, as a decimal).
- T : *float*
    - Time to expiration of the option, in years.
- model : *str, optional*
    - Pricing model to use. Options are:
        - ```"BS"```: Black-Scholes model
        - ```"BIN"```: Binomial model
        - ```"BS"```: Monte Carlo simulation
- S_max : *float, optional*
    - Maximum underlying price to show on x-axis in P&L plot. If ```None``` defaults to ```1.5 * K2```.
- num_points : *int, optional*
    - Number of stock price points to plot P&L. If ```None``` defaults to 100.

#### Returns

- None
    - The function does not return a value but generates a plot of the P&L and prints an error message if ```K2 <= K1```.

#### Examples

```python
# Example using Black-Scholes model
Bull_Put_Spread(S=100, K1=95, K2=105, r=0.05, sigma=0.2, T=1.0, model="BS")

# Example using Binomial model with custom S_max
Bull_Put_Spread(S=50, K1=45, K2=55, r=0.03, sigma=0.25, T=0.5, model="BIN", S_max=80, num_points=200)
```
---

### Bear_Call_Spread

Compute and visualize the profit and loss (P&L) of a bear call spread strategy using different pricing models.

The `Bear_Call_Spread` function calculates the payoff and P&L of a bear call spread. This strategy involves **selling a call option with a lower strike price (K1) and buying a call option with a higher strike price (K2)**. This strategy is useful limiting potential downside losses of sold call option by buying a call at higher strike price. The function supports three pricing models: Black-Scholes (`BS`), Binomial (`BIN`), and Monte Carlo (`MC`). It also generates a plot of the P&L across a range of stock prices.

#### Usage

```python
Bear_Call_Spread(S, K1, K2, r, sigma, T, model="BS", S_max=None, num_points=100)
```

#### Parameters

- S : *float* 
    - Current stock price.
- K1 : *float* 
    - Lower strike price for selling call option.
- K2 : *float* 
    - Higher strike price for buying call option(higher strike).
- r : *float* 
    - Risk-free interest rate (annualized, as a decimal).
- sigma : *float*
    - Implied volatility of underlying (annualized, as a decimal).
- T : *float*
    - Time to expiration of the option, in years.
- model : *str, optional*
    - Pricing model to use. Options are:
        - ```"BS"```: Black-Scholes model
        - ```"BIN"```: Binomial model
        - ```"BS"```: Monte Carlo simulation
- S_max : *float, optional*
    - Maximum underlying price to show on x-axis in P&L plot. If ```None``` defaults to ```1.5 * K2```.
- num_points : *int, optional*
    - Number of stock price points to plot P&L. If ```None``` defaults to 100.

#### Returns

- None
    - The function does not return a value but generates a plot of the P&L and prints an error message if ```K2 <= K1```.

#### Examples

```python
# Example using Black-Scholes model
Bear_Call_Spread(S=100, K1=95, K2=105, r=0.05, sigma=0.2, T=1.0, model="BS")

# Example using Binomial model with custom S_max
Bear_Call_Spread(S=50, K1=45, K2=55, r=0.03, sigma=0.25, T=0.5, model="BIN", S_max=80, num_points=200)
```
---

### Bear_Put_Spread

Compute and visualize the profit and loss (P&L) of a bear put spread strategy using different pricing models.

The `Bear_Put_Spread` function calculates the payoff and P&L of a bear put spread. This strategy involves **selling a put option with a lower strike price (K1) and buying a put option with a higher strike price (K2)**. This reduces the upfront investment due to the gained premium of the sold put option, hence increases returns for a moderately bearish market. The function supports three pricing models: Black-Scholes (`BS`), Binomial (`BIN`), and Monte Carlo (`MC`). It also generates a plot of the P&L across a range of stock prices.

#### Usage

```python
Bear_Put_Spread(S, K1, K2, r, sigma, T, model="BS", S_max=None, num_points=100)
```

#### Parameters

- S : *float* 
    - Current stock price.
- K1 : *float* 
    - Lower strike price for selling put option.
- K2 : *float* 
    - Higher strike price for buying put option(higher strike).
- r : *float* 
    - Risk-free interest rate (annualized, as a decimal).
- sigma : *float*
    - Implied volatility of underlying (annualized, as a decimal).
- T : *float*
    - Time to expiration of the option, in years.
- model : *str, optional*
    - Pricing model to use. Options are:
        - ```"BS"```: Black-Scholes model
        - ```"BIN"```: Binomial model
        - ```"BS"```: Monte Carlo simulation
- S_max : *float, optional*
    - Maximum underlying price to show on x-axis in P&L plot. If ```None``` defaults to ```1.5 * K2```.
- num_points : *int, optional*
    - Number of stock price points to plot P&L. If ```None``` defaults to 100.

#### Returns

- None
    - The function does not return a value but generates a plot of the P&L and prints an error message if ```K2 <= K1```.

#### Examples

```python
# Example using Black-Scholes model
Bear_Put_Spread(S=100, K1=95, K2=105, r=0.05, sigma=0.2, T=1.0, model="BS")

# Example using Monte Carlo model with custom S_max
Bear_Put_Spread(S=50, K1=45, K2=55, r=0.03, sigma=0.25, T=0.5, model="MC", S_max=80, num_points=200)
```
---

### Straddle

Compute and visualize the profit and loss (P&L) of a long straddle options strategy using different pricing models.

The `Straddle` function calculates the payoff and P&L of a long straddle. This strategy involves **buying both a call option and a put option with the same strike price (K) and the same expiration date**. A long straddle is typically employed when an investor anticipates a significant price movement in the underlying asset, but is unsure of the direction (i.e., high volatility is expected). The function supports three pricing models: Black-Scholes (`BS`), Binomial (`BIN`), and Monte Carlo (`MC`). It also generates a plot of the P&L across a range of stock prices.

#### Usage

```python
Straddle(S, K, sigma, r, T, model="BS", num_points=100)
```

#### Parameters

- S : *float* 
    - Current stock price.
- K : *float* 
    - Strike price for buying both put and call options.
- r : *float* 
    - Risk-free interest rate (annualized, as a decimal).
- sigma : *float*
    - Implied volatility of underlying (annualized, as a decimal).
- T : *float*
    - Time to expiration of the option, in years.
- model : *str, optional*
    - Pricing model to use. Options are:
        - ```"BS"```: Black-Scholes model
        - ```"BIN"```: Binomial model
        - ```"BS"```: Monte Carlo simulation
- S_max : *float, optional*
    - Maximum underlying price to show on x-axis in P&L plot. If ```None``` defaults to ```1.5 * K2```.
- num_points : *int, optional*
    - Number of stock price points to plot P&L. If ```None``` defaults to 100.

#### Returns

- None
    - The function does not return a value but generates a plot of the P&L.

#### Examples

```python
# Example using Black-Scholes model
Straddle(S=100, K=100, sigma=0.2, r=0.05, T=1.0, model="BS")

# Example using Binomial model
Straddle(S=50, K=50, sigma=0.25, r=0.03, T=0.5, model="BIN", num_points=200)
```
---

### Strangle

Compute and visualize the profit and loss (P&L) of a long strangle options strategy using different pricing models.

The `Strangle` function calculates the payoff and P&L of a long strangle. This strategy involves **buying an out-of-the-money (OTM) call option and an out-of-the-money (OTM) put option with different strike prices (K1 for call, K2 for put) but the same expiration date**. A long strangle is used when an investor anticipates a large price movement in the underlying asset, but is uncertain about the direction. It is similar to a straddle but generally costs less due to the options being OTM, though it requires a larger price movement to become profitable. The function supports three pricing models: Black-Scholes (`BS`), Binomial (`BIN`), and Monte Carlo (`MC`). It also generates a plot of the P&L across a range of stock prices.

#### Usage

```python
Strangle(S, K1, K2, sigma, r, T, model="BS", num_points=100)
```

#### Parameters

- S : *float* 
    - Current stock price.
- K1 : *float* 
    - Strike price for buying call option.
- K2 : *float*
    - Strike price for buying put option.
- r : *float* 
    - Risk-free interest rate (annualized, as a decimal).
- sigma : *float*
    - Implied volatility of underlying (annualized, as a decimal).
- T : *float*
    - Time to expiration of the option, in years.
- model : *str, optional*
    - Pricing model to use. Options are:
        - ```"BS"```: Black-Scholes model
        - ```"BIN"```: Binomial model
        - ```"BS"```: Monte Carlo simulation
- S_max : *float, optional*
    - Maximum underlying price to show on x-axis in P&L plot. If ```None``` defaults to ```1.5 * K2```.
- num_points : *int, optional*
    - Number of stock price points to plot P&L. If ```None``` defaults to 100.

#### Returns

- None
    - The function does not return a value but generates a plot of the P&L and prints an error message if ```K2 <= K1```.

#### Examples

```python
# Example using Black-Scholes model
Strangle(S=100, K1=90, K2=110, sigma=0.2, r=0.05, T=1.0, model="BS")

# Example using Binomial model with different parameters
Strangle(S=50, K1=45, K2=55, sigma=0.25, r=0.03, T=0.5, model="BIN", num_points=200)
```
---

### Collar

Compute and visualize the profit and loss (P&L) of a collar options strategy using different pricing models.

The `Collar` function calculates the payoff and P&L of a collar strategy. A collar involves **holding shares of an underlying stock, buying an out-of-the-money (OTM) put option (to protect against downside risk), and selling an out-of-the-money (OTM) call option (to generate income and partially offset the cost of the put)**. This strategy is typically used by investors who hold a long position in a stock and want to protect against a significant price drop while being willing to cap their upside potential. The function supports three pricing models: Black-Scholes (`BS`), Binomial (`BIN`), and Monte Carlo (`MC`). It also generates a plot of the P&L across a range of stock prices.

#### Usage

```python
Collar(S, K1, K2, sigma, r, T, model="BS", num_points=100)
```

#### Parameters

- S : *float* 
    - Current stock price.
- K1 : *float* 
    - Strike price for buying call option.
- K2 : *float*
    - Strike price for buying put option.
- r : *float* 
    - Risk-free interest rate (annualized, as a decimal).
- sigma : *float*
    - Implied volatility of underlying (annualized, as a decimal).
- T : *float*
    - Time to expiration of the option, in years.
- model : *str, optional*
    - Pricing model to use. Options are:
        - ```"BS"```: Black-Scholes model
        - ```"BIN"```: Binomial model
        - ```"BS"```: Monte Carlo simulation
- S_max : *float, optional*
    - Maximum underlying price to show on x-axis in P&L plot. If ```None``` defaults to ```1.5 * K2```.
- num_points : *int, optional*
    - Number of stock price points to plot P&L. If ```None``` defaults to 100.

#### Returns

- None
    - The function does not return a value but generates a plot of the P&L and prints an error message if ```K2 <= K1```.

#### Examples

```python
# Example using Black-Scholes model
Collar(S=100, K1=95, K2=105, sigma=0.2, r=0.05, T=1.0, model="BS")

# Example using Binomial model with different parameters
Collar(S=50, K1=45, K2=55, sigma=0.25, r=0.03, T=0.5, model="BIN", num_points=200)
```
---

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

