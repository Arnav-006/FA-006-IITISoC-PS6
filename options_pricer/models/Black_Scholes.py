import numpy as np
import pandas as pd
from scipy.stats import norm


class BlackScholes:
    def __init__(self, S, K, sigma, r, T):
        self.S = S
        self.K = K
        self.sigma = sigma
        self.r = r
        self.T = T
        self._compute_d1_d2()

    def _compute_d1_d2(self):
        self.d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
        self.d2 = self.d1 - self.sigma * np.sqrt(self.T)

    def price(self, option_type):
        if option_type == 'call':
            return self.S * norm.cdf(self.d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2)
        else:
            return self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2) - self.S * norm.cdf(-self.d1)

    def delta(self, option_type):
        return norm.cdf(self.d1) if option_type == 'call' else norm.cdf(self.d1) - 1

    def gamma(self):
        return norm.pdf(self.d1) / (self.S * self.sigma * np.sqrt(self.T))

    def vega(self):
        return self.S * norm.pdf(self.d1) * np.sqrt(self.T) / 100

    def theta(self, option_type):
        term1 = -self.S * norm.pdf(self.d1) * self.sigma / (2 * np.sqrt(self.T))
        term2 = self.r * self.K * np.exp(-self.r * self.T)
        return (term1 - term2 * norm.cdf(self.d2)) / 365 if option_type == 'call' else (term1 + term2 * norm.cdf(-self.d2)) / 365

    def rho(self, option_type):
        rho_val = self.K * self.T * np.exp(-self.r * self.T)
        return rho_val * norm.cdf(self.d2) / 100 if option_type == 'call' else -rho_val * norm.cdf(-self.d2) / 100
    

    #Classic Option Strategies

    #Bull Spreads
    """Bull Call Spread - buy a call at a strike price K, and sell a put at a higher strike price K2
                        - ideal if we are moderately bullish, expecting underlying price to rise till the higher strike and not skyrocket above it
                        - selling a put for a higher strike K2 also reduces the upfront cost as buying only a call for a low strike can be pretty expensive
    """
    def Bull_Call_Spread(self, K2):
        if(K2 <= self.K):
            print("Invalid input (K < K1 does not hold)")
        else:
            call_buy = np.maximum(self.S - self.K, 0.0)
            call_sell = np.maximum(self.S - K2,0.0)
            payoff = call_buy - call_sell
            buy_prem = self.price('call')
            sell_prem = BlackScholes(self.S,K2,self.sigma,self.r,self.T).price('call')
            PL = payoff - buy_prem + sell_prem          #PL is less than payoff
            return payoff,PL
    

    """Bull Put Spread - buy a put at a strike price K, and sell a put at a higher strike price K2
                       - useful if we want to limit our loss by selling a put at strike K2
                       - also investment in buying a call at lower strike is much less expensive than higher strike, hence premium gained on selling put
                       at higher price is not affected majorly
    """
    def Bull_Pull_Spread(self, K2):
        if(K2 <= self.K):
            print("Invalid input (K < K1 does not hold)")
        else:
            put_buy = np.maximum(self.K - self.S, 0.0)
            put_sell = np.maximum(K2 - self.S,0.0)
            payoff = put_buy - put_sell
            buy_prem = self.price('put')
            sell_prem = BlackScholes(self.S,K2,self.sigma,self.r,self.T).price('put')
            PL = payoff - buy_prem + sell_prem          #PL is greater than payoff
            return payoff,PL


    #Bear Spreads
    """Bear Call Spread - buy a call at a strike price K, and sell a put at a higher strike price K2
                        - ideal if we are moderately bullish, expecting underlying price to rise till the higher strike and not skyrocket above it
                        - selling a put for a higher strike K2 also reduces the upfront cost as buying only a call for a low strike can be pretty expensive
    """
    def Bear_Call_Spread(self, K2):
        if(K2 <= self.K):
            print("Invalid input (K < K1 does not hold)")
        else:
            call_buy = np.maximum(self.S - self.K, 0.0)
            call_sell = np.maximum(self.S - K2,0.0)
            payoff = call_buy - call_sell
            buy_prem = self.price('call')
            sell_prem = BlackScholes(self.S,K2,self.sigma,self.r,self.T).price('call')
            PL = payoff - buy_prem + sell_prem          #PL is less than payoff
            return payoff,PL
    

    """Bear Put Spread - buy a put at a strike price K, and sell a put at a higher strike price K2
                       - useful if we want to limit our loss by selling a put at strike K2
                       - also investment in buying a call at lower strike is much less expensive than higher strike, hence premium gained on selling put
                       at higher price is not affected majorly
    """
    def Bear_Pull_Spread(self, K2):
        if(K2 <= self.K):
            print("Invalid input (K < K1 does not hold)")
        else:
            put_buy = np.maximum(self.K - self.S, 0.0)
            put_sell = np.maximum(K2 - self.S,0.0)
            payoff = put_buy - put_sell
            buy_prem = self.price('put')
            sell_prem = BlackScholes(self.S,K2,self.sigma,self.r,self.T).price('put')
            PL = payoff - buy_prem + sell_prem          #PL is greater than payoff
            return payoff,PL

    """Straddle - 
    """
    def Straddle(self):
        put = np.maximum(self.K-self.S, 0.0)
        call = np.maximum(self.S-self.K, 0.0)
        payoff = put+call
        put_price = self.price('put')
        call_price = self.price('call')
        PL = payoff - put_price - call_price
        return payoff,PL
    
    """Strangle - 
    """
    def Strangle(self,K2):
        if(K2 <= self.K):
            print("Invalid input (K < K1 does not hold)")
        else:
            put = np.maximum(self.K2-self.stock_price, 0.0)
            call = np.maximum(self.stock_price-self.K, 0.0)
            payoff = put+call
            put_price = BlackScholes(self.S,K2,self.sigma,self.r,self.T).price('put')
            call_price = self.price('call')
            PL = payoff - call_price - put_price
            return payoff,PL
    

    """Collar -
    """
    def Collar(self,K2):
        if not (self.K < K2):
            print("Invalid input (K < K1 does not hold)")
            quit()                                              ## needs to be looked at
        else:
            put = np.maximum(self.K-self.S, 0.0)
            call = np.maximum(self.S-self.K2, 0.0)
            payoff = put-call
            call_price = BlackScholes(self.S,K2,self.sigma,self.r,self.T).price('call')
            put_price = self.price('put')
            PL = payoff - put_price + call_price
        return payoff,PL
    
