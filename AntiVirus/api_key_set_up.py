import base64
from pathlib import Path

def decode_api_key(api_key: str) -> str:
    try:
        return base64.b64decode(api_key).decode('utf-8').strip()
    except Exception as e:
        raise ValueError(f"Invalid API key: {e}")

def get_api_key(api_key_path: str | Path = "API.txt") -> str:
    """
    Read API key from a file.
    
    :param key_path: Path to the API key file
    :return: API key as a string
    :raises FileNotFoundError: If key file does not exist
    """
    try:
        path = Path(api_key_path) if isinstance(api_key_path, str) else api_key_path
        
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"API key file not found: {path}")
        
        with path.open('r') as file:
            return decode_api_key(decode_api_key(file.read().strip()))
        
    except FileNotFoundError:
        raise ValueError(f"API key file not found: {path}")
    except Exception as e:
        raise ValueError(f"Error reading API key: {e}")

