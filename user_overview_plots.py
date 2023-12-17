from data_exploration.visualizations import plot_univariate_distributions

# List of variables to plot
graphical_variables = [
    'Dur. (ms)', 'Total UL (Bytes)', 'Total DL (Bytes)',
    'Social Media Data', 'Google Data', 'Email Data',
    'Youtube Data', 'Netflix Data', 'Gaming Data', 'Other Data'
]

# Assuming 'df' is your DataFrame
plot_univariate_distributions(df=df, variables=graphical_variables)


