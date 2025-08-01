
import pytest
from options_pricer_European.models.Binomial import Binomial

# -- Standard Tests --

def test_call_option_standard():
    price = Binomial(100, 100, 1, 0.05, 0.2, 'call')
    assert abs(price.price_options() - 10.45) < 1.0

def test_put_option_standard():
    price = Binomial(100, 100, 1, 0.05, 0.2,  'put')
    assert abs(price.price_options() - 5.57) < 1.0

# -- Zero Time to Maturity --

def test_zero_time_call():
    price = Binomial(120, 100, 0, 0.05, 0.2, 'call')
    assert price.price_options() == 20

def test_zero_time_put():
    price = Binomial(80, 100, 0, 0.05, 0.2, 'put')
    assert price.price_options() == 20

# -- Zero Volatility --

def test_zero_volatility_call():
    price = Binomial(105, 100, 1, 0.05, 0.0,  'call')
    assert price.price_options() > 0

def test_zero_volatility_put():
    price = Binomial(95, 100, 1, 0.05, 0.0,  'put')
    assert price.price_options() > 0

# -- Single Step Tree --

def test_one_step_call():
    price = Binomial(100, 100, 1, 0.05, 0.2, 'call')
    assert price.price_options() >= 0

def test_one_step_put():
    price = Binomial(100, 100, 1, 0.05, 0.2, 'put')
    assert price.price_options() >= 0

# -- Deep ITM / OTM --

def test_deep_itm_call():
    price = Binomial(200, 100, 1, 0.05, 0.2,  'call')
    assert price.price_options() > 95

def test_deep_otm_put():
    price = Binomial(200, 100, 1, 0.05, 0.2,  'put')
    assert price.price_options() < 1

# -- Zero Risk-Free Rate --

def test_zero_risk_free_call():
    price = Binomial(100, 100, 1, 0.0, 0.2,  'call')
    assert price.price_options() > 0

def test_zero_risk_free_put():
    price = Binomial(100, 100, 1, 0.0, 0.2,  'put')
    assert price.price_options() > 0

# -- Invalid Inputs --

def test_negative_stock_price():
    with pytest.raises(ValueError):
        Binomial(-100, 100, 1, 0.05, 0.2).price_options()

def test_zero_steps():
    with pytest.raises(ValueError):
        Binomial(100, 100, 1, 0.05, 0.2).price_options()
