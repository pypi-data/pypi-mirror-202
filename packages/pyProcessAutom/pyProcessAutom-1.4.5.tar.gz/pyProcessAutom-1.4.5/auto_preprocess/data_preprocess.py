import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder

class DataPreprocessor:
    
    def __init__(self, df):
        self.df = df
        
    def remove_outliers(self):
        num_cols = self.df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        for col in num_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            self.df = self.df[(self.df[col] >= lower_bound) & (self.df[col] <= upper_bound)]
    
    def scale(self, scaler_type):
        num_cols = self.df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        if scaler_type == 'standard':
            scaler = StandardScaler()
        elif scaler_type == 'minmax':
            scaler = MinMaxScaler()
        else:
            raise ValueError('Invalid scaler type. Valid options are "standard" or "minmax"')
        self.df[num_cols] = scaler.fit_transform(self.df[num_cols])
        
    def label_encode(self):
        bin_cols = self.df.select_dtypes(include=['bool']).columns.tolist()
        le = LabelEncoder()
        for col in bin_cols:
            self.df[col] = le.fit_transform(self.df[col])
    
    def impute(self, method='mean'):
    # Get numeric columns with missing values
        num_cols = self.df.select_dtypes(include=['float64', 'int64']).columns[self.df.select_dtypes(include=['float64', 'int64']).isna().any()].tolist()
        # Fill missing values with specified method or default to mean
        if method == 'mean':
            self.df[num_cols] = self.df[num_cols].fillna(self.df[num_cols].mean())
    
        elif method == 'mode':
            self.df[num_cols] = self.df[num_cols].fillna(self.df[num_cols].mode())
        elif method == 'median':
            self.df[num_cols] = self.df[num_cols].fillna(self.df[num_cols].median())
        else:
            raise ValueError('Invalid imputation method. Valid options are "mean", "mode", or "median"')

    def drop(self):
        nan_percent = self.df.isna().sum() / self.df.shape[0]
        cols_to_drop = nan_percent[nan_percent > 0.3].index.tolist()
        self.df = self.df.drop(columns=cols_to_drop)
