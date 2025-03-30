import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and preprocess the job postings data."""
    if df.empty:
        return df
    # Standardize column names to lower case and strip whitespace
    df.columns = df.columns.str.lower().str.strip()
    # Check for missing required columns
    required = ["job_title", "location", "salary_in_usd"]
    missing = set(required) - set(df.columns)
    if missing:
        # Log error and return an empty DataFrame if required columns are missing
        print(f"Missing required columns: {', '.join(missing)}")
        return pd.DataFrame()
    # Handle missing values: Drop rows missing required columns
    df = df.dropna(subset=required)
    # Convert salary to numeric in case of improper types
    df["salary_in_usd"] = pd.to_numeric(df["salary_in_usd"], errors="coerce")
    # Optionally fill or drop any extra missing values
    df = df.fillna({"employment_type": "Not Specified"})
    return df
