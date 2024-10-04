import gdown
import os

file_id = input("File ID: ")
filename = None
destination = input("Destination Folde(Leave blank for current folder): ")

if not destination:
  destination = "."

filename = os.path.join(destination file_id)

gdown.download(id=file_id, output=filename, quiet=False)
print(f"Downloaded file {filename}")
