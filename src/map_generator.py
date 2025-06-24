import matplotlib.pyplot as plt
import contextily as ctx
import geopandas as gpd
from shapely.geometry import LineString, Point
from matplotlib.collections import LineCollection
import numpy as np

class MapGenerator:
    def __init__(self, all_route_analysis, all_speeds=None):
        self.all_route_analysis = all_route_analysis
        self.all_speeds = all_speeds

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

    def plot_routes_by_speed(self, zoom=16, cmap='plasma', outlier_indices=None):
        """
        Plots the GPX routes as color-coded lines based on speed on top of a satellite image.
        """
        segments = []
        speeds = []
        outlier_x = []
        outlier_y = []

        for idx, (route, speed_list) in enumerate(zip(self.all_route_analysis, self.all_speeds)):
            lats = route.get('latitudes', [])
            lons = route.get('longitudes', [])
            if len(lats) < 2 or len(lons) < 2 or len(speed_list) < 2:
                continue
            n = min(len(lats), len(lons), len(speed_list))
            gdf = gpd.GeoDataFrame(
                geometry=[Point(lon, lat) for lon, lat in zip(lons[:n], lats[:n])],
                crs='EPSG:4326'
            ).to_crs(epsg=3857)
            xs = gdf.geometry.x.values
            ys = gdf.geometry.y.values
            for i in range(n - 1):
                segments.append([(xs[i], ys[i]), (xs[i+1], ys[i+1])])
                speeds.append((speed_list[i] + speed_list[i+1]) / 2)
            # Collect outlier points
            if outlier_indices is not None:
                for oi in outlier_indices[idx]:
                    if oi < len(xs):
                        outlier_x.append(xs[oi])
                        outlier_y.append(ys[oi])

        if not segments:
            print("No route data to plot.")
            return

        fig, ax = plt.subplots(figsize=(10, 10))
        lc = LineCollection(segments, cmap=cmap, linewidths=3, array=np.array(speeds), zorder=2)
        ax.add_collection(lc)
        ax.relim()
        ax.autoscale_view()

        xmin = min([min(seg[0][0], seg[1][0]) for seg in segments])
        xmax = max([max(seg[0][0], seg[1][0]) for seg in segments])
        ymin = min([min(seg[0][1], seg[1][1]) for seg in segments])
        ymax = max([max(seg[0][1], seg[1][1]) for seg in segments])
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)

        ctx.add_basemap(ax, source=ctx.providers.Esri.WorldImagery, crs='EPSG:3857', zoom=zoom)
        # Plot outliers as red dots
        if outlier_x and outlier_y:
            ax.scatter(outlier_x, outlier_y, color='red', s=30, label='Speed Outlier', zorder=3)
            ax.legend()
        ax.set_axis_off()
        fig.colorbar(lc, ax=ax, label='Speed (m/s)')
        ax.set_title('Color-Coded Speed on Satellite Image (Outliers in Red)')
        plt.show()