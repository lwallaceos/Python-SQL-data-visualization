import matplotlib.pyplot as plt
import pandas as pd


def plot_bar(data, x_label, y_label, title):
    df = pd.DataFrame(data, columns=[x_label, y_label])
    fig, ax = plt.subplots()
    ax.bar(df[x_label], df[y_label], color="skyblue")
    ax.set_title(title)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    return fig
