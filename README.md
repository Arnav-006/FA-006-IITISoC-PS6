

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
│      
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

---

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

---

## Monte Carlo Model (European Options)

Monte Carlo simulation is extensively used in pricing European, American as well as exotic options. The speciality of this model lies in the fact that it can provide a good estmiate of the parameters of any system that cannot be modelled using analytical approaches like by solving differential equations. 

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
    - Defines instance variables: 
        - ```dt``` : duration of one time step
        - ```nudt``` : drift factor for modelling stock price movement
        - ```volsdt``` : volatility of the underlying asset times the squareroot of time step
        - ```lnS``` : log of the initial underlying asset price
        - ```erdt``` : total payoff discount defined as $discount = e^{r\cdot T}$
        - ```cv``` : control variate for delta hedging
        - ```beta1``` : coefficient of control variate
    - Parameters : ```None```
    - Returns : ```None```

- #### calculate_stock_price()
    - Calculates the stock price using the equation for Brownian Motion.
    - Parameters : ```None```
    - Returns : ```ST``` and ```cv```
        - The stock price matrix (price at each time step for all simulations)
        - Control variate based on delta hedging

- #### calculate_option_price()
    - Calculates option price by finding the payoff at maturity and discouting it to present date 
    - Adds the hedging factor to reduce the spread of all simulated values
    - Parameters : ```ST``` and ```cv```
    - Returns : ```C0``` and ```CT```
        - Option Price 
        - Payoffs after the final time step

- #### delta_calc()
    - Calculates delta corresponding to the option
    - Parameters : ```None```
    - Returns : ```delta```

- #### simulate()
    - a single callable function to run the entire process 
    - Parameters : ```None```
    - Returns : ```C0``` and ```SE```
        - Option Price
        - Standard Error
<br><br><br>

<<<<<<< HEAD
# Utilities for European options
=======
# Utilities for European Options

>>>>>>> 99f04713b2d4a9951cb0053a3ecbcf1d2bbc1426

## Strategies
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
<<<<<<< HEAD

=======
>>>>>>> 99f04713b2d4a9951cb0053a3ecbcf1d2bbc1426
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

## Visualisation Tools for European Options

Various visualization tools are provided for European options using the Black-Scholes model, implemented using
the BlackScholes class under models.

*class* BSOptionsVisualizer

*module* - **options_pricer_European.utils.Visualization_Tools_Black_Scholes**

Class that implements various methods to visualize how options' prices varies using plotly and pandas

### Usage
```python
vis = BSOptionsVisualizer(K, r, sigma, option_types=('call', 'put'))
```

### Parameters

- K : *float*
    - The strike price.
- r : *float*
    - The risk-free rate of interest(annualized, as a decimal).
- sigma : *float*
    - The volatility of the underlying stock.
- option_types : *tuple*
    - Tuple of types of options used for making database.

### Returns
- object of class BSOptionsVisualizer

### Methods

- generate_data()
    - returns a Pandas dataframe containing prices calculated for various option contracts
    - Parameters:
        - T_days_range : *array-type* - a range like object that is used for choosing values of time of expiration.
        - mode : *str, optional* - mode that specifies what to make the graph against. Accepts ```stock```or ```time```.
    - Returns:
        - a Pandas dataframe containing prices data for options dataframe

- visualize()
    - The visualize function generates visualizations of option pricing metrics (Greeks and price) against the underlying stock price. It offers two primary modes of operation: 'stock' for a static visualization at a single point in time, and 'time' for an animated visualization showing the evolution of the metrics as the time to expiration changes. The function relies on a self.generate_data method (assumed to exist within the class) to produce the necessary data for plotting.
    - Parameters:
        - mode: *str, optional* - The visualization mode. Can take inputs ```stock``` and ```time```. Defaults to ```stock```.
        - y_metric: *str, optional* - The metric to be plotted on the y-axis. Defaults to ```Delta```. Valid values: ```Delta```, ```Gamma```, ```Vega```, ```Theta```, ```Rho```, ```Price```.
        - option_type: *str, optional* - The type of option to visualize. Defaults to ```call```. Valid values: ```call```, ```put```. This parameter is only used in    ```time``` mode.
        - T_days_static: *int, optional* - The fixed number of days to expiry for the ```stock``` mode. Defaults to ```30```.
        - T_days_range: *numpy.ndarray, optional* - A range of days to expiry for the ```time``` mode. Defaults to ```np.arange(7, 181, 7)```.