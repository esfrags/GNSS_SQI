# GNSS_SQI Project

## Overview
GNSS Signal Quality Inference is a Python project designed to determine conflictive RF zones in urban environments. 
The application processes GPX files of running strava activities and generates heatmaps visualizing the quality of GNSS signals along those routes.
The aim of the project is to detect GNSS interferences purely from post-activity data, analyzing gpx tracks in search of speed outliers, abrupt elevation changes, and positional inconsistencies. 

In the long run, this data will be correlated with external factors such as 5G tower locations, urban canyons, and multipath-prone areas to infer patterns of GNSS degradation in the city.

This project is useful for runners, cyclists, and researchers who want to better understand GNSS behavior in dense urban areas, using only consumer-grade GNSS devices.

## Features
- Load and parse GPX files to extract GNSS signal quality data.
- Analyze routes to identify areas of signal interference.
- Generate heatmaps to visualize GNSS signal quality.

## Workflow
- Processing
- Calculations
- Analysis
- Representation

## Relevant Studies
- Airbus: https://safetyfirst.airbus.com/gnss-interference/
- Garmin: https://ieeexplore.ieee.org/document/10444238
- Polar: https://support.polar.com/en/what-is-gnss
- Septentrio: https://www.ion.org/gnss/upload/files/2157_Septentrio_GNSS_Interference_A5_LR.pdf
- Sportwatch study: https://www.sciencedirect.com/science/article/pii/S0263224124003117

## Installation
To set up the project, clone the repository and install the required dependencies. You can do this using pip:

```bash
git clone <repository-url>
cd GNSS_SQI
pip install -r requirements.txt
```

## Usage
To run the application, use the following command:

```bash
python src/main.py <path_to_gpx_file1> <path_to_gpx_file2> ...
```

Replace `<path_to_gpx_file>` with the path(s) to your GPX files.

## Future Work
- Adding more sophisticated checks (e.g., signal loss, duplicate points, missing data).
- Implementing abrupt elevation change and positional inconsitency detection
- Returning indices to cross-reference with your heatmap.


## Contributing
Contributions are welcome! If you have suggestions for improvements or find bugs, please open an issue or submit a pull request.

## License
This project is licensed under the MISKO License. See the LICENSE file for more details.