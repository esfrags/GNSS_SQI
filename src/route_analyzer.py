import numpy as np

class RouteDataAnalyzer:
    def __init__(self, all_speeds, speed_threshold=8.0):
        """
        all_speeds: list of lists, each containing speeds (m/s) for a route.
        speed_threshold: maximum plausible running speed (m/s), default ~28.8 km/h.
        """
        self.all_speeds = all_speeds
        self.speed_threshold = speed_threshold

    def detect_speed_outliers(self):
        """
        Returns a list of boolean lists, True if the speed is an outlier (too high).
        """
        outliers = []
        for speeds in self.all_speeds:
            outliers_route = [s > self.speed_threshold for s in speeds]
            outliers.append(outliers_route)
        return outliers

    def get_outlier_indices(self):
        """
        Returns a list of lists with indices of outlier points for each route.
        """
        outlier_indices = []
        for speeds in self.all_speeds:
            indices = [i for i, s in enumerate(speeds) if s > self.speed_threshold]
            outlier_indices.append(indices)
        return outlier_indices

    def summary(self):
        """
        Prints a summary of outliers detected.
        """
        total_points = sum(len(speeds) for speeds in self.all_speeds)
        total_outliers = sum(sum(s > self.speed_threshold for s in speeds) for speeds in self.all_speeds)
        print(f"Total points: {total_points}")
        print(f"Total outlier speeds: {total_outliers}")
        print(f"Outlier percentage: {100 * total_outliers / total_points:.2f}%")