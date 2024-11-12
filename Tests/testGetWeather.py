import unittest
from src.EnhancedWeatherApp import getWeather

class TestGetWeather(unittest.TestCase):
    def testGetWeatherValidLocation(self):
        result = getWeather("Bismarck, North Dakota")
        self.assertIsNotNone(result)
        self.assertIn("main", result)
        self.assertIn("weather", result)
    
    def testGetWeatherInvalidLocation(self):
        result = getWeather("InvalidCity")
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
