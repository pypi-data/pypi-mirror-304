import os
import pandas as pd
import numpy as np
import scipy.stats as st
import shap
from tqdm import tqdm
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from lightgbm import LGBMRegressor
from xgboost import XGBRegressor
from .funkit import *
import warnings


class EVkit:
    def __init__(self, data_dir, feature_set=None):
        """
        Initializes the ShapEV class.
        
        Parameters:
        data_dir (str): Directory of the dataset in CSV format. It is assumed to be a regression problem 
                        with the target in the last column.
        feature_set (list, optional): List of feature names to focus on. If not provided, it uses 
                                       all available features.
        """
        os.makedirs('ShapEV', exist_ok=True)
        warnings.filterwarnings("ignore")

        self.feature_set = feature_set
        df = pd.read_csv(data_dir)
        self.X = df.iloc[:, :-1]  # Features
        self.y = np.array(df.iloc[:, -1])  # Target variable
        self.fea = df.columns[:-1]  # Feature names

    def fit(self, model_type='XGBoost', n_iter=500):
        """
        Fits the model using the specified algorithm and performs hyperparameter optimization.

        Parameters:
            model_type (str): The type of model to use. Options include:
                - 'GradientBoosting'
                - 'RandomForest'
                - 'LightGBM'
                - 'XGBoost'
            Default is 'XGBoost'.
            
            n_iter (int): The number of iterations for hyperparameter optimization. 
            Default is 500.

        Returns:
            Trained model instance with optimized hyperparameters.
        """
        # Configure model and hyperparameter distribution based on model type
        if model_type == 'GradientBoosting':
            self.cal_model = GradientBoostingRegressor()
            param_dist = {
                'n_estimators': st.randint(50, 200),
                'learning_rate': st.uniform(0.01, 0.3),
                'max_depth': st.randint(1, 10)
            }
        elif model_type == 'RandomForest':
            self.cal_model = RandomForestRegressor()
            param_dist = {
                'n_estimators': st.randint(50, 200),
                'max_depth': st.randint(1, 20),
                'min_samples_split': st.randint(2, 20),
                'min_samples_leaf': st.randint(1, 10)
            }
        elif model_type == 'LightGBM':
            self.cal_model = LGBMRegressor()
            param_dist = {
                'n_estimators': st.randint(50, 200),
                'learning_rate': st.uniform(0.01, 0.3),
                'max_depth': st.randint(1, 15),
                'num_leaves': st.randint(20, 150)
            }
        elif model_type == 'XGBoost':
            self.cal_model = XGBRegressor()
            param_dist = {
                'n_estimators': st.randint(50, 200),
                'learning_rate': st.uniform(0.01, 0.3),
                'max_depth': st.randint(1, 10),
                'gamma': st.uniform(0, 5)
            }
        else:
            raise ValueError("Undefined model type")

        # Setup hyperparameter search
        self.search = RandomizedSearchCV(
            self.cal_model,
            param_distributions=param_dist,
            n_iter=n_iter,
            scoring='r2',  # Use R² as the scoring metric
            random_state=42,
            n_jobs=-1,
            cv=5,
            verbose=0
        )


        try:
            self.search.fit(self.X, self.y)
            self.model = self.search.best_estimator_
            print(f"Optimized best parameters: {self.search.best_params_}")
            if self.search.best_score_>= 0.75:
                print(f"Optimized best score R² = {self.search.best_score_}")
                
            
        except Exception as e:
            print("All iterations failed; using the model's default parameters.")
            self.model = self.cal_model.fit(self.X, self.y)
            print(f"Error : {e}. Skipping this optimization and continuing.")
           

    def shap(self, SPACE=5):
        """
        Computes SHAP values and identifies the best feature combinations based on SHAP interaction values.
        
        Parameters:
        SPACE (int): The truncation coefficient (default is 5).
        
        Returns:
        bool: True if processing is successful.
        """
        explainer = shap.TreeExplainer(self.model)
        shap_values = explainer.shap_values(self.X)
        shap_interaction_values = explainer.shap_interaction_values(self.X)

        if self.feature_set is None:
            print('No feature set assigned. ShapEV will search all potential combinations.')
            comb = generate_combinations(self.fea)
        elif isinstance(self.feature_set, list):
            print('ShapEV will search the combinations assigned by the user.')
            comb = generate_combinations(self.feature_set)

        best_combination = base_search(shap_interaction_values, comb, self.fea, self.X, SPACE)
        print(f'A subset containing a total of {len(best_combination)} has been screened.')

        _, _, X_updated, equival_value = cal_equal_coef(shap_interaction_values, best_combination, self.fea, self.X)

      
        try:
            self.search.fit(X_updated, self.y)
            _model = self.search.best_estimator_
            print(f"Optimized best parameters: {self.search.best_params_}")
           
        except Exception as e:
            print("All iterations failed; using the model's default parameters.")
            _model = self.cal_model.fit(X_updated, self.y)
            print(f"Error: {e}. Skipping this optimization and continuing.")
           

        _explainer = shap.TreeExplainer(_model)
        _interaction_value = _explainer.shap_interaction_values(X_updated)
        plot_scatter(_interaction_value[:, 0, 0], equival_value)

        # Prepare data for saving
        data = {
            "Equivalent Values": equival_value,
            "Joint SHAP Values": _interaction_value[:, 0, 0]
        }

        # Convert dictionary to DataFrame and save as CSV
        df = pd.DataFrame(data)
        df.to_csv("./ShapEV/equivalent_values.csv", index=False, encoding='utf-8-sig')

        print("Equivalent CSV file has been saved: equivalent_values.csv")

        return True
