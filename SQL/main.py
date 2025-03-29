import streamlit as st
from data import load_job_data, clean_data
from database import init_db, insert_jobs
from query import get_top_titles, get_location_distribution
from utils import plot_bar

st.title("Job Insights Dashboard")

uploaded_file = st.file_uploader("Upload Job Postings CSV", type=["csv"])

if uploaded_file:
    df = load_job_data(uploaded_file)
    df = clean_data(df)
    init_db()
    insert_jobs(df)

    st.subheader("Top Job Titles")
    top_titles = get_top_titles()
    fig1 = plot_bar(top_titles, "job_title", "count", "Top Job Titles")
    st.pyplot(fig1)

    st.subheader("Job Locations")
    loc_dist = get_location_distribution()
    fig2 = plot_bar(loc_dist[:10], "location", "count", "Top Locations")
    st.pyplot(fig2)

    st.success("Dashboard loaded successfully!")
