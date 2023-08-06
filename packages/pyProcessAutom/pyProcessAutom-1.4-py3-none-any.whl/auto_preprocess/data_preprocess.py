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
        num_missing = self.df.select_dtypes(include=['float64', 'int64']).isna().sum()
        num_cols = num_missing[num_missing > 0].index.tolist()
        for col in num_cols:
            if self.df[col].isna().sum() / self.df.shape[0] < 0.1:
                if method == 'mean':
                    self.df[col] = self.df[col].fillna(self.df[col].mean())
                elif method == 'mode':
                    self.df[col] = self.df[col].fillna(self.df[col].mode().iloc[0])
                elif method == 'median':
                    self.df[col] = self.df[col].fillna(self.df[col].median())
                else:
                    raise ValueError('Invalid imputation method. Valid options are "mean", "mode", or "median"')
    
    def drop(self):
        nan_percent = self.df.isna().sum() / self.df.shape[0]
        cols_to_drop = nan_percent[nan_percent > 0.3].index.tolist()
        self.df = self.df.drop(columns=cols_to_drop)
