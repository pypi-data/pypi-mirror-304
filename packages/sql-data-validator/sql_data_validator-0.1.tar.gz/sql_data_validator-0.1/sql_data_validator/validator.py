import pandas as pd
import numpy as np
import sqlite3  # Replace with a specific SQL connector if needed, e.g., psycopg2 for PostgreSQL

class SQLDataValidator:
    def __init__(self, db_connection):
        """
        Initializes the validator with a database connection.
        :param db_connection: Database connection object
        """
        self.db_connection = db_connection

    def fetch_table_data(self, table_name):
        """
        Fetches data from the specified table.
        :param table_name: Name of the table to fetch data from
        :return: DataFrame of the table data
        """
        query = f"SELECT * FROM {table_name}"
        return pd.read_sql(query, self.db_connection)

    def check_missing_values(self, df):
        """
        Checks for missing values in each column of the DataFrame.
        :param df: DataFrame to check
        :return: Dictionary with counts of missing values per column
        """
        missing_report = df.isnull().sum()
        return missing_report[missing_report > 0].to_dict()

    def check_data_type_inconsistencies(self, df):
        """
        Checks for data type inconsistencies in each column.
        :param df: DataFrame to check
        :return: Dictionary of columns with type inconsistencies
        """
        type_inconsistencies = {}
        for col in df.columns:
            if df[col].apply(lambda x: isinstance(x, type(df[col].iloc[0]))).sum() != len(df):
                type_inconsistencies[col] = str(df[col].dtype)
        return type_inconsistencies

    def check_outliers(self, df, z_threshold=3):
        """
        Identifies outliers in numeric columns using the Z-score method.
        :param df: DataFrame to check
        :param z_threshold: Threshold for Z-score to consider as outlier
        :return: Dictionary with outlier counts per column
        """
        numeric_cols = df.select_dtypes(include=[np.number])
        outliers = {}
        for col in numeric_cols.columns:
            z_scores = (numeric_cols[col] - numeric_cols[col].mean()) / numeric_cols[col].std()
            outliers[col] = df[(z_scores.abs() > z_threshold)].shape[0]
        return outliers

    def run_validations(self, table_name):
        """
        Runs all validation checks on a table and returns a summary report.
        :param table_name: Name of the table to validate
        :return: Dictionary containing results of all validations
        """
        df = self.fetch_table_data(table_name)
        return {
            "missing_values": self.check_missing_values(df),
            "type_inconsistencies": self.check_data_type_inconsistencies(df),
            "outliers": self.check_outliers(df)
        }
