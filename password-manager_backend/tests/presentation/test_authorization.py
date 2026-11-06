import json
import uuid
from typing import Any, Optional

import pytest
from conftest import FakeAccessReader
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from application.security.access_policy import AccessPolicy
from domain.generate_user_code import USER_CODE_LENGTH
from config import Container
from infrastructure.databases.database import get_db
from presentation.controllers import (
    categories_controller,
    sub_account_categories_controller,
    sub_account_controller,
    sub_account_history_controller,
    team_controller,
    team_members_controller,
    team_perm_levels_controller,
    user_controller,
    user_favorite_controller,
    user_teams_keys_controller,
)
from presentation.security.dependencies import (
    CurrentUser,
    get_access_policy,
    get_current_user,
    get_token_subject,
)

T, SA, C, PL, MR, K = (uuid.uuid4() for _ in range(6))
OWNER, MEMBER, STRANGER = (uuid.uuid4() for _ in range(3))
OWN_ID = {OWNER: uuid.uuid4(), MEMBER: uuid.uuid4(), STRANGER: uuid.uuid4()}

ROUTERS = [
    (user_controller, "/api/user"),
    (sub_account_controller, "/api/subaccount"),
    (team_controller, "/api/team"),
    (team_members_controller, "/api/team-members"),
    (user_teams_keys_controller, "/api/user-teams-keys"),
    (categories_controller, "/api/categories"),
    (sub_account_categories_controller, "/api/subaccount-categories"),
    (team_perm_levels_controller, "/api/team-perm-levels"),
    (user_favorite_controller, "/api/favorites"),
    (sub_account_history_controller, "/api/subaccount-history"),
]


def sub_account_payload() -> dict[str, Any]:
    return {
        "team_id": str(T),
        "username_encrypted": "u",
        "email_encrypted": "e",
        "password_encrypted": "p",
        "site_link_encrypted": "s",
        "required_perm_level_id": str(PL),
        "dek_wrapped": "d",
    }


def sub_account_update_payload() -> dict[str, Any]:
    return {
        "id": str(SA),
        "username_encrypted": None,
        "email_encrypted": None,
        "password_encrypted": None,
        "site_link_encrypted": None,
        "required_perm_level_id": None,
    }


# (method, url, json, who): "member" = team members only, "owner" = team owner only,
# "user:<role>" = only that very user.
ENDPOINTS: list[tuple[str, str, Optional[dict[str, Any]], str]] = [
    ("GET", f"/api/team/{T}", None, "member"),
    ("GET", f"/api/team/user/{MEMBER}", None, "user"),
    ("PUT", f"/api/team/{T}", {"id": str(T), "name": "n"}, "owner"),
    ("DELETE", f"/api/team/{T}", {"id": str(T)}, "owner"),
    (
        "POST",
        f"/api/team-members/{T}/members",
        {"user_id": str(STRANGER), "team_id": str(T), "perm_level_id": str(PL)},
        "owner",
    ),
    ("GET", f"/api/team-members/members/{MR}", None, "member"),
    ("GET", f"/api/team-members/{T}/members", None, "member"),
    (
        "PUT",
        f"/api/team-members/{T}/members/{MR}/role",
        {"user_id": str(MEMBER), "team_id": str(T), "perm_level_id": str(PL)},
        "owner",
    ),
    (
        "DELETE",
        f"/api/team-members/{T}/members/{MR}",
        {"member_id": str(MR), "team_id": str(T)},
        "member",
    ),
    (
        "POST",
        f"/api/user-teams-keys/{T}/keys",
        {"user_id": str(STRANGER), "team_id": str(T), "team_key_encrypted": "k"},
        "owner",
    ),
    ("GET", f"/api/user-teams-keys/keys/{K}", None, "user"),
    ("GET", f"/api/user-teams-keys/{T}/keys", None, "member"),
    ("GET", f"/api/user-teams-keys/user/{MEMBER}/keys", None, "user"),
    (
        "PUT",
        f"/api/user-teams-keys/{T}/keys/{MEMBER}",
        {"user_id": str(MEMBER), "team_id": str(T), "team_key_encrypted": "k"},
        "owner",
    ),
    (
        "DELETE",
        f"/api/user-teams-keys/{T}/keys/{MEMBER}",
        {"user_id": str(MEMBER), "team_id": str(T)},
        "member",
    ),
    ("POST", f"/api/subaccount/{T}", sub_account_payload(), "member"),
    ("GET", f"/api/subaccount/{SA}", None, "member"),
    ("GET", f"/api/subaccount/team/{T}", None, "member"),
    ("PUT", f"/api/subaccount/{SA}", sub_account_update_payload(), "member"),
    ("DELETE", f"/api/subaccount/{SA}", None, "member"),
    (
        "PUT",
        f"/api/subaccount/team/{T}/rotate-deks",
        {"sub_accounts": [], "history": []},
        "owner",
    ),
    ("POST", f"/api/categories/{T}", {"team_id": str(T), "name": "n"}, "member"),
    ("GET", f"/api/categories/{T}", None, "member"),
    ("PUT", f"/api/categories/{C}", {"name": "n"}, "member"),
    ("DELETE", f"/api/categories/{C}", None, "member"),
    (
        "POST",
        "/api/subaccount-categories/",
        {"sub_account_id": str(SA), "category_id": str(C)},
        "member",
    ),
    ("GET", f"/api/subaccount-categories/{SA}", None, "member"),
    (
        "DELETE",
        f"/api/subaccount-categories/{SA}/{C}",
        {"sub_account_id": str(SA), "category_id": str(C)},
        "member",
    ),
    (
        "POST",
        f"/api/team-perm-levels/{T}",
        {"team_id": str(T), "name": "n", "rank": 2},
        "owner",
    ),
    ("GET", f"/api/team-perm-levels/{PL}", None, "member"),
    ("GET", f"/api/team-perm-levels/team/{T}", None, "member"),
    ("PUT", f"/api/team-perm-levels/{PL}", {"name": "n"}, "owner"),
    ("DELETE", f"/api/team-perm-levels/{PL}", None, "owner"),
    (
        "POST",
        "/api/favorites/",
        {"user_id": str(MEMBER), "sub_account_id": str(SA)},
        "user",
    ),
    ("GET", f"/api/favorites/user/{MEMBER}", None, "user"),
    ("DELETE", f"/api/favorites/{MEMBER}/{SA}", None, "user"),
    ("GET", f"/api/subaccount-history/{SA}", None, "member"),
    ("GET", f"/api/subaccount-history/team/{T}", None, "member"),
]


@pytest.fixture
def seeded(reader: FakeAccessReader) -> FakeAccessReader:
    reader.ranks[(OWN_ID[OWNER], T)] = 0
    reader.ranks[(OWN_ID[MEMBER], T)] = 1
    reader.teams_with_members.add(T)
    reader.sub_account_teams[SA] = T
    reader.category_teams[C] = T
    reader.perm_level_teams[PL] = T
    reader.member_rows[MR] = (T, OWN_ID[MEMBER])
    reader.key_rows[K] = (T, OWN_ID[MEMBER])
    return reader


def build_client(reader: FakeAccessReader, caller: uuid.UUID) -> TestClient:
    app = FastAPI()
    for module, prefix in ROUTERS:
        app.include_router(module.router, prefix=prefix)
    app.state.container = Container()
    user = CurrentUser(id=OWN_ID[caller], keycloak_id=caller)
    app.dependency_overrides[get_db] = lambda: MagicMock()
    app.dependency_overrides[get_current_user] = lambda: user
    app.dependency_overrides[get_token_subject] = lambda: caller
    app.dependency_overrides[get_access_policy] = lambda: AccessPolicy(reader)
    return TestClient(app, raise_server_exceptions=False)


def call(
    client: TestClient, method: str, url: str, body: Optional[dict[str, Any]]
) -> int:
    response = client.request(method, url, json=body)  # pyright: ignore
    return int(response.status_code)  # pyright: ignore


def materialize(
    url: str, body: Optional[dict[str, Any]]
) -> tuple[str, Optional[dict[str, Any]]]:
    """Endpoints refer to MEMBER/STRANGER by keycloak id; user-owned resources are
    stored under the internal id, so swap them in."""
    swapped = url.replace(str(MEMBER), str(OWN_ID[MEMBER]))
    swapped = swapped.replace(str(STRANGER), str(OWN_ID[STRANGER]))
    if body is not None:
        text = json.dumps(body).replace(str(MEMBER), str(OWN_ID[MEMBER]))
        text = text.replace(str(STRANGER), str(OWN_ID[STRANGER]))
        body = json.loads(text)
    return swapped, body


@pytest.mark.parametrize("method,url,body,who", ENDPOINTS)
def test_stranger_is_forbidden_everywhere(
    seeded: FakeAccessReader,
    method: str,
    url: str,
    body: Optional[dict[str, Any]],
    who: str,
) -> None:
    url, body = materialize(url, body)
    client = build_client(seeded, STRANGER)
    assert call(client, method, url, body) == 403


@pytest.mark.parametrize("method,url,body,who", ENDPOINTS)
def test_plain_member_is_forbidden_on_owner_endpoints(
    seeded: FakeAccessReader,
    method: str,
    url: str,
    body: Optional[dict[str, Any]],
    who: str,
) -> None:
    url, body = materialize(url, body)
    client = build_client(seeded, MEMBER)
    status = call(client, method, url, body)
    if who == "owner":
        assert status == 403
    else:
        assert status != 403


@pytest.mark.parametrize("method,url,body,who", ENDPOINTS)
def test_owner_is_allowed_except_on_other_users_resources(
    seeded: FakeAccessReader,
    method: str,
    url: str,
    body: Optional[dict[str, Any]],
    who: str,
) -> None:
    url, body = materialize(url, body)
    client = build_client(seeded, OWNER)
    status = call(client, method, url, body)
    if who == "user":
        assert status == 403
    else:
        assert status != 403


def test_registration_requires_matching_token_subject(
    seeded: FakeAccessReader,
) -> None:
    client = build_client(seeded, STRANGER)
    payload: dict[str, Any] = {
        "id": str(uuid.uuid4()),
        "keycloak_id": str(uuid.uuid4()),
        "username": "mallory",
        "code": "A" * USER_CODE_LENGTH,
        "salt": "s",
        "public_key_ec": "a",
        "private_key_ec": "a",
        "public_key_pq": "a",
        "private_key_pq": "a",
        "team_key_encrypted": "k",
    }
    assert call(client, "POST", "/api/user/", payload) == 403


def test_user_secrets_only_for_owner_of_the_token(seeded: FakeAccessReader) -> None:
    client = build_client(seeded, STRANGER)
    assert call(client, "GET", f"/api/user/{MEMBER}", None) == 403
    assert call(client, "GET", f"/api/user/{STRANGER}", None) != 403


def test_user_update_and_delete_only_on_self(seeded: FakeAccessReader) -> None:
    client = build_client(seeded, STRANGER)
    assert call(client, "DELETE", f"/api/user/{MEMBER}", None) == 403
    assert call(client, "DELETE", f"/api/user/{STRANGER}", None) != 403


def test_body_team_id_must_match_path(seeded: FakeAccessReader) -> None:
    client = build_client(seeded, OWNER)
    other = uuid.uuid4()
    assert call(client, "PUT", f"/api/team/{other}", {"id": str(T), "name": "n"}) == 403


def test_perm_level_of_another_team_is_rejected(seeded: FakeAccessReader) -> None:
    foreign_level = uuid.uuid4()
    seeded.perm_level_teams[foreign_level] = uuid.uuid4()
    client = build_client(seeded, OWNER)
    body = {
        "user_id": str(STRANGER),
        "team_id": str(T),
        "perm_level_id": str(foreign_level),
    }
    assert call(client, "POST", f"/api/team-members/{T}/members", body) == 403


def test_empty_team_can_be_bootstrapped_by_its_creator(
    seeded: FakeAccessReader,
) -> None:
    new_team = uuid.uuid4()
    client = build_client(seeded, STRANGER)
    level = {"team_id": str(new_team), "name": "Owner", "rank": 0}
    assert call(client, "POST", f"/api/team-perm-levels/{new_team}", level) != 403
    member = {
        "user_id": str(OWN_ID[STRANGER]),
        "team_id": str(new_team),
        "perm_level_id": str(PL),
    }
    assert call(client, "POST", f"/api/team-members/{new_team}/members", member) == 403
    seeded.perm_level_teams[PL] = new_team
    assert call(client, "POST", f"/api/team-members/{new_team}/members", member) != 403
