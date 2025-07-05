import matplotlib.pyplot as plt
from options_pricer.models.Monte_Carlo import MonteCarlo 
import numpy as np

class MC_Visualiser:
    def __init__(self, obj):        
        self.mc=MonteCarlo(obj.S, obj.K, obj.vol, obj.r, obj.T, obj.option_type)

    def stock_graph(self):
        stock_data= np.exp(self.mc.calculate_stock_price())     #Predicted stock price matrix
        plt.plot(stock_data)
        plt.ylabel('Stock Price')
        plt.xlabel('Time Steps')
        plt.title('MC simulation of a stock price')
        plt.show()

    def option_price_graph(self):
        payoffs=np.exp(self.mc.calculate_stock_price())-self.mc.K   #Payoff matrix
        option_prices=[np.exp(-self.mc.r*(MonteCarlo.N - i)*self.mc.T/MonteCarlo.N)*payoffs[i,:] 
                       for i in range(MonteCarlo.N+1)]
        plt.plot(option_prices)
        plt.ylabel('Option Premium')
        plt.xlabel('Time Steps')
        plt.title('MC simulation of an option premium')
        plt.show()

mc=MonteCarlo(101.15, 98.01, 0.0991, 0.01, 0.1644, 'call', 0, 0)
mc_v=MC_Visualiser(mc)
mc_v.stock_graph()      #Variation of stock price with time until maturity
mc_v.option_price_graph()   #Variation of premium with time until maturity
