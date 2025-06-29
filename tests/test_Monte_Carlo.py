import pytest
from options_pricer.models.Monte_Carlo import MonteCarlo

S = 101.15          #stock price
K = 98.01           #strike price
vol = 0.0991        #volatility (%)
r = 0.01            #risk-free rate (%)
N = 1000            #number of time steps
M = 10000           #number of simulations

#Testing code functionality for call options
test_monte_carlo=MonteCarlo(101.15, 98.01, 0.0991, 0.01, 0.1644, 'call', 0, 0)
def test_calculate_stock_price():
    assert test_monte_carlo.calculate_stock_price().shape == (test_monte_carlo.N + 1, test_monte_carlo.M)\
    
def test_calculate_option_price_for_call():
    lnSt = test_monte_carlo.calculate_stock_price()
    C0, CT = test_monte_carlo.calculate_option_price(lnSt)
    assert C0 == 3.7588
    assert CT[-1].mean() == pytest.approx(3.765, rel=1e-3)

def test_simulate_for_call():
    SE=test_monte_carlo.simulate()
    assert SE == pytest.approx(0.03, rel=1e-3)

#Testing code functionality for put options
test_monte_carlo=MonteCarlo(101.15, 98.01, 0.0991, 0.01, 0.1644, 'put', 0, 0)
def test_calculate_option_price_for_put():
    lnSt = test_monte_carlo.calculate_stock_price()
    C0, CT = test_monte_carlo.calculate_option_price(lnSt)
    assert C0 == 0.4405
    assert CT[-1].mean() == pytest.approx(0.4412, rel=1e-3)

def test_simulate_for_put():
    SE=test_monte_carlo.simulate()
    assert SE == pytest.approx(0.01, rel=1e-3)


