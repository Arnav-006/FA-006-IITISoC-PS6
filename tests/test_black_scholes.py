import pytest
import pandas as pd
from options_pricer_European.models.Black_Scholes import BlackScholes
from options_pricer_European.utils.Visualisation_Tools_Black_Scholes import BSOptionsVisualizer

@pytest.fixture
def bs_call():
    return BlackScholes(S=17854.05, K=17750, sigma=0.0839, r=0.10, T=6/365)

def test_call_price(bs_call):
    price = bs_call.price('call')
    assert isinstance(price, float) and price > 0

def test_delta_range(bs_call):
    d = bs_call.delta('call')
    assert 0 <= d <= 1

def test_greeks_signs(bs_call):
    assert bs_call.gamma() > 0
    assert bs_call.vega() > 0
    assert isinstance(bs_call.theta('call'), float)

def test_visualizer_dataframe():
    vis = BSOptionsVisualizer(K=17750, r=0.10, sigma=0.0839, T=6/365)
    vis.generate_data()
    df = vis.df
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert 'Price' in df.columns

