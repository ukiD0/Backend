from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

cookie_transport = CookieTransport(cookie_name="bonds",cookie_max_age = 3600)

SECRET = "SECRET"
#нужно будет в файл env и изменить  и в конфиг импортировать ~23-25min 5 les

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name = "jet",
    transport = cookie_transport,
    get_strategy = get_jwt_strategy,
)