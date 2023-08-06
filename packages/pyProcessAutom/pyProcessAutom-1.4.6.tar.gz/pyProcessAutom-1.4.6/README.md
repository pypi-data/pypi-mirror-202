Data Preprocessing Library - Aryan Sakhala
---
This library provides a set of functions for preprocessing data in pandas DataFrames.

Installation
You can install this package using pip:

```
pip install pyProcessAutom
```
# Usage
To use this library, simply import the DataPreprocessor class from the data_preprocess module and instantiate it with a pandas DataFrame. You can then call various methods of the DataPreprocessor class to preprocess the data.

Here's an example of how to use this library:
```
import pandas as pd
from auto_preprocess.data_preprocess import DataPreprocessor

# Load data into a pandas DataFrame
df = pd.read_csv("my_data.csv")

# Preprocess the data using the DataPreprocessor class
preprocessor = DataPreprocessor(df)
preprocessor.remove_outliers()
preprocessor.scale(scaler_type='standard')
preprocessor.label_encode()
preprocessor.impute(method='mean')
preprocessor.drop()
preprocessed_df = preprocessor.df
```
# Use the preprocessed data as needed
Functions
This library provides the following functions for preprocessing data:

* remove_outliers(): Removes outliers from all numeric columns in the DataFrame.
* scale(scaler_type): Scales all numeric columns in the DataFrame using either a standard scaler or a min-max scaler.
* label_encode(): Encodes all columns with binary categories using label encoding.
* impute(method): Fills all columns with less than 10% NaN values with either the mean, median, or mode, as specified by the user.
* drop(): Drops all columns with more than 30% NaN values from the DataFrame.
License

This project is licensed under the MIT License - see the LICENSE.txt file for details.