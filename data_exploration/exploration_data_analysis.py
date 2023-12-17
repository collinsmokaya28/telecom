# Task 2.1: Aggregate User Behaviour Data

# Identifying the relevant columns for aggregation
relevant_columns = [
    'MSISDN/Number', 'Dur. (ms)', 'Total UL (Bytes)', 'Total DL (Bytes)',
    'Social Media DL (Bytes)', 'Social Media UL (Bytes)',
    'Google DL (Bytes)', 'Google UL (Bytes)',
    'Email DL (Bytes)', 'Email UL (Bytes)',
    'Youtube DL (Bytes)', 'Youtube UL (Bytes)',
    'Netflix DL (Bytes)', 'Netflix UL (Bytes)',
    'Gaming DL (Bytes)', 'Gaming UL (Bytes)',
    'Other DL (Bytes)', 'Other UL (Bytes)'
]

# Selecting the relevant columns from the dataframe
user_data = df[relevant_columns]

# Aggregating data for each user
# Calculate the total data volume for each application
user_data['Social Media Data'] = user_data['Social Media DL (Bytes)'] + user_data['Social Media UL (Bytes)']
user_data['Google Data'] = user_data['Google DL (Bytes)'] + user_data['Google UL (Bytes)']
user_data['Email Data'] = user_data['Email DL (Bytes)'] + user_data['Email UL (Bytes)']
user_data['Youtube Data'] = user_data['Youtube DL (Bytes)'] + user_data['Youtube UL (Bytes)']
user_data['Netflix Data'] = user_data['Netflix DL (Bytes)'] + user_data['Netflix UL (Bytes)']
user_data['Gaming Data'] = user_data['Gaming DL (Bytes)'] + user_data['Gaming UL (Bytes)']
user_data['Other Data'] = user_data['Other DL (Bytes)'] + user_data['Other UL (Bytes)']

# Aggregate per user
aggregated_data = user_data.groupby('MSISDN/Number').agg({
    'Dur. (ms)': 'sum',
    'Total UL (Bytes)': 'sum',
    'Total DL (Bytes)': 'sum',
    'Social Media Data': 'sum',
    'Google Data': 'sum',
    'Email Data': 'sum',
    'Youtube Data': 'sum',
    'Netflix Data': 'sum',
    'Gaming Data': 'sum',
    'Other Data': 'sum'
}).reset_index()

# Counting the number of xDR sessions per user
aggregated_data['Number of xDR Sessions'] = df.groupby('MSISDN/Number')['Bearer Id'].count().reset_index(drop=True)

# Displaying the first few rows of the aggregated data
aggregated_data.head()

# Task 2.2: Exploratory Data Analysis

# Step 1: Describe Variables & Data Types
variables_description = aggregated_data.dtypes.reset_index()
variables_description.columns = ['Variable', 'DataType']

# Step 2: Basic Metrics Analysis
basic_metrics = aggregated_data.describe()

variables_description, basic_metrics

# Step 3: Non-Graphical Univariate Analysis - Computing dispersion parameters

# Handling missing values by replacing them with the mean of the corresponding column
aggregated_data.fillna(aggregated_data.mean(), inplace=True)

# Computing dispersion parameters: variance, standard deviation, range
dispersion_parameters = aggregated_data.var().reset_index()
dispersion_parameters.columns = ['Variable', 'Variance']
dispersion_parameters['Standard Deviation'] = aggregated_data.std()
dispersion_parameters['Range'] = aggregated_data.max() - aggregated_data.min()

# Handling outliers by replacing them with the mean of the corresponding column
for col in aggregated_data.select_dtypes(include=['float64']):
    mean = aggregated_data[col].mean()
    std = aggregated_data[col].std()
    upper_limit = mean + 3 * std
    lower_limit = mean - 3 * std
    aggregated_data[col] = aggregated_data[col].apply(lambda x: mean if x < lower_limit or x > upper_limit else x)

dispersion_parameters

