from authlib.integrations.flask_oauth2 import (
    AuthorizationServer,
    ResourceProtector,
)
from authlib.oauth2.rfc7636 import CodeChallenge
from ...oauth import (OAuthClient, OAuthToken, OpenIDAuthorizationCodeGrant as AuthCodeGrant,TokenValidator, TokenGenerator)
from ...oauth import OpenIDImplicitGrant, OpenIDHybridGrant, OpenIDCode
from authlib.integrations.flask_client import OAuth
oidc_authorization_server = AuthorizationServer()
require_oidc_oauth = ResourceProtector()
import os
import requests

flask_oauth = OAuth();
provider = None;

def get_adafri_provider_cfg(base=None):
    if base is not None:
        discovery_url = base + "/.well-known/openid-configuration"
        return requests.get(discovery_url).json()
    return None

def config_oidc_oauth(app, query_client=None, save_token=None, token_generators=[]):
    flask_oauth.init_app(app)
    if query_client is None:
        query_client = OAuthClient().get_by_client_id
    if save_token is None:
        save_token = OAuthToken().save
    oidc_authorization_server.query_client = query_client
    oidc_authorization_server.save_token = save_token
    oidc_authorization_server.init_app(app)
    # oidc_authorization_server.register_grant(AuthCodeGrant, [
    #     OpenIDCode(require_nonce=True),
    #     CodeChallenge(required=True)
    # ])
    # oidc_authorization_server.register_grant(OpenIDImplicitGrant)
    oidc_authorization_server.register_grant(OpenIDHybridGrant)
    # for token_generator in token_generators:
    #     type = getattr(token_generator, 'type', None);
    #     generator = getattr(token_generator, 'generator', None);
    #     if None not in [type, generator]:
    #         oidc_authorization_server.register_token_generator(type, generator)
    oidc_authorization_server.register_token_generator("default", TokenGenerator.generate)
    oidc_authorization_server.register_token_generator("client_credentials", TokenGenerator.generate)
    require_oidc_oauth.register_token_validator(TokenValidator())
