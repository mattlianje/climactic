from secrets import AWS_ACCES_KEY, AWS_SECRET_KEY
import io
import pickle
import boto3
from botocore.exceptions import NoCredentialsError

AWS_ACCES_KEY = '****'
AWS_SECRET_KEY = '********'
s3 = boto3.client('s3',
                  aws_access_key_id=AWS_ACCES_KEY,
                  aws_secret_access_key=AWS_SECRET_KEY)

def upload_file_to_s3(file_name, bucket_name, s3_file_name):
    try:
        s3.upload_file(file_name, bucket_name, s3_file_name)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

# s3_file_name = 'your_file_name.pkl'
def upload_npy_to_s3(npy_array, bucket_name, s3_file_name):
    try:
        array_data = io.BytesIO()
        pickle.dump(npy_array, array_data)
        array_data.seek(0)
        s3.upload_fileobj(array_data, bucket_name, s3_file_name)
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

