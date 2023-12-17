# Bivariate Analysis - Exploring the relationship between application data usage and total data (DL+UL)

# Calculating the total data (DL+UL)
aggregated_data['Total Data'] = aggregated_data['Total UL (Bytes)'] + aggregated_data['Total DL (Bytes)']

# Selecting the application data columns for bivariate analysis
application_data_columns = [
    'Social Media Data', 'Google Data', 'Email Data',
    'Youtube Data', 'Netflix Data', 'Gaming Data', 'Other Data'
]

# Creating scatter plots to explore relationships
fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(15, 20))
axes = axes.flatten()
axes[-1].axis('off')  # Hide the last subplot as we have an odd number of plots

for i, col in enumerate(application_data_columns):
    sns.scatterplot(x=aggregated_data[col], y=aggregated_data['Total Data'], ax=axes[i])
    axes[i].set_title(f'Total Data vs {col}')
    axes[i].set_xlabel(col)
    axes[i].set_ylabel('Total Data (DL+UL)')

plt.tight_layout()
plt.show()
