# FA-006-IITISoC-PS6
This repository contains an extensive python package for pricing options.

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
-num_points : *int, optional*
    - Number of stock price points to plot P&L. If ```None``` defaults to 100.

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
-num_points : *int, optional*
    - Number of stock price points to plot P&L. If ```None``` defaults to 100.

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
-num_points : *int, optional*
    - Number of stock price points to plot P&L. If ```None``` defaults to 100.

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
-num_points : *int, optional*
    - Number of stock price points to plot P&L. If ```None``` defaults to 100.

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
-num_points : *int, optional*
    - Number of stock price points to plot P&L. If ```None``` defaults to 100.

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
-num_points : *int, optional*
    - Number of stock price points to plot P&L. If ```None``` defaults to 100.

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
-num_points : *int, optional*
    - Number of stock price points to plot P&L. If ```None``` defaults to 100.

#### Examples

```python
# Example using Black-Scholes model
Collar(S=100, K1=95, K2=105, sigma=0.2, r=0.05, T=1.0, model="BS")

# Example using Binomial model with different parameters
Collar(S=50, K1=45, K2=55, sigma=0.25, r=0.03, T=0.5, model="BIN", num_points=200)
```
---
