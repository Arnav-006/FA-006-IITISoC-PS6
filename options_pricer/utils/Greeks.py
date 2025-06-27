from models.Monte_Carlo import MonteCarlo 
from models.Black_Scholes import BlackScholes

"""
The plan is to implement the greek functions on the objects of the models which would have parameters 
passed into their constructors.
"""

def delta(type, obj):
    match type:
        case 'MC':
            """
            Functions to compute option price will be implemented on the object 'montecarlo' of class
            MonteCarlo
            """
            montecarlo=MonteCarlo(obj.S, obj.K, obj.vol, obj.r, obj.T, obj.option_type)

            # Change of $1 assumed in the stock price
            return montecarlo.calculate_option_price(montecarlo.calculate_stock_price(), 1)[0]-montecarlo.calculate_option_price(montecarlo.calculate_stock_price(), 0)[0]
        case 'BS':
            bs = BlackScholes(obj.S, obj.K, obj.vol, obj.r, obj.T)
            return bs.delta(option_type=obj.option_type)
        case 'BOPM':
            pass

def gamma(type, obj):
    match type:
        case 'MC':
            montecarlo=MonteCarlo(obj.S, obj.K, obj.vol, obj.r, obj.T, obj.option_type)
            delta_1= delta('MC', obj, 0)
            delta_2= delta('MC', obj, 1)
            """
            Finding the difference between the deltas of two intervals of stock prices and then dividing it
            by the total interval
            """
            return (delta_2 - delta_1) / 2
        case 'BS':
            bs = BlackScholes(obj.S, obj.K, obj.vol, obj.r, obj.T)
            return bs.gamma()
        case 'BOPM':
            pass

def theta(type, obj):
    match type:
        case 'MC':
            montecarlo_1=MonteCarlo(obj.S, obj.K, obj.vol, obj.r, obj.T, obj.option_type, 1/MonteCarlo.N)
            montecarlo_2=MonteCarlo(obj.S, obj.K, obj.vol, obj.r, obj.T, obj.option_type)

            # Difference in values calculated over a period of 1/N years
            return (montecarlo_1.calculate_option_price(montecarlo_1.calculate_stock_price())[0]-
                    montecarlo_2.calculate_option_price(montecarlo_2.calculate_stock_price())[0])*MonteCarlo.N
        case 'BS':
            bs = BlackScholes(obj.S, obj.K, obj.vol, obj.r, obj.T)
            return bs.theta(option_type=obj.option_type)
        case 'BOPM':
            pass

def vega(type, obj):
    match type:
        case 'MC':
            montecarlo_1=MonteCarlo(obj.S, obj.K, obj.vol, obj.r, obj.T, obj.option_type, 0, 
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
            pass
