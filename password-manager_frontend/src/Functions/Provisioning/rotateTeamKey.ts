import { generateSymmetricTeamKey, wrapTeamKey, base64ToBytes, importAesKey, wrapDek, unwrapDek } from "../Cripting-Decripting/Cript-Dectipr";
import {
  getTeamMembersByTeamId,
  getUserById,
  updateUserTeamsKey,
  getSubAccountsByTeamId,
  getSubAccountHistoryByTeamId,
  rotateSubAccountDeks,
} from "../../api/apis";

// Rotates a team's symmetric key: generates a fresh key client-side, re-wraps
// every sub-account's and history row's data key (DEK) from the old team key
// to the new one — content ciphertext never moves, only these small blobs —
// then re-wraps the team key itself for every current member. oldTeamKeyRaw
// must be the key already unlocked in this session; it's the only copy of it
// left anywhere once rotation finishes, so without it the DEKs (and every
// password behind them) would be unrecoverable.
export async function rotateTeamKey(
  teamId: string,
  interactorId: string,
  oldTeamKeyRaw: Uint8Array
): Promise<Uint8Array> {
  const oldTeamAesKey = await importAesKey(oldTeamKeyRaw);
  const newTeamKeyRaw = generateSymmetricTeamKey();
  const newTeamAesKey = await importAesKey(newTeamKeyRaw);

  const [subAccounts, history] = await Promise.all([
    getSubAccountsByTeamId(teamId),
    getSubAccountHistoryByTeamId(teamId),
  ]);

  // ponytail: rows created before envelope encryption have no dek_wrapped
  // and are skipped here — they stay readable only under keys already
  // rotated away. Backfill a DEK for them before enabling rotation in prod.
  const rewrap = async (dekWrapped: string | null) => {
    if (!dekWrapped) return null;
    const dekRaw = await unwrapDek(dekWrapped, oldTeamAesKey);
    return wrapDek(dekRaw, newTeamAesKey);
  };

  const rotation = {
    sub_accounts: (
      await Promise.all(
        subAccounts.map(async (sa) => {
          const dek_wrapped = await rewrap(sa.dek_wrapped);
          return dek_wrapped ? { id: sa.id, dek_wrapped } : null;
        })
      )
    ).filter((item): item is { id: string; dek_wrapped: string } => item !== null),
    history: (
      await Promise.all(
        history.map(async (h) => {
          const dek_wrapped = await rewrap(h.dek_wrapped);
          return dek_wrapped ? { id: h.id, dek_wrapped } : null;
        })
      )
    ).filter((item): item is { id: string; dek_wrapped: string } => item !== null),
  };

  if (rotation.sub_accounts.length > 0 || rotation.history.length > 0) {
    await rotateSubAccountDeks(teamId, interactorId, rotation);
  }

  const members = await getTeamMembersByTeamId(teamId);

  for (const member of members) {
    const recipient = await getUserById(member.user_id);
    if (!recipient) continue;

    const wrapped = await wrapTeamKey(
      newTeamKeyRaw,
      base64ToBytes(recipient.public_key_ec),
      base64ToBytes(recipient.public_key_pq)
    );

    await updateUserTeamsKey(
      { user_id: member.user_id, team_id: teamId, team_key_encrypted: wrapped },
      interactorId
    );
  }

  return newTeamKeyRaw;
}
