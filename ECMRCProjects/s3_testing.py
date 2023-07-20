from amazons3 import AmazonS3Helper

s3_helper = AmazonS3Helper()
s3_helper.initialize_s3_client()

# Test upload_to_s3 method
file_path = '/home/mahesh/Documents/ECMRC/ECMRCProjects/sample.txt'  # Replace with your local file path
file_name = 'sample.txt'
with open(file_path, 'rb') as file:
    file_data = file.read()
    s3_url = s3_helper.upload_to_s3(file, file_name, file_data)
    print(f"Uploaded file URL: {s3_url}")

# Test download_file_from_s3 method
downloaded_file_path = s3_helper.download_file_from_s3(s3_url, 'downloaded_file.txt')
print(f"Downloaded file path: {downloaded_file_path}")

# Test get_s3_folder_name method
folder_name = s3_helper.get_s3_folder_name()
print(f"S3 Folder name: {folder_name}")
