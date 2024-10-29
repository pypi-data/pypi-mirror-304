# modelinsightharsh/model_loader.py

from sklearn.base import BaseEstimator
import xgboost as xgb
import tensorflow as tf

class ModelLoader:
    def __init__(self, model):
        self.model = model
        self.model_type = self._detect_model_type()
    
    def _detect_model_type(self):
        # Check for XGBoost model type first
        if isinstance(self.model, xgb.XGBModel):
            return 'xgboost'
        elif isinstance(self.model, BaseEstimator):
            return 'sklearn'
        elif isinstance(self.model, tf.keras.Model):
            return 'tensorflow'
        else:
            raise ValueError("Unsupported model type.")
    
    def predict(self, X):
        if hasattr(self.model, "predict_proba"):
            return self.model.predict_proba(X)
        elif self.model_type == 'tensorflow':
            return self.model.predict(X).flatten()
        else:
            return self.model.predict(X)
