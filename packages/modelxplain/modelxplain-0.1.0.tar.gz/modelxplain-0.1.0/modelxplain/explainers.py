# modelinsightharsh/explainers.py

import shap
from lime.lime_tabular import LimeTabularExplainer
from sklearn.inspection import permutation_importance
import pandas as pd
import numpy as np

class Explainer:
    def __init__(self, model_loader, X_train, mode='classification'):
        self.model_loader = model_loader
        self.X_train = X_train.copy()
        self.mode = mode

        # Initialize SHAP and LIME explainers
        self.shap_explainer = self._init_shap_explainer()
        self.lime_explainer = self._init_lime_explainer()

    def _init_shap_explainer(self):
        if self.model_loader.model_type == 'tensorflow':
            # For TensorFlow models, use DeepExplainer
            return shap.DeepExplainer(self.model_loader.model, self.X_train)
        else:
            # Initialize TreeExplainer without check_additivity in the constructor
            return shap.TreeExplainer(self.model_loader.model, data=self.X_train)

    def _init_lime_explainer(self):
        return LimeTabularExplainer(
            self.X_train.values,
            feature_names=self.X_train.columns.tolist(),
            mode=self.mode
        )

    def explain_shap(self, X_sample):
        # Ensure that X_sample is a DataFrame
        if not isinstance(X_sample, pd.DataFrame):
            X_sample = pd.DataFrame(X_sample, columns=self.X_train.columns)

        # Check that the features match between X_train and X_sample
        assert list(self.X_train.columns) == list(X_sample.columns), "Feature columns do not match!"

        # Ensure data types are consistent
        X_sample = X_sample.astype(self.X_train.dtypes)

        # Compute SHAP values with check_additivity=False passed in shap_values
        shap_values = self.shap_explainer.shap_values(X_sample, check_additivity=False)
        return shap_values

    def explain_lime(self, X_sample):
        # Ensure that X_sample is a DataFrame
        if not isinstance(X_sample, pd.DataFrame):
            X_sample = pd.DataFrame(X_sample, columns=self.X_train.columns)

        # Ensure data types are consistent
        X_sample = X_sample.astype(self.X_train.dtypes)

        # Explain the first instance in X_sample using LIME
        exp = self.lime_explainer.explain_instance(
            X_sample.values[0],
            self.model_loader.predict,
            num_features=len(X_sample.columns)
        )
        return exp

    def permutation_importance(self, X_val, y_val):
        # Ensure that X_val is a DataFrame
        if not isinstance(X_val, pd.DataFrame):
            X_val = pd.DataFrame(X_val, columns=self.X_train.columns)

        # Ensure data types are consistent
        X_val = X_val.astype(self.X_train.dtypes)

        # Compute permutation importance
        perm = permutation_importance(
            self.model_loader.model,
            X_val,
            y_val,
            random_state=42
        )
        return perm





