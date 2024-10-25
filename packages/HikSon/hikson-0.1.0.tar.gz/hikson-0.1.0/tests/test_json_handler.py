import unittest
import os
import json
from hikson import HikSon

class TestHikSon(unittest.TestCase):

    def setUp(self):
        """Set up a temporary JSON file for testing."""
        self.test_file = 'test_data.json'
        self.data = {"key1": "value1"}
        HikSon.save_json(self.test_file, self.data)

    def test_read_json(self):
        """Test reading JSON data from a file."""
        data = HikSon.read_json(self.test_file)
        self.assertEqual(data["key1"], "value1")

    def test_save_json(self):
        """Test saving JSON data to a file."""
        new_data = {"key2": "value2"}
        HikSon.save_json(self.test_file, new_data)
        data = HikSon.read_json(self.test_file)
        self.assertEqual(data["key2"], "value2")

    def tearDown(self):
        """Remove the temporary JSON file after tests are complete."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == '__main__':
    unittest.main()
