import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from options_pricer_European.models.Black_Scholes import BlackScholes

class BSOptionsVisualizer:
    def __init__(self, K, r, sigma, option_types=('call', 'put')):
        self.K = K
        self.r = r
        self.sigma = sigma
        self.option_types = option_types

    def generate_data(self, T_days_range, mode='time'):
        stock_prices = np.linspace(self.K * 0.8, self.K * 1.2, 100)
        rows = []

        for T_days in T_days_range:
            T = T_days / 365
            for S in stock_prices:
                for opt_type in self.option_types:
                    bs = BlackScholes(S, self.K, self.sigma, self.r, T)
                    rows.append({
                        'Stock Price': S,
                        'Option Type': opt_type,
                        'T_days': T_days,
                        'Price': bs.price(opt_type),
                        'Delta': bs.delta(opt_type),
                        'Gamma': bs.gamma(),
                        'Vega': bs.vega(),
                        'Theta': bs.theta(opt_type),
                        'Rho': bs.rho(opt_type)
                    })
            if mode == 'stock':
                break  # Only use the first T_days for static plot
        return pd.DataFrame(rows)

    def visualize(self, mode='stock', y_metric='Delta', option_type='call', T_days_static=30, T_days_range=np.arange(7, 181, 7)):
        """
        mode: 'stock' (for static) or 'time' (for animation)
        y_metric: Greek or 'Price'
        option_type: 'call' or 'put'
        """
        if mode not in ['stock', 'time']:
            raise ValueError("Invalid mode. Choose 'stock' or 'time'.")

        if y_metric not in ['Delta', 'Gamma', 'Vega', 'Theta', 'Rho', 'Price']:
            raise ValueError("Invalid metric. Choose from Delta, Gamma, Vega, Theta, Rho, Price.")

        if mode == 'stock':
            df = self.generate_data([T_days_static], mode='stock')
            fig = go.Figure()

            for opt_type in self.option_types:
                data = df[df['Option Type'] == opt_type]
                fig.add_trace(go.Scatter(
                    x=data['Stock Price'],
                    y=data[y_metric],
                    mode='lines',
                    name=f"{y_metric} ({opt_type})"
                ))

            fig.update_layout(
                title=f"{y_metric} vs Stock Price (T = {T_days_static} days)",
                xaxis_title='Stock Price',
                yaxis_title=y_metric,
                height=500
            )
            fig.show()

        elif mode == 'time':
            df = self.generate_data(T_days_range, mode='time')
            df = df[df['Option Type'] == option_type]

            fig = px.line(
                df,
                x='Stock Price',
                y=y_metric,
                color='T_days',
                animation_frame='T_days',
                title=f"{option_type.capitalize()} Option: {y_metric} vs Stock Price over Time",
                labels={"T_days": "Days to Expiry"}
            )
            fig.update_layout(height=500)
            fig.show()

# Initialize visualizer
#vis = BSOptionsVisualizer(K=18000, r=0.1, sigma=0.08)

# 🔵 Stock price vs Greek at fixed time
#vis.visualize(mode='stock', y_metric='Vega', T_days_static=45)

# 🔴 Greek vs stock over time (animated)
#vis.visualize(mode='time', y_metric='Theta', option_type='call')
