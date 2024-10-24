import xarray as xr   #pip install xarray
import numpy as np
def convert_longitude(nc_input_path, nc_output_path):
    ds = xr.open_dataset(nc_input_path)
    if 'lon' not in ds.coords:
        raise ValueError("输入文件中没有'lon'坐标")
    ds['lon'] = xr.where(ds['lon'] > 180, ds['lon'] - 360, ds['lon'])
    ds = ds.sortby('lon')
    ds = ds.sortby('lat', ascending=False)
    ds.to_netcdf(nc_output_path)
    print(f"成功将数据转换并保存到 {nc_output_path}")
convert_longitude('CMORPH2_0.25deg-30min_202410160100.RT.nc', 'output_rain_data1.nc')
