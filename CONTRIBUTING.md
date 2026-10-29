# Contributing to Keyden

Thanks for helping out! Bug reports, fixes, docs and ideas are all welcome.

## Setup

Follow [Getting started](readme.md#getting-started) to run the dev stack, backend and frontend.

## Workflow

1. Open an issue first for anything bigger than a small fix (see [TODO.md](TODO.md) for known work).
2. Fork, then branch from `develop`: `feature/<short-name>` or `fix/<short-name>`.
3. Keep changes focused: one concern per PR.
4. Make sure checks pass locally (same as [CI](.github/workflows/ci.yml)):
   ```bash
   cd password-manager_backend && pytest
   cd password-manager_frontend && npm run lint && npm run build
   ```
5. Open a PR against `develop` and fill in the template.

## Code style

- **Backend:** Python 3.13, type hints, follow the existing layering (domain → application → infrastructure → presentation). New use cases get a unit test in `password-manager_backend/tests`.
- **Frontend:** TypeScript, ESLint config in the repo.
- Formatting basics are in [.editorconfig](.editorconfig).

## Commits

Conventional style preferred: `feat: ...`, `fix: ...`, `docs: ...`, `refactor: ...`, `test: ...`.

## Security

Never open a public issue for a vulnerability. See [SECURITY.md](SECURITY.md).

By contributing you agree your work is licensed under the [AGPL-3.0](LICENSE).
