import requests
from urllib.parse import urlparse
import os

def download_file(url, output_dir=".", api_key=None):
    headers = {}
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'
    elif os.path.exists("api_key.txt"):
        with open("api_key.txt", "r") as f:
            api_key = f.read().strip()
            headers['Authorization'] = f'Bearer {api_key}'

    try:
        response = requests.get(url, stream=True, headers=headers)
        response.raise_for_status()

        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        downloaded = 0

        filename = os.path.basename(urlparse(url).path)
        if "Content-Disposition" in response.headers:
            content_disposition = response.headers["Content-Disposition"]
            if "filename" in content_disposition:
                filename = content_disposition.split("filename=")[1].strip('"')

        output_path = os.path.join(output_dir, filename)

        with open(output_path, 'wb') as f:
            for data in response.iter_content(block_size):
                downloaded += len(data)
                f.write(data)
                progress = (downloaded / total_size_in_bytes) * 100 if total_size_in_bytes else 0
                print(f"Download Progress: {progress:.2f}%", end="\r")

        print(f"\nDownloaded file to {output_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")


url = input("Enter the URL of the file: ")
output_dir = input("Enter the desired output directory (leave blank for current directory): ") or "."
api_key = input("Enter your Civitai API key (optional, will be saved for future use): ")

if api_key:
    with open("api_key.txt", "w") as f:
        f.write(api_key)

download_file(url, output_dir, api_key)
