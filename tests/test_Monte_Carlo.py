import pytest
from options_pricer.models.Monte_Carlo import MonteCarlo

S = 101.15          #stock price
K = 98.01           #strike price
vol = 0.0991        #volatility (%)
r = 0.01            #risk-free rate (%)
N = 1000            #number of time steps
M = 10000           #number  simulations

#Condition when put option is ITM

test_monte_carlo=MonteCarlo(101.15, 98.01, 0.0991, 0.01, 0.1644, 0, 0)

def test_calculate_stock_price():
    assert test_monte_carlo.calculate_stock_price().shape == (test_monte_carlo.N + 1, test_monte_carlo.M)

def test_calculate_option_price_for_call_1():
    lnSt = test_monte_carlo.calculate_stock_price()
    C0, CT = test_monte_carlo.calculate_option_price(lnSt, 'call')
    assert C0 == 3.7588
    assert CT[-1].mean() == pytest.approx(3.75, rel=5*(1e-2))

def test_simulate_for_call_1():
    SE=test_monte_carlo.simulate('call')[1]
    assert SE == pytest.approx(0.03, rel=1e-3)

def test_calculate_option_price_for_put_1():
    lnSt = test_monte_carlo.calculate_stock_price()
    C0, CT = test_monte_carlo.calculate_option_price(lnSt, 'put')
    assert C0 == S - K
    assert CT == S - K

def test_simulate_for_put_1():
    SE=test_monte_carlo.simulate('put')[1]
    assert SE == 0


#Condition when call option is ITM

test_monte_carlo=MonteCarlo(98.01, 101.15, 0.0991, 0.01, 0.1644, 0, 0)

def test_calculate_option_price_for_put_2():
    lnSt = test_monte_carlo.calculate_stock_price()
    C0, CT = test_monte_carlo.calculate_option_price(lnSt, 'put')
    assert C0 == 3.4674
    assert CT[-1].mean() == pytest.approx(3.473, rel=1e-3)

def test_simulate_for_put_2():
    SE=test_monte_carlo.simulate('put')[1]
    assert SE == pytest.approx(0.03, rel=1e-3)

def test_calculate_option_price_for_call_2():
    lnSt = test_monte_carlo.calculate_stock_price()
    C0, CT = test_monte_carlo.calculate_option_price(lnSt, 'call')
    assert C0 == K - S
    assert CT == K - S

def test_simulate_for_call_2():
    SE=test_monte_carlo.simulate('call')[1]
    assert SE == 0

