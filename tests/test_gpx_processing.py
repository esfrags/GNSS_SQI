import unittest
from src.gpx_processing import GPXProcessor

class TestGPXProcessing(unittest.TestCase):

    def setUp(self):
        self.processor = GPXProcessor()

    def test_load_gpx(self):
        # Test loading a valid GPX file
        valid_gpx_file = 'path/to/valid.gpx'
        result = self.processor.load_gpx(valid_gpx_file)
        self.assertIsNotNone(result)
        self.assertTrue(hasattr(result, 'tracks'))

    def test_load_invalid_gpx(self):
        # Test loading an invalid GPX file
        invalid_gpx_file = 'path/to/invalid.gpx'
        with self.assertRaises(ValueError):
            self.processor.load_gpx(invalid_gpx_file)

    def test_extract_signal_quality(self):
        # Test extracting signal quality from a GPX track
        gpx_data = self.processor.load_gpx('path/to/valid.gpx')
        signal_quality = self.processor.extract_signal_quality(gpx_data)
        self.assertIsInstance(signal_quality, list)
        self.assertGreater(len(signal_quality), 0)

    def test_analyze_route(self):
        # Test analyzing a route for signal quality
        gpx_data = self.processor.load_gpx('path/to/valid.gpx')
        analysis_result = self.processor.analyze_route(gpx_data)
        self.assertIn('average_quality', analysis_result)
        self.assertIn('max_quality', analysis_result)

if __name__ == '__main__':
    unittest.main()