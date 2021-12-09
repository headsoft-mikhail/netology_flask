from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, BadSignature
from config import SECRET_KEY, EXPIRE_TIME
from models import User, Post

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth('Token')
multi_auth = MultiAuth(basic_auth, token_auth)
serializer = TimedJSONWebSignatureSerializer(SECRET_KEY, expires_in=EXPIRE_TIME)


def create_token(email):
    token = serializer.dumps({'email': email})
    print(token.decode('utf-8'))


@token_auth.verify_token
def verify_token(token):
    try:
        data = serializer.loads(token)
    except SignatureExpired:
        return None  # valid token, but expired
    except (BadSignature, TypeError, ValueError):
        return None  # invalid token

    if 'email' in data.keys():
        email = data['email']
        return email
    else:
        return False


@basic_auth.verify_password
def verify_password(email, password):
    user = User.get_by_email(email)
    if not user or not user.verify_password(password):
        return False
    create_token(email)
    return email


def check_owner(obj_class: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            obj = globals()[obj_class].get_by_id(kwargs['obj_id'])
            if obj.owner.email == multi_auth.current_user():
                result = func(*args, **kwargs)
            else:
                raise BadSignature
            return result
        return wrapper
    return decorator
