import jwt


class ParseJWTToken:
    """Return user_id from token."""
    def __call__(self, jwt_token: str):
        self.jwt_token = jwt_token
        token_clean: str = self.jwt_token.replace("Bearer ", "")
        user_id: str = jwt.decode(
            token_clean, options={"verify_signature": False}
        )['sub']
        return user_id
