# Prepare Data for GWR

import pandas as pd
import numpy as np
from mgwr.gwr import GWR
from mgwr.sel_bw import Sel_BW
import geopandas as gpd
from libpysal.weights import KNN
import matplotlib.pyplot as plt

# Load dataset
file_path = "output.csv"
df = pd.read_csv(file_path)


# Ensure observed_date is in datetime format
df["observed_date"] = pd.to_datetime(df["observed_date"])

# Select a category to analyze (e.g., Amphibia)
selected_category = "Amphibia"
df_filtered = df[df["category"] == selected_category].copy()

# Define dependent variable (e.g., species observation count)
df_filtered["species_count"] = df_filtered.groupby(["latitude", "longitude"])["scientific_name"].transform("count")
y = df_filtered["species_count"].values.reshape(-1, 1)  # Dependent variable

# Define independent variables (weather conditions)
X = df_filtered[["temperature_2m_mean", "precipitation_sum", "wind_speed_10m_max"]].values

# Define spatial coordinates (Latitude & Longitude)
coords = df_filtered[["longitude", "latitude"]].values






# 3️⃣ Select the Optimal Bandwidth (Kernel Size)
# The bandwidth determines how many nearby points are included for each local regression.


# Automatically find best bandwidth
bw = Sel_BW(coords, y, X, kernel="bisquare").search()
print(f"Optimal Bandwidth: {bw}")







# 4️⃣ Fit the GWR Model


# Run GWR with the selected bandwidth
gwr_model = GWR(coords, y, X, bw, kernel="bisquare")
gwr_results = gwr_model.fit()

# Print summary
print(gwr_results.summary())








# How to Visualize GWR Results
# Map the Temperature Coefficients



# Convert results into a DataFrame
df_filtered["temp_coeff"] = gwr_results.params[:, 0]  # Coefficients for temperature

# Convert to GeoDataFrame
gdf = gpd.GeoDataFrame(df_filtered, geometry=gpd.points_from_xy(df_filtered.longitude, df_filtered.latitude))

# Plot the results as a heatmap
fig, ax = plt.subplots(figsize=(10, 6))
gdf.plot(column="temp_coeff", cmap="coolwarm", legend=True, ax=ax)
plt.title("GWR Coefficients for Temperature Effect on Wildlife")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()