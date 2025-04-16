class FetchS3File:

    @staticmethod
    def get_latest_file(s3_client,bucket_name: str, folder_name: str):
        try:
            # List objects in the specified folder
            response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_name + "/")

            # Ensure the folder has files
            if "Contents" not in response:
                print(f"No files found in {folder_name}")
                return None
            
            # Sort files by LastModified timestamp (latest first)
            files = sorted(response["Contents"], key=lambda x: x["LastModified"], reverse=True)

            # Get the latest file key
            latest_file_key = files[0]["Key"]
            print(f"Latest file in {folder_name}: {latest_file_key}")

            return latest_file_key
        except Exception as e:
            print(f"Error fetching latest file: {e}")
            return None