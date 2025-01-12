import random
import string
from django.core import signing
import os
from rest_framework.response import Response
from rest_framework import status


def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def generate_token(user_id):
    token = signing.dumps({'user_id': user_id,},salt= os.environ.get('SECRET_KEY'))
    print("This is encoded token", token)
    return token

def verify_token(token):
    try:
        data = signing.loads(token, salt=os.environ.get('SECRET_KEY'), max_age=3600)
        return data
    except (signing.BadSignature, signing.SignatureExpired):
        return None
    
def format_response(message, data=None, error=None, status_code=status.HTTP_200_OK):
    response = {
        "message": message,
        "status": status_code
    }
    if error:
        response["error"] = error
    else:
        response["data"] = data
    return Response(response, status=status_code)