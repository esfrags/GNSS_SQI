class GPXProcessor:
    def __init__(self, gpx_file):
        self.gpx_file = gpx_file
        self.data = None

    def load_gpx(self):
        import gpxpy
        with open(self.gpx_file, 'r') as file:
            self.data = gpxpy.parse(file)

    def extract_signal_quality(self):
        """
        Extracts a proxy for signal quality at each point.
        For now, uses horizontal speed jumps and elevation jumps as a proxy for GPS noise.
        Returns a list of 'signal quality' values (lower is better).
        """
        if self.data is None:
            raise ValueError("GPX data not loaded. Please call load_gpx() first.")

        signal_quality = []
        prev_point = None
        import math

        for track in self.data.tracks:
            for segment in track.segments:
                for point in segment.points:
                    if prev_point is not None:
                        # Calculate distance (meters) and time difference (seconds)
                        dist = point.distance_2d(prev_point)
                        time_diff = (point.time - prev_point.time).total_seconds() if point.time and prev_point.time else 1
                        speed = dist / time_diff if time_diff > 0 else 0

                        # Calculate elevation jump
                        ele_jump = abs(point.elevation - prev_point.elevation) if point.elevation and prev_point.elevation else 0

                        # Proxy for signal interference: large speed or elevation jumps
                        quality = speed + ele_jump
                    else:
                        quality = 0
                    signal_quality.append(quality)
                    prev_point = point
        return signal_quality

    def analyze_route(self):
        """
        Returns latitudes, longitudes, and total distance for the route.
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

        route_analysis = {
            'latitudes': latitudes,
            'longitudes': longitudes,
            'total_distance': sum(segment.length_3d() for track in self.data.tracks for segment in track.segments),
        }
        return route_analysis

    def detect_weak_signal_spots(self, speed_threshold=10, ele_jump_threshold=5):
        """
        Identifies points with likely GPS interference based on speed/elevation jumps.
        Returns a list of dicts with lat, lon, and reason for flagging.
        """
        if self.data is None:
            raise ValueError("GPX data not loaded. Please call load_gpx() first.")

        weak_spots = []
        prev_point = None

        for track in self.data.tracks:
            for segment in track.segments:
                for point in segment.points:
                    if prev_point is not None:
                        dist = point.distance_2d(prev_point)
                        time_diff = (point.time - prev_point.time).total_seconds() if point.time and prev_point.time else 1
                        speed = dist / time_diff if time_diff > 0 else 0
                        ele_jump = abs(point.elevation - prev_point.elevation) if point.elevation and prev_point.elevation else 0

                        reasons = []
                        if speed > speed_threshold:
                            reasons.append(f"High speed jump: {speed:.2f} m/s")
                        if ele_jump > ele_jump_threshold:
                            reasons.append(f"Elevation jump: {ele_jump:.2f} m")

                        if reasons:
                            weak_spots.append({
                                'latitude': point.latitude,
                                'longitude': point.longitude,
                                'time': point.time,
                                'reasons': reasons
                            })
                    prev_point = point
        return weak_spots