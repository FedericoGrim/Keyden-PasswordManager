<p align="center">
  <img src="password-manager_frontend/public/KeydenLogo.png" alt="Keyden" width="180">
</p>

<h1 align="center">Keyden</h1>

<p align="center">
  A self-hosted, zero-knowledge password manager with post-quantum-hybrid team sharing.
</p>

<p align="center">
  <img alt="FastAPI" src="https://img.shields.io/badge/backend-FastAPI-009688?logo=fastapi&logoColor=white">
  <img alt="Next.js" src="https://img.shields.io/badge/frontend-Next.js%2016-black?logo=next.js&logoColor=white">
  <img alt="PostgreSQL" src="https://img.shields.io/badge/database-PostgreSQL-4169E1?logo=postgresql&logoColor=white">
  <img alt="Keycloak" src="https://img.shields.io/badge/auth-Keycloak-4D4D4D?logo=keycloak&logoColor=white">
  <img alt="Docker" src="https://img.shields.io/badge/deploy-Docker-2496ED?logo=docker&logoColor=white">
</p>

<p align="center">
  <img alt="CI" src="https://github.com/FedericoGrim/Keyden-PasswordManager/actions/workflows/ci.yml/badge.svg">
  <img alt="License: AGPL v3" src="https://img.shields.io/badge/license-AGPL--3.0-blue">
  <img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen">
</p>

---

Keyden is a password manager built around a simple rule: **the server never sees your secrets in plaintext.** Every password is encrypted client-side before it ever leaves the browser, and vaults can be shared with a team without the backend — or anyone but the intended recipients — ever holding a usable key.

## Highlights

- **Zero-knowledge encryption** — entries are encrypted in the browser with AES-256-GCM using a key derived from your master password via Argon2id (OWASP-recommended parameters). The server stores ciphertext only.
- **Post-quantum-hybrid key sharing** — when a vault is shared with a team, the team's symmetric key is wrapped for each member using a hybrid of ECDH (P-256) and **ML-KEM-768**, so shared keys stay protected even against a future quantum-capable attacker.
- **Team-based vaults with permission levels** — create teams, invite members, assign per-team permission levels, and organize shared entries by category.
- **Personal organization** — categories and favorites for quickly finding the entries you use most.
- **Keycloak-backed authentication** — login, registration, and session handling delegate to Keycloak (OIDC) rather than a homegrown auth layer.
- **Clean architecture backend** — the FastAPI API is layered into domain, application (use cases), infrastructure, and presentation, wired together with `dependency-injector`.

## Tech stack

| | |
|---|---|
| **Frontend** | Next.js 16, React 19, TypeScript, MUI, Tailwind CSS, `keycloak-js`, `argon2-browser`, `mlkem` |
| **Backend** | FastAPI, SQLAlchemy, Alembic, `dependency-injector`, `python-jose`, Argon2 (`argon2-cffi`) |
| **Data & auth** | PostgreSQL, Keycloak |
| **Docs & tests** | Sphinx (API docs), pytest / `unittest` |
| **Infra** | Docker Compose (separate dev and production stacks) |

## Architecture

```
password-manager_frontend/   Next.js app — UI, client-side crypto, Keycloak login
password-manager_backend/    FastAPI app
  src/domain/                 entities & repository interfaces
  src/application/            use cases (business logic) & DTOs
  src/infrastructure/         PostgreSQL repositories, Keycloak JWT validation
  src/presentation/           FastAPI controllers/routers
SDK/develop/                  Postgres + Keycloak dev stack (docker-compose)
SDK/production/               production stack (docker-compose)
```

Entries (`sub-accounts`), teams, team members, permission levels, categories, and favorites are each their own domain module, following the same entity → use case → repository → controller flow end to end.

## Getting started

### Prerequisites

- Docker & Docker Compose
- Node.js (for running the frontend outside Docker)
- Python 3.13 (for running the backend outside Docker)

### 1. Start the dev infrastructure (PostgreSQL + Keycloak)

```bash
docker compose -f SDK/develop/docker-compose.yml up -d
```

This publishes the `pm_dev_network` network and a Keycloak instance at `http://localhost:8080`. Import `SDK/realm-export.json` into Keycloak to get the `PasswordManager` realm.

### 2. Run the backend

```bash
cd password-manager_backend
cp .env.example .env   # fill in DB and Keycloak values
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload --app-dir src
```

The API is now available at `http://localhost:8000`, with interactive docs at:

- Swagger UI — `http://localhost:8000/docs`
- ReDoc — `http://localhost:8000/redoc`

Alternatively, build and run the backend in Docker (it joins the `pm_dev_network` created above):

```bash
docker compose up -d
```

### 3. Run the frontend

```bash
cd password-manager_frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

## Testing

Unit tests for the backend's use case layer, run with `pytest` (see [`password-manager_backend/tests`](password-manager_backend/tests/Readme.md)):

```bash
cd password-manager_backend
pytest
```

## API documentation

Beyond the live Swagger/ReDoc UIs, the backend's internal architecture is documented with Sphinx — see [`password-manager_backend/docs`](password-manager_backend/docs/readme.md).

## Project status

Keyden is an active, evolving project. Contributions, issues, and suggestions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). Known bugs and planned work are tracked in [Issues](https://github.com/FedericoGrim/Keyden-PasswordManager/issues). The database schema diagram is in [`docs/`](docs/PasswordManager_Schema.drawio). Report vulnerabilities via [SECURITY.md](SECURITY.md).

## License

Keyden is licensed under the [GNU Affero General Public License v3.0](LICENSE). In short: you're free to use, modify, and self-host it, but if you run a modified version as a network service, you must make that modified source available to its users.
