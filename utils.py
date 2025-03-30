try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    import streamlit as st

    st.error(
        "Matplotlib module is not installed. Please run 'pip install matplotlib' in your terminal."
    )
    raise

import streamlit as st


def plot_bar_chart(df, x, y, title, color):
    """Plot a bar chart using pandas and matplotlib."""
    if df.empty or df[y].dropna().empty:
        st.info(f"No numeric data available to plot for {title}.")
        return
    fig, ax = plt.subplots()
    df.plot.bar(x=x, y=y, color=color, ax=ax, legend=False)
    ax.set_title(title)
    st.pyplot(fig)


def plot_histogram(df, x, title, color):
    """Plot a histogram using matplotlib."""
    if df.empty or df[x].dropna().empty:
        st.info(f"No numeric data available to plot for {title}.")
        return
    fig, ax = plt.subplots()
    ax.hist(df[x].dropna(), bins=30, color=color)
    ax.set_title(title)
    st.pyplot(fig)


def plot_pie_chart(df, names, values, title, style=None):
    """Plot a pie chart using matplotlib."""
    if df.empty or df[values].dropna().empty:
        st.info(f"No numeric data available to plot for {title}.")
        return
    fig, ax = plt.subplots()
    ax.pie(df[values], labels=df[names], autopct="%1.1f%%")
    ax.set_title(title, fontsize=style.get("title_fontsize", 18) if style else 18)
    st.pyplot(fig)
