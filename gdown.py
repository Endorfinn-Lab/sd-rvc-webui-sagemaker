import gdown

file_id = input("File ID: ")
filename = None

gdown.download(id=file_id, output=filename)
print(f"Downloaded file {filename}")
