"use client";

import { FormEvent, useState } from "react";

import { createSubAccount, updateSubAccount, createSubAccountCategory } from "@/api/apis";
import { encrypt, generateSymmetricTeamKey, importAesKey, wrapDek, unwrapDek } from "@/Functions/Cripting-Decripting/Cript-Dectipr";
import { teamPermLevel } from "@/api/entities/teamPermLevel";
import { category } from "@/api/entities/category";
import "./subAccountForm.css";

export type DecryptedSubAccount = {
  id: string;
  username: string;
  email: string;
  password: string;
  siteLink: string;
  requiredPermLevelId: string;
  dekWrapped: string;
};

export default function SubAccountForm({
  teamId,
  teamAesKey,
  interactorId,
  permLevels,
  categories,
  editing,
  onClose,
  onSaved,
}: {
  teamId: string;
  teamAesKey: CryptoKey;
  interactorId: string;
  permLevels: teamPermLevel[];
  categories: category[];
  editing: DecryptedSubAccount | null;
  onClose: () => void;
  onSaved: () => void;
}) {
  const lowestRank = [...permLevels].sort((a, b) => a.rank - b.rank)[0];

  const [username, setUsername] = useState(editing?.username ?? "");
  const [email, setEmail] = useState(editing?.email ?? "");
  const [password, setPassword] = useState(editing?.password ?? "");
  const [siteLink, setSiteLink] = useState(editing?.siteLink ?? "");
  const [permLevelId, setPermLevelId] = useState(editing?.requiredPermLevelId ?? lowestRank?.id ?? "");
  const [selectedCategoryIds, setSelectedCategoryIds] = useState<string[]>([]);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      // Every entry is encrypted with its own data key (DEK), not the team
      // key directly — reuse the existing DEK on edit, mint one on create.
      const dekRaw = editing
        ? await unwrapDek(editing.dekWrapped, teamAesKey)
        : generateSymmetricTeamKey();
      const dek = await importAesKey(dekRaw);

      const [usernameEnc, emailEnc, passwordEnc, siteLinkEnc] = await Promise.all([
        encrypt(username, dek),
        encrypt(email, dek),
        encrypt(password, dek),
        encrypt(siteLink, dek),
      ]);

      if (editing) {
        await updateSubAccount(editing.id, {
          username_encrypted: usernameEnc,
          email_encrypted: emailEnc,
          password_encrypted: passwordEnc,
          site_link_encrypted: siteLinkEnc,
          required_perm_level_id: permLevelId,
        }, interactorId);
      } else {
        const newId = await createSubAccount(
          {
            team_id: teamId,
            username_encrypted: usernameEnc,
            email_encrypted: emailEnc,
            password_encrypted: passwordEnc,
            site_link_encrypted: siteLinkEnc,
            required_perm_level_id: permLevelId,
            dek_wrapped: await wrapDek(dekRaw, teamAesKey),
          },
          interactorId
        );
        await Promise.all(selectedCategoryIds.map((categoryId) => createSubAccountCategory(newId, categoryId)));
      }

      onSaved();
    } catch (err) {
      console.error("Error saving sub-account:", err);
      setError("Could not save. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="subaccount-form-overlay" onClick={onClose}>
      <form
        onSubmit={handleSubmit}
        onClick={(e) => e.stopPropagation()}
        className="subaccount-form"
      >
        <h2>{editing ? "Edit entry" : "New entry"}</h2>

        <label>Username</label>
        <input value={username} onChange={(e) => setUsername(e.target.value)} />

        <label>Email</label>
        <input value={email} onChange={(e) => setEmail(e.target.value)} />

        <label>Password</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />

        <label>Site link</label>
        <input value={siteLink} onChange={(e) => setSiteLink(e.target.value)} />

        {permLevels.length > 1 && (
          <>
            <label>Required permission level</label>
            <select value={permLevelId} onChange={(e) => setPermLevelId(e.target.value)}>
              {[...permLevels].sort((a, b) => a.rank - b.rank).map((pl) => (
                <option key={pl.id} value={pl.id}>{pl.name}</option>
              ))}
            </select>
          </>
        )}

        {!editing && categories.length > 0 && (
          <>
            <label>Categories</label>
            <div className="subaccount-form-categories">
              {categories.map((c) => (
                <label key={c.id} className="subaccount-form-category-chip">
                  <input
                    type="checkbox"
                    checked={selectedCategoryIds.includes(c.id)}
                    onChange={(e) =>
                      setSelectedCategoryIds((prev) =>
                        e.target.checked ? [...prev, c.id] : prev.filter((id) => id !== c.id)
                      )
                    }
                  />
                  {c.name}
                </label>
              ))}
            </div>
          </>
        )}

        {error && <p className="subaccount-form-error">{error}</p>}

        <div className="subaccount-form-actions">
          <button type="button" onClick={onClose} disabled={submitting}>Cancel</button>
          <button type="submit" disabled={submitting}>{submitting ? "Saving..." : "Save"}</button>
        </div>
      </form>
    </div>
  );
}
