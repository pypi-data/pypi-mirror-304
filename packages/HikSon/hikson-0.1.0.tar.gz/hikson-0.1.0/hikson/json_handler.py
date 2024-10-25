import json

class HikSon:
    @staticmethod
    def read_json(file_path):
        """Read and return JSON data from a file."""
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise Exception(f"The file {file_path} does not exist.")
        except json.JSONDecodeError:
            raise Exception("Invalid JSON format.")

    @staticmethod
    def save_json(file_path, data):
        """Save JSON data to a file."""
        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
                return "Done"
        except Exception as e:
            raise Exception(f"Error saving JSON: {str(e)}")
        
    @staticmethod
    def delete_json(file_path):
        """Delete a JSON file."""
        try:
            import os
            os.remove(file_path)
            return "Done"
        except FileNotFoundError:
            raise Exception(f"The file {file_path} does not exist.")


# By Hikaro
# Instagram : hikaro.yy
# CyberSecurity & Programmer