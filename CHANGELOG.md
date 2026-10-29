# Changelog

## [0.1.0](https://github.com/FedericoGrim/Keyden-PasswordManager/compare/v0.1.0...v0.1.0) (2026-10-29)


### Features

* **api:** add team, member, perm-level, category, favorite and user-teams-key calls ([c8a59ba](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/c8a59ba60be5a95ed7bad9d24e7cf4896e6d3891))
* **api:** add typed entities for team, member, perm level, category, favorite, user-teams-key ([cba5cd7](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/cba5cd7ef5418089a3b41c8a31aff74f2f652b8b))
* **api:** Implement main user and sub-account management ([5a9aabf](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/5a9aabf95977be9fbd10eb6d8be1663af998530c))
* **auth:** client-side first-login provisioning ([01d5eb0](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/01d5eb08ed33f902e14e7cb1eb4d5732c70ca6c4))
* **auth:** provider-agnostic OIDC/JWKS token validation ([#75](https://github.com/FedericoGrim/Keyden-PasswordManager/issues/75)) ([25b6727](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/25b6727942717e325a31a06b356237b8bb2497d2))
* **auth:** refactor authentication flow and add new routes ([e9ab6ee](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/e9ab6ee5645bdadbbc5aced5eb956d432134eb57))
* **auth:** vault unlock/signup gate ([9a91968](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/9a91968ea2b15f355f2303765164781efd00bda7))
* **crypto:** Argon2id master key + AES-GCM + EC/PQ hybrid key-wrap ([2143544](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/214354405444ceb49ce1a1438a01d21413250d76))
* **crypto:** client-side team-key rotation ([41543fc](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/41543fcb0e4b46708597e426bc80eb1a4de10ff5))
* **di:** wire user-teams-keys, lookup and favorites providers ([9bc8191](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/9bc8191e2b079bf1577dd03ca2d5573dd21ca53a))
* **favorites:** add user-favorites domain, use cases and repository ([349f1e1](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/349f1e186fac32aa233f5785daaaa441dac55e6f))
* **favorites:** expose favorites REST endpoints ([03f7604](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/03f76045b27114b1b3e66307df63b88809095dc9))
* implement team management use cases and DTOs, including create, update, retrieve, and delete functionalities ([560b465](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/560b465a958ab61bc0d28448df81178613d1e56c))
* **sub-account:** password history + envelope-encrypted DEKs ([804550b](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/804550b416fa03fe318d5912f157ee201991ee6e))
* **sub-account:** password history + envelope-encrypted DEKs ([a68bc15](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/a68bc150491f88547e5dd426cd15397db491406a))
* **subaccount:** move team-scoped list to /team/{team_id} ([02953f8](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/02953f8f0f5dca0df58dab65fd6c194c288914f9))
* **team:** allow duplicate team names ([9d8729b](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/9d8729bba7c1d41c872b80cd5ddeef81148628cc))
* **ui:** rework home page with favorites column and team-scoped grid ([70998f5](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/70998f5cb1d15d54fdbafba74060dc6f3e639840))
* **ui:** sidebar nav cleanup, 404 page, mount AuthGate in layout ([9fe6e4f](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/9fe6e4f49e235334325e1f0b4643b1a0c625dcc0))
* **ui:** teams list, new-team and team-detail pages ([0d47f0c](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/0d47f0c6f56fe8c628f0c11735e87943140424f6))
* update authentication routes and add login-register page ([4de4539](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/4de4539ca67cbddfc853602ea3dd841de7c59fd6))
* Update dependencies and add create subaccount functionality ([d190989](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/d1909896fe3a1b8a6fd04daf776c941f75a37b8d))
* update dependencies and refactor encryption methods ([877f63b](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/877f63b3820151a7372a1266166fdafb1d5c3688))
* **user:** add UserPublicDTO and extend CreateUserDTO ([25ba654](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/25ba654eaf5a120e411aa42a63a807c4663214e6))
* **user:** support lookup by username+code and by id ([498b7eb](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/498b7ebbb4bf41d8482990f217e12083ede3fbe0))
* **user:** wire personal team-key into signup, add lookup endpoints ([931cf60](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/931cf60137440cba86ff1b665d5402c86f24882d))


### Bug Fixes

* **auth:** disable checkLoginIframe ([18c04ee](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/18c04ee0760a5c752c288f8bc3e7a351b154ab29))
* **ci:** fetch full history in sync-develop so origin/develop exists ([#81](https://github.com/FedericoGrim/Keyden-PasswordManager/issues/81)) ([8c65af6](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/8c65af6118c405598ec07e24ce1c54402618fc22))
* **frontend:** repair the lint pipeline broken by three stacked upgrade issues ([a571913](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/a571913cc1b3a8e81f1cb2b58b4aa325e8ea4578))
* **frontend:** resolve all remaining lint errors and warnings ([6103bed](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/6103bed1ce41986b5907b26c0e8da9c5dc833111))
* standardize casing for database module imports and update container definitions ([e0b200e](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/e0b200eac673b7874a098305b2584431b58658c4))
* standardize casing for database module references in user_controller.py ([c228abd](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/c228abd60e832c22c9ec61bd241fe634f75639c4))
* standardize casing for SQL database import in main.py ([e6dd3f5](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/e6dd3f5ea51b2ba2c8fc4f6977cb5d8913bf80ce))
* **team:** resolve DI container via request.app.state ([ae2e181](https://github.com/FedericoGrim/Keyden-PasswordManager/commit/ae2e181d3c5c4a27c6ae22a4ceea9c6ebfa68683))
