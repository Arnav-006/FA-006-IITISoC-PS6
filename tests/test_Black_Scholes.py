import pytest
import pandas as pd
from options_pricer.models.Black_Scholes import BlackScholes
from options_pricer.utils.Visualisation_Tools import BS_Options_Visualizer

@pytest.fixture
def bs_call(_option_type):
    return BlackScholes(S=17854.05, K=17750, sigma=0.0839, r=0.10, T=6/365, option_type=_option_type)

def test_price_options_for_call(bs_call):
    price = bs_call('call').price_options()
    assert price == 104.34

def test_price_options_for_put(bs_call):
    price = bs_call('put').price_options()
    assert price == 104.34



