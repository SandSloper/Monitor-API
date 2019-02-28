from itsdangerous import URLSafeTimedSerializer

from app.config import Config

class Token:
    def generate_confirmation_token(self,email):
        serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
        return serializer.dumps(email, salt=Config.SECURITY_PASSWORD_SALT)

    def confirm_token(self,token, expiration=3600):
        serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
        try:
            email = serializer.loads(
                token,
                salt=Config.SECURITY_PASSWORD_SALT,
                max_age=expiration
            )
        except:
            return False
        return email