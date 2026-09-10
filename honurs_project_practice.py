# import list
import os
import osmnx as ox
import matplotlib.pyplot as plt
import csv
import pandas as pd

# saving images to folder maps
save_folder = "/Users/kesterwebster/Desktop/honours/maps"

# lists
postcode = []
latitude = []
longitude = []
lsoa_code = []
lsoa_name = []

# Read csv file and store data in lists

with open("saved_postcodes.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header row

    for row in reader:

        postcode.append(row[0])
        latitude.append(float(row[1]))
        longitude.append(float(row[2]))
        lsoa_code.append(row[3])
        lsoa_name.append(row[4])

# Create dataframe from lists

df = pd.DataFrame({
    "Postcode": postcode,
    "Latitude": latitude,
    "Longitude": longitude,
    "LSOA Code": lsoa_code,
    "LSOA Name": lsoa_name
})

# Create one point per LSOA by averaging the coordinates of all postcodes in that LSOA

lsoa_points = (
    df.groupby(["LSOA Code", "LSOA Name"])
      .agg({
          "Latitude": "mean",
          "Longitude": "mean"
      })
      .reset_index()
)

# Check for how many LSOAs we have 

print("Total postcodes:", len(df))
print("Total LSOA points:", len(lsoa_points))

print("\nLSOA POINTS:")

for x in range(len(lsoa_points)):
    print(
        lsoa_points.iloc[x]["LSOA Code"],
        "-",
        lsoa_points.iloc[x]["LSOA Name"],
        "-",
        lsoa_points.iloc[x]["Latitude"],
        lsoa_points.iloc[x]["Longitude"]
    )

# Create a map folder if it doesn't exist

os.makedirs(save_folder, exist_ok=True)

# AREA INFORMATION

area_info = {
    "Edinburgh": (55.9533, -3.1883),
}

# Download and plot map

for name, (lat, lon) in area_info.items():

    print(f"\nDownloading {name}")

    G = ox.graph_from_point(
        (lat, lon),
        dist=10000,
        network_type="drive"
    )

    print(name, G)

    # Project lsoa points to the same CRS as the graph

    G = ox.project_graph(G)

    # Create GeoDataFrame from LSOA coordinates
    import geopandas as gpd

    lsoa_gdf = gpd.GeoDataFrame(
        lsoa_points,
        geometry=gpd.points_from_xy(
            lsoa_points["Longitude"],
            lsoa_points["Latitude"]
        ),
        crs="EPSG:4326"
    )

    # Project LSOA points
    lsoa_gdf = lsoa_gdf.to_crs(G.graph["crs"])

    # Plot road network

    fig, ax = ox.plot_graph(
        G,
        figsize=(16, 16),
        node_size=0,
        edge_color="white",
        show=False,
        close=False
    )

    # PLOT LSOA points
   
    lsoa_gdf.plot(
        ax=ax,
        markersize=12
    )

    # Title and save the map
    ax.set_title(
        f"{name} - LSOA Points",
        color="white"
    )
    filepath = f"{save_folder}/{name}_LSOA_points.png"

    plt.savefig(
        filepath,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)

    print(f"Saved {filepath}")