class GPXProcessor:
    def __init__(self, gpx_file):
        self.gpx_file = gpx_file
        self.data = None

    def load_gpx(self):
        import gpxpy
        with open(self.gpx_file, 'r') as file:
            self.data = gpxpy.parse(file)

    def extract_route(self):
        """
        Returns latitudes and longitudes for the route.
        """
        if self.data is None:
            raise ValueError("GPX data not loaded. Please call load_gpx() first.")

        latitudes = []
        longitudes = []
        for track in self.data.tracks:
            for segment in track.segments:
                for point in segment.points:
                    latitudes.append(point.latitude)
                    longitudes.append(point.longitude)

        return {
            'latitudes': latitudes,
            'longitudes': longitudes
        }