# data_quality_validator/validator.py

import pandas as pd
import numpy as np
from scipy.stats import zscore
from pandas_profiling import ProfileReport

class DataQualityValidator:
    def __init__(self, df):
        self.df = df
    
    def check_missing_values(self):
        return self.df.isnull().sum()

    def check_duplicates(self):
        return self.df[self.df.duplicated()]

    def detect_outliers(self, method="IQR", z_threshold=3):
        outliers = {}
        if method == "IQR":
            for col in self.df.select_dtypes(include=[np.number]).columns:
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers[col] = self.df[(self.df[col] < (Q1 - 1.5 * IQR)) | (self.df[col] > (Q3 + 1.5 * IQR))]
        elif method == "zscore":
            for col in self.df.select_dtypes(include=[np.number]).columns:
                outliers[col] = self.df[np.abs(zscore(self.df[col])) > z_threshold]
        return outliers

    def validate_data_types(self, expected_dtypes):
        anomalies = {}
        for col, expected_type in expected_dtypes.items():
            if col in self.df.columns:
                if not np.issubdtype(self.df[col].dtype, expected_type):
                    anomalies[col] = self.df[col].dtype
        return anomalies

    def detect_anomalies(self, method="zscore", z_threshold=3):
        anomalies = {}
        if method == "zscore":
            for col in self.df.select_dtypes(include=[np.number]).columns:
                anomalies[col] = self.df[np.abs(zscore(self.df[col])) > z_threshold]
        # Additional methods such as Mahalanobis distance can be implemented here
        return anomalies

    def generate_report(self, output="report.html"):
        report = ProfileReport(self.df, title="Data Quality Report")
        report.to_file(output)
        return f"Report generated: {output}"
