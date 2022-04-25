from fastapi.security import OpenIdConnect, OAuth2AuthorizationCodeBearer

oauth2_code_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="/oauth/authorize",
    tokenUrl="/oauth/token",
    refreshUrl="/oauth/token/refresh",
    scheme_name="authorization_code",
    scopes={
        "openid": "Open ID information",
        "email": "User email",
        "profile": "User profile information",
        "products": "Read information about de products",
    },
    description="""
        This schema define how the authorization code grant type works in
        our application, that defines the main endpoints for alll clients.
    """
)

open_id_connect = OpenIdConnect(
    openIdConnectUrl="/"
)