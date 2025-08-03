
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from options_pricer_European.models.Black_Scholes import BlackScholes

class BSOptionsVisualizer:
    """
    Various visualization tools are provided for European options using the Black-Scholes model, implemented using
    the BlackScholes class under models.

    *class* BSOptionsVisualizer
    *module* - **options_pricer_European.utils.Visualization_Tools_Black_Scholes**

    Class that implements various methods to visualize how options' prices varies using plotly and pandas

    ### Usage
    ```python
    vis = BSOptionsVisualizer(K, r, sigma, option_types=('call', 'put'))
    ```

    ### Parameters

    - K : *float*
        - The strike price.
    - r : *float*
        - The risk-free rate of interest(annualized, as a decimal).
    - sigma : *float*
        - The volatility of the underlying stock.
    - option_types : *tuple*
        - Tuple of types of options used for making database.

    ### Returns
        - object of class BSOptionsVisualizer
    
    ### Methods

        - generate_data()
            - returns a Pandas dataframe containing prices calculated for various option contracts
            - Parameters:
                - T_days_range : *array-type* - a range like object that is used for choosing values of time of expiration.
                - mode : *str, optional* - mode that specifies what to make the graph against. Accepts ```stock```or ```time```.
            - Returns:
                - a Pandas dataframe containing prices data for options dataframe

        - visualize()
            - The visualize function generates visualizations of option pricing metrics (Greeks and price) against the underlying stock price. It offers two primary modes of operation: 'stock' for a static visualization at a single point in time, and 'time' for an animated visualization showing the evolution of the metrics as the time to expiration changes. The function relies on a self.generate_data method (assumed to exist within the class) to produce the necessary data for plotting.
            - Parameters:
                - mode: *str, optional* - The visualization mode. Can take inputs ```stock``` and ```time```. Defaults to ```stock```.
                - y_metric: *str, optional* - The metric to be plotted on the y-axis. Defaults to ```Delta```. Valid values: ```Delta```, ```Gamma```, ```Vega```, ```Theta```, ```Rho```, ```Price```.
                - option_type: *str, optional* - The type of option to visualize. Defaults to ```call```. Valid values: ```call```, ```put```. This parameter is only used in    ```time``` mode.
                - T_days_static: *int, optional* - The fixed number of days to expiry for the ```stock``` mode. Defaults to ```30```.
                - T_days_range: *numpy.ndarray, optional* - A range of days to expiry for the ```time``` mode. Defaults to ```np.arange(7, 181, 7)```.
    """
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

