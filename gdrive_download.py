import gdown

file_id = '1xPbqLJYpa1UTHvm5kQe9GOSyAKczcsKz'  # Replace with the actual ID. How to find : https://drive.google.com/file/d/FILE_ID/view?usp=sharing
output_filename = 'nagi_XL_v2.safetensors'  # Replace with desired filename

gdown.download(id=file_id, output=output_filename)
print(f"Downloaded file to {output_filename}")
