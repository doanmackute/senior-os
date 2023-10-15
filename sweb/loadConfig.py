import json, sys

# Load together configuration for all applications in OS
def load_config_json():
    # Exit when error occurs and print notification to log
    try:
        with open("../sconf/config.json", "r") as f:
            configData = json.load(f)
        f.close()
        return configData
    except FileNotFoundError:
        print(f"Configuration file not found /sconf/config.json")
    except json.JSONDecodeError:
        print(f"Error parsing JSON file: /sconf/config.json")

# Load language text and audio for web browser
def load_sweb_config_json():
    # Exit when error occurs and print notification to log
    try:
        with open("../sconf/SWEB_config.json", "r") as f:
            langDB = json.load(f)
        f.close()
        return langDB
    except FileNotFoundError:
        print(f"Configuration file not found /sconf/SWEB_config.json")
    except json.JSONDecodeError:
        print(f"Error parsing JSON file: /sconf/SWEB_config.json")

def load_config_in_same_directory(file_name):
    # Exit when error occurs and print notification to log
    try:
        with open(file_name, 'r') as f:
            data = json.load(f)
        f.close
        return data
    except FileNotFoundError:
        print(f"Configuration file not found: {file_name}")
    except json.JSONDecodeError:
        print(f"Error parsing JSON file: {file_name}")