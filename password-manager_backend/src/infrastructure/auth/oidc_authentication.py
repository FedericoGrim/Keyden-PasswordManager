import os
import time
from functools import lru_cache
from typing import Any

import requests
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

# Provider-agnostic: works with any OpenID Connect issuer (Keycloak, Auth0, Entra, ...).
# Only OIDC_ISSUER and OIDC_AUDIENCE are required; everything else comes from discovery.

HTTP_TIMEOUT_SECONDS = 5
JWKS_MIN_REFRESH_SECONDS = 60
# Asymmetric only: HS* would let anyone holding a public key forge tokens, "none" skips signing.
ALLOWED_ALGORITHMS = ["RS256", "RS384", "RS512", "ES256", "ES384", "ES512"]

bearer_scheme = HTTPBearer()

_jwks_keys: dict[str, dict[str, Any]] = {}
_jwks_fetched_at = float("-inf")


def _http_get_json(url: str) -> dict[str, Any]:
    response = requests.get(url, timeout=HTTP_TIMEOUT_SECONDS)
    response.raise_for_status()
    return response.json()


@lru_cache(maxsize=1)
def _discovery_document() -> dict[str, Any]:
    # OIDC_DISCOVERY_URL is only needed when the backend reaches the IdP on a different
    # host than the one in the token's "iss" (e.g. docker-internal hostname).
    discovery_url = os.getenv("OIDC_DISCOVERY_URL") or (
        f"{os.environ['OIDC_ISSUER'].rstrip('/')}/.well-known/openid-configuration"
    )
    return _http_get_json(discovery_url)


def _signing_key(kid: str) -> dict[str, Any]:
    global _jwks_keys, _jwks_fetched_at

    # Unknown kid usually means the IdP rotated its keys: refetch, but rate-limited so
    # tokens with random kids can't turn this service into a request amplifier.
    if kid not in _jwks_keys and time.monotonic() - _jwks_fetched_at > JWKS_MIN_REFRESH_SECONDS:
        jwks = _http_get_json(_discovery_document()["jwks_uri"])
        _jwks_keys = {key["kid"]: key for key in jwks.get("keys", []) if "kid" in key}
        _jwks_fetched_at = time.monotonic()

    if kid not in _jwks_keys:
        raise JWTError(f"Unknown signing key: {kid}")
    return _jwks_keys[kid]


# Sync on purpose: FastAPI runs it in a threadpool, so the blocking IdP fetch never stalls the event loop.
def jwt_authentication(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict[str, Any]:
    """Verifies the bearer token against the OIDC issuer's JWKS and returns its payload."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = credentials.credentials

    try:
        header = jwt.get_unverified_header(token)
        payload = jwt.decode(
            token,
            _signing_key(header.get("kid", "")),
            algorithms=ALLOWED_ALGORITHMS,
            audience=os.environ["OIDC_AUDIENCE"],
            issuer=os.environ["OIDC_ISSUER"],
        )
    except JWTError as e:
        raise credentials_exception from e
    except requests.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Identity provider unreachable",
        ) from e

    if payload.get("sub") is None:
        raise credentials_exception

    return payload
