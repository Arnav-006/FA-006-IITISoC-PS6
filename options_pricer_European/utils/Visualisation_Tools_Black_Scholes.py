from options_pricer_European.models.Black_Scholes import BlackScholes 
import numpy as np
import pandas as pd
from scipy.stats import norm
import plotly.graph_objs as go
from plotly.subplots import make_subplots

class BS_Options_Visualizer:
    def __init__(self, K, r, sigma, T, option_types=('call', 'put')):
        self.K = K
        self.r = r
        self.sigma = sigma
        self.T = T
        self.option_types = option_types
        self.stock_prices = np.linspace(K * 0.8, K * 1.2, 100)
        self.df = None

    def generate_data(self):
        rows = []
        for S in self.stock_prices:
            for opt_type in self.option_types:
                bs = BlackScholes(S, self.K, self.sigma, self.r, self.T)
                rows.append({
                    'Stock Price': S,
                    'Option Type': opt_type,
                    'Price': bs.price(opt_type),
                    'Delta': bs.delta(opt_type),
                    'Gamma': bs.gamma(),
                    'Vega': bs.vega(),
                    'Theta': bs.theta(opt_type),
                    'Rho': bs.rho(opt_type)
                })
        self.df = pd.DataFrame(rows)

    def save_to_excel(self, filename='option_greeks.xlsx'):
        self.df.to_excel(filename, index=False)

    def plot(self):
        if self.df is None:
            self.generate_data()

        fig = make_subplots(rows=3, cols=2, subplot_titles=('Delta', 'Gamma', 'Vega', 'Theta', 'Rho', 'Price'))

        greeks = ['Delta', 'Gamma', 'Vega', 'Theta', 'Rho', 'Price']
        row_col = [(1, 1), (1, 2), (2, 1), (2, 2), (3, 1), (3, 2)]

        for (greek, (r, c)) in zip(greeks, row_col):
            for opt_type in self.option_types:
                data = self.df[self.df['Option Type'] == opt_type]
                fig.add_trace(go.Scatter(x=data['Stock Price'], y=data[greek],
                                         mode='lines', name=f'{greek} ({opt_type})'),
                              row=r, col=c)

        fig.update_layout(height=1000, width=1000, title_text="Black-Scholes Option Greeks")
        fig.show()

# --- Run Visualization ---

# vis = BS_Options_Visualizer(K=17750, r=0.10, sigma=0.0839, T=6/365)
# vis.generate_data()
# vis.plot()
# vis.save_to_excel()
