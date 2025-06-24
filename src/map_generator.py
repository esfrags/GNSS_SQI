import matplotlib.pyplot as plt
import contextily as ctx
import geopandas as gpd
from shapely.geometry import LineString

class MapGenerator:
    def __init__(self, all_route_analysis):
        self.all_route_analysis = all_route_analysis

    def plot_routes_on_satellite(self, zoom=16):
        lines = []
        for route in self.all_route_analysis:
            lats = route.get('latitudes', [])
            lons = route.get('longitudes', [])
            if lats and lons and len(lats) > 1:
                coords = list(zip(lons, lats))
                lines.append(LineString(coords))

        if not lines:
            print("No route data to plot.")
            return

        gdf = gpd.GeoDataFrame(geometry=lines, crs='EPSG:4326').to_crs(epsg=3857)
        fig, ax = plt.subplots(figsize=(10, 10))
        gdf.plot(ax=ax, color='blue', linewidth=2)
        ctx.add_basemap(ax, source=ctx.providers.Esri.WorldImagery, crs='EPSG:3857', zoom=zoom)
        ax.set_axis_off()
        ax.set_title('GPX Routes on Satellite Image')
        plt.show()