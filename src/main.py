import argparse
import os
from gpx_processing import GPXProcessor
from heatmap import create_heatmap
from utils import validate_gpx_file, log_message

def main():
    parser = argparse.ArgumentParser(description='Analyze GPS signal interferences and generate a heatmap.')
    parser.add_argument('gpx_files', nargs='+', help='One or more GPX files to process')
    args = parser.parse_args()

    for gpx_file in args.gpx_files:
        if not validate_gpx_file(gpx_file):
            log_message(f"Invalid GPX file: {gpx_file}")
            continue
        
        log_message(f"Processing file: {gpx_file}")
        processor = GPXProcessor(gpx_file)
        signal_quality_data = processor.extract_signal_quality()
        route_analysis = processor.analyze_route()

        create_heatmap(signal_quality_data, route_analysis)

if __name__ == '__main__':
    main()