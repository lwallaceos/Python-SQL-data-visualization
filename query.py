import pandas as pd


def get_top_titles(df):
    # Returns top 10 job titles based on frequency
    if df.empty or "job_title" not in df.columns:
        return pd.DataFrame(columns=["job_title", "count"])
    top = df["job_title"].value_counts().head(10).reset_index()
    top.columns = ["job_title", "count"]
    top["count"] = pd.to_numeric(top["count"], errors="coerce")
    return top


def get_location_distribution(df):
    # Aggregates job counts by location
    if df.empty or "location" not in df.columns:
        return pd.DataFrame(columns=["location", "count"])
    loc = df["location"].value_counts().reset_index()
    loc.columns = ["location", "count"]
    loc["count"] = pd.to_numeric(loc["count"], errors="coerce")
    return loc


def get_salary_distribution(df):
    # Returns the salary column for histogram plotting
    if df.empty or "salary_in_usd" not in df.columns:
        return pd.DataFrame(columns=["salary"])
    return df[["salary_in_usd"]].rename(columns={"salary_in_usd": "salary"})
