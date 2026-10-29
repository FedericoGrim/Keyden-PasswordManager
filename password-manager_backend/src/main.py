from fastapi import Depends, FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import RequestResponseEndpoint

from config import Container
from infrastructure.auth.oidc_authentication import jwt_authentication
from presentation.controllers.user_controller import router as user_router
from presentation.controllers.sub_account_controller import router as subaccount_router
from presentation.controllers.team_controller import router as team_router
from presentation.controllers.team_members_controller import router as team_members_router
from presentation.controllers.user_teams_keys_controller import router as user_teams_keys_router
from presentation.controllers.categories_controller import router as categories_router
from presentation.controllers.sub_account_categories_controller import router as subacc_categories_router
from presentation.controllers.team_perm_levels_controller import router as team_perm_levels_router
from presentation.controllers.user_favorite_controller import router as user_favorites_router
from presentation.controllers.sub_account_history_controller import router as subaccount_history_router

from infrastructure.databases.database import SessionLocal

from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Comma-separated list of allowed origins, e.g. "http://localhost:3000,https://app.keyden.example"
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("FRONTEND_URL", "http://localhost:3000").split(",")
    if origin.strip()
]

# ------------------------------
# FastAPI App
# ------------------------------
container = Container()
container.wire(modules=["presentation.controllers.user_controller", 
                        "presentation.controllers.sub_account_controller", 
                        "presentation.controllers.team_controller",
                        "presentation.controllers.team_members_controller",
                        "presentation.controllers.user_teams_keys_controller",
                        "presentation.controllers.categories_controller",
                        "presentation.controllers.sub_account_categories_controller",
                        "presentation.controllers.team_perm_levels_controller",
                        "presentation.controllers.user_favorite_controller",
                        "presentation.controllers.sub_account_history_controller"
                        ])

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.container = container

app.include_router(
    user_router,
    prefix="/api/user",
    tags=["User"],
    dependencies=[Depends(jwt_authentication)],
)

app.include_router(
    subaccount_router,
    prefix="/api/subaccount",
    tags=["SubAccount"],
    dependencies=[Depends(jwt_authentication)],
)

app.include_router(
    team_router,
    prefix="/api/team",
    tags=["Team"],
    dependencies=[Depends(jwt_authentication)],
)

app.include_router(
    team_members_router,
    prefix="/api/team-members",
    tags=["TeamMembers"],
    dependencies=[Depends(jwt_authentication)],
)

app.include_router(
    user_teams_keys_router,
    prefix="/api/user-teams-keys",
    tags=["UserTeamsKeys"],
    dependencies=[Depends(jwt_authentication)],
)

app.include_router(
    categories_router,
    prefix="/api/categories",
    tags=["Categories"],
    dependencies=[Depends(jwt_authentication)],
)

app.include_router(
    subacc_categories_router,
    prefix="/api/subaccount-categories",
    tags=["SubAccountCategories"],
    dependencies=[Depends(jwt_authentication)],
)

app.include_router(
    team_perm_levels_router,
    prefix="/api/team-perm-levels",
    tags=["TeamPermLevels"],
    dependencies=[Depends(jwt_authentication)],
)

app.include_router(
    user_favorites_router,
    prefix="/api/favorites",
    tags=["Favorites"],
    dependencies=[Depends(jwt_authentication)],
)

app.include_router(
    subaccount_history_router,
    prefix="/api/subaccount-history",
    tags=["SubAccountHistory"],
    dependencies=[Depends(jwt_authentication)],
)

# ------------------------------
# Middlewares DB + Log
# ------------------------------
@app.middleware("http")
async def DbSessionMiddleware(request: Request, call_next: RequestResponseEndpoint):
    response = Response("Internal server error", status_code=500)
    request.state.db = SessionLocal()
    try:
        response = await call_next(request)
        if request.method != "GET":
            request.state.db.commit()

    except Exception as e:
        request.state.db.rollback()
        raise e
    
    finally:
        request.state.db.close()

    return response


@app.middleware("http")
async def LogExceptionsMiddleware(request: Request, call_next: RequestResponseEndpoint):
    try:
        response = await call_next(request)
        return response
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise e