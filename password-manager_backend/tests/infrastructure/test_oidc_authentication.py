import time
from unittest.mock import MagicMock

import pytest
import requests
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwk, jwt

from infrastructure.auth import oidc_authentication as oidc

ISSUER = "https://idp.example.com/realms/test"
AUDIENCE = "api"
JWKS_URI = f"{ISSUER}/certs"


def _rsa_key(kid: str) -> tuple[str, dict]:
    private_pem = rsa.generate_private_key(public_exponent=65537, key_size=2048).private_bytes(
        serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()
    ).decode()
    public_jwk = jwk.construct(private_pem, "RS256").public_key().to_dict()
    public_jwk["kid"] = kid
    return private_pem, public_jwk


def _token(private_pem: str, kid: str, **claims) -> str:
    payload = {"sub": "user-1", "iss": ISSUER, "aud": AUDIENCE, "exp": int(time.time()) + 60, **claims}
    return jwt.encode(payload, private_pem, algorithm="RS256", headers={"kid": kid})


def _authenticate(token: str) -> dict:
    return oidc.jwt_authentication(HTTPAuthorizationCredentials(scheme="Bearer", credentials=token))


@pytest.fixture
def idp(monkeypatch):
    """Fake IdP: tests set idp.jwks; every GET is recorded in idp.calls."""
    state = MagicMock(jwks={"keys": []}, calls=[], down=False)

    def fake_get(url, timeout):
        state.calls.append(url)
        if state.down:
            raise requests.ConnectionError("down")
        body = {"jwks_uri": JWKS_URI} if url.endswith("/.well-known/openid-configuration") else state.jwks
        return MagicMock(json=lambda: body, raise_for_status=lambda: None)

    monkeypatch.setenv("OIDC_ISSUER", ISSUER)
    monkeypatch.setenv("OIDC_AUDIENCE", AUDIENCE)
    monkeypatch.delenv("OIDC_DISCOVERY_URL", raising=False)
    monkeypatch.setattr(oidc.requests, "get", fake_get)
    monkeypatch.setattr(oidc, "_jwks_keys", {})
    monkeypatch.setattr(oidc, "_jwks_fetched_at", float("-inf"))
    oidc._discovery_document.cache_clear()
    return state


def test_valid_token_uses_discovery_and_caches_jwks(idp):
    private_pem, public_jwk = _rsa_key("k1")
    idp.jwks = {"keys": [public_jwk]}

    assert _authenticate(_token(private_pem, "k1"))["sub"] == "user-1"
    _authenticate(_token(private_pem, "k1"))

    assert idp.calls == [f"{ISSUER}/.well-known/openid-configuration", JWKS_URI]


def test_rotated_key_triggers_jwks_refetch(idp, monkeypatch):
    old_pem, old_jwk = _rsa_key("old")
    new_pem, new_jwk = _rsa_key("new")
    idp.jwks = {"keys": [old_jwk]}
    _authenticate(_token(old_pem, "old"))

    idp.jwks = {"keys": [new_jwk]}
    monkeypatch.setattr(oidc, "_jwks_fetched_at", float("-inf"))

    assert _authenticate(_token(new_pem, "new"))["sub"] == "user-1"


def test_unknown_kid_refetch_is_rate_limited(idp):
    private_pem, public_jwk = _rsa_key("k1")
    idp.jwks = {"keys": [public_jwk]}
    _authenticate(_token(private_pem, "k1"))

    for _ in range(3):
        with pytest.raises(HTTPException) as exc:
            _authenticate(_token(private_pem, "forged-kid"))
        assert exc.value.status_code == 401

    assert idp.calls.count(JWKS_URI) == 1


@pytest.mark.parametrize("claims", [{"iss": "https://evil.example.com"}, {"aud": "other"}, {"exp": 1}])
def test_rejects_wrong_issuer_audience_or_expired(idp, claims):
    private_pem, public_jwk = _rsa_key("k1")
    idp.jwks = {"keys": [public_jwk]}

    with pytest.raises(HTTPException) as exc:
        _authenticate(_token(private_pem, "k1", **claims))
    assert exc.value.status_code == 401


def test_rejects_symmetric_token_signed_with_public_key(idp):
    _, public_jwk = _rsa_key("k1")
    idp.jwks = {"keys": [public_jwk]}
    forged = jwt.encode(
        {"sub": "attacker", "iss": ISSUER, "aud": AUDIENCE, "exp": int(time.time()) + 60},
        "any-secret",
        algorithm="HS256",
        headers={"kid": "k1"},
    )

    with pytest.raises(HTTPException) as exc:
        _authenticate(forged)
    assert exc.value.status_code == 401


def test_unreachable_idp_returns_503(idp):
    private_pem, _ = _rsa_key("k1")
    idp.down = True

    with pytest.raises(HTTPException) as exc:
        _authenticate(_token(private_pem, "k1"))
    assert exc.value.status_code == 503
