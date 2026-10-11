from __future__ import annotations

from dependency_injector import containers, providers

from infrastructure.databases.user_postgreSQL import UserService
from infrastructure.databases.suc_account_postgreSQL import SubAccountService
from infrastructure.databases.team_postgreSQL import TeamService
from infrastructure.databases.team_member_postgreSQL import TeamMembersService
from infrastructure.databases.user_teams_keys_postgreSQL import UserTeamsKeysService
from infrastructure.databases.categories_postgresql import CategoriesService
from infrastructure.databases.sub_account_categories_postgresql import SubAccountCategoriesService
from infrastructure.databases.team_perm_levels_postgresql import TeamPermLevelsService
from infrastructure.databases.user_favorites_postgreSQL import UserFavoritesService
from infrastructure.databases.sub_account_history_postgreSQL import SubAccountHistoryService



from application.use_case.user_use_case import (
    CreateUserUseCase,
    GetUserByKeycloakIdUseCase,
    GetUserByUsernameAndCodeUseCase,
    GetUserByIdUseCase,
    UpdateUserByIdUseCase,
    DeleteUserByIdUseCase,
)

from application.use_case.sub_account_use_case import (
    CreateSubAccountUseCase,
    GetSubAccountByIdUseCase,
    GetAllSubAccountsByTeamIdUseCase,
    UpdateSubAccountByIdUseCase,
    DeleteSubAccountByIdUseCase,
    RotateSubAccountDeksUseCase,
)

from application.use_case.sub_account_history_use_case import (
    GetSubAccountHistoryBySubAccountIdUseCase,
    GetSubAccountHistoryByTeamIdUseCase,
)

from application.use_case.team_use_case import (
    CreateTeamUseCase,
    GetTeamByIdUseCase,
    GetTeamsByUserIdUseCase,
    UpdateTeamByIdUseCase,
    DeleteTeamByIdUseCase,
)

from application.use_case.team_member_use_case import (
    AddMemberToTeamUseCase,
    GetTeamMemberByIdUseCase,
    GetTeamMembersByTeamIdUseCase,
    UpdateTeamMemberRoleUseCase,
    RemoveMemberFromTeamUseCase
)

from application.use_case.user_teams_keys_use_case import (
    AddUserTeamsKeyUseCase,
    GetUserTeamsKeyByIdUseCase,
    GetUserTeamsKeysByTeamIdUseCase,
    GetUserTeamsKeysByUserIdUseCase,
    UpdateUserTeamsKeyUseCase,
    RemoveUserTeamsKeyUseCase
)

from application.use_case.categories_use_case import (
    CreateCategoriesUseCase,
    GetAllCategoriesByTeamIdUseCase,
    UpdateCategoryByIdUseCase,
    DeleteCategoryByIdUseCase,
)

from application.use_case.sub_account_categories_use_case import (
    CreateSubAccountCategoryUseCase,
    GetAllCategoriesBySubAccountIdUseCase,
    DeleteSubAccountCategoryUseCase,
)

from application.use_case.team_perm_levels_use_case import (
    CreateTeamPermLevelUseCase,
    GetTeamPermLevelByIdUseCase,
    GetAllTeamPermLevelsByTeamIdUseCase,
    UpdateTeamPermLevelByIdUseCase,
    DeleteTeamPermLevelByIdUseCase,
)

from application.use_case.user_favorite_use_case import (
    AddFavoriteUseCase,
    GetFavoritesByUserIdUseCase,
    RemoveFavoriteUseCase,
)


# ------------------- sql Containers -------------------
class UserContainer(containers.DeclarativeContainer):
    UserRepositoryFactory = providers.Factory(UserService, db=providers.Dependency())
    TeamRepositoryFactory = providers.Factory(TeamService, db=providers.Dependency())
    TeamPermLevelRepositoryFactory = providers.Factory(TeamPermLevelsService, db=providers.Dependency())
    TeamMembersRepositoryFactory = providers.Factory(TeamMembersService, db=providers.Dependency())
    UserTeamsKeysRepositoryFactory = providers.Factory(UserTeamsKeysService, db=providers.Dependency())

    CreateUserProvider = providers.Factory(
        CreateUserUseCase,
        UserRepository=UserRepositoryFactory,
        TeamRepository=TeamRepositoryFactory,
        TeamPermLevelRepository=TeamPermLevelRepositoryFactory,
        TeamMembersRepository=TeamMembersRepositoryFactory,
        UserTeamsKeysRepository=UserTeamsKeysRepositoryFactory,
    )
    GetUserByKeycloakIdProvider = providers.Factory(
        GetUserByKeycloakIdUseCase,
        UserRepository=UserRepositoryFactory,
    )
    GetUserByUsernameAndCodeProvider = providers.Factory(
        GetUserByUsernameAndCodeUseCase,
        UserRepository=UserRepositoryFactory,
    )
    GetUserByIdProvider = providers.Factory(
        GetUserByIdUseCase,
        UserRepository=UserRepositoryFactory,
    )
    UpdateUserByIdProvider = providers.Factory(
        UpdateUserByIdUseCase,
        UserRepository=UserRepositoryFactory,
    )
    DeleteUserByIdProvider = providers.Factory(
        DeleteUserByIdUseCase,
        UserRepository=UserRepositoryFactory,
    )


class SubAccountContainer(containers.DeclarativeContainer):
    SubAccountRepositoryFactory = providers.Factory(SubAccountService, db=providers.Dependency())
    SubAccountHistoryRepositoryFactory = providers.Factory(SubAccountHistoryService, db=providers.Dependency())

    CreateSubAccountProvider = providers.Factory(
        CreateSubAccountUseCase,
        SubAccountRepository=SubAccountRepositoryFactory,
    )
    GetSubAccountByIdProvider = providers.Factory(
        GetSubAccountByIdUseCase,
        SubAccountRepository=SubAccountRepositoryFactory,
    )
    GetAllSubAccountsByTeamIdProvider = providers.Factory(
        GetAllSubAccountsByTeamIdUseCase,
        SubAccountRepository=SubAccountRepositoryFactory,
    )
    UpdateSubAccountByIdProvider = providers.Factory(
        UpdateSubAccountByIdUseCase,
        SubAccountRepository=SubAccountRepositoryFactory,
        SubAccountHistoryRepository=SubAccountHistoryRepositoryFactory,
    )
    DeleteSubAccountByIdProvider = providers.Factory(
        DeleteSubAccountByIdUseCase,
        SubAccountRepository=SubAccountRepositoryFactory,
    )
    RotateSubAccountDeksProvider = providers.Factory(
        RotateSubAccountDeksUseCase,
        SubAccountRepository=SubAccountRepositoryFactory,
        SubAccountHistoryRepository=SubAccountHistoryRepositoryFactory,
    )

class SubAccountHistoryContainer(containers.DeclarativeContainer):
    SubAccountHistoryRepositoryFactory = providers.Factory(SubAccountHistoryService, db=providers.Dependency())

    GetSubAccountHistoryBySubAccountIdProvider = providers.Factory(
        GetSubAccountHistoryBySubAccountIdUseCase,
        SubAccountHistoryRepository=SubAccountHistoryRepositoryFactory,
    )
    GetSubAccountHistoryByTeamIdProvider = providers.Factory(
        GetSubAccountHistoryByTeamIdUseCase,
        SubAccountHistoryRepository=SubAccountHistoryRepositoryFactory,
    )


class TeamContainer(containers.DeclarativeContainer):
    TeamRepositoryFactory = providers.Factory(TeamService, db=providers.Dependency())

    CreateTeamProvider = providers.Factory(
        CreateTeamUseCase,
        TeamRepository=TeamRepositoryFactory,
    )
    GetTeamByIdProvider = providers.Factory(
        GetTeamByIdUseCase,
        TeamRepository=TeamRepositoryFactory,
    )
    GetTeamsByUserIdProvider = providers.Factory(
        GetTeamsByUserIdUseCase,
        TeamRepository=TeamRepositoryFactory,
    )
    UpdateTeamByIdProvider = providers.Factory(
        UpdateTeamByIdUseCase,
        TeamRepository=TeamRepositoryFactory,
    )
    DeleteTeamByIdProvider = providers.Factory(
        DeleteTeamByIdUseCase,
        TeamRepository=TeamRepositoryFactory,
    )

class TeamMembersContainer(containers.DeclarativeContainer):
    TeamMembersRepositoryFactory = providers.Factory(TeamMembersService, db=providers.Dependency())

    AddMemberToTeamProvider = providers.Factory(
        AddMemberToTeamUseCase,
        TeamMembersRepository=TeamMembersRepositoryFactory,
    )
    
    GetTeamMemberByIdProvider = providers.Factory(
        GetTeamMemberByIdUseCase,
        TeamMembersRepository=TeamMembersRepositoryFactory,
    )
    
    GetTeamMembersByTeamIdProvider = providers.Factory(
        GetTeamMembersByTeamIdUseCase,
        TeamMembersRepository=TeamMembersRepositoryFactory,
    )

    UpdateTeamMemberRoleProvider = providers.Factory(
        UpdateTeamMemberRoleUseCase,
        TeamMembersRepository=TeamMembersRepositoryFactory,
    )
    RemoveMemberFromTeamProvider = providers.Factory(
        RemoveMemberFromTeamUseCase,
        TeamMembersRepository=TeamMembersRepositoryFactory,
    )

class UserTeamsKeysContainer(containers.DeclarativeContainer):
    UserTeamsKeysRepositoryFactory = providers.Factory(UserTeamsKeysService, db=providers.Dependency())

    AddUserTeamsKeyProvider = providers.Factory(
        AddUserTeamsKeyUseCase,
        UserTeamsKeysRepository=UserTeamsKeysRepositoryFactory,
    )

    GetUserTeamsKeyByIdProvider = providers.Factory(
        GetUserTeamsKeyByIdUseCase,
        UserTeamsKeysRepository=UserTeamsKeysRepositoryFactory,
    )

    GetUserTeamsKeysByTeamIdProvider = providers.Factory(
        GetUserTeamsKeysByTeamIdUseCase,
        UserTeamsKeysRepository=UserTeamsKeysRepositoryFactory,
    )

    GetUserTeamsKeysByUserIdProvider = providers.Factory(
        GetUserTeamsKeysByUserIdUseCase,
        UserTeamsKeysRepository=UserTeamsKeysRepositoryFactory,
    )

    UpdateUserTeamsKeyProvider = providers.Factory(
        UpdateUserTeamsKeyUseCase,
        UserTeamsKeysRepository=UserTeamsKeysRepositoryFactory,
    )
    RemoveUserTeamsKeyProvider = providers.Factory(
        RemoveUserTeamsKeyUseCase,
        UserTeamsKeysRepository=UserTeamsKeysRepositoryFactory,
    )

class CategoriesContainer(containers.DeclarativeContainer):
    CategoriesRepositoryFactory = providers.Factory(CategoriesService, db=providers.Dependency())

    CreateCategoriesProvider = providers.Factory(
        CreateCategoriesUseCase,
        CategoriesRepository=CategoriesRepositoryFactory,
    )
    GetAllCategoriesByTeamIdProvider = providers.Factory(
        GetAllCategoriesByTeamIdUseCase,
        CategoriesRepository=CategoriesRepositoryFactory,
    )
    UpdateCategoryByIdProvider = providers.Factory(
        UpdateCategoryByIdUseCase,
        CategoriesRepository=CategoriesRepositoryFactory,
    )
    DeleteCategoryByIdProvider = providers.Factory(
        DeleteCategoryByIdUseCase,
        CategoriesRepository=CategoriesRepositoryFactory,
    )

class SubAccountCategoriesContainer(containers.DeclarativeContainer):
    SubAccountCategoriesRepositoryFactory = providers.Factory(SubAccountCategoriesService, db=providers.Dependency())

    CreateSubAccountCategoryProvider = providers.Factory(
        CreateSubAccountCategoryUseCase,
        SubAccountCategoriesRepository=SubAccountCategoriesRepositoryFactory,
    )
    GetAllCategoriesBySubAccountIdProvider = providers.Factory(
        GetAllCategoriesBySubAccountIdUseCase,
        SubAccountCategoriesRepository=SubAccountCategoriesRepositoryFactory,
    )

    DeleteSubAccountCategoryProvider = providers.Factory(
        DeleteSubAccountCategoryUseCase,
        SubAccountCategoriesRepository=SubAccountCategoriesRepositoryFactory,
    )

class TeamPermLevelsContainer(containers.DeclarativeContainer):
    TeamPermLevelRepositoryFactory = providers.Factory(TeamPermLevelsService, db=providers.Dependency())

    CreateTeamPermLevelProvider = providers.Factory(
        CreateTeamPermLevelUseCase,
        TeamPermLevelRepository=TeamPermLevelRepositoryFactory,
    )
    GetTeamPermLevelByIdProvider = providers.Factory(
        GetTeamPermLevelByIdUseCase,
        TeamPermLevelRepository=TeamPermLevelRepositoryFactory,
    )
    GetAllTeamPermLevelsByTeamIdProvider = providers.Factory(
        GetAllTeamPermLevelsByTeamIdUseCase,
        TeamPermLevelRepository=TeamPermLevelRepositoryFactory,
    )
    UpdateTeamPermLevelByIdProvider = providers.Factory(
        UpdateTeamPermLevelByIdUseCase,
        TeamPermLevelRepository=TeamPermLevelRepositoryFactory,
    )
    DeleteTeamPermLevelByIdProvider = providers.Factory(
        DeleteTeamPermLevelByIdUseCase,
        TeamPermLevelRepository=TeamPermLevelRepositoryFactory,
    )

class UserFavoritesContainer(containers.DeclarativeContainer):
    UserFavoriteRepositoryFactory = providers.Factory(UserFavoritesService, db=providers.Dependency())

    AddFavoriteProvider = providers.Factory(
        AddFavoriteUseCase,
        UserFavoriteRepository=UserFavoriteRepositoryFactory,
    )
    GetFavoritesByUserIdProvider = providers.Factory(
        GetFavoritesByUserIdUseCase,
        UserFavoriteRepository=UserFavoriteRepositoryFactory,
    )
    RemoveFavoriteProvider = providers.Factory(
        RemoveFavoriteUseCase,
        UserFavoriteRepository=UserFavoriteRepositoryFactory,
    )

# ------------------- Aggregated Container -------------------
class Container(containers.DeclarativeContainer):
    user = providers.Container(UserContainer)
    subaccount = providers.Container(SubAccountContainer)
    team = providers.Container(TeamContainer)
    team_members = providers.Container(TeamMembersContainer)
    user_teams_keys = providers.Container(UserTeamsKeysContainer)
    categories = providers.Container(CategoriesContainer)
    sub_account_categories = providers.Container(SubAccountCategoriesContainer)
    team_perm_levels = providers.Container(TeamPermLevelsContainer)
    user_favorites = providers.Container(UserFavoritesContainer)
    sub_account_history = providers.Container(SubAccountHistoryContainer)

