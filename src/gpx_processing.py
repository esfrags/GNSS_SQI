from datetime import datetime

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

    def extract_speeds(self):
        """
        Returns a list of speeds (in m/s) for each segment between points in the route.
        The first point will have speed 0.
        """
        if self.data is None:
            raise ValueError("GPX data not loaded. Please call load_gpx() first.")

        latitudes = []
        longitudes = []
        times = []
        for track in self.data.tracks:
            for segment in track.segments:
                for point in segment.points:
                    latitudes.append(point.latitude)
                    longitudes.append(point.longitude)
                    times.append(point.time)

        speeds = [0.0]
        from math import radians, sin, cos, sqrt, atan2
        for i in range(1, len(latitudes)):
            # Haversine distance
            lat1, lon1 = radians(latitudes[i-1]), radians(longitudes[i-1])
            lat2, lon2 = radians(latitudes[i]), radians(longitudes[i])
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            R = 6371000  # meters
            distance = R * c

            # Time difference in seconds
            t1, t2 = times[i-1], times[i]
            if t1 is not None and t2 is not None:
                dt = (t2 - t1).total_seconds()
                speed = distance / dt if dt > 0 else 0.0
            else:
                speed = 0.0
            speeds.append(speed)

        return speeds

    def extract_altitudes(self):
        """
        Returns a list of altitudes (elevations in meters) for each point in the route.
        """
        if self.data is None:
            raise ValueError("GPX data not loaded. Please call load_gpx() first.")

        altitudes = []
        for track in self.data.tracks:
            for segment in track.segments:
                for point in segment.points:
                    # Some GPX points may not have elevation; use 0.0 or np.nan if missing
                    altitudes.append(point.elevation if point.elevation is not None else 0.0)
        return altitudes