from pathlib import Path

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


class PremiumFeatureEngineer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        X["bmi"] = X["weight"] / (X["height"] ** 2)
        X["age_group"] = X["age"].apply(self._age_group)
        X["city_tier"] = X["city"].apply(self._city_tier)
        X["lifestyle_risk"] = X.apply(self._lifestyle_risk, axis=1)
        X["smoker"] = X["smoker"].astype(int)

        return X[
            ["age", "income_lpa", "bmi", "city_tier", "smoker", "city", "occupation", "age_group", "lifestyle_risk"]
        ]

    @staticmethod
    def _age_group(age):
        if age < 25:
            return "young"
        if age < 45:
            return "adult"
        if age < 60:
            return "middle_aged"
        return "senior"

    @staticmethod
    def _city_tier(city):
        tier_1_cities = {
            "Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"
        }
        tier_2_cities = {
            "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
            "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
            "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
            "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
            "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
            "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
        }
        if city in tier_1_cities:
            return 1
        if city in tier_2_cities:
            return 2
        return 3

    @staticmethod
    def _lifestyle_risk(row):
        bmi = row["bmi"]
        smoker = bool(row["smoker"])
        if smoker and bmi > 30:
            return "high"
        if smoker or bmi > 27:
            return "medium"
        return "low"


def build_pipeline() -> Pipeline:
    numeric_features = ["age", "income_lpa", "bmi", "city_tier", "smoker"]
    categorical_features = ["city", "occupation", "age_group", "lifestyle_risk"]

    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown="ignore", sparse_output=False)

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ],
        remainder="drop",
        sparse_threshold=0,
    )

    pipeline = Pipeline(
        steps=[
            ("feature_engineer", PremiumFeatureEngineer()),
            ("preprocessor", preprocessor),
            ("classifier", RandomForestClassifier(random_state=42, n_jobs=-1)),
        ]
    )
    return pipeline
