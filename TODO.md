# TODO

## Bugs

- [ ] `UpdateUserByIdUseCase` looks the user up by `keycloak_id` but updates by `id`: the two UUIDs never match, so `PUT /api/user/{user_id}` always fails.
- [ ] Deleting a user leaves their personal team orphaned (no members, never deleted).
- [ ] Removing a team member does not delete their row in `user_teams_keys`.
- [ ] Sub-accounts created before envelope encryption have no `dek_wrapped` and are skipped by `rotateTeamKey()`: backfill a DEK for them before enabling key rotation in production.

## Frontend UI missing (backend already available)

- [ ] Profile page: view user, change username, change master password (re-encrypt only the EC + PQ private keys).
- [ ] Delete user (backend + Keycloak).
- [ ] Sub-account password history view.
- [ ] Change member role.
- [ ] Remove member and wire `rotateTeamKey()` after the removal.
- [ ] Update / delete team.
- [ ] Manage permission levels (get, update, delete).
- [ ] Update / delete category.
- [ ] Unlink a category from a sub-account.

## Planned features

- [ ] Email notifications (team invites and similar).
- [ ] Enable Keycloak brute force protection (`bruteForceProtected` is `false` in `SDK/realm-export.json`).
- [ ] Export account backup.
- [ ] Detect logins from a new location.
- [ ] Detect excessive login attempts.
- [ ] Send security notifications.

## To evaluate

- [ ] Event / audit log: no practical use case found yet.

## Docs

- [ ] Align the "Funzionalità" list in `PasswordManager_Schema.drawio` with what is implemented and planned.
