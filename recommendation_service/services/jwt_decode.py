import jwt


def decode_jwt(token: str) -> str:
    """Return user_id from token."""
    token_clean: str = token.replace("Bearer ", "")
    user_id: str = jwt.decode(
        token_clean, options={"verify_signature": False}
    )['sub']
    return user_id
