from models.Monte_Carlo import MonteCarlo 

"""
The plan is to implement the greek functions on the objects of the models which would have parameters 
passed into their constructors.
"""

def delta(type, obj, dev):
    match type:
        case 'MC':
            """
            Functions to compute option price will be implemented on the object 'montecarlo' of class
            MonteCarlo
            """
            montecarlo=MonteCarlo(obj.S, obj.K, obj.vol, obj.r, obj.T)

            # Change of $1 assumed in the stock price
            return montecarlo.calculate_option_price(montecarlo.calculate_stock_price(), 1+dev)[0]-montecarlo.calculate_option_price(montecarlo.calculate_stock_price(), 0+dev)[0]
        case 'BS':
            pass
        case 'BOPM':
            pass

def gamma(type, obj):
    match type:
        case 'MC':
            montecarlo=MonteCarlo(obj.S, obj.K, obj.vol, obj.r, obj.T)
            delta_1= delta('MC', obj, 0)
            delta_2= delta('MC', obj, 1)
            """
            Finding the difference between the deltas of two intervals of stock prices and then dividing it
            by the total interval
            """
            return (delta_2 - delta_1) / 2
        case 'BS':
            pass
        case 'BOPM':
            pass

def theta(type, obj):
    match type:
        case 'MC':
            montecarlo=MonteCarlo(obj.S, obj.K, obj.vol, obj.r, obj.T)
        case 'BS':
            pass
        case 'BOPM':
            pass

def vega(type, obj):
    match type:
        case 'MC':
            montecarlo=MonteCarlo(obj.S, obj.K, obj.vol, obj.r, obj.T)
        case 'BS':
            pass
        case 'BOPM':
            pass