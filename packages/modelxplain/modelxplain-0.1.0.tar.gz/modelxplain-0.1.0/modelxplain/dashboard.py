# modelinsightharsh/dashboard.py

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from .visualization import create_shap_plot, create_lime_plot

class Dashboard:
    def __init__(self, explainer, X_test):
        self.explainer = explainer
        self.X_test = X_test.reset_index(drop=True)
        self.app = dash.Dash(__name__)
        self._setup_layout()
        
    def _setup_layout(self):
        self.app.layout = html.Div([
            html.H1("Model Insight Harsh Dashboard"),
            dcc.Dropdown(
                id='instance-dropdown',
                options=[{'label': f'Instance {i}', 'value': i} for i in self.X_test.index],
                value=0
            ),
            dcc.Graph(id='shap-plot'),
            dcc.Graph(id='lime-plot'),
            html.Button("Export Visuals", id='export-button'),
            dcc.Download(id='download-report')
        ])
        
        @self.app.callback(
            [Output('shap-plot', 'figure'), Output('lime-plot', 'figure')],
            [Input('instance-dropdown', 'value')]
        )
        def update_plots(instance_index):
            X_instance = self.X_test.iloc[[instance_index]]
            shap_values = self.explainer.explain_shap(X_instance)
            lime_exp = self.explainer.explain_lime(X_instance)
            
            shap_fig = create_shap_plot(shap_values, X_instance.columns)
            lime_fig = create_lime_plot(lime_exp)
            return shap_fig, lime_fig
        
        @self.app.callback(
            Output('download-report', 'data'),
            [Input('export-button', 'n_clicks')],
            prevent_initial_call=True
        )
        def export_visuals(n_clicks):
            # Implement export functionality here
            pass  # Placeholder for actual implementation
        
    def run(self):
        self.app.run_server(debug=True)
