import matplotlib.pyplot as plt
import numpy as np

from ..models.Black_Scholes import BlackScholes
from ..models.Monte_Carlo import MonteCarlo
from ..models.Binomial import Binomial

#Classic Option Strategies
#Functions that return PnL graphs based on option premium prices calculated using model chosen by user - BS, BIN, MC

#Bull Spreads
"""Bull Call Spread - buy a call at a strike price K, and sell a put at a higher strike price K2
                    - ideal if we are moderately bullish, expecting underlying price to rise till the higher strike and not skyrocket above it
                    - selling a put for a higher strike K2 also reduces the upfront cost as buying only a call for a low strike can be pretty expensive
"""
def Bull_Call_Spread(S, K1, K2, r, sigma, T, model = "BS", S_max=None, num_points=100):

    if K2 <= K1:
        print("Invalid input (K2 <= K1 does not hold)")
        return
    
    # Define stock price range
    S_min = 0
    S_max = S_max if S_max is not None else 1.5 * K2  
    S_range = np.linspace(S_min, S_max, num_points)
    
    # Calculate payoff for each stock price
    call_buy = np.maximum(S_range - K1, 0.0)
    call_sell = np.maximum(S_range - K2, 0.0)
    payoff = call_buy - call_sell
    
    # Calculate premiums
    if(model == "BS"):
        buy_prem = BlackScholes(S, K1, sigma, r, T).price('call')  
        sell_prem = BlackScholes(S, K2, sigma, r, T).price('call')
    elif(model == "BIN"):
        buy_prem = Binomial(S,K1,sigma,r,T,'call').price_options()
        sell_prem = Binomial(S,K2,sigma,r,T,'call').price_options()
    elif(model == "MC"):
        buy_prem = MonteCarlo(S,K1,sigma,r,T,'call').simulate()[0]
        sell_prem = MonteCarlo(S,K2,sigma,r,T,'call').simulate()[0]
    
    # Calculate P&L
    PL = payoff - buy_prem + sell_prem
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(S_range, PL, label='P&L', color='blue')
    plt.axhline(0, color='black', linestyle='--', linewidth=0.5)
    plt.axvline(K1, color='gray', linestyle='--', label=f'K1 = {K1}')
    plt.axvline(K2, color='gray', linestyle='--', label=f'K2 = {K2}')
    plt.title('Bull Call Spread P&L')
    plt.xlabel('Stock Price')
    plt.ylabel('Profit and Loss')
    plt.legend()
    plt.grid(True)
    plt.show()


"""Bull Put Spread - buy a put at a strike price K, and sell a put at a higher strike price K2
                    - useful if we want to limit our loss by selling a put at strike K2
                    - also investment in buying a call at lower strike is much less expensive than higher strike, hence premium gained on selling put
                    at higher price is not affected majorly
"""
def Bull_Put_Spread(S, K1, K2, r, sigma, T, model = "BS", S_max=None, num_points=100):

    if K2 <= K1:
        print("Invalid input (K2 <= K1 does not hold)")
        return
    
    # Define stock price range
    S_min = 0
    S_max = S_max if S_max is not None else 1.5 * K2  
    S_range = np.linspace(S_min, S_max, num_points)
    
    # Calculate payoff for each stock price
    put_buy = np.maximum(K1 - S_range, 0.0)
    put_sell = np.maximum(K2 - S_range, 0.0)
    payoff = put_buy - put_sell
    
    # Calculate premiums
    if(model == "BS"):
        buy_prem = BlackScholes(S, K1, sigma, r, T).price('put')  
        sell_prem = BlackScholes(S, K2, sigma, r, T).price('put')
    elif(model == "BIN"):
        buy_prem = Binomial(S,K1,sigma,r,T,'put').price_options()
        sell_prem = Binomial(S,K2,sigma,r,T,'put').price_options()
    elif(model == "MC"):
        buy_prem = MonteCarlo(S,K1,sigma,r,T,'put').simulate()[0]
        sell_prem = MonteCarlo(S,K2,sigma,r,T,'put').simulate()[0]
    
    # Calculate P&L
    PL = payoff - buy_prem + sell_prem
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(S_range, PL, label='P&L', color='blue')
    plt.axhline(0, color='black', linestyle='--', linewidth=0.5)
    plt.axvline(K1, color='gray', linestyle='--', label=f'K1 = {K1}')
    plt.axvline(K2, color='gray', linestyle='--', label=f'K2 = {K2}')
    plt.title('Bull Put Spread P&L')
    plt.xlabel('Stock Price')
    plt.ylabel('Profit and Loss')
    plt.legend()
    plt.grid(True)
    plt.show()

#Bear Spreads
"""Bear Call Spread - buy a call at a strike price K, and sell a put at a higher strike price K2
                    - ideal if we are moderately bullish, expecting underlying price to rise till the higher strike and not skyrocket above it
                    - selling a put for a higher strike K2 also reduces the upfront cost as buying only a call for a low strike can be pretty expensive
"""
def Bear_Call_Spread(S, K1, K2, r, sigma, T, model = "BS", S_max=None, num_points=100):

    if K2 <= K1:
        print("Invalid input (K2 <= K1 does not hold)")
        return
    
    # Define stock price range
    S_min = 0
    S_max = S_max if S_max is not None else 1.5 * K2  
    S_range = np.linspace(S_min, S_max, num_points)
    
    # Calculate payoff for each stock price
    call_buy = np.maximum(S_range - K2, 0.0)
    call_sell = np.maximum(S_range - K1, 0.0)
    payoff = call_buy - call_sell
    
    #Calculate premiums
    if(model == "BS"):
        sell_prem = BlackScholes(S, K1, sigma, r, T).price('call')  
        buy_prem = BlackScholes(S, K2, sigma, r, T).price('call')
    elif(model == "BIN"):
        sell_prem = Binomial(S,K1,sigma,r,T,'call').price_options()
        buy_prem = Binomial(S,K2,sigma,r,T,'call').price_options()
    elif(model == "MC"):
        sell_prem = MonteCarlo(S,K1,sigma,r,T,'call').simulate()[0]
        buy_prem = MonteCarlo(S,K2,sigma,r,T,'call').simulate()[0]
    
    # Calculate P&L
    PL = payoff - buy_prem + sell_prem
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(S_range, PL, label='P&L', color='blue')
    plt.axhline(0, color='black', linestyle='--', linewidth=0.5)
    plt.axvline(K1, color='gray', linestyle='--', label=f'K1 = {K1}')
    plt.axvline(K2, color='gray', linestyle='--', label=f'K2 = {K2}')
    plt.title('Bear Call Spread P&L')
    plt.xlabel('Stock Price')
    plt.ylabel('Profit and Loss')
    plt.legend()
    plt.grid(True)
    plt.show()


"""Bear Put Spread - buy a put at a strike price K, and sell a put at a higher strike price K2
                    - useful if we want to limit our loss by selling a put at strike K2
                    - also investment in buying a put at lower strike is much less expensive than higher strike, hence premium gained on selling put
                    at higher price is not affected majorly
"""
def Bear_Put_Spread(S, K1, K2, r, sigma, T, model = "BS", S_max=None, num_points=100):

    if K2 <= K1:
        print("Invalid input (K2 <= K1 does not hold)")
        return
    
    # Define stock price range
    S_min = 0
    S_max = S_max if S_max is not None else 1.5 * K2  
    S_range = np.linspace(S_min, S_max, num_points)
    
    # Calculate payoff for each stock price
    put_buy = np.maximum(K2 - S_range, 0.0)
    put_sell = np.maximum(K1 - S_range, 0.0)
    payoff = put_buy - put_sell
    
    #Calculate premiums
    if(model == "BS"):
        sell_prem = BlackScholes(S, K1, sigma, r, T).price('put')  
        buy_prem = BlackScholes(S, K2, sigma, r, T).price('put')
    elif(model == "BIN"):
        sell_prem = Binomial(S,K1,sigma,r,T,'put').price_options()
        buy_prem = Binomial(S,K2,sigma,r,T,'put').price_options()
    elif(model == "MC"):
        sell_prem = MonteCarlo(S,K1,sigma,r,T,'put').simulate()[0]
        buy_prem = MonteCarlo(S,K2,sigma,r,T,'put').simulate()[0]
    
    # Calculate P&L
    PL = payoff - buy_prem + sell_prem
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(S_range, PL, label='P&L', color='blue')
    plt.axhline(0, color='black', linestyle='--', linewidth=0.5)
    plt.axvline(K1, color='gray', linestyle='--', label=f'K1 = {K1}')
    plt.axvline(K2, color='gray', linestyle='--', label=f'K2 = {K2}')
    plt.title('Bear Put Spread P&L')
    plt.xlabel('Stock Price')
    plt.ylabel('Profit and Loss')
    plt.legend()
    plt.grid(True)
    plt.show()


"""Straddle - Buying a put and a call at the same strike price
            - Payoff increases as underlying moves away from the strike, in either direction
            - Hence good strategy if underlying is expecting to move wildly in any direction
"""
def Straddle(S,K,sigma,r,T,model = "BS", num_points = 100):

    # Define stock price range
    S_min = 0
    S_max = S_max if S_max is not None else 2 * K
    S_range = np.linspace(S_min, S_max, num_points)

    #Calculate premiums
    if(model == "BS"):
        call_prem = BlackScholes(S, K, sigma, r, T).price('call')  
        put_prem = BlackScholes(S, K, sigma, r, T).price('put')
    elif(model == "BIN"):
        call_prem = Binomial(S,K,sigma,r,T,'call').price_options()
        put_prem = Binomial(S,K,sigma,r,T,'put').price_options()
    elif(model == "MC"):
        call_prem = MonteCarlo(S,K,sigma,r,T,'call').simulate()[0]
        put_prem = MonteCarlo(S,K,sigma,r,T,'put').simulate()[0]
    
    put = np.maximum(K - S_range, 0.0)
    call = np.maximum(S_range - K, 0.0)
    payoff = put+call


    PL = payoff - put_prem - call_prem
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(S_range, PL, label='P&L', color='blue')
    plt.axhline(0, color='black', linestyle='--', linewidth=0.5)
    plt.axvline(K, color='gray', linestyle='--', label=f'K = {K}')
    plt.title('Straddle P&L')
    plt.xlabel('Stock Price')
    plt.ylabel('Profit and Loss')
    plt.legend()
    plt.grid(True)
    plt.show()

"""Strangle - Buying a call at a lower strike and buying a put at a higher strike
            - Payoff remains constant when underlying remains between K1 and K2, increases when it moves away from it
"""
def Strangle(S,K1,K2,sigma,r,T,model = "BS", num_points = 100):

    if K2 <= K1:
        print("Invalid input (K2 <= K1 does not hold)")
        return
    
    # Define stock price range
    S_min = 0
    S_max = S_max if S_max is not None else 1.5 * K2
    S_range = np.linspace(S_min, S_max, num_points)

    #Calculate premiums
    if(model == "BS"):
        call_prem = BlackScholes(S, K1, sigma, r, T).price('call')  
        put_prem = BlackScholes(S, K2, sigma, r, T).price('put')
    elif(model == "BIN"):
        call_prem = Binomial(S,K1,sigma,r,T,'call').price_options()
        put_prem = Binomial(S,K2,sigma,r,T,'put').price_options()
    elif(model == "MC"):
        call_prem = MonteCarlo(S,K1,sigma,r,T,'call').simulate()[0]
        put_prem = MonteCarlo(S,K2,sigma,r,T,'put').simulate()[0]
    
    put = np.maximum(K2 - S_range, 0.0)
    call = np.maximum(S_range - K1, 0.0)
    payoff = put+call


    PL = payoff - put_prem - call_prem
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(S_range, PL, label='P&L', color='blue')
    plt.axhline(0, color='black', linestyle='--', linewidth=0.5)
    plt.axvline(K1, color='gray', linestyle='--', label=f'K = {K1}')
    plt.axvline(K2, color='gray', linestyle='--', label=f'K = {K2}')
    plt.title('Strangle P&L')
    plt.xlabel('Stock Price')
    plt.ylabel('Profit and Loss')
    plt.legend()
    plt.grid(True)
    plt.show()


"""Collar - Selling a call at a higher price to earn some upfront, and buying a put at a lower price to hedge downside movements
"""
def Collar(S,K1,K2,sigma,r,T,model = "BS", num_points = 100):

    if K2 <= K1:
        print("Invalid input (K2 <= K1 does not hold)")
        return
    
    # Define stock price range
    S_min = 0
    S_max = S_max if S_max is not None else 1.5 * K2
    S_range = np.linspace(S_min, S_max, num_points)

    #Calculate premiums
    if(model == "BS"):
        call_prem = BlackScholes(S, K2, sigma, r, T).price('call')  
        put_prem = BlackScholes(S, K1, sigma, r, T).price('put')
    elif(model == "BIN"):
        call_prem = Binomial(S,K2,sigma,r,T,'call').price_options()
        put_prem = Binomial(S,K1,sigma,r,T,'put').price_options()
    elif(model == "MC"):
        call_prem = MonteCarlo(S,K2,sigma,r,T,'call').simulate()[0]
        put_prem = MonteCarlo(S,K1,sigma,r,T,'put').simulate()[0]
    
    put = np.maximum(K1 - S_range, 0.0)
    call = np.maximum(S_range - K2, 0.0)
    payoff = put - call


    PL = payoff - put_prem + call_prem
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(S_range, PL, label='P&L', color='blue')
    plt.axhline(0, color='black', linestyle='--', linewidth=0.5)
    plt.axvline(K1, color='gray', linestyle='--', label=f'K = {K1}')
    plt.axvline(K2, color='gray', linestyle='--', label=f'K = {K2}')
    plt.title('Strangle P&L')
    plt.xlabel('Stock Price')
    plt.ylabel('Profit and Loss')
    plt.legend()
    plt.grid(True)
    plt.show()
