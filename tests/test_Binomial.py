# test_binomial_model.py

import pytest
from options_pricer.models.Binomial import price_options

@pytest.fixture.mark.parametrize


# -- Standard Tests --

def test_call_option_standard():
    price = binomial_option_pricing(100, 100, 1, 0.05, 0.2 'call')
    assert abs(price - 10.45) < 1.0

def test_put_option_standard():
    price = binomial_option_pricing(100, 100, 1, 0.05, 0.2 'put')
    assert abs(price - 5.57) < 1.0

# -- Zero Time to Maturity --

def test_zero_time_call():
    price = binomial_option_pricing(120, 100, 0, 0.05, 0.2, 'call')
    assert price == 20

def test_zero_time_put():
    price = binomial_option_pricing(80, 100, 0, 0.05, 0.2, 'put')
    assert price == 20

# -- Zero Volatility --

def test_zero_volatility_call():
    price = binomial_option_pricing(105, 100, 1, 0.05, 0.0, 'call')
    assert price > 0

def test_zero_volatility_put():
    price = binomial_option_pricing(95, 100, 1, 0.05, 0.0, 'put')
    assert price > 0

# -- Single Step Tree --

def test_one_step_call():
    price = binomial_option_pricing(100, 100, 1, 0.05, 0.2, 'call')
    assert price >= 0

def test_one_step_put():
    price = binomial_option_pricing(100, 100, 1, 0.05, 0.2, 'put')
    assert price >= 0

# -- Deep ITM / OTM --

def test_deep_itm_call():
    price = binomial_option_pricing(200, 100, 1, 0.05, 0.2, 'call')
    assert price > 95

def test_deep_otm_put():
    price = binomial_option_pricing(200, 100, 1, 0.05, 0.2, 'put')
    assert price < 1

# -- Zero Risk-Free Rate --

def test_zero_risk_free_call():
    price = binomial_option_pricing(100, 100, 1, 0.0, 0.2, 'call')
    assert price > 0

def test_zero_risk_free_put():
    price = binomial_option_pricing(100, 100, 1, 0.0, 0.2, 'put')
    assert price > 0

# -- Invalid Inputs --

def test_negative_stock_price():
    with pytest.raises(ValueError):
        binomial_option_pricing(-100, 100, 1, 0.05, 0.2)
