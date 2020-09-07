from storages.backends.s3boto3 import S3Boto3Storage
import boto3
from ebdjango.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

URL_BUCKET = 'https://tenecesito-bucket.s3-us-west-1.amazonaws.com/'

class ProfilePictureStorage(S3Boto3Storage):
    location = 'profile-images/media'
    file_overwrite = True

class ProjectFileStorage(S3Boto3Storage):
    location = 'project-files'
    file_overwrite = True

def delete_in_folder(folder):
    s3 = boto3.resource('s3',
                      aws_access_key_id=AWS_ACCESS_KEY_ID, 
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    bucket = s3.Bucket('tenecesito-bucket')
    bucket.objects.filter(Prefix="profile-images/media/{}/".format(folder)).delete()

def delete_file(url):
    url = url[len(URL_BUCKET):]
    s3 = boto3.resource('s3',
                      aws_access_key_id=AWS_ACCESS_KEY_ID, 
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    bucket = s3.Bucket('tenecesito-bucket')
    bucket.objects.filter(Prefix="{}".format(url)).delete()