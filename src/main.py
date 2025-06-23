import argparse
import os
from gpx_processing import GPXProcessor
from heatmap import route_signal_strength
from utils import validate_gpx_file, log_message

def main():
    parser = argparse.ArgumentParser(description='Analyze GPS signal interferences and generate a heatmap.')
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

    all_signal_quality_data = []
    all_route_analysis = []

    for gpx_file in gpx_files:
        if not validate_gpx_file(gpx_file):
            log_message(f"Invalid GPX file: {gpx_file}")
            continue
        
        log_message(f"Processing file: {gpx_file}")
        processor = GPXProcessor(gpx_file)
        processor.load_gpx()
        signal_quality_data = processor.extract_signal_quality()
        route_analysis = processor.analyze_route()
        
        all_signal_quality_data.append(signal_quality_data)
        all_route_analysis.append(route_analysis)

    route_signal_strength(all_signal_quality_data, all_route_analysis)

if __name__ == '__main__':
    main()