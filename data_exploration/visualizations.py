import matplotlib.pyplot as plt
import seaborn as sns

def plot_univariate_distributions(df, variables, nrows=5, ncols=2, fig_width=15, fig_height=20):
    """
    Plot histograms for a list of variables in a DataFrame.

    Args:
    df (DataFrame): The DataFrame containing the data.
    variables (list): List of column names in the DataFrame to plot.
    nrows (int): Number of rows in the subplot grid.
    ncols (int): Number of columns in the subplot grid.
    fig_width (int): Width of the entire subplot grid.
    fig_height (int): Height of the entire subplot grid.
    """
    # Check if the number of subplots is enough to display all variables
    if nrows * ncols < len(variables):
        raise ValueError("Number of rows and columns in subplot grid is not enough to display all variables")

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(fig_width, fig_height))
    axes = axes.flatten()

    for i, col in enumerate(variables):
        if col in df.columns:
            sns.histplot(df[col], ax=axes[i], kde=True)
            axes[i].set_title(col)
            axes[i].set_xlabel('')
            axes[i].set_ylabel('Frequency')
        else:
            axes[i].set_visible(False)  # Hide axes if there are no more variables to plot

    plt.tight_layout()
    plt.show()

