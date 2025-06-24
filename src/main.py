import argparse
import os
from gpx_processing import GPXProcessor
from map_generator import MapGenerator
from route_analyzer import RouteDataAnalyzer
from utils import validate_gpx_file, log_message

def main():
    parser = argparse.ArgumentParser(description='Plot GPX routes on a satellite map.')
    parser.add_argument('gpx_folder', help='Folder containing GPX files to process')
    args = parser.parse_args()

    gpx_files = [
        os.path.join(args.gpx_folder, f)
        for f in os.listdir(args.gpx_folder)
        if f.lower().endswith('.gpx')
    ]

    if not gpx_files:
        log_message(f"No GPX files found in folder: {args.gpx_folder}")
        return

    all_route_analysis = []
    all_speeds = []

    for gpx_file in gpx_files:
        if not validate_gpx_file(gpx_file):
            log_message(f"Invalid GPX file: {gpx_file}")
            continue
        
        log_message(f"Processing file: {gpx_file}")
        processor = GPXProcessor(gpx_file)
        processor.load_gpx()
        route_analysis = processor.extract_route()
        speeds = processor.extract_speeds()
        all_route_analysis.append(route_analysis)
        all_speeds.append(speeds)

    # Detect outliers
    analyzer = RouteDataAnalyzer(all_speeds, speed_threshold=8.0)
    outlier_indices = analyzer.get_outlier_indices()

    # Log outlier locations and speeds
    for route_idx, (route, speeds, outliers) in enumerate(zip(all_route_analysis, all_speeds, outlier_indices)):
        lats = route.get('latitudes', [])
        lons = route.get('longitudes', [])
        for idx in outliers:
            if idx < len(lats) and idx < len(lons) and idx < len(speeds):
                msg = (f"Outlier detected in route {route_idx}: "
                       f"lat={lats[idx]:.6f}, lon={lons[idx]:.6f}, speed={speeds[idx]:.2f} m/s")
                log_message(msg)

    map_gen = MapGenerator(all_route_analysis, all_speeds)
    map_gen.plot_routes_by_speed(outlier_indices=outlier_indices)

if __name__ == '__main__':
    main()