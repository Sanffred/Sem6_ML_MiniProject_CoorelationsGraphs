# we used here folium library to create a heatmap of the data points based on the selected weather attribute and category.
# This code assumes you have a CSV file with columns: 'latitude', 'longitude', 'observed_date', 'category', and weather attributes.



import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

import folium
from folium.plugins import HeatMap

file_path = "output.csv"

df = pd.read_csv(file_path)


# Load your dataset (Ensure 'observed_date' is datetime)
df["observed_date"] = pd.to_datetime(df["observed_date"])

# Manually select category and weather attribute
selected_category = "Amphibia"  # Change category as needed
selected_weather_attr = "temperature_2m_mean"  # Choose a weather column

# Filter the dataset for the selected category
df_filtered = df[df["category"] == selected_category].copy()

# Drop rows with missing values in required columns
# df_filtered = df_filtered.dropna(subset=["latitude", "longitude", selected_weather_attr])

# Initialize Folium Map (centered around median lat/lon)
m = folium.Map(location=[df_filtered["latitude"].median(), df_filtered["longitude"].median()], zoom_start=5)

# Create HeatMap layer
heat_data = df_filtered[["latitude", "longitude", selected_weather_attr]].values.tolist()
HeatMap(heat_data, radius=10, blur=15, max_zoom=1).add_to(m)

# Save and display
m.save("heatmap.html")
print("Heatmap saved as heatmap.html. Open it in a browser.")
