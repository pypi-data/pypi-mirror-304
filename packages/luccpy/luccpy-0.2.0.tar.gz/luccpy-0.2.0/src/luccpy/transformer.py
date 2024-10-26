from __future__ import annotations

import os
import xarray as xr
import salem
import pandas as pd
import geopandas as gpd
import rioxarray as rio

__all__ = [
    "read_tif_to_ds",
    "read_wrfout_to_ds",
    "trans_tif_to_shp",
    "save_da_to_tif",
]


def _swap_bounds(min_val, max_val):
    if min_val > max_val:
        min_val, max_val = max_val, min_val
    return min_val, max_val


def _check_geographic_bounds(bounds):
    minx, miny, maxx, maxy = bounds

    minx, maxx = _swap_bounds(minx, maxx)
    miny, maxy = _swap_bounds(miny, maxy)

    is_valid_x_range = -180 <= minx <= maxx <= 180
    is_valid_y_range = -90 <= miny <= maxy <= 90

    return is_valid_x_range and is_valid_y_range

def _determine_input_var(var):
    if not isinstance(var, list):
        var = [var]
    return var


def _read_file_list(path, suffix):

    file_list = [file for file in os.listdir(path) if file.endswith(suffix)]

    assert len(file_list) > 0, f"No files with the suffix '{suffix}' exist in the specified directory."

    return sorted(file_list)


def read_tif_to_ds(raster_path, time_coords, band_name="band_data"):

    raster_files_sorted = _read_file_list(raster_path, ".tif")

    assert len(time_coords) == len(raster_files_sorted), "Length of raster files must match the length of time coords."

    raster_list = [os.path.join(raster_path, raster_file) for raster_file in raster_files_sorted]

    da_list = [rio.open_rasterio(raster) for raster in raster_list]

    combined = xr.concat(da_list, dim="band")

    combined = combined.rename({"band": "time", "y": "lat", "x": "lon"})
    combined["time"] = time_coords
    combined.name = band_name

    out_dataset = combined.to_dataset()

    return out_dataset


def read_wrfout_to_ds(wrfout_file, varlist=None):

    ds = salem.open_wrf_dataset(wrfout_file)
    ds = ds.reset_coords().drop_vars(["lat", "lon", "xtime"]).rename({"south_north": "lat", "west_east": "lon"})

    if varlist is not None:
        varlist = _determine_input_var(varlist)
        return ds[varlist]
    else:
        return ds


def trans_tif_to_shp(raster_file, outshap_file, extract_value=None):

    raster = rio.open_rasterio(raster_file).squeeze()
    raster_crs = raster.rio.crs

    rds = raster.drop("spatial_ref").drop("band")
    rds.name = "data"
    df = rds.to_dataframe().reset_index().dropna()

    if extract_value is not None:
        vaild_df = df[df["data"] == extract_value]
    else:
        vaild_df = df.copy()

    ilon, ilat = vaild_df.x.values, vaild_df.y.values

    ser = pd.Series([f'POINT ({ii} {jj})' for ii, jj in list(zip(ilon, ilat))], name="wkd")
    gs = gpd.GeoSeries.from_wkt(ser)
    gdf = gpd.GeoDataFrame(data=vaild_df, geometry=gs, crs=raster_crs)

    gdf.to_file(outshap_file)

    print(f"Transformation of {raster_file} completed and saved as {outshap_file}!")


def save_da_to_tif(da, ofile, crs="epsg:4326", is_wrfout=False):

    if is_wrfout:
        wrf_crs = '+proj=lcc +lat_0=43.5 +lon_0=126 +lat_1=30 +lat_2=60 +x_0=0 +y_0=0 +datum=WGS84 +units=m ' \
                  '+no_defs=True '
        da_set_crs = da.rio.write_crs(wrf_crs)
    else:
        da_set_crs = da.rio.write_crs(crs)

    da_set_crs.rio.set_spatial_dims(x_dim="lon", y_dim="lat", inplace=True)
    da_set_crs.rio.to_raster(ofile)
    print(f"save {ofile} done!")
