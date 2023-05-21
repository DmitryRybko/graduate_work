import jwt


def decode_jwt(token):

    token_clean = token.replace("Bearer ", "")
    user_id = jwt.decode(token_clean, options={"verify_signature": False})['sub']
    return user_id
