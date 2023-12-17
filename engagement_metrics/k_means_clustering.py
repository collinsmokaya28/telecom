# Re-running K-means clustering with k=3 on the normalized engagement metrics
kmeans = KMeans(n_clusters=3, random_state=0).fit(normalized_data)
aggregated_data['Cluster'] = kmeans.labels_

# Analyzing the clusters formed by computing metrics for each cluster
cluster_analysis = aggregated_data.groupby('Cluster').agg({
    'Dur. (ms)': ['min', 'max', 'mean', 'sum'],
    'Total UL (Bytes)': ['min', 'max', 'mean', 'sum'],
    'Total DL (Bytes)': ['min', 'max', 'mean', 'sum'],
    'Total Data': ['min', 'max', 'mean', 'sum']
})

cluster_analysis

# Preparing data for the bar plot to visually display clusters

# Aggregating data for the plot
plot_data = clustered_data_display.groupby('Cluster').mean()

# Creating the bar plot
plot_data.plot(kind='bar', figsize=(15, 7), rot=0)
plt.title('Average Engagement Metrics per Cluster')
plt.xlabel('Cluster')
plt.ylabel('Average Value')
plt.legend(title='Metrics', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

