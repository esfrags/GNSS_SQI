import numpy as np
from utils import log_message

class RouteDataAnalyzer:
    def __init__(self, all_speeds, all_altitudes, speed_threshold=8.0, elevation_threshold=5.0):
        """
        all_speeds: list of lists, each containing speeds (m/s) for a route.
        all_altitudes: list of lists, each containing altitudes (m) for a route.
        speed_threshold: maximum plausible running speed (m/s), default ~28.8 km/h.
        """
        self.all_speeds = all_speeds
        self.all_altitudes = all_altitudes
        self.speed_threshold = speed_threshold
        self.elevation_threshold = elevation_threshold

    def detect_speed_outliers(self):
        """
        Returns a list of lists with indices of speed outliers (too high) for each route.
        """
        outlier_indices = []
        for speeds in self.all_speeds:
            indices = [i for i, s in enumerate(speeds) if s > self.speed_threshold]
            outlier_indices.append(indices)
        return outlier_indices
    
    def detect_altitude_outliers(self):
        """
        Returns a list of lists with indices of abrupt elevation change points for each route.
        """
        outlier_indices = []
        for altitudes in self.all_altitudes:
            indices = [i for i in range(1, len(altitudes))
                    if abs(altitudes[i] - altitudes[i-1]) > self.elevation_threshold]
            outlier_indices.append(indices)
        return outlier_indices

    def summary(self):
        """
        Logs a summary of outliers detected using log_message.
        """
        total_points = sum(len(speeds) for speeds in self.all_speeds)
        total_speed_outliers = sum(sum(s > self.speed_threshold for s in speeds) for speeds in self.all_speeds)
        total_altitude_outliers = sum(
            sum(abs(altitudes[i] - altitudes[i-1]) > self.elevation_threshold for i in range(1, len(altitudes)))
            for altitudes in self.all_altitudes
        )
        log_message(f"Total points: {total_points}")
        log_message(f"Total speed outliers: {total_speed_outliers}")
        log_message(f"Total altitude outliers: {total_altitude_outliers}")
        log_message(f"Speed outlier percentage: {100 * total_speed_outliers / total_points:.2f}%")
        log_message(f"Altitude outlier percentage: {100 * total_altitude_outliers / total_points:.2f}%")