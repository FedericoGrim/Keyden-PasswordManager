import axios from 'axios';
import axiosClient from './axiosClient';
import { mainUser } from './entities/mainUser';
import { userPublic } from './entities/userPublic';
import { subAccount } from './entities/subAccount';
import { subAccountHistory } from './entities/subAccountHistory';
import { team } from './entities/team';
import { teamMember } from './entities/teamMember';
import { teamPermLevel } from './entities/teamPermLevel';
import { userTeamsKey } from './entities/userTeamsKey';
import { category } from './entities/category';
import { favorite } from './entities/favorite';
import { UUID } from 'crypto';

axiosClient.defaults.headers.common['Content-Type'] = 'application/json';

// -------------------- User --------------------

const createMainUser = async (user: mainUser): Promise<mainUser> => {
    try {
        const response = await axiosClient.post('/api/user/', user);
        return response.data.user as mainUser;
    } catch (error) {
        console.error('Error creating main user:', error);
        throw error;
    }
}

const getMainUserByKeycloakId = async (keycloak_user_id: UUID): Promise<mainUser | null> => {
    try {
        const response = await axiosClient.get(`/api/user/${keycloak_user_id}`);
        return response.data.user as mainUser;
    } catch (error) {
        if (axios.isAxiosError(error) && error.response?.status === 404) {
            return null;
        }
        console.error('Error fetching main user by keycloak id:', error);
        throw error;
    }
};

const updateMainUser = async (user: mainUser): Promise<void> => {
    try {
        await axiosClient.put(`/api/user/${user.id}`, user);
    } catch (error) {
        console.error('Error updating main user:', error);
        throw error;
    }
};

const deleteMainUser = async (id: UUID): Promise<void> => {
    try {
        await axiosClient.delete(`/api/user/${id}`);
    } catch (error) {
        console.error('Error deleting main user:', error);
        throw error;
    }
};

const getUserByUsernameAndCode = async (username: string, code: string): Promise<userPublic | null> => {
    try {
        const response = await axiosClient.get(`/api/user/lookup/${username}/${code}`);
        return response.data.user as userPublic;
    } catch {
        return null;
    }
};

const getUserById = async (userId: string): Promise<userPublic | null> => {
    try {
        const response = await axiosClient.get(`/api/user/id/${userId}`);
        return response.data.user as userPublic;
    } catch {
        return null;
    }
};

// -------------------- Team --------------------

const createTeam = async (name: string, interactorId: string): Promise<team> => {
    const response = await axiosClient.post(
        '/api/team/',
        { name },
        { params: { user_interactor_id: interactorId } }
    );
    return response.data.team_id
        ? new team({ id: response.data.team_id, name, is_personal: false })
        : (response.data.team as team);
};

const getTeamById = async (teamId: string): Promise<team> => {
    const response = await axiosClient.get(`/api/team/${teamId}`);
    return response.data.team as team;
};

const getTeamsByUserId = async (userId: string): Promise<team[]> => {
    const response = await axiosClient.get(`/api/team/user/${userId}`);
    return response.data.teams as team[];
};

const updateTeam = async (teamId: string, name: string, interactorId: string): Promise<team> => {
    const response = await axiosClient.put(
        `/api/team/${teamId}`,
        { id: teamId, name },
        { params: { user_interactor_id: interactorId } }
    );
    return response.data.team as team;
};

const deleteTeam = async (teamId: string, interactorId: string): Promise<void> => {
    await axiosClient.delete(`/api/team/${teamId}`, {
        params: { interactor_id: interactorId },
        data: { id: teamId },
    });
};

// -------------------- Team members --------------------

const addMemberToTeam = async (teamMemberData: { user_id: string; team_id: string; perm_level_id: string }, interactorId: string): Promise<teamMember> => {
    const response = await axiosClient.post(
        `/api/team-members/${teamMemberData.team_id}/members`,
        teamMemberData,
        { params: { interactor_id: interactorId } }
    );
    return response.data.team_member as teamMember;
};

const getTeamMembersByTeamId = async (teamId: string): Promise<teamMember[]> => {
    const response = await axiosClient.get(`/api/team-members/${teamId}/members`);
    return response.data.team_members as teamMember[];
};

const removeMemberFromTeam = async (teamId: string, memberId: string, interactorId: string): Promise<void> => {
    await axiosClient.delete(`/api/team-members/${teamId}/members/${memberId}`, {
        params: { interactor_id: interactorId },
        data: { member_id: memberId, team_id: teamId },
    });
};

// -------------------- Team perm levels --------------------

const createTeamPermLevel = async (data: { team_id: string; name: string; rank: number }, interactorId: string): Promise<teamPermLevel> => {
    const response = await axiosClient.post(
        `/api/team-perm-levels/${data.team_id}`,
        data,
        { params: { user_interactor_id: interactorId } }
    );
    return response.data[1] as teamPermLevel;
};

const getAllTeamPermLevelsByTeamId = async (teamId: string): Promise<teamPermLevel[]> => {
    const response = await axiosClient.get(`/api/team-perm-levels/team/${teamId}`);
    return response.data[1] as teamPermLevel[];
};

// -------------------- User <-> team keys --------------------

const addUserTeamsKey = async (data: { user_id: string; team_id: string; team_key_encrypted: string }, interactorId: string): Promise<userTeamsKey> => {
    const response = await axiosClient.post(
        `/api/user-teams-keys/${data.team_id}/keys`,
        data,
        { params: { interactor_id: interactorId } }
    );
    return response.data.user_teams_key as userTeamsKey;
};

const getUserTeamsKeysByUserId = async (userId: string): Promise<userTeamsKey[]> => {
    const response = await axiosClient.get(`/api/user-teams-keys/user/${userId}/keys`);
    return response.data.user_teams_keys as userTeamsKey[];
};

const updateUserTeamsKey = async (data: { user_id: string; team_id: string; team_key_encrypted: string }, interactorId: string): Promise<userTeamsKey> => {
    const response = await axiosClient.put(
        `/api/user-teams-keys/${data.team_id}/keys/${data.user_id}`,
        data,
        { params: { interactor_id: interactorId } }
    );
    return response.data.updated_key as userTeamsKey;
};

// -------------------- Categories --------------------

const createCategory = async (data: { team_id: string; name: string }, interactorId: string): Promise<category> => {
    const response = await axiosClient.post(
        `/api/categories/${data.team_id}`,
        data,
        { params: { user_interactor_id: interactorId } }
    );
    return response.data[1] as category;
};

const getCategoriesByTeamId = async (teamId: string): Promise<category[]> => {
    const response = await axiosClient.get(`/api/categories/${teamId}`);
    return response.data[1] as category[];
};

const createSubAccountCategory = async (subAccountId: string, categoryId: string): Promise<void> => {
    await axiosClient.post('/api/subaccount-categories/', {
        sub_account_id: subAccountId,
        category_id: categoryId,
    });
};

// Returns join rows ({sub_account_id, category_id}), not full category
// objects — resolve names against a team's category list fetched separately.
const getCategoryIdsBySubAccountId = async (subAccountId: string): Promise<string[]> => {
    const response = await axiosClient.get(`/api/subaccount-categories/${subAccountId}`);
    const rows = response.data[1] as { sub_account_id: string; category_id: string }[];
    return rows.map((row) => row.category_id);
};

// -------------------- Sub-accounts --------------------

const createSubAccount = async (data: Omit<subAccount, 'id'>, interactorId: string): Promise<string> => {
    const response = await axiosClient.post(`/api/subaccount/${data.team_id}`, data, {
        params: { interactor_id: interactorId },
    });
    return response.data.subaccount_id as string;
};

const getSubAccountById = async (subaccountId: string): Promise<subAccount | null> => {
    try {
        const response = await axiosClient.get(`/api/subaccount/${subaccountId}`);
        return response.data.subaccount as subAccount;
    } catch {
        return null;
    }
};

const getSubAccountsByTeamId = async (teamId: string): Promise<subAccount[]> => {
    try {
        const response = await axiosClient.get(`/api/subaccount/team/${teamId}`);
        return response.data.subaccounts as subAccount[];
    } catch (error) {
        console.error('Error fetching sub accounts:', error);
        return [];
    }
};

const updateSubAccount = async (subaccountId: string, data: Partial<Omit<subAccount, 'id' | 'team_id' | 'dek_wrapped'>>, interactorId: string): Promise<void> => {
    await axiosClient.put(`/api/subaccount/${subaccountId}`, { id: subaccountId, ...data }, {
        params: { interactor_id: interactorId },
    });
};

const deleteSubAccount = async (subaccountId: string, interactorId: string): Promise<void> => {
    await axiosClient.delete(`/api/subaccount/${subaccountId}`, {
        params: { interactor_id: interactorId },
    });
};

const rotateSubAccountDeks = async (
    teamId: string,
    interactorId: string,
    rotation: { sub_accounts: { id: string; dek_wrapped: string }[]; history: { id: string; dek_wrapped: string }[] }
): Promise<void> => {
    await axiosClient.put(`/api/subaccount/team/${teamId}/rotate-deks`, rotation, {
        params: { interactor_id: interactorId },
    });
};

// -------------------- Sub-account history --------------------

const getSubAccountHistory = async (subaccountId: string): Promise<subAccountHistory[]> => {
    try {
        const response = await axiosClient.get(`/api/subaccount-history/${subaccountId}`);
        return response.data.history as subAccountHistory[];
    } catch (error) {
        console.error('Error fetching sub-account history:', error);
        return [];
    }
};

const getSubAccountHistoryByTeamId = async (teamId: string): Promise<subAccountHistory[]> => {
    try {
        const response = await axiosClient.get(`/api/subaccount-history/team/${teamId}`);
        return response.data.history as subAccountHistory[];
    } catch (error) {
        console.error('Error fetching team sub-account history:', error);
        return [];
    }
};

// -------------------- Favorites --------------------

const addFavorite = async (userId: string, subAccountId: string): Promise<favorite> => {
    const response = await axiosClient.post('/api/favorites/', { user_id: userId, sub_account_id: subAccountId });
    return response.data.favorite as favorite;
};

const removeFavorite = async (userId: string, subAccountId: string): Promise<void> => {
    await axiosClient.delete(`/api/favorites/${userId}/${subAccountId}`);
};

const getFavoritesByUserId = async (userId: string): Promise<favorite[]> => {
    const response = await axiosClient.get(`/api/favorites/user/${userId}`);
    return response.data.favorites as favorite[];
};

export {
    createMainUser,
    getMainUserByKeycloakId,
    updateMainUser,
    deleteMainUser,
    getUserByUsernameAndCode,
    getUserById,
    createTeam,
    getTeamById,
    getTeamsByUserId,
    updateTeam,
    deleteTeam,
    addMemberToTeam,
    getTeamMembersByTeamId,
    removeMemberFromTeam,
    createTeamPermLevel,
    getAllTeamPermLevelsByTeamId,
    addUserTeamsKey,
    getUserTeamsKeysByUserId,
    updateUserTeamsKey,
    createCategory,
    getCategoriesByTeamId,
    createSubAccountCategory,
    getCategoryIdsBySubAccountId,
    createSubAccount,
    getSubAccountById,
    getSubAccountsByTeamId,
    updateSubAccount,
    deleteSubAccount,
    rotateSubAccountDeks,
    getSubAccountHistory,
    getSubAccountHistoryByTeamId,
    addFavorite,
    removeFavorite,
    getFavoritesByUserId,
};
