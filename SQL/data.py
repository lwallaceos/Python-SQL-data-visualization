import matplotlib.pyplot as plt
import pandas as pd


def load_job_data(filepath):
    return pd.read_csv(filepath)


def clean_data(df):
    df.dropna(subset=["job_title", "company", "location"], inplace=True)
    df["posted_date"] = pd.to_datetime(df["posted_date"], errors="coerce")
    return df
