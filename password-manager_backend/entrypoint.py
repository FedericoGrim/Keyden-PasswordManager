"""Production entrypoint (distroless-compatible: no shell, no pg_isready).

Waits for the database to accept TCP connections, applies Alembic
migrations programmatically, then starts uvicorn.
"""

import os
import socket
import sys
import time

import uvicorn
from alembic import command
from alembic.config import Config


def wait_for_db(
    host: str, port: int, timeout: float = 60.0, interval: float = 2.0
) -> None:
    deadline = time.monotonic() + timeout
    while True:
        try:
            with socket.create_connection((host, port), timeout=interval):
                return
        except OSError:
            if time.monotonic() >= deadline:
                print(
                    f"Timed out waiting for database at {host}:{port}", file=sys.stderr
                )
                sys.exit(1)
            time.sleep(interval)


def run_migrations() -> None:
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


def main() -> None:
    wait_for_db(os.environ["DB_HOST"], int(os.environ["DB_PORT"]))
    run_migrations()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, app_dir="src")


if __name__ == "__main__":
    main()
