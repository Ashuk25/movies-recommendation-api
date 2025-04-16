import pickle
import io

class ReadFile:

    @staticmethod
    def read_pkl_from_s3(s3_client, bucket_name: str, file_key: str):
        try:
            response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
            file_content = response["Body"].read()
            print(f"read {file_key}")
            data = pickle.load(io.BytesIO(file_content))
            return data
        except Exception as e:
            print(f"Error reading pickle file: {e}")
            return None