import boto3

session = boto3.Session(
    aws_access_key_id='YCAJE7EasWFd2LlH_j9tbt1Ar',
    aws_secret_access_key='YCP5frOh73GPSCHB8_1OhKw7Nk259ak4wILSFhoF',
)
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)

# Creating a new bucket
# s3.create_bucket(Bucket='bucket-name')

# Uploading objects into the bucket

## From a string
s3.put_object(Bucket='mlops-storage-misis', Key='object_name', Body='TEST', StorageClass='COLD')

## From a file
s3.upload_file('setup.py', 'mlops-storage-misis', 'py_script.py')
s3.upload_file('setup.py', 'mlops-storage-misis', 'script/py_script.py')

# Getting a list of objects in the bucket
for key in s3.list_objects(Bucket='mlops-storage-misis')['Contents']:
    print(key['Key'])

# Deleting multiple objects
forDeletion = [{'Key':'object_name'}, {'Key':'script/py_script.py'}]
response = s3.delete_objects(Bucket='mlops-storage-misis', Delete={'Objects': forDeletion})

# Retrieving an object
get_object_response = s3.get_object(Bucket='mlops-storage-misis',Key='py_script.py')
print(get_object_response['Body'].read())