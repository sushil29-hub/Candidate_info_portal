from candidate_portal import settings
import boto3

def get_s3_connection():
    session = boto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    return session

s3_connection = get_s3_connection()