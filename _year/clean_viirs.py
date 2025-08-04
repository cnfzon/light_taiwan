import geopandas as gpd
import pandas as pd
import rasterio
import rasterio.mask
import numpy as np
from shapely.geometry import mapping

counties = gpd.read_file("taiwan_counties_clean.geojson")

years = range(2013, 2020)

for year in years:
    tif_path = f"DVNL_{year}.tif"
    features = []

    with rasterio.open(tif_path) as src:
        for _, row in counties.iterrows():
            geom = [row["geometry"]]
            out_image, _ = rasterio.mask.mask(src, geom, crop=True)
            data = out_image[0]
            valid = data[data > 0]

            avg = float(np.mean(valid)) if valid.size else 0.0
            mx = float(np.max(valid)) if valid.size else 0.0

            features.append({
                "geometry": row["geometry"],  # 保留 geometry 物件
                "county": row["COUNTYNAME"],
                "avg_light": round(avg, 2),
                "max_light": round(mx, 2),
                "pixel_count": int(valid.size)
            })

    gdf = gpd.GeoDataFrame(features, geometry="geometry", crs=src.crs)
    gdf.to_file(f"taiwan_light_{year}.geojson", driver="GeoJSON", encoding="utf-8")
