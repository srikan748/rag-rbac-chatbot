from jose import jwt
from jose import JWTError

from datetime import datetime
from datetime import timedelta


# =========================
# Secret Config
# =========================

SECRET_KEY = "mysecretkey"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


# =========================
# Dummy Users
# =========================

fake_users = {

    "hr_user": {
        "password": "hr123",
        "role": "hr"
    },

    "finance_user": {
        "password": "finance123",
        "role": "finance"
    },

    "marketing_user": {
        "password": "marketing123",
        "role": "marketing"
    },

    "executive_user": {
        "password": "executive123",
        "role": "executive"
    }
}


# =========================
# Authenticate User
# =========================

def authenticate_user(username, password):

    user = fake_users.get(username)

    if not user:

        return None

    if user["password"] != password:

        return None

    return user


# =========================
# Create JWT Token
# =========================

def create_access_token(data):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    encoded_jwt = jwt.encode(

        to_encode,

        SECRET_KEY,

        algorithm=ALGORITHM
    )

    return encoded_jwt


# =========================
# Verify JWT Token
# =========================

def verify_token(token):

    try:

        payload = jwt.decode(

            token,

            SECRET_KEY,

            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        return None