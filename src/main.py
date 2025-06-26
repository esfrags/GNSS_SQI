import argparse
import os
from gpx_processing import GPXProcessor
from map_generator import MapGenerator
from route_analyzer import RouteDataAnalyzer
from utils import validate_gpx_file, log_message

speed_threshold = 8.0  # m/s, ~28.8 km/h
elevation_threshold = 5.0  # m, threshold for abrupt elevation changes

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
    all_altitudes = []

    for gpx_file in gpx_files:
        if not validate_gpx_file(gpx_file):
            log_message(f"Invalid GPX file: {gpx_file}")
            continue
        
        log_message(f"Processing file: {gpx_file}")
        processor = GPXProcessor(gpx_file)
        processor.load_gpx()
        
        route_analysis = processor.extract_route()
        speeds = processor.extract_speeds()
        altitudes = processor.extract_altitudes()
        
        all_route_analysis.append(route_analysis)
        all_speeds.append(speeds)
        all_altitudes.append(altitudes)

    # Detect outliers
    analyzer = RouteDataAnalyzer(all_speeds, all_altitudes, speed_threshold, elevation_threshold)
    speed_outliers = analyzer.detect_speed_outliers()
    altitude_outliers = analyzer.detect_altitude_outliers()

    # Log speed outlier locations and speeds
    for route_idx, (route, speeds, outliers) in enumerate(zip(all_route_analysis, all_speeds, speed_outliers)):
        lats = route.get('latitudes', [])
        lons = route.get('longitudes', [])
        for idx in outliers:
            if idx < len(lats) and idx < len(lons) and idx < len(speeds):
                msg = (f"Speed outlier in route {route_idx}: "
                       f"lat={lats[idx]:.6f}, lon={lons[idx]:.6f}, speed={speeds[idx]:.2f} m/s")
                log_message(msg)

    # Log altitude outlier locations and altitudes
    for route_idx, (route, altitudes, outliers) in enumerate(zip(all_route_analysis, all_altitudes, altitude_outliers)):
        lats = route.get('latitudes', [])
        lons = route.get('longitudes', [])
        for idx in outliers:
            if idx < len(lats) and idx < len(lons) and idx < len(altitudes):
                msg = (f"Altitude outlier in route {route_idx}: "
                       f"lat={lats[idx]:.6f}, lon={lons[idx]:.6f}, altitude={altitudes[idx]:.2f} m")
                log_message(msg)
                
    analyzer.summary()
    
    map_gen = MapGenerator(all_route_analysis, all_speeds)
    map_gen.plot_routes_by_speed(outlier_indices=speed_outliers)

if __name__ == '__main__':
    main()