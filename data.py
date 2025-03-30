import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and preprocess the job postings data."""
    if df.empty:
        return df
    # Standardize column names to lower case and strip whitespace
    df.columns = df.columns.str.lower().str.strip()

    # Enhanced mapping: define alternate candidates for each required column
    mapping_candidates = {
        "job_title": ["job title", "title", "position", "job"],
        "location": ["job location", "location", "city", "area", "region", "state"],
        "salary_in_usd": ["salary", "salary usd", "compensation", "salary_in_usd"],
    }
    for required_col, alternatives in mapping_candidates.items():
        if required_col not in df.columns:
            for candidate in alternatives:
                if candidate in df.columns:
                    df = df.rename(columns={candidate: required_col})
                    break

    # Check for missing required columns after mapping
    required = ["job_title", "location", "salary_in_usd"]
    missing = set(required) - set(df.columns)
    if missing:
        print(f"Missing required columns: {', '.join(missing)}")
        return pd.DataFrame()

    # Handle missing values: Drop rows missing required columns
    df = df.dropna(subset=required)
    # Convert salary to numeric in case of improper types
    df["salary_in_usd"] = pd.to_numeric(df["salary_in_usd"], errors="coerce")
    # Optionally fill or drop any extra missing values
    df = df.fillna({"employment_type": "Not Specified"})
    return df
