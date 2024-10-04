import gdown
import os

file_id = input("File ID: ")
destination = input("Destination Folder (leave blank for current folder): ")
filename = input("File Name (with extension): ")

if not destination:
  destination = "."

output = os.path.join(destination, filename)

gdown.download(id=file_id, output=output, quiet=False)
print(f"Downloaded file {filename}")
