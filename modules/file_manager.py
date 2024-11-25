import requests
from urllib.parse import urlparse
import zipfile
import os

class FileManager:
    def download_file(self, url, output_path):
        """
        Downloads a file with enhanced error handling and SharePoint support.
        """
        try:
            # Parse the URL
            parsed_url = urlparse(url)
            
            # Configure headers for SharePoint
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            # First request to handle potential redirects
            initial_response = requests.get(url, headers=headers, allow_redirects=True)
            
            if initial_response.status_code == 403:
                raise Exception("Access Denied. Please check if the SharePoint link is properly shared and accessible.")
            
            if initial_response.status_code != 200:
                raise Exception(f"Failed to download file: HTTP {initial_response.status_code} - {initial_response.reason}")

            # Check content type
            content_type = initial_response.headers.get('Content-Type', '')
            if 'html' in content_type.lower():
                raise Exception("Received HTML instead of file. The SharePoint link might require authentication or isn't a direct download link.")

            # Save the file
            with open(output_path, 'wb') as f:
                f.write(initial_response.content)

            # Verify file size
            file_size = os.path.getsize(output_path)
            if file_size == 0:
                raise Exception("Downloaded file is empty")

            # Verify if it's a valid ZIP file
            if not zipfile.is_zipfile(output_path):
                raise Exception("Downloaded file is not a valid ZIP file. Please check the SharePoint sharing settings and URL.")

            print(f"Successfully downloaded file: {output_path}")
            print(f"File size: {file_size} bytes")
            print(f"Content-Type: {content_type}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error while downloading: {str(e)}")
        except Exception as e:
            if os.path.exists(output_path):
                os.remove(output_path)  # Clean up partial download
            raise

    def extract_zip(self, zip_file, extract_folder):
        """
        Extracts a ZIP file with validation.
        """
        if not os.path.exists(zip_file):
            raise Exception(f"ZIP file not found: {zip_file}")

        if not zipfile.is_zipfile(zip_file):
            raise Exception(f"Not a valid ZIP file: {zip_file}")

        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)
            print(f"Successfully extracted {zip_file} to {extract_folder}")

    def diagnose_download(self, url):
        """
        Diagnoses issues with file download.
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, allow_redirects=True)
            
            print("\nDownload Diagnosis:")
            print(f"Status Code: {response.status_code}")
            print(f"Content-Type: {response.headers.get('Content-Type')}")
            print(f"Content-Length: {response.headers.get('Content-Length', 'Unknown')} bytes")
            print(f"URL after redirects: {response.url}")
            print("\nResponse Headers:")
            for key, value in response.headers.items():
                print(f"{key}: {value}")

            return response.status_code == 200

        except Exception as e:
            print(f"\nError during diagnosis: {str(e)}")
            return False