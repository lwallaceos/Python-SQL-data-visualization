import streamlit as st
import pandas as pd
from database import setup_database, insert_jobs
from query import get_top_titles, get_location_distribution, get_salary_distribution
from utils import plot_bar_chart, plot_histogram, plot_pie_chart
from data import clean_data


st.set_page_config(
    page_title="Job Insights Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Initialize database
setup_database()

# Load the dataset into a DataFrame
try:
    df = pd.read_csv("job_postings.csv")  # Replace with the actual path to your dataset
    df = clean_data(df)  # Clean the data using the clean_data function
except FileNotFoundError:
    st.error("Default dataset not found. Please upload a CSV file to proceed.")
    df = pd.DataFrame()  # Initialize an empty DataFrame

# Dynamic filter values (if dataset available)
if not df.empty and "salary_in_usd" in df.columns:
    salary_min = int(df["salary_in_usd"].min())
    salary_max = int(df["salary_in_usd"].max())
    job_titles = sorted(df["job_title"].dropna().unique())
    locations_list = sorted(df["location"].dropna().unique())
else:
    salary_min, salary_max = 0, 300000
    job_titles, locations_list = [], []

st.title("📊 Job Insights Dashboard")

# File upload
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.dataframe(
            df.head(), use_container_width=True
        )  # Use full width for better display
        if "Unnamed: 0" in df.columns:
            df = df.drop(
                columns=["Unnamed: 0"]
            )  # Drop the Unnamed: 0 column if it exists
        insert_jobs(df)
    except Exception as e:
        st.error(f"Error processing uploaded file: {e}")

# Sidebar Filters (updated to use multiselects and dynamic slider)
st.sidebar.header("🔍 Filters")
selected_job_titles = st.sidebar.multiselect(
    "Select Job Title(s)", options=job_titles, default=job_titles
)
selected_locations = st.sidebar.multiselect(
    "Select Location(s)", options=locations_list, default=locations_list
)
salary_range = st.sidebar.slider(
    "Filter by Salary (USD)",
    min_value=salary_min,
    max_value=salary_max,
    value=(salary_min, salary_max),
    step=1000,
)

# Define required columns
required_columns = {"job_title", "location", "salary_in_usd"}

# Check if all required columns are present
missing_columns = required_columns - set(df.columns)
if missing_columns:
    st.error(
        f"The dataset is missing the following required columns: {', '.join(missing_columns)}. "
        "Please upload a valid dataset."
    )
    # Continue with the unfiltered data so that some visuals are shown
    filtered_df = df
else:
    # Apply filters to the DataFrame
    filtered_df = df[
        df["job_title"].isin(selected_job_titles)
        & df["location"].isin(selected_locations)
        & df["salary_in_usd"].between(salary_range[0], salary_range[1])
    ]
    if filtered_df.empty:
        st.info("No data with the selected filters. Showing overall dataset instead.")
        filtered_df = df

# Summary KPIs
st.sidebar.header("📈 Summary KPIs")
if not filtered_df.empty:
    st.sidebar.metric("Total Jobs", len(filtered_df))
    avg_salary = filtered_df["salary_in_usd"].mean(skipna=True)
    max_salary = filtered_df["salary_in_usd"].max()
    st.sidebar.metric(
        "Average Salary (USD)",
        f"${round(avg_salary, 2):,}" if pd.notnull(avg_salary) else "N/A",
    )
    st.sidebar.metric(
        "Max Salary (USD)", f"${max_salary:,}" if pd.notnull(max_salary) else "N/A"
    )

# Main Content
st.markdown("## 📊 Data Overview")
st.dataframe(filtered_df.head(), use_container_width=True)

# Visualizations
st.markdown("## 📈 Visualizations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📍 Jobs by Location")
    locations_data = get_location_distribution(filtered_df)
    plot_bar_chart(
        locations_data, "location", "count", "Jobs by Location", color="green"
    )

    st.markdown("### 📊 Top Job Titles")
    top_titles = get_top_titles(filtered_df)
    plot_bar_chart(top_titles, "job_title", "count", "Top Job Titles", color="blue")

with col2:
    st.markdown("### 💰 Salary Distribution")
    salaries = get_salary_distribution(filtered_df)
    plot_histogram(
        salaries,
        "salary",
        "Salary Distribution",
        color="orange",
    )

    st.markdown("### 📊 Employment Type Distribution")
    if "employment_type" in filtered_df.columns:
        emp_counts = filtered_df["employment_type"].value_counts().reset_index()
        emp_counts.columns = ["employment_type", "count"]
        plot_pie_chart(
            emp_counts,
            "employment_type",
            "count",
            "Employment Type Distribution",
            style={"title_fontsize": 18, "label_fontsize": 14},
        )
    else:
        st.info("Employment type data not available in the current CSV file.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "© 2023 Job Insights Dashboard | Built with ❤️ using Streamlit"
    "</div>",
    unsafe_allow_html=True,
)
