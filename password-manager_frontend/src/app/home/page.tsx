"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Poppins } from "next/font/google";

import { useVault } from "@/Components/AuthGate/VaultContext";
import {
  getTeamsByUserId,
  getUserTeamsKeysByUserId,
  getFavoritesByUserId,
  addFavorite,
  removeFavorite,
  getSubAccountById,
  getSubAccountsByTeamId,
  getAllTeamPermLevelsByTeamId,
  getCategoriesByTeamId,
} from "@/api/apis";
import { team } from "@/api/entities/team";
import { teamPermLevel } from "@/api/entities/teamPermLevel";
import { category } from "@/api/entities/category";
import { unwrapTeamKey, importAesKey, decryptSubAccountFields } from "@/Functions/Cripting-Decripting/Cript-Dectipr";
import SubAccountForm, { DecryptedSubAccount } from "../teams/[teamId]/page-components/subAccountForm/subAccountForm";

import "./styles.css";
import "./page-components/favMenu/favMenu.css";
import "./page-components/menu/menu.css";
import "./home-extra.css";

const poppins = Poppins({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
  display: "swap",
});

const FAV_PER_PAGE = 3;
const GRID_PER_PAGE = 6;

type FavoriteCard = DecryptedSubAccount & { teamId: string };

export default function Home() {
  const vault = useVault();

  // team-key cache shared by the favorites column (many teams) and the
  // right panel (one team at a time) — unwrapped only once per team_id.
  const teamKeyCache = useRef<Map<string, CryptoKey>>(new Map());
  const userTeamsKeysRef = useRef<{ team_id: string; team_key_encrypted: string }[]>([]);

  const getTeamAesKey = useCallback(
    async (teamId: string): Promise<CryptoKey | null> => {
      const cached = teamKeyCache.current.get(teamId);
      if (cached) return cached;

      const match = userTeamsKeysRef.current.find((k) => k.team_id === teamId);
      if (!match) return null;

      const raw = await unwrapTeamKey(match.team_key_encrypted, vault.privateKeyEc, vault.privateKeyPq);
      const aesKey = await importAesKey(raw);
      teamKeyCache.current.set(teamId, aesKey);
      return aesKey;
    },
    [vault]
  );

  const [teams, setTeams] = useState<team[]>([]);
  const [selectedTeamId, setSelectedTeamId] = useState<string | null>(null);

  const [favoriteIds, setFavoriteIds] = useState<Set<string>>(new Set());
  const [favoriteCards, setFavoriteCards] = useState<FavoriteCard[]>([]);
  const [favPage, setFavPage] = useState(1);

  const [gridAccounts, setGridAccounts] = useState<DecryptedSubAccount[]>([]);
  const [permLevels, setPermLevels] = useState<teamPermLevel[]>([]);
  const [categories, setCategories] = useState<category[]>([]);
  const [searchText, setSearchText] = useState("");
  const [gridPage, setGridPage] = useState(1);
  const [formTarget, setFormTarget] = useState<DecryptedSubAccount | "new" | null>(null);

  const loadFavorites = useCallback(async () => {
    const favorites = await getFavoritesByUserId(vault.user.id);
    setFavoriteIds(new Set(favorites.map((f) => f.sub_account_id)));

    const cards = await Promise.all(
      favorites.map(async (f) => {
        const sa = await getSubAccountById(f.sub_account_id);
        if (!sa) return null;
        const aesKey = await getTeamAesKey(sa.team_id);
        if (!aesKey) return null;
        return {
          id: sa.id,
          teamId: sa.team_id,
          ...(await decryptSubAccountFields(sa, aesKey)),
          requiredPermLevelId: sa.required_perm_level_id,
          dekWrapped: sa.dek_wrapped,
        } as FavoriteCard;
      })
    );
    setFavoriteCards(cards.filter((c): c is FavoriteCard => c !== null));
  }, [vault.user.id, getTeamAesKey]);

  const loadGrid = useCallback(
    async (teamId: string) => {
      const aesKey = await getTeamAesKey(teamId);
      if (!aesKey) return;
      const raw = await getSubAccountsByTeamId(teamId);
      const decrypted = await Promise.all(
        raw.map(async (sa) => ({
          id: sa.id,
          ...(await decryptSubAccountFields(sa, aesKey)),
          requiredPermLevelId: sa.required_perm_level_id,
          dekWrapped: sa.dek_wrapped,
        }))
      );
      setGridAccounts(decrypted);
      setGridPage(1);
    },
    [getTeamAesKey]
  );

  // Initial load: teams (for the dropdown), this user's wrapped keys (cache
  // source), and favorites (which may reference any of those teams).
  useEffect(() => {
    getTeamsByUserId(vault.user.id).then((fetchedTeams) => {
      setTeams(fetchedTeams);
      const personal = fetchedTeams.find((t) => t.is_personal);
      setSelectedTeamId((personal ?? fetchedTeams[0])?.id ?? null);
    });
    getUserTeamsKeysByUserId(vault.user.id).then((keys) => {
      userTeamsKeysRef.current = keys;
      loadFavorites();
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [vault.user.id]);

  useEffect(() => {
    if (selectedTeamId) {
      // loadGrid sets state, but only after awaiting the network/crypto work
      // below — this is the standard "fetch when a dependency changes"
      // effect, not a synchronous setState-in-render.
      // eslint-disable-next-line react-hooks/set-state-in-effect
      loadGrid(selectedTeamId);
      getAllTeamPermLevelsByTeamId(selectedTeamId).then(setPermLevels);
      getCategoriesByTeamId(selectedTeamId).then(setCategories);
    }
  }, [selectedTeamId, loadGrid]);

  const toggleFavorite = async (subAccountId: string) => {
    if (favoriteIds.has(subAccountId)) {
      await removeFavorite(vault.user.id, subAccountId);
    } else {
      await addFavorite(vault.user.id, subAccountId);
    }
    await loadFavorites();
  };

  const filteredGrid = useMemo(
    () =>
      gridAccounts.filter((a) =>
        `${a.username} ${a.email} ${a.siteLink}`.toLowerCase().includes(searchText.toLowerCase())
      ),
    [gridAccounts, searchText]
  );

  const favTotalPages = Math.max(1, Math.ceil(favoriteCards.length / FAV_PER_PAGE));
  const visibleFavs = favoriteCards.slice((favPage - 1) * FAV_PER_PAGE, favPage * FAV_PER_PAGE);

  const gridTotalPages = Math.max(1, Math.ceil(filteredGrid.length / GRID_PER_PAGE));
  const visibleGrid = filteredGrid.slice((gridPage - 1) * GRID_PER_PAGE, gridPage * GRID_PER_PAGE);

  return (
    <main className="main-layout">
      <section className="content-area">
        <div className="column-fav">
          <h1 className={`title ${poppins.className}`}>KEYDEN</h1>

          <div className="fav-container">
            <div className="fav-grid">
              {visibleFavs.length === 0 && <p className="empty-state">No favorites yet.</p>}
              {visibleFavs.map((f) => (
                <button key={f.id} className="fav-card" onClick={() => setSelectedTeamId(f.teamId)}>
                  {f.username || f.email || "(untitled)"}
                  <span
                    className="fav-card-unfav"
                    onClick={(e) => {
                      e.stopPropagation();
                      toggleFavorite(f.id);
                    }}
                  >
                    ✕
                  </span>
                </button>
              ))}
            </div>

            <div className="fav-pagination">
              <button className="pagination-arrow" onClick={() => setFavPage((p) => Math.max(1, p - 1))} disabled={favPage === 1}>‹</button>
              {Array.from({ length: favTotalPages }, (_, i) => i + 1).map((p) => (
                <button key={p} className={`pagination-page ${p === favPage ? "active" : ""}`} onClick={() => setFavPage(p)}>{p}</button>
              ))}
              <button className="pagination-arrow" onClick={() => setFavPage((p) => Math.min(favTotalPages, p + 1))} disabled={favPage === favTotalPages}>›</button>
            </div>
          </div>
        </div>

        <div className="divider"></div>

        <div className="column-menu">
          <div className="grid-container">
            <div className="grid-toolbar">
              <button className="add-btn" onClick={() => setFormTarget("new")}>ADD</button>
            </div>

            <div className="grid-search">
              <select
                className="team-select"
                value={selectedTeamId ?? ""}
                onChange={(e) => setSelectedTeamId(e.target.value)}
              >
                {teams.map((t) => (
                  <option key={t.id} value={t.id}>{t.name}</option>
                ))}
              </select>
              <input
                type="text"
                placeholder="SEARCH..."
                value={searchText}
                onChange={(e) => {
                  setSearchText(e.target.value);
                  setGridPage(1);
                }}
              />
              <button className="filter-btn" title="Filters coming soon">⏷</button>
            </div>

            <div className="grid">
              {visibleGrid.length === 0 && <p className="empty-state">No entries yet.</p>}
              {visibleGrid.map((a) => (
                <button key={a.id} className="grid-card" onClick={() => setFormTarget(a)}>
                  {a.username || a.email || "(untitled)"}
                  <span
                    className={`grid-card-star ${favoriteIds.has(a.id) ? "" : "inactive"}`}
                    onClick={(e) => {
                      e.stopPropagation();
                      toggleFavorite(a.id);
                    }}
                  >
                    ★
                  </span>
                </button>
              ))}
            </div>

            <div className="grid-pagination">
              <button className="pagination-arrow" onClick={() => setGridPage((p) => Math.max(1, p - 1))} disabled={gridPage === 1}>‹</button>
              {Array.from({ length: gridTotalPages }, (_, i) => i + 1).map((p) => (
                <button key={p} className={`pagination-page ${p === gridPage ? "active" : ""}`} onClick={() => setGridPage(p)}>{p}</button>
              ))}
              <button className="pagination-arrow" onClick={() => setGridPage((p) => Math.min(gridTotalPages, p + 1))} disabled={gridPage === gridTotalPages}>›</button>
            </div>
          </div>
        </div>
      </section>

      {formTarget && selectedTeamId && (
        <SubAccountForm
          teamId={selectedTeamId}
          // teamKeyCache is a plain out-of-React cache keyed by team id, already
          // populated (awaited) by loadGrid before the form can be opened —
          // reading it here is a synchronous lookup, not a mutation read race.
          // eslint-disable-next-line react-hooks/refs
          teamAesKey={teamKeyCache.current.get(selectedTeamId)!}
          interactorId={vault.user.id}
          permLevels={permLevels}
          categories={categories}
          editing={formTarget === "new" ? null : formTarget}
          onClose={() => setFormTarget(null)}
          onSaved={() => {
            setFormTarget(null);
            loadGrid(selectedTeamId);
          }}
        />
      )}
    </main>
  );
}
