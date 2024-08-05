import requests
from urllib.parse import urlparse
import os

def download_file(url, output_dir=".", api_key=None):

    headers = {}
    if api_key:
        headers['Authorization'] = f'Bearer {api-key}'

    try:
        response = requests.get(url, stream=True, headers=headers)
        response.raise_for_status()

        filename = os.path.basename(urlparse(url).path)
        if "Content-Disposition" in response.headers:
            content_disposition = response.headers["Content-Disposition"]
            if "filename" in content_disposition:
                filename = content_disposition.split("filename=")[1].strip('"')

        output_path = os.path.join(output_dir, filename)

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        print(f"Downloaded file to {output_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        
url = input("Enter the URL of the file: ")
output_dir = input("Enter the desired output directory (leave blank for current directory): ") or "."
api_key = input("Enter your Civitai API key (optional): ")

download_file(url, output_dir, api_key)
