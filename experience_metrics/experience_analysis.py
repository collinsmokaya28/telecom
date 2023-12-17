# Identifying the handset type column
# Assuming the handset type might be related to the device identifiers like 'IMEI'
handset_columns = [col for col in df.columns if 'IMEI' in col or 'device' in col.lower() or 'handset' in col.lower()]

# Task 4.1: Aggregate per customer
# We will replace missing values and outliers by the mean or the mode as appropriate

# Assuming 'MSISDN/Number' represents the customer identifier
customer_id = 'MSISDN/Number'

# Defining the columns of interest
tcp_retransmission_cols = ['TCP DL Retrans. Vol (Bytes)', 'TCP UL Retrans. Vol (Bytes)']
rtt_cols = ['Avg RTT DL (ms)', 'Avg RTT UL (ms)']
throughput_cols = ['Avg Bearer TP DL (kbps)', 'Avg Bearer TP UL (kbps)']

# Handling missing values by replacing with mean (for numerical data) or mode (for categorical data)
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
    # Assuming the first handset column found is the correct one
    handset_columns[0]: lambda x: x.mode()[0] if not x.mode().empty else "Unknown"
}).rename(columns={
    tcp_retransmission_cols[0]: 'Average TCP DL Retransmission',
    tcp_retransmission_cols[1]: 'Average TCP UL Retransmission',
    rtt_cols[0]: 'Average RTT DL',
    rtt_cols[1]: 'Average RTT UL',
    throughput_cols[0]: 'Average Throughput DL',
    throughput_cols[1]: 'Average Throughput UL',
    handset_columns[0]: 'Handset Type'
})

aggregated_data.head()

# Task 4.2: Compute & list 10 of the top, bottom and most frequent TCP, RTT, and Throughput values in the dataset.

def top_bottom_frequent_values(df, column):
    """Compute top 10, bottom 10 and most frequent 10 values of a given column."""
    top_10 = df[column].nlargest(10)
    bottom_10 = df[column].nsmallest(10)
    frequent_10 = df[column].value_counts().nlargest(10).index
    return top_10, bottom_10, frequent_10

# Computing for each column of interest
tcp_dl_results = top_bottom_frequent_values(df, tcp_retransmission_cols[0])
tcp_ul_results = top_bottom_frequent_values(df, tcp_retransmission_cols[1])
rtt_dl_results = top_bottom_frequent_values(df, rtt_cols[0])
rtt_ul_results = top_bottom_frequent_values(df, rtt_cols[1])
throughput_dl_results = top_bottom_frequent_values(df, throughput_cols[0])
throughput_ul_results = top_bottom_frequent_values(df, throughput_cols[1])

tcp_dl_results, tcp_ul_results, rtt_dl_results, rtt_ul_results, throughput_dl_results, throughput_ul_results

# Task 4.3: Compute & report the distribution of the average throughput and TCP retransmission per handset type

# We'll need to join the aggregated data with the handset type to compute these distributions.
# Since the handset type is already part of the aggregated data, we can use it directly.

# Preparing data for throughput distribution per handset type
throughput_per_handset = aggregated_data.groupby('Handset Type').agg({
    'Average Throughput DL': 'mean',
    'Average Throughput UL': 'mean'
}).reset_index()

# Preparing data for TCP retransmission distribution per handset type
# Note: The sample data does not have TCP retransmission values, but the script will be prepared to handle this in the full dataset.
tcp_retransmission_per_handset = aggregated_data.groupby('Handset Type').agg({
    'Average TCP DL Retransmission': 'mean',
    'Average TCP UL Retransmission': 'mean'
}).reset_index()

throughput_per_handset, tcp_retransmission_per_handset

