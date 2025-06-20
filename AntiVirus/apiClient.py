import requests
from pathlib import Path
from typing import Union
from api_key_set_up import get_api_key
import time

class ApiClient:
    def __init__(self) -> None:
        self.API_KEY: str = get_api_key()
        self.virustotal_api_url_scan: str = 'https://www.virustotal.com/vtapi/v2/file/scan'
        self.virustotal_api_url_report = 'https://www.virustotal.com/vtapi/v2/file/report'
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
        print(f"Connection closed.\nexc_type: {exc_type}\nexc_val: {exc_val}\nexc_tb: {exc_tb}")

    def path_exists(self, path: Union[str, Path]) -> bool:
        """Check if a file path exists using pathlib."""
        return Path(path).exists()

    def scan_folder(self, folder_path: Union[str, Path]) -> None:
        """Scan all files in a folder using VirusTotal API"""
        if not self.path_exists(folder_path) or not Path(folder_path).is_dir():
            raise FileNotFoundError(f"Folder not found: {folder_path} or is not a directory")

        folder = Path(folder_path)
        for file in folder.iterdir():
            if file.is_file():
                self.scan_file(file)
            if file.is_dir():
                self.scan_folder(file)
            else:
                print(f"Skipping non-file item: {file}")
                
    # Scan one file 
    def scan_file(self, file_path: Union[str, Path]) -> bool:
        """Scan a file using VirusTotal API with proper error handling"""
        if not self.path_exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        print("Scanning: ", file_path)
        
        try:
            scan_request = self.send_scan_request(file_path)
            is_virus = self.get_scan_report(scan_id=scan_request['scan_id'])
            
            if is_virus:
                print("VIRUS DETECTED!!! Filepath: ", file_path)
                return True
            else:
                print("{} is not virus".format(file_path))
                return False
                
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to scan file {file_path}: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error during file scan: {e}")

    def send_scan_request(self, file_path: Union[str, Path]) -> str:
        params = {'apikey': f'{self.API_KEY}'}
        
        file_name = Path(file_path).name
        files = {'file': (file_name, open(file_name, 'rb'))}
        response = requests.post(self.virustotal_api_url_scan, files=files, params=params)
        return response.json()
        
        
    def get_scan_report(self, scan_id: str) -> dict:
        params = {'apikey': f'{self.API_KEY}', 'resource': f'{scan_id}'}
        response = requests.get(self.virustotal_api_url_report, params=params)
        if not response:
            raise RuntimeError(f"Failed to retrieve report for analysis ID: {scan_id}")
        
        if response.status_code == 200:
            result = response.json()
            if result["verbose_msg"] == "Your resource is queued for analysis":
                print("Waiting for file to be analyzed...")
                time.sleep(5)
                self.get_scan_report(scan_id)
                return False
            else:
                return result["positives"] > 0
        else:
            print("Received unexpected response with status code:", response.status_code)
            return False


