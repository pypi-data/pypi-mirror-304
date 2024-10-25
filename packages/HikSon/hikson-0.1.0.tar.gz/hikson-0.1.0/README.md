
# HikSon

HikSon is a simple and efficient Python package designed to make it easier to **read**, **save**, and **delete** JSON data files. This package provides a clean and intuitive API for handling basic JSON file operations in Python.

## Features

- **Read JSON**: Easily load and return data from a JSON file.
- **Save JSON**: Save or overwrite data in a JSON file with simple method calls.
- **Delete JSON**: Remove JSON files from your system.

## Installation

HikSon can be installed using pip (once published on PyPI):
```bash
pip install HikSon
```

Or you can clone the repository and install it manually:
```bash
git clone https://github.com/1cz1/HikSon.git
cd HikSon
pip install .
```

## Usage

### 1. **Reading a JSON file:**
Use the `read_json` method to load data from a JSON file.
```python
from hikson import HikSon

data = HikSon.read_json('data.json')
print(data)
```

### 2. **Saving data to a JSON file:**
Use the `save_json` method to write or update data in a JSON file.
```python
from hikson import HikSon

data = {
    "name": "Hikaro",
    "skills": ["Cybersecurity", "Programming"]
}

HikSon.save_json('data.json', data)
```

### 3. **Deleting a JSON file:**
Use the `delete_json` method to delete a JSON file from the system.
```python
from hikson import HikSon

HikSon.delete_json('data.json')
```

## API Reference

### `read_json(file_path)`
- **Description**: Reads a JSON file from the provided file path and returns its data.
- **Arguments**: 
  - `file_path` (str): The path to the JSON file.
- **Returns**: The contents of the JSON file as a Python dictionary or list.
- **Exceptions**: Raises an exception if the file is not found or contains invalid JSON.

### `save_json(file_path, data)`
- **Description**: Saves Python data (dict, list, etc.) to a JSON file at the specified path.
- **Arguments**: 
  - `file_path` (str): The path to save the JSON file.
  - `data` (dict or list): The data to be saved.
- **Returns**: "Done" when the file is successfully saved.
- **Exceptions**: Raises an exception if there’s an issue saving the file.

### `delete_json(file_path)`
- **Description**: Deletes a JSON file from the specified path.
- **Arguments**: 
  - `file_path` (str): The path to the JSON file to be deleted.
- **Returns**: "Done" when the file is successfully deleted.
- **Exceptions**: Raises an exception if the file does not exist.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/yourusername/HikSon/issues) or open a pull request.

## Author

**Hikaro**  
Cybersecurity & Programmer  
[Instagram: @hikaro.yy](https://instagram.com/hikaro.yy)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
