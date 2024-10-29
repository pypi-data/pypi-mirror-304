# modelinsightharsh/visualizations.py

import plotly.graph_objs as go

def create_shap_plot(shap_values, feature_names):
    # Ensure shap_values is correctly formatted as a single array
    shap_values = shap_values[0] if isinstance(shap_values, list) else shap_values
    data = [go.Bar(
        x=feature_names,
        y=shap_values,
        marker=dict(color=shap_values, colorscale='RdBu')
    )]
    layout = go.Layout(title='SHAP Feature Importance')
    return go.Figure(data=data, layout=layout)

def create_lime_plot(lime_exp):
    # Use as_list() to convert Explanation object to list of tuples
    exp_list = lime_exp.as_list()  # This ensures we have a list of (feature, weight) tuples
    features, weights = zip(*exp_list)  # Unpack features and weights

    # Plot with Plotly
    data = [go.Bar(
        x=features,
        y=weights,
        marker=dict(color=weights, colorscale='RdBu')
    )]
    layout = go.Layout(title='LIME Explanation')
    return go.Figure(data=data, layout=layout)
