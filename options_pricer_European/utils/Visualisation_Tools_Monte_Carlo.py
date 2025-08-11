#Visualisation tools for Greeks are not functioning.

import matplotlib.pyplot as plt
from options_pricer_European.models.Monte_Carlo import MonteCarlo 
import numpy as np
from scipy import stats
from options_pricer_European.utils.Greeks import delta, gamma, vega, theta



class MC_Visualiser:
    def __init__(self, obj):        
        self.mc=obj

    def visualise_greeks(self,type):
        stock_data= (np.exp(self.mc.calculate_stock_price()[0]) + np.exp(self.mc.calculate_stock_price()[1]))*0.5
        payoffs=np.maximum(0,(stock_data-self.mc.K))   #Payoff matrix
        option_prices=[np.exp(-self.mc.r*(MonteCarlo.N - i)*self.mc.T/MonteCarlo.N)*payoffs[i,:] 
                       for i in range(MonteCarlo.N+1)][-1]  #Option price matrix obtained from simulations
        k=0
        risk_metric_values=[]
        match type:
            case 'delta':
                for p in option_prices:
                    temp_obj=MonteCarlo(p, self.mc.K, self.mc.vol, self.mc.r, 
                                        (MonteCarlo.N-k)*self.mc.T/MonteCarlo.N, self.mc.option_type)
                    risk_metric_values.append(delta('MC',temp_obj))
                    k+=1

                plt.plot(risk_metric_values)
                plt.ylabel('Delta')
                plt.xlabel('Time Steps')
                plt.title('Variation of Delta')
        
            case 'gamma':
                for p in option_prices:
                    temp_obj=MonteCarlo(p, self.mc.K, self.mc.vol, self.mc.r, 
                                        (MonteCarlo.N-k)*self.mc.T/MonteCarlo.N, self.mc.option_type)
                    risk_metric_values.append(delta('MC',temp_obj))
                    k+=1

                plt.plot(risk_metric_values)
                plt.ylabel('Gamma')
                plt.xlabel('Time Steps')
                plt.title('Variation of Gamma')

            case 'theta':
                for p in option_prices:
                    temp_obj=MonteCarlo(p, self.mc.K, self.mc.vol, self.mc.r, 
                                        (MonteCarlo.N-k)*self.mc.T/MonteCarlo.N, self.mc.option_type)
                    risk_metric_values.append(delta('MC',temp_obj))
                    k+=1

                plt.plot(risk_metric_values)
                plt.ylabel('Theta')
                plt.xlabel('Time Steps')
                plt.title('Variation of Theta')

            case 'vega':
                for p in option_prices:
                    temp_obj=MonteCarlo(p, self.mc.K, self.mc.vol, self.mc.r, 
                                        (MonteCarlo.N-k)*self.mc.T/MonteCarlo.N, self.mc.option_type)
                    risk_metric_values.append(delta('MC',temp_obj))
                    k+=1
                
                plt.plot(risk_metric_values)
                plt.ylabel('Vega')
                plt.xlabel('Time Steps')
                plt.title('Variation of Vega')


        plt.show()


    """
    The function below helps the user understand the accuracy of the simulation against a test input (where 
    market price is already known).
    """

    def probability_distribution(self, market_value):
        C0=self.mc.simulate()[0]
        SE=self.mc.simulate()[1]

        x1 = np.linspace(C0-3*SE, C0-1*SE, 100)
        x2 = np.linspace(C0-1*SE, C0+1*SE, 100)
        x3 = np.linspace(C0+1*SE, C0+3*SE, 100)

        s1 = stats.norm.pdf(x1, C0, SE)
        s2 = stats.norm.pdf(x2, C0, SE)
        s3 = stats.norm.pdf(x3, C0, SE)

        plt.fill_between(x1, s1, color='tab:blue',label='> StDev')
        plt.fill_between(x2, s2, color='cornflowerblue',label='1 StDev')
        plt.fill_between(x3, s3, color='tab:blue')

        plt.plot([C0,C0],[0, max(s2)*1.1], 'k',
        label='Theoretical Value')
        plt.plot([market_value,market_value],[0, max(s2)*1.1], 'r',
        label='Market Value')

        plt.ylabel("Probability")
        plt.xlabel("Option Price")
        plt.legend()
        plt.show()

    def histogram(self):
        C0=self.mc.simulate()[0]
        SE=self.mc.simulate()[1]
        payoffs=np.maximum(0,(np.exp(self.mc.calculate_stock_price())-self.mc.K))   #Payoff matrix
        option_prices=[np.exp(-self.mc.r*(MonteCarlo.N - i)*self.mc.T/MonteCarlo.N)*payoffs[i,:] 
                       for i in range(MonteCarlo.N+1)][-1]  #Option price matrix obtained from simulations
        # print(C0)
        # print(payoffs)
        # print(f"\n{option_prices}")
        plt.hist(option_prices, bins=12, edgecolor='black')
        plt.show()

    def stock_graph(self):
        stock_data= (np.exp(self.mc.calculate_stock_price()[0]) + np.exp(self.mc.calculate_stock_price()[1]))*0.5     #Predicted stock price matrix
        plt.plot(stock_data)
        plt.ylabel('Stock Price')
        plt.xlabel('Time Steps')
        plt.title('MC simulation of a stock price')
        plt.show()

    def option_price_graph(self):
        stock_data= (np.exp(self.mc.calculate_stock_price()[0]) + np.exp(self.mc.calculate_stock_price()[1]))*0.5
        payoffs=np.maximum(0,(stock_data-self.mc.K))   #Payoff matrix
        option_prices=[np.exp(-self.mc.r*(MonteCarlo.N - i)*self.mc.T/MonteCarlo.N)*payoffs[i,:] 
                       for i in range(MonteCarlo.N+1)]      #option price matrix obtained from simulations
        plt.plot(option_prices)
        plt.ylabel('Option Premium')
        plt.xlabel('Time Steps')
        plt.title('MC simulation of an option premium')
        plt.show()



