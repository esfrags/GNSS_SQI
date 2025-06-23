# GPS_SQI Project

## Overview
GPS_SQI is a Python project designed to analyze GPS signal interferences during a run. The application processes one or more GPX files that represent similar routes and generates a heatmap visualizing the quality of GPS signals along those routes.

## Features
- Load and parse GPX files to extract GPS signal quality data.
- Analyze routes to identify areas of signal interference.
- Generate heatmaps to visualize GPS signal quality.

## Installation
To set up the project, clone the repository and install the required dependencies. You can do this using pip:

```bash
git clone <repository-url>
cd GPS_SQI
pip install -r requirements.txt
```

## Usage
To run the application, use the following command:

```bash
python src/main.py <path_to_gpx_file1> <path_to_gpx_file2> ...
```

Replace `<path_to_gpx_file>` with the path(s) to your GPX files.

## 🔭 Future Work
- Adding more sophisticated checks (e.g., signal loss, duplicate points, missing data).
- Allowing thresholds to be set per activity or user.
- Returning indices to cross-reference with your heatmap.


## Contributing
Contributions are welcome! If you have suggestions for improvements or find bugs, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.