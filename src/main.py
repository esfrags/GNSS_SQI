import argparse
import os
from gpx_processing import GPXProcessor
from map_generator import MapGenerator
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

    for gpx_file in gpx_files:
        if not validate_gpx_file(gpx_file):
            log_message(f"Invalid GPX file: {gpx_file}")
            continue
        
        log_message(f"Processing file: {gpx_file}")
        processor = GPXProcessor(gpx_file)
        processor.load_gpx()
        route_analysis = processor.extract_route()
        all_route_analysis.append(route_analysis)

    map_gen = MapGenerator(all_route_analysis)
    map_gen.plot_routes_on_satellite()

if __name__ == '__main__':
    main()