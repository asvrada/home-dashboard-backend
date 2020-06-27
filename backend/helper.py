from rest_framework_simplejwt.tokens import RefreshToken


def get_jwt_token(user):
    refresh_token_obj = RefreshToken.for_user(user)

    refresh = str(refresh_token_obj)
    access = str(refresh_token_obj.access_token)

    return access, refresh
