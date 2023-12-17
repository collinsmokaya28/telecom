import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load the dataset
file_path = 'path_to_your_dataset.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)

# Task 4.1: Aggregate per customer
# Assuming 'MSISDN/Number' represents the customer identifier
customer_id = 'MSISDN/Number'
# Define columns of interest (replace with actual column names from your dataset)
tcp_retransmission_cols = ['TCP_DL_Retransmission', 'TCP_UL_Retransmission']
rtt_cols = ['RTT_DL', 'RTT_UL']
throughput_cols = ['Throughput_DL', 'Throughput_UL']
handset_type_col = 'Handset_Type'  # Replace with the actual handset type column

# Handling missing values
for col in tcp_retransmission_cols + rtt_cols + throughput_cols:
    df[col].fillna(df[col].mean(), inplace=True)

# Aggregate the data per customer
aggregated_data = df.groupby(customer_id).agg({
    tcp_retransmission_cols[0]: 'mean',
    tcp_retransmission_cols[1]: 'mean',
    rtt_cols[0]: 'mean',
    rtt_cols[1]: 'mean',
    throughput_cols[0]: 'mean',
    throughput_cols[1]: 'mean',
    handset_type_col: lambda x: x.mode()[0] if not x.mode().empty else "Unknown"
})

# Task 4.3: Distribution of throughput and TCP retransmission per handset type
# Throughput distribution per handset type
throughput_per_handset = aggregated_data.groupby(handset_type_col).agg({
    'Average Throughput DL': 'mean',
    'Average Throughput UL': 'mean'
}).reset_index()

# TCP retransmission distribution per handset type
tcp_retransmission_per_handset = aggregated_data.groupby(handset_type_col).agg({
    'Average TCP DL Retransmission': 'mean',
    'Average TCP UL Retransmission': 'mean'
}).reset_index()

# Visualizations for distribution of throughput and TCP retransmission per handset type
# (Add your code for visualization here)

# Task 4.4: K-Means Clustering and Visualization
# Preparing data for clustering
clustering_columns = [
    'Average TCP DL Retransmission', 'Average TCP UL Retransmission',
    'Average RTT DL', 'Average RTT UL',
    'Average Throughput DL', 'Average Throughput UL'
]
clustering_data = aggregated_data[clustering_columns].fillna(0)

# Scaling the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(clustering_data)

# Performing K-Means clustering with k=3
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(scaled_data)
aggregated_data['Cluster'] = kmeans.labels_

# Bar plots to visually display clustering results
cluster_means = aggregated_data.groupby('Cluster').mean()
plot_data = cluster_means.reset_index().melt(id_vars='Cluster', var_name='Metric', value_name='Average Value')
plot_data = plot_data[~plot_data['Metric'].str.contains('Handset Type')]
plt.figure(figsize=(15, 8))
sns.barplot(x='Metric', y='Average Value', hue='Cluster', data=plot_data)
plt.title('Average Experience Metrics per Cluster')
plt.xticks(rotation=45)
plt.ylabel('Average Value')
plt.xlabel('Metric')
plt.legend(title='Cluster')
plt.tight_layout()
plt.show()
