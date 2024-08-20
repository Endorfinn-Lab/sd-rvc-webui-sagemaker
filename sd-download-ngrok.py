try:
    import gradio as gr
    import requests
    from gdown import download as gdd_download
    from pyngrok import ngrok
except ImportError:
    import pip
    pip.main(['install', 'gradio', 'requests', 'gdown', 'pyngrok'])
    import gradio
    import requests
    from gdown import download as gdd_download
    from pyngrok import ngrok

from urllib.parse import urlparse
import os
import webbrowser

# Load ngrok token from a file (or set it directly)
NGROK_TOKEN_FILE = "ngrok_token.txt"
if os.path.exists(NGROK_TOKEN_FILE):
    with open(NGROK_TOKEN_FILE, "r") as f:
        ngrok_token = f.read().strip()
else:
    ngrok_token = "2cVeyhfCmmjEU1eGXsGFQdqHuL2_32ptgmLzuGC9MmtjYVx2c"  # Replace with your actual token

# Authenticate with ngrok
ngrok.set_auth_token(ngrok_token)

def download_file(url, output_dir=".", api_key=None, is_gdrive=False):
    if is_gdrive:
        try:
            file_id = url.split('/')[-2]

            response = requests.get(f'https://drive.google.com/uc?id={file_id}&export=download')
            content_disposition = response.headers.get('Content-Disposition')
            if content_disposition:
                original_filename = content_disposition.split('filename="')[1].split('"')[0]
            else:
                original_filename = 'downloaded_file'  

            output_path = os.path.join(output_dir, original_filename)

            gdd_download(f'https://drive.google.com/uc?id={file_id}', output_path, quiet=True)

            yield f"Downloaded file from Google Drive to {output_path}"
        except Exception as e:
            yield f"Error downloading file from Google Drive: {e}"
    else:
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

            filename = os.path.basename(urlparse(url).path)
            if "Content-Disposition" in response.headers:
                content_disposition = response.headers["Content-Disposition"]
                if "filename" in content_disposition:
                    filename = content_disposition.split("filename=")[1].strip('"')

            output_path = os.path.join(output_dir, filename)

            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            yield f"Downloaded file to {output_path}"

        except requests.exceptions.RequestException as e:
            yield f"Error downloading file: {e}"

iface = gr.Interface(
    fn=download_file,
    inputs=[
        gr.Textbox(label="URL of the file"),
        gr.Textbox(label="Output directory (leave blank for current directory)", value="."),
        gr.Textbox(label="Civitai API key (optional, will be saved for future use)"),
        gr.Checkbox(label="Is Google Drive Link?")
    ],
    outputs=gr.Textbox(label="Output"),
)

# Create the ngrok tunnel
ngrok_tunnel = ngrok.connect(7860)  # Connect to Gradio's default port

if __name__ == "__main__":
    print(f" * Running on local URL:  http://127.0.0.1:7860/")
    print(f" * Public ngrok URL:   {ngrok_tunnel.public_url}")
    iface.launch()
