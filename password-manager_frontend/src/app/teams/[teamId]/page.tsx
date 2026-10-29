"use client";

import { useCallback, useEffect, useState } from "react";
import { useParams } from "next/navigation";

import { useVault } from "@/Components/AuthGate/VaultContext";
import {
  getTeamById,
  getUserTeamsKeysByUserId,
  getSubAccountsByTeamId,
  getAllTeamPermLevelsByTeamId,
  getCategoriesByTeamId,
  getCategoryIdsBySubAccountId,
  deleteSubAccount,
  createCategory,
} from "@/api/apis";
import { team } from "@/api/entities/team";
import { teamPermLevel } from "@/api/entities/teamPermLevel";
import { category } from "@/api/entities/category";
import { unwrapTeamKey, importAesKey, decryptSubAccountFields } from "@/Functions/Cripting-Decripting/Cript-Dectipr";
import SubAccountForm, { DecryptedSubAccount } from "./page-components/subAccountForm/subAccountForm";
import ShareTeamDialog from "./page-components/shareTeamDialog/shareTeamDialog";
import MembersList from "./page-components/membersList/membersList";
import "./team-detail.css";

export default function TeamDetailPage() {
  const { teamId } = useParams<{ teamId: string }>();
  const vault = useVault();

  const [teamInfo, setTeamInfo] = useState<team | null>(null);
  const [teamKeyRaw, setTeamKeyRaw] = useState<Uint8Array | null>(null);
  const [teamAesKey, setTeamAesKey] = useState<CryptoKey | null>(null);
  const [accessError, setAccessError] = useState<string | null>(null);

  const [subAccounts, setSubAccounts] = useState<DecryptedSubAccount[] | null>(null);
  const [permLevels, setPermLevels] = useState<teamPermLevel[]>([]);
  const [categories, setCategories] = useState<category[]>([]);
  const [tagsBySubAccount, setTagsBySubAccount] = useState<Record<string, string[]>>({});

  const [formTarget, setFormTarget] = useState<DecryptedSubAccount | "new" | null>(null);
  const [showShareDialog, setShowShareDialog] = useState(false);
  const [newCategoryName, setNewCategoryName] = useState("");

  // Team header + this user's unwrapped team key.
  useEffect(() => {
    getTeamById(teamId).then(setTeamInfo);

    getUserTeamsKeysByUserId(vault.user.id).then(async (keys) => {
      const match = keys.find((k) => k.team_id === teamId);
      if (!match) {
        setAccessError("You don't have access to this team.");
        return;
      }
      const raw = await unwrapTeamKey(match.team_key_encrypted, vault.privateKeyEc, vault.privateKeyPq);
      const aesKey = await importAesKey(raw);
      setTeamKeyRaw(raw);
      setTeamAesKey(aesKey);
    });

    getAllTeamPermLevelsByTeamId(teamId).then(setPermLevels);
    getCategoriesByTeamId(teamId).then(setCategories);
  }, [teamId, vault]);

  const loadSubAccounts = useCallback(async () => {
    if (!teamAesKey) return;
    const raw = await getSubAccountsByTeamId(teamId);
    const decrypted = await Promise.all(
      raw.map(async (sa) => ({
        id: sa.id,
        ...(await decryptSubAccountFields(sa, teamAesKey)),
        requiredPermLevelId: sa.required_perm_level_id,
        dekWrapped: sa.dek_wrapped,
      }))
    );
    setSubAccounts(decrypted);
  }, [teamId, teamAesKey]);

  useEffect(() => {
    // Same shape as home/page.tsx: loadSubAccounts only sets state after
    // awaiting the network/crypto work, re-run whenever the team key changes.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    loadSubAccounts();
  }, [loadSubAccounts]);

  const loadTags = useCallback(
    async (subAccountId: string) => {
      const ids = await getCategoryIdsBySubAccountId(subAccountId);
      const names = ids.map((id) => categories.find((c) => c.id === id)?.name).filter((n): n is string => !!n);
      setTagsBySubAccount((prev) => ({ ...prev, [subAccountId]: names }));
    },
    [categories]
  );

  const handleAddCategory = async () => {
    if (!newCategoryName.trim()) return;
    await createCategory({ team_id: teamId, name: newCategoryName.trim() }, vault.user.id);
    setNewCategoryName("");
    getCategoriesByTeamId(teamId).then(setCategories);
  };

  if (accessError) {
    return <div className="team-detail-page"><p>{accessError}</p></div>;
  }

  if (!teamAesKey || !subAccounts) {
    return <div className="team-detail-page"><p>Unlocking team vault...</p></div>;
  }

  return (
    <div className="team-detail-page">
      <div className="team-detail-header">
        <h1>{teamInfo?.name ?? "..."}</h1>
        <div className="team-detail-actions">
          {!teamInfo?.is_personal && (
            <button onClick={() => setShowShareDialog(true)}>Share</button>
          )}
          <button onClick={() => setFormTarget("new")}>+ Add entry</button>
        </div>
      </div>

      <div className="team-detail-grid">
        {subAccounts.length === 0 && <p>No entries yet.</p>}
        {subAccounts.map((sa) => (
          <button
            key={sa.id}
            className="team-detail-card"
            onClick={() => setFormTarget(sa)}
            onMouseEnter={() => !(sa.id in tagsBySubAccount) && loadTags(sa.id)}
          >
            <div className="team-detail-card-title">{sa.username || sa.email || "(untitled)"}</div>
            {sa.siteLink && <div className="team-detail-card-sub">{sa.siteLink}</div>}
            {tagsBySubAccount[sa.id]?.length > 0 && (
              <div className="team-detail-card-tags">{tagsBySubAccount[sa.id].join(", ")}</div>
            )}
            <span
              className="team-detail-card-delete"
              onClick={async (e) => {
                e.stopPropagation();
                if (!confirm("Delete this entry?")) return;
                await deleteSubAccount(sa.id, vault.user.id);
                loadSubAccounts();
              }}
            >
              ✕
            </span>
          </button>
        ))}
      </div>

      <div className="team-detail-section">
        <h2>Members</h2>
        <MembersList teamId={teamId} permLevels={permLevels} />
      </div>

      <div className="team-detail-section">
        <h2>Categories</h2>
        <div className="team-detail-category-add">
          <input
            value={newCategoryName}
            onChange={(e) => setNewCategoryName(e.target.value)}
            placeholder="New category"
          />
          <button onClick={handleAddCategory}>Add</button>
        </div>
        <div className="team-detail-category-list">
          {categories.map((c) => (
            <span key={c.id} className="team-detail-category-chip">{c.name}</span>
          ))}
        </div>
      </div>

      {formTarget && (
        <SubAccountForm
          teamId={teamId}
          teamAesKey={teamAesKey}
          interactorId={vault.user.id}
          permLevels={permLevels}
          categories={categories}
          editing={formTarget === "new" ? null : formTarget}
          onClose={() => setFormTarget(null)}
          onSaved={() => {
            setFormTarget(null);
            loadSubAccounts();
          }}
        />
      )}

      {showShareDialog && teamKeyRaw && (
        <ShareTeamDialog
          teamId={teamId}
          teamKeyRaw={teamKeyRaw}
          interactorId={vault.user.id}
          permLevels={permLevels}
          onClose={() => setShowShareDialog(false)}
          onShared={() => setShowShareDialog(false)}
        />
      )}
    </div>
  );
}
