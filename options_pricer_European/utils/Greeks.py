#This code requires certain changes to re-configure it with Monte_Carlo.py


from options_pricer_European.models.Monte_Carlo import MonteCarlo 
from options_pricer_European.models.Black_Scholes import BlackScholes
from options_pricer_European.models.Binomial import Binomial

"""
The plan is to implement the greek functions on the objects of the models which would have parameters 
passed into their constructors.
"""
eps=0.01
def delta(type, obj, dev=0):
    match type:
        case 'MC':
            """
            Functions to compute option price will be implemented on the object 'montecarlo' of class
            MonteCarlo
            """
            montecarlo_0=MonteCarlo(obj.S, obj.K, obj.vol, obj.r, obj.T, obj.option_type, 0+dev)
            montecarlo_1=MonteCarlo(obj.S, obj.K, obj.vol, obj.r, obj.T, obj.option_type, eps+dev)

            # Change of $1 assumed in the stock price
            return (montecarlo_1.calculate_option_price(montecarlo_1.calculate_stock_price())[0]-
                    montecarlo_0.calculate_option_price(montecarlo_0.calculate_stock_price())[0])/eps
        case 'BS':
            bs = BlackScholes(obj.S, obj.K, obj.vol, obj.r, obj.T)
            return bs.delta(option_type=obj.option_type)
        case 'BOPM':
            binomial_1=Binomial(obj.S, obj.K, obj.sigma, obj.r, obj.T, obj.option_type, eps)
            binomial_2=Binomial(obj.S, obj.K, obj.sigma, obj.r, obj.T, obj.option_type, -eps)
            delta = (binomial_1.price_options()["price"] - binomial_2.price_options()["price"]) / (2 * eps)
            return delta

def gamma(type, obj):
    match type:
        case 'MC':
            montecarlo=MonteCarlo(obj.S, obj.K, obj.vol, obj.r, obj.T, obj.option_type)
            delta_1= delta('MC', obj, 0)
            delta_2= delta('MC', obj, eps)
            """
            Finding the difference between the deltas of two intervals of stock prices and then dividing it
            by the total interval
            """
            return (delta_2 - delta_1) / (2*eps)
        case 'BS':
            bs = BlackScholes(obj.S, obj.K, obj.vol, obj.r, obj.T)
            return bs.gamma()
        case 'BOPM':
            binomial_1=Binomial(obj.S, obj.K, obj.sigma, obj.r, obj.T, obj.option_type, eps)
            binomial_2=Binomial(obj.S, obj.K, obj.sigma, obj.r, obj.T, obj.option_type, -eps)
            binomial_3=Binomial(obj.S, obj.K, obj.sigma, obj.r, obj.T, obj.option_type, 0)
            gamma = (binomial_1.price_options()["price"] - 2*binomial_3.price_options()["price"] + binomial_2.price_options()["price"]) / (eps ** 2)
            return gamma

def theta(type, obj):
    match type:
        case 'MC':
            montecarlo_1=MonteCarlo(obj.S, obj.K, obj.vol, obj.r, obj.T, obj.option_type, 0, 1/MonteCarlo.N)
            montecarlo_2=MonteCarlo(obj.S, obj.K, obj.vol, obj.r, obj.T, obj.option_type)

            # Difference in values calculated over a period of 1/N years
            return (montecarlo_1.calculate_option_price(montecarlo_1.calculate_stock_price())[0]-
                    montecarlo_2.calculate_option_price(montecarlo_2.calculate_stock_price())[0])*MonteCarlo.N
        case 'BS':
            bs = BlackScholes(obj.S, obj.K, obj.vol, obj.r, obj.T)
            return bs.theta(option_type=obj.option_type)
        case 'BOPM':
            binomial_1=Binomial(obj.S, obj.K, obj.sigma, obj.r, obj.T, obj.option_type, 0, -eps)
            binomial_2=Binomial(obj.S, obj.K, obj.sigma, obj.r, obj.T, obj.option_type, 0, 0)
            theta = (binomial_1.price_options()["price"] - binomial_2.price_options()["price"]) / eps
            return theta

def vega(type, obj):
    match type:
        case 'MC':
            montecarlo_1=MonteCarlo(obj.S, obj.K, obj.vol, obj.r, obj.T, obj.option_type, 0, 0, 
                                    obj.vol*(obj.T/MonteCarlo.N))
            montecarlo_2=MonteCarlo(obj.S, obj.K, obj.vol, obj.r, obj.T, obj.option_type)

            """
            Increment in volatility done over the infinitesimal interval of T/N, over which each discrete 
            increment of stock price is calculated
            """
            return (montecarlo_1.calculate_option_price(montecarlo_1.calculate_stock_price())[0]-
                    montecarlo_2.calculate_option_price(montecarlo_2.calculate_stock_price())[0])/(obj.vol*(obj.T/MonteCarlo.N))
        case 'BS':
             bs = BlackScholes(obj.S, obj.K, obj.vol, obj.r, obj.T)
             return bs.vega()
        case 'BOPM':
            binomial_1=Binomial(obj.S, obj.K, obj.sigma, obj.r, obj.T, obj.option_type, 0, 0, eps)
            binomial_2=Binomial(obj.S, obj.K, obj.sigma, obj.r, obj.T, obj.option_type, 0, 0, -eps)
            vega = (binomial_1.price_options()["price"] - binomial_2.price_options()["price"]) / (2 * eps)
            return vega