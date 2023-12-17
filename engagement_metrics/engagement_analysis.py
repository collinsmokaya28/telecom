from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import numpy as np

# Step 1: Aggregate Metrics per Customer ID and Report Top 10 Customers per Engagement Metric
# Engagement metrics: Dur. (ms), Total UL (Bytes), Total DL (Bytes), Total Data

# Sorting by each engagement metric and getting top 10 customers
top_10_duration = aggregated_data.nlargest(10, 'Dur. (ms)')[['MSISDN/Number', 'Dur. (ms)']]
top_10_total_ul = aggregated_data.nlargest(10, 'Total UL (Bytes)')[['MSISDN/Number', 'Total UL (Bytes)']]
top_10_total_dl = aggregated_data.nlargest(10, 'Total DL (Bytes)')[['MSISDN/Number', 'Total DL (Bytes)']]
top_10_total_data = aggregated_data.nlargest(10, 'Total Data')[['MSISDN/Number', 'Total Data']]

# Step 2: Normalization and K-Means Clustering (k=3)
# Selecting the engagement metrics for normalization
engagement_metrics = aggregated_data[['Dur. (ms)', 'Total UL (Bytes)', 'Total DL (Bytes)', 'Total Data']]

# Normalizing the data
scaler = StandardScaler()
normalized_data = scaler.fit_transform(engagement_metrics)

# Running K-means clustering
kmeans = KMeans(n_clusters=3, random_state=0).fit(normalized_data)
aggregated_data['Cluster'] = kmeans.labels_

# Step 3: Cluster Analysis - Compute Metrics for Each Cluster
cluster_analysis = aggregated_data.groupby('Cluster').agg({
    'Dur. (ms)': ['min', 'max', 'mean', 'sum'],
    'Total UL (Bytes)': ['min', 'max', 'mean', 'sum'],
    'Total DL (Bytes)': ['min', 'max', 'mean', 'sum'],
    'Total Data': ['min', 'max', 'mean', 'sum']
})

# Displaying the top 10 customers per engagement metric and the cluster analysis
top_10_duration, top_10_total_ul, top_10_total_dl, top_10_total_data, cluster_analysis

# Aggregating user total traffic per application and deriving the top 10 most engaged users per application

# Selecting the application data columns
application_columns = [
    'Social Media Data', 'Google Data', 'Email Data', 
    'Youtube Data', 'Netflix Data', 'Gaming Data', 'Other Data'
]

# Aggregating total traffic per application and finding top 10 most engaged users
top_users_per_app = {}
for app in application_columns:
    top_users = aggregated_data.nlargest(10, app)[['MSISDN/Number', app]]
    top_users_per_app[app] = top_users

# Displaying the top 10 most engaged users for each application
top_users_per_app['Social Media Data'], top_users_per_app['Google Data'], top_users_per_app['Email Data']  # Displaying a few for brevity

# Calculating total traffic per application across all users
total_traffic_per_app = aggregated_data[application_columns].sum().sort_values(ascending=False)

# Selecting the top 3 most used applications
top_3_apps = total_traffic_per_app.head(3)

# Plotting the top 3 most used applications
plt.figure(figsize=(10, 6))
sns.barplot(x=top_3_apps.index, y=top_3_apps.values)
plt.title('Top 3 Most Used Applications')
plt.ylabel('Total Data Usage (Bytes)')
plt.xlabel('Application')
plt.show()


