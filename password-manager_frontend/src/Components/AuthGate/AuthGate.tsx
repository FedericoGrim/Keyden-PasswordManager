"use client";

import { FormEvent, useEffect, useState } from "react";
import type { UUID } from "crypto";

import { keycloakFactory } from "@/api/keycloakClient";
import { getMainUserByKeycloakId } from "@/api/apis";
import { mainUser } from "@/api/entities/mainUser";
import { provisionUser } from "@/Functions/Provisioning/provisionUser";
import { deriveMasterKey, decrypt, base64ToBytes, ARGON2_PARAMS } from "@/Functions/Cripting-Decripting/Cript-Dectipr";
import { VaultContext, VaultKeys } from "./VaultContext";

type GateState = "loading" | "needsMasterPassword" | "locked" | "ready" | "error";

export default function AuthGate({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<GateState>("loading");
  const [existingUser, setExistingUser] = useState<mainUser | null>(null);
  const [vault, setVault] = useState<VaultKeys | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    const keycloak = keycloakFactory();

    const checkProvisioned = async () => {
      const keycloakId = keycloak.tokenParsed?.sub;
      if (!keycloakId) return;

      try {
        const user = await getMainUserByKeycloakId(keycloakId as UUID);
        if (user) {
          setExistingUser(user);
          setState("locked");
        } else {
          setState("needsMasterPassword");
        }
      } catch (err) {
        console.error("Error checking provisioning status:", err);
        setError("Could not reach the server. Please try again.");
        setState("error");
      }
    };

    if (keycloak.authenticated) {
      checkProvisioned();
    } else {
      keycloak.onAuthSuccess = checkProvisioned;
    }
  }, []);

  const handleSignup = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.currentTarget;
    const masterPassword = (form.elements.namedItem("masterPassword") as HTMLInputElement).value;
    const confirmPassword = (form.elements.namedItem("confirmPassword") as HTMLInputElement).value;

    if (masterPassword !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }
    if (masterPassword.length < 8) {
      setError("Master password must be at least 8 characters.");
      return;
    }

    setError(null);
    setSubmitting(true);
    try {
      const keycloak = keycloakFactory();
      const keycloakId = keycloak.tokenParsed?.sub as string;
      const username =
        (keycloak.tokenParsed?.preferred_username as string) ||
        (keycloak.tokenParsed?.name as string) ||
        keycloakId;

      const provisioned = await provisionUser(keycloakId, username, masterPassword);
      setVault(provisioned);
      setState("ready");
    } catch (err) {
      console.error("Error provisioning user:", err);
      setError("Could not set up your account. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleUnlock = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!existingUser) return;
    const form = e.currentTarget;
    const masterPassword = (form.elements.namedItem("masterPassword") as HTMLInputElement).value;

    setError(null);
    setSubmitting(true);
    try {
      const masterKey = await deriveMasterKey(masterPassword, base64ToBytes(existingUser.salt), ARGON2_PARAMS);
      const privateKeyEc = base64ToBytes(await decrypt(existingUser.private_key_ec, masterKey));
      const privateKeyPq = base64ToBytes(await decrypt(existingUser.private_key_pq, masterKey));

      setVault({ user: existingUser, privateKeyEc, privateKeyPq, masterKey });
      setState("ready");
    } catch (err) {
      console.error("Error unlocking vault:", err);
      setError("Incorrect master password.");
    } finally {
      setSubmitting(false);
    }
  };

  if (state === "loading") {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Loading...</p>
      </div>
    );
  }

  if (state === "error") {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>{error ?? "Something went wrong."}</p>
      </div>
    );
  }

  if (state === "needsMasterPassword") {
    return (
      <div className="min-h-screen bg-[#778da9] text-[#0d1b2a] flex items-center justify-center">
        <form
          onSubmit={handleSignup}
          className="bg-[#e0e1dd] rounded-xl shadow-lg p-8 border border-[#415a77] w-full max-w-sm"
        >
          <h1 className="text-2xl font-bold mb-2">Set your master password</h1>
          <p className="text-[#415a77] mb-6">
            This password encrypts your vault. It is never sent to the server and cannot be recovered if lost.
          </p>

          <label className="block mb-1 text-sm font-medium" htmlFor="masterPassword">
            Master password
          </label>
          <input
            id="masterPassword"
            name="masterPassword"
            type="password"
            required
            className="w-full mb-4 px-3 py-2 rounded border border-[#415a77] bg-white"
          />

          <label className="block mb-1 text-sm font-medium" htmlFor="confirmPassword">
            Confirm master password
          </label>
          <input
            id="confirmPassword"
            name="confirmPassword"
            type="password"
            required
            className="w-full mb-4 px-3 py-2 rounded border border-[#415a77] bg-white"
          />

          {error && <p className="text-red-700 mb-4">{error}</p>}

          <button
            type="submit"
            disabled={submitting}
            className="w-full py-2 rounded bg-[#0d1b2a] text-white font-semibold disabled:opacity-50"
          >
            {submitting ? "Setting up..." : "Continue"}
          </button>
        </form>
      </div>
    );
  }

  if (state === "locked") {
    return (
      <div className="min-h-screen bg-[#778da9] text-[#0d1b2a] flex items-center justify-center">
        <form
          onSubmit={handleUnlock}
          className="bg-[#e0e1dd] rounded-xl shadow-lg p-8 border border-[#415a77] w-full max-w-sm"
        >
          <h1 className="text-2xl font-bold mb-2">Unlock your vault</h1>
          <p className="text-[#415a77] mb-6">Enter your master password to decrypt your vault.</p>

          <label className="block mb-1 text-sm font-medium" htmlFor="masterPassword">
            Master password
          </label>
          <input
            id="masterPassword"
            name="masterPassword"
            type="password"
            required
            autoFocus
            className="w-full mb-4 px-3 py-2 rounded border border-[#415a77] bg-white"
          />

          {error && <p className="text-red-700 mb-4">{error}</p>}

          <button
            type="submit"
            disabled={submitting}
            className="w-full py-2 rounded bg-[#0d1b2a] text-white font-semibold disabled:opacity-50"
          >
            {submitting ? "Unlocking..." : "Unlock"}
          </button>
        </form>
      </div>
    );
  }

  return <VaultContext.Provider value={vault}>{children}</VaultContext.Provider>;
}
