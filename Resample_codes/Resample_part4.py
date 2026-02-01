import xarray as xr
import numpy as np
import pandas as pd
import os
from glob import glob
from tqdm import tqdm

# === Path Settings ===
# Input data folder
input_folder = "/data3/interns/NRT_CO2_Emission_Map_Project/PinyiLu_work/GFAS/"  
# Target grid file (including longitude, latitude, and time grid information)
target_grid_nc = "/data3/interns/NRT_CO2_Emission_Map_Project/PinyiLu_work/GFAS_resample/global_grid_0.1degree_2019_2025.nc"  
# Interpolation result output path
output_nc = "/data3/interns/NRT_CO2_Emission_Map_Project/PinyiLu_work/GFAS_resample/GFAS_resample_final"  

# === Read target grid information ===
target_grid = xr.open_dataset(target_grid_nc)
target_lat = target_grid['lat']
target_lon = target_grid['lon']
target_time = target_grid['time'].values  # Target time series

# === Collecting file paths by year (mapping by year) ===
file_list = sorted(glob(os.path.join(input_folder, "*.nc")))  # Match all nc files
file_dict = {}
for file in file_list:
    filename = os.path.basename(file)
    # Take the first four characters of the file name as the year
    year = filename[:4]  
    file_dict[year] = file  

# === Initialize output array (to store interpolation results) ===
# Construct an empty array with dimensions matching the target grid and fill it with NaN
CO2_all = xr.DataArray(
    np.full((len(target_time), len(target_lat), len(target_lon)), np.nan, dtype=np.float32),
    coords={"time": target_time, "lat": target_lat, "lon": target_lon},
    dims=["time", "lat", "lon"],
    name="CO2_fire"
)

# === Traverse the target time points and interpolate point by point ===
for i, time_point in enumerate(tqdm(target_time, desc="Interpolating CO2")):
    # Parse the year of the current time point (e.g. 2020-01-01 → 2020)
    year = pd.to_datetime(str(time_point)).strftime("%Y")  
    # If there is no corresponding file for the current year, skip it
    if year not in file_dict:
        continue

    # Open the dataset corresponding to the specified year
    ds = xr.open_dataset(file_dict[year])

    # If the time dimension of the dataset is valid_time, rename it to time (for a unified dimension name)
    if "valid_time" in ds.dims:
        ds = ds.rename({"valid_time": "time"})

    # Obtain the timestamp of the input dataset and perform an overall adjustment (shift forward by one day)
    input_time = pd.to_datetime(ds['time'].values)
    input_time_adjusted = input_time - pd.Timedelta(days=1)  # Move the time forward by one day as a whole

    # Update the time dimension of the dataset to the adjusted timestamp
    ds['time'] = ("time", input_time_adjusted.values)

    # Check whether the time point is within the range of the dataset
    if not (ds['time'].min() <= time_point <= ds['time'].max()):
        continue  

    # Extract CO2 data at the current time point (sliced by time)
    co2fire = ds['co2fire'].sel(time=time_point, method='nearest')  
    # If the original data dimension is latitude/longitude, rename it uniformly as lat/lon
    if "latitude" in co2fire.dims and "longitude" in co2fire.dims:
        co2fire = co2fire.rename({"latitude": "lat", "longitude": "lon"})

    # Linear interpolation to the target grid
    interp_day = co2fire.interp(lat=target_lat, lon=target_lon, method="linear")
    # Negative value handling (adjustable according to business logic if necessary)
    interp_day = interp_day.where(interp_day >= 0, 0)  

    # Write the interpolation results into the array
    CO2_all[i, :, :] = interp_day.values  

# === Save the result to a netCDF file ===
out_ds = xr.Dataset({"CO2_fire": CO2_all})
out_ds.to_netcdf(output_nc)
print(f"Interpolation completed! The result has been saved to:{output_nc}")
