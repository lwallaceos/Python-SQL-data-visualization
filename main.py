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
# Custom CSS for better visuals
st.markdown(
    """
    <style>
    .big-title { font-size: 40px; font-weight: bold; }
    .subheader { font-size: 28px; }
    </style>
""",
    unsafe_allow_html=True,
)


# Initialize database
setup_database()

# Load dataset from default CSV and clean
try:
    df = pd.read_csv("job_postings.csv")  # Reference CSV for SQL information
    df = clean_data(df)
except FileNotFoundError:
    st.error("Default dataset not found. Please upload a CSV file to proceed.")
    df = pd.DataFrame()

# Dynamic filter values based on CSV columns
if not df.empty:
    available_columns = set(df.columns)
    salary_min = (
        int(df["salary_in_usd"].min()) if "salary_in_usd" in available_columns else 0
    )
    salary_max = (
        int(df["salary_in_usd"].max())
        if "salary_in_usd" in available_columns
        else 300000
    )
    job_titles = (
        sorted(df["job_title"].dropna().unique())
        if "job_title" in available_columns
        else []
    )
    locations_list = (
        sorted(df["location"].dropna().unique())
        if "location" in available_columns
        else []
    )
    companies = (
        sorted(df["company"].dropna().unique())
        if "company" in available_columns
        else []
    )
else:
    salary_min, salary_max, job_titles, locations_list, companies = (
        0,
        300000,
        [],
        [],
        [],
    )

# File upload and insertion into database
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head(), use_container_width=True)
        if "Unnamed: 0" in df.columns:
            df = df.drop(columns=["Unnamed: 0"])
        insert_jobs(df)
        df = clean_data(df)
    except Exception as e:
        st.error(f"Error processing uploaded file: {e}")

# Sidebar Filters and Summary KPIs
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
if companies:
    selected_companies = st.sidebar.multiselect(
        "Select Company(s)", options=companies, default=companies
    )
else:
    selected_companies = None

required_columns = {"job_title", "location", "salary_in_usd"}
missing_columns = required_columns - set(df.columns)
if missing_columns:
    st.error(f"Missing columns: {', '.join(missing_columns)}. Showing unfiltered data.")
    filtered_df = df
else:
    filtered_df = df[
        df["job_title"].isin(selected_job_titles)
        & df["location"].isin(selected_locations)
        & df["salary_in_usd"].between(salary_range[0], salary_range[1])
    ]
    if selected_companies is not None:
        filtered_df = filtered_df[filtered_df["company"].isin(selected_companies)]
    if filtered_df.empty:
        st.info("No data with the selected filters. Showing overall dataset instead.")
        filtered_df = df

if not filtered_df.empty:
    st.sidebar.header("📈 Summary KPIs")
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

# Create two tabs: Dashboard and SQL Data
tabs = st.tabs(["Dashboard", "SQL Data"])

with tabs[0]:
    st.markdown(
        '<p class="big-title">📊 Job Insights Dashboard</p>', unsafe_allow_html=True
    )
    st.markdown("### Data Overview")
    st.dataframe(filtered_df.head(), use_container_width=True)

    st.markdown("#### Data Source")
    if uploaded_file:
        st.info("CSV file uploaded and processed into SQL database.")
    else:
        st.info("Default CSV loaded for SQL reference.")

    st.markdown("## Visualizations")
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

        # Additional Insight: Average Salary by Job Title
        if (
            "salary_in_usd" in filtered_df.columns
            and "job_title" in filtered_df.columns
        ):
            st.markdown("### 💼 Average Salary by Job Title")
            avg_salary_title = (
                filtered_df.groupby("job_title")["salary_in_usd"].mean().reset_index()
            )
            avg_salary_title.columns = ["job_title", "avg_salary"]
            plot_bar_chart(
                avg_salary_title,
                "job_title",
                "avg_salary",
                "Average Salary by Job Title",
                color="purple",
            )
    with col2:
        st.markdown("### 💰 Salary Distribution")
        salaries = get_salary_distribution(filtered_df)
        plot_histogram(salaries, "salary", "Salary Distribution", color="orange")

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
            st.info("Employment type data not available.")

        # Additional Insight: Top Companies by Job Postings
        if "company" in filtered_df.columns:
            st.markdown("### 🏢 Top Companies by Job Postings")
            top_companies = filtered_df["company"].value_counts().reset_index()
            top_companies.columns = ["company", "count"]
            plot_bar_chart(
                top_companies, "company", "count", "Top Companies", color="teal"
            )

with tabs[1]:
    st.markdown('<p class="big-title">SQL Data Integration</p>', unsafe_allow_html=True)
    st.markdown("### Overview")
    st.markdown(
        "The CSV file used in this dashboard is integrated with a SQL database. Data insertion is handled on upload, with synchronization to SQL."
    )
    st.write("Total job postings available:", len(df) if not df.empty else "N/A")

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>© 2023 Job Insights Dashboard | Built with ❤️ using Streamlit</div>",
    unsafe_allow_html=True,
)
