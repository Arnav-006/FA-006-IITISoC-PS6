# FA-006-IITISoC-PS6
This repository contains an extensive python package for pricing options.
📈 Black-Scholes Option Pricing Model
This repository implements the Black-Scholes model to price European call and put options, along with visualizations of various Greeks (Delta, Gamma, Vega, Theta, Rho) and time-based animations. It is designed for interactive use in Google Colab and VS Code with support for Plotly, Matplotlib, and NumPy.

# What is the Black-Scholes Model?
The Black-Scholes model is a mathematical model for pricing European-style options. It provides closed-form formulas for calculating the theoretical value of options, assuming the underlying asset follows geometric Brownian motion with constant volatility and interest rates.

## Features
📌 European Call and Put pricing\
📊 Calculation of Greeks: Delta, Gamma, Vega, Theta, Rho\
📈 Interactive visualizations using Plotly (2D and 3D)\
⏳ Time-to-maturity animation\
🧮 Easily customizable parameters: Strike, Volatility, Rate, Time, etc.\

## Formula
Black-Scholes for Call and Put:\
S: Current stock price\
K: Strike price\
T: Time to maturity (in years)\
r: Risk-free interest rate\
σ: Volatility of the stock\
Then,\
𝑑1=(ln(𝑆/𝐾)+(𝑟+𝜎^2/2)𝑇)/𝜎𝑇,𝑑2=𝑑1−𝜎𝑇\
Call Option Price:\
𝐶=𝑆⋅𝑁(𝑑1)−𝐾𝑒^(−𝑟𝑇)⋅𝑁(𝑑2)\
Put Option Price:\
𝑃=𝐾𝑒−𝑟𝑇⋅𝑁(−𝑑2)−𝑆⋅𝑁(−𝑑1)\
where 𝑁(⋅)is the cumulative distribution function of the standard normal distribution.\
## Greeks
Greek	Interpretation\
Delta	Rate of change of option price w.r.t. underlying\
Gamma	Rate of change of Delta\
Vega	Sensitivity to volatility\
Theta	Time decay\
Rho	Sensitivity to interest rate\
## Visualizations
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
option_type	Call or Put\

## Applications
Financial modeling and trading simulations\
Sensitivity analysis for hedging strategies\
Educational tool for understanding derivatives\
Comparing models like Binomial Tree or Monte Carlo\
## Example Use Case
A trader is considering buying a call option on NIFTY at ₹17,750. Using the Black-Scholes model:\
They estimate a fair price of ₹320.\
The market is asking ₹370 → option is overpriced.\
Delta is 0.65, so for every ₹10 move in NIFTY, the option will move ₹6.5.\
Theta is -5, meaning the option loses ₹5 per day if all else is constant.\
→ This helps the trader decide when to buy, how much to hedge, and when to exit.\
## Fair Valuation of Options
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
Why helpful: Institutions and funds use these sensitivities to hedge positions and manage risk.\
