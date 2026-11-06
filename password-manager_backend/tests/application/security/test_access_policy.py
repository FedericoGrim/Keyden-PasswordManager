import uuid

import pytest

from application.security.access_policy import AccessDenied, AccessPolicy
from conftest import FakeAccessReader


@pytest.fixture
def policy(reader: FakeAccessReader) -> AccessPolicy:
    return AccessPolicy(reader)


team = uuid.uuid4()
owner = uuid.uuid4()
member = uuid.uuid4()
stranger = uuid.uuid4()


@pytest.fixture(autouse=True)
def seed(reader: FakeAccessReader) -> None:
    reader.ranks[(owner, team)] = 0
    reader.ranks[(member, team)] = 1
    reader.teams_with_members.add(team)


class TestTeamAccess:
    def test_member_is_allowed(self, policy: AccessPolicy) -> None:
        policy.require_member(member, team)

    def test_stranger_is_denied(self, policy: AccessPolicy) -> None:
        with pytest.raises(AccessDenied):
            policy.require_member(stranger, team)

    def test_owner_is_allowed_owner_actions(self, policy: AccessPolicy) -> None:
        policy.require_owner(owner, team)

    def test_plain_member_cannot_do_owner_actions(self, policy: AccessPolicy) -> None:
        with pytest.raises(AccessDenied):
            policy.require_owner(member, team)

    def test_stranger_cannot_do_owner_actions(self, policy: AccessPolicy) -> None:
        with pytest.raises(AccessDenied):
            policy.require_owner(stranger, team)


class TestBootstrap:
    def test_anyone_can_bootstrap_an_empty_team(
        self, policy: AccessPolicy, reader: FakeAccessReader
    ) -> None:
        empty_team = uuid.uuid4()
        policy.require_owner_or_empty_team(stranger, empty_team)

    def test_nobody_but_owner_can_manage_a_populated_team(
        self, policy: AccessPolicy
    ) -> None:
        policy.require_owner_or_empty_team(owner, team)
        with pytest.raises(AccessDenied):
            policy.require_owner_or_empty_team(stranger, team)
        with pytest.raises(AccessDenied):
            policy.require_owner_or_empty_team(member, team)


class TestResourceAccess:
    def test_sub_account_follows_its_team(
        self, policy: AccessPolicy, reader: FakeAccessReader
    ) -> None:
        sub_account = uuid.uuid4()
        reader.sub_account_teams[sub_account] = team
        assert policy.require_member_of_sub_account(member, sub_account) == team
        with pytest.raises(AccessDenied):
            policy.require_member_of_sub_account(stranger, sub_account)

    def test_unknown_sub_account_is_denied(self, policy: AccessPolicy) -> None:
        with pytest.raises(AccessDenied):
            policy.require_member_of_sub_account(owner, uuid.uuid4())

    def test_category_follows_its_team(
        self, policy: AccessPolicy, reader: FakeAccessReader
    ) -> None:
        category = uuid.uuid4()
        reader.category_teams[category] = team
        assert policy.require_member_of_category(member, category) == team
        with pytest.raises(AccessDenied):
            policy.require_member_of_category(stranger, category)

    def test_perm_level_owner_actions(
        self, policy: AccessPolicy, reader: FakeAccessReader
    ) -> None:
        level = uuid.uuid4()
        reader.perm_level_teams[level] = team
        assert policy.require_owner_of_perm_level(owner, level) == team
        with pytest.raises(AccessDenied):
            policy.require_owner_of_perm_level(member, level)

    def test_member_row_of_other_team_is_denied(
        self, policy: AccessPolicy, reader: FakeAccessReader
    ) -> None:
        row = uuid.uuid4()
        reader.member_rows[row] = (uuid.uuid4(), member)
        with pytest.raises(AccessDenied):
            policy.require_member_of_member_row(member, row)

    def test_key_row_readable_by_its_user_only(
        self, policy: AccessPolicy, reader: FakeAccessReader
    ) -> None:
        key = uuid.uuid4()
        reader.key_rows[key] = (team, member)
        policy.require_own_key(member, key)
        with pytest.raises(AccessDenied):
            policy.require_own_key(owner, key)


class TestSelf:
    def test_self_only(self, policy: AccessPolicy) -> None:
        policy.require_self(member, member)
        with pytest.raises(AccessDenied):
            policy.require_self(member, owner)


class TestMembershipRules:
    def test_perm_level_must_belong_to_team(
        self, policy: AccessPolicy, reader: FakeAccessReader
    ) -> None:
        level = uuid.uuid4()
        reader.perm_level_teams[level] = team
        policy.require_perm_level_in_team(level, team)
        with pytest.raises(AccessDenied):
            policy.require_perm_level_in_team(level, uuid.uuid4())
        with pytest.raises(AccessDenied):
            policy.require_perm_level_in_team(uuid.uuid4(), team)

    def test_owner_can_add_anyone(self, policy: AccessPolicy) -> None:
        policy.require_can_add_member(owner, team, stranger)

    def test_member_cannot_add_anyone(self, policy: AccessPolicy) -> None:
        with pytest.raises(AccessDenied):
            policy.require_can_add_member(member, team, stranger)

    def test_empty_team_only_lets_caller_add_self(self, policy: AccessPolicy) -> None:
        empty_team = uuid.uuid4()
        policy.require_can_add_member(stranger, empty_team, stranger)
        with pytest.raises(AccessDenied):
            policy.require_can_add_member(stranger, empty_team, member)

    def test_owner_or_self_member_row(
        self, policy: AccessPolicy, reader: FakeAccessReader
    ) -> None:
        row = uuid.uuid4()
        reader.member_rows[row] = (team, member)
        policy.require_owner_or_self_member_row(owner, team, row)
        policy.require_owner_or_self_member_row(member, team, row)
        with pytest.raises(AccessDenied):
            policy.require_owner_or_self_member_row(stranger, team, row)

    def test_member_row_must_belong_to_team(
        self, policy: AccessPolicy, reader: FakeAccessReader
    ) -> None:
        row = uuid.uuid4()
        reader.member_rows[row] = (uuid.uuid4(), member)
        with pytest.raises(AccessDenied):
            policy.require_owner_or_self_member_row(owner, team, row)
