from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Task 4.4: K-Means Clustering

# Preparing data for clustering
# We will use the aggregated experience metrics (TCP, RTT, Throughput) for clustering
clustering_columns = [
    'Average TCP DL Retransmission', 'Average TCP UL Retransmission',
    'Average RTT DL', 'Average RTT UL',
    'Average Throughput DL', 'Average Throughput UL'
]
clustering_data = aggregated_data[clustering_columns].fillna(0)  # Replacing NaN with 0 for clustering

# Scaling the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(clustering_data)

# Performing K-Means clustering with k=3
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(scaled_data)

# Adding the cluster labels to the aggregated data
aggregated_data['Cluster'] = kmeans.labels_

# Viewing the first few rows with cluster labels
aggregated_data.head()

import matplotlib.pyplot as plt
import seaborn as sns

# Calculating average values for each metric in each cluster
cluster_means = aggregated_data.groupby('Cluster').mean()

# Preparing the data for plotting
plot_data = cluster_means.reset_index().melt(id_vars='Cluster', var_name='Metric', value_name='Average Value')

# Filtering out the 'Handset Type' from the metrics as it's not a numerical value
plot_data = plot_data[~plot_data['Metric'].str.contains('Handset Type')]

# Creating bar plots
plt.figure(figsize=(15, 8))
sns.barplot(x='Metric', y='Average Value', hue='Cluster', data=plot_data)
plt.title('Average Experience Metrics per Cluster')
plt.xticks(rotation=45)
plt.ylabel('Average Value')
plt.xlabel('Metric')
plt.legend(title='Cluster')
plt.tight_layout()

plt.show()
