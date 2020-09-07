from django.core.management.base import BaseCommand
from api.fixtures.user_tokens import userSeed
import boto3
# from boto3.s3 import key
# BUCKET_NAME = 'tenecesito-bucket'
# AWS_ACCESS_KEY_ID = 'AKIATB4B75DESLQQFIFQ'
# AWS_SECRET_ACCESS_KEY = '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'

# def push_picture_to_s3(id):
#     try:
#         # s3 = boto3.resource('s3')
#         # for bucket in s3.buckets.all():
#         #     print(bucket.name)
#         # set boto lib debug to critical
#         logging.getLogger('boto3').setLevel(logging.CRITICAL)
#         bucket_name = settings.BUCKET_NAME
#         # connect to the bucket
#         conn = boto3 .connect_s3(settings.AWS_ACCESS_KEY_ID,
#                         settings.AWS_SECRET_ACCESS_KEY)
#         bucket = conn.get_bucket(bucket_name)
#         print('lll')
#         # go through each version of the file
#         key = 'Foto_233458.jpg' % id
#         fn = 'Foto_233458.jpg' % id
#         # create a key to keep track of our file in the storage
#         k = Key(bucket)
#         k.key = key
#         k.set_contents_from_filename(fn)
#         # we need to make it public so it can be accessed publicly
#         # using a URL like http://s3.amazonaws.com/bucket_name/key
#         k.make_public()
#     except:
#         print('ALGO NO FUNCIONA')

class Command(BaseCommand):
    def handle(self, *args, **options):
        userSeed()
        print("seeds generated.")