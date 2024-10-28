import pandas as pd
from sklearn.preprocessing import PolynomialFeatures, OneHotEncoder, OrdinalEncoder
from sklearn.feature_selection import VarianceThreshold, mutual_info_classif
from category_encoders import TargetEncoder
from sklearn.ensemble import RandomForestClassifier
import numpy as np

class AutoFeatureEngineering:
    def __init__(self, target_col, encoding_method="onehot"):
        """
        Initialize with specified encoding method for categorical variables.
        
        Parameters:
            target_col (str): The target column for supervised feature engineering.
            encoding_method (str): Encoding method for categorical features.
                Options: "onehot", "ordinal", "target", "frequency"
        """
        self.target_col = target_col
        self.encoding_method = encoding_method
        self.categorical_cols = []
        self.numerical_cols = []
        self.datetime_cols = []

    def detect_column_types(self, df):
        """Detects column types."""
        self.categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        self.numerical_cols = df.select_dtypes(include=['number']).columns
        self.datetime_cols = df.select_dtypes(include=['datetime']).columns

    def encode_categorical(self, df):
        """Encodes categorical features based on the specified encoding method."""
        if self.encoding_method == "onehot":
            df = pd.get_dummies(df, columns=self.categorical_cols, drop_first=True)
        elif self.encoding_method == "ordinal":
            encoder = OrdinalEncoder()
            df[self.categorical_cols] = encoder.fit_transform(df[self.categorical_cols])
        elif self.encoding_method == "target":
            encoder = TargetEncoder()
            df[self.categorical_cols] = encoder.fit_transform(df[self.categorical_cols], df[self.target_col])
        elif self.encoding_method == "frequency":
            for col in self.categorical_cols:
                freq_encoding = df[col].value_counts() / len(df)
                df[col] = df[col].map(freq_encoding)
        return df

    def engineer_features(self, df):
        """Applies polynomial and interaction features to numerical columns."""
        poly = PolynomialFeatures(degree=2, include_bias=False)
        poly_features = poly.fit_transform(df[self.numerical_cols])
        poly_df = pd.DataFrame(poly_features, columns=poly.get_feature_names_out(self.numerical_cols))
        df = pd.concat([df.reset_index(drop=True), poly_df.reset_index(drop=True)], axis=1)
        return df

    def rank_features(self, df):
        """Ranks features based on importance using Random Forest."""
        X = df.drop(columns=[self.target_col])
        y = df[self.target_col]
        model = RandomForestClassifier()
        model.fit(X, y)
        feature_importances = pd.Series(model.feature_importances_, index=X.columns)
        return feature_importances.sort_values(ascending=False)

    def remove_irrelevant_features(self, df, feature_importances, threshold=0.01):
        """Removes features below the importance threshold."""
        relevant_features = feature_importances[feature_importances > threshold].index
        return df[relevant_features]

    def fit_transform(self, df):
        """Combines all steps into a single fit and transform process."""
        # Step 1: Detect column types
        self.detect_column_types(df)

        # Step 2: Encode categorical features
        df = self.encode_categorical(df)

        # Step 3: Engineer polynomial and interaction features
        df = self.engineer_features(df)

        # Step 4: Rank features by importance
        feature_importances = self.rank_features(df)

        # Step 5: Remove irrelevant features
        df = self.remove_irrelevant_features(df, feature_importances)

        return df
