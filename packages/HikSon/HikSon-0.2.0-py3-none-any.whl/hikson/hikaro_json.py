import json

class HikSon:
    @staticmethod
    def read_json(file_path) -> dict:
        """Read and return JSON data from a file as a dictionary."""
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                
                # Ensure that the data is a dictionary
                if not isinstance(data, dict):
                    raise ValueError(f"The JSON content in {file_path} is not a dictionary.")
                
                return data

        except FileNotFoundError:
            raise Exception(f"The file {file_path} does not exist.")
        except json.JSONDecodeError:
            raise Exception("Invalid JSON format.")
        except ValueError as e:
            raise Exception(str(e))

    @staticmethod
    def save_json(file_path, data: dict):
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
