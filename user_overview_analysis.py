import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

top_handsets = df['Handset Type'].value_counts().head(10)

top_manufacturers = df['Handset Manufacturer'].value_counts().head(3)

top_handsets_per_manufacturer = df.groupby('Handset Manufacturer')['Handset Type'].value_counts().loc[top_manufacturers.index].groupby(level=0).head(5)
