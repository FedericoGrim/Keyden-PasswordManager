// Plain "argon2-browser" ships a WASM-loader entry that Turbopack/webpack
// can't resolve (dynamic "WASM_PATH"/"fs" imports); the bundled build inlines
// the WASM as base64 instead, so use that entry point for bundler compat.
import argon2 from "argon2-browser/dist/argon2-bundled.min.js";
import { createMlKem768 } from "mlkem";

const enc = new TextEncoder();
const dec = new TextDecoder();

// OWASP-recommended Argon2id defaults (19 MiB memory, 2 iterations, 1 thread).
// Single source of truth: signup (provisionUser.ts) and unlock (AuthGate.tsx)
// must derive the same key from the same password+salt, or every returning
// user's private keys become permanently undecryptable.
export const ARGON2_PARAMS = { m: 19456, t: 2, p: 1 };

export async function deriveMasterKey(
  masterPassword: string,
  salt: Uint8Array,
  parametri: { m: number; t: number; p: number }
): Promise<CryptoKey> {
  const { hash } = await argon2.hash({
    pass: masterPassword,
    salt,
    type: argon2.ArgonType.Argon2id,
    mem: parametri.m,
    time: parametri.t,
    parallelism: parametri.p,
    hashLen: 32,
  });
  return crypto.subtle.importKey("raw", hash, "AES-GCM", false, ["encrypt", "decrypt"]);
}

export async function encrypt(dato: string, chiave: CryptoKey): Promise<string> {
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const cifrato = await crypto.subtle.encrypt({ name: "AES-GCM", iv }, chiave, enc.encode(dato));
  const payload = new Uint8Array(iv.length + cifrato.byteLength);
  payload.set(iv);
  payload.set(new Uint8Array(cifrato), iv.length);
  return btoa(String.fromCharCode(...payload));
}

export async function decrypt(payloadB64: string, chiave: CryptoKey): Promise<string> {
  const payload = Uint8Array.from(atob(payloadB64), (c) => c.charCodeAt(0));
  const iv = payload.subarray(0, 12);
  const cifrato = payload.subarray(12);
  const chiaro = await crypto.subtle.decrypt({ name: "AES-GCM", iv }, chiave, cifrato);
  return dec.decode(chiaro);
}

export function generateSalt(): Uint8Array {
  return crypto.getRandomValues(new Uint8Array(16));
}

export function bytesToBase64(bytes: Uint8Array): string {
  return btoa(String.fromCharCode(...bytes));
}

export function base64ToBytes(b64: string): Uint8Array {
  return Uint8Array.from(atob(b64), (c) => c.charCodeAt(0));
}

export function importAesKey(raw: Uint8Array): Promise<CryptoKey> {
  return crypto.subtle.importKey("raw", raw, "AES-GCM", false, ["encrypt", "decrypt"]);
}

// Envelope encryption for sub-account rows: each row has its own random data
// key (DEK, same shape as a team key — generateSymmetricTeamKey() doubles as
// the generator), wrapped with the team's AES key. Rotating the team key
// only needs to re-wrap these small blobs, never the row's ciphertext.
export async function wrapDek(dekRaw: Uint8Array, teamKey: CryptoKey): Promise<string> {
  return encrypt(bytesToBase64(dekRaw), teamKey);
}

export async function unwrapDek(dekWrapped: string, teamKey: CryptoKey): Promise<Uint8Array> {
  return base64ToBytes(await decrypt(dekWrapped, teamKey));
}

// Shared by every screen that lists sub-accounts: unwrap the row's DEK with
// the team key, then decrypt its four fields with that DEK.
export async function decryptSubAccountFields(
  sa: { username_encrypted: string; email_encrypted: string; password_encrypted: string; site_link_encrypted: string; dek_wrapped: string },
  teamKey: CryptoKey
): Promise<{ username: string; email: string; password: string; siteLink: string }> {
  const dek = await importAesKey(await unwrapDek(sa.dek_wrapped, teamKey));
  const [username, email, password, siteLink] = await Promise.all([
    decrypt(sa.username_encrypted, dek),
    decrypt(sa.email_encrypted, dek),
    decrypt(sa.password_encrypted, dek),
    decrypt(sa.site_link_encrypted, dek),
  ]);
  return { username, email, password, siteLink };
}

// EC keypair (ECDH P-256), used for key-wrapping (not signing).
export async function generateEcKeyPair(): Promise<{ publicKey: Uint8Array; privateKey: Uint8Array }> {
  const keyPair = await crypto.subtle.generateKey({ name: "ECDH", namedCurve: "P-256" }, true, ["deriveBits"]);
  const publicKey = new Uint8Array(await crypto.subtle.exportKey("raw", keyPair.publicKey));
  const privateKey = new Uint8Array(await crypto.subtle.exportKey("pkcs8", keyPair.privateKey));
  return { publicKey, privateKey };
}

// Post-quantum ML-KEM-768 keypair, used for key-wrapping (not signing).
export async function generatePqKeyPair(): Promise<{ publicKey: Uint8Array; privateKey: Uint8Array }> {
  const kem = await createMlKem768();
  const [publicKey, privateKey] = kem.generateKeyPair();
  return { publicKey, privateKey };
}

export function generateSymmetricTeamKey(): Uint8Array {
  return crypto.getRandomValues(new Uint8Array(32));
}

const TEAM_KEY_WRAP_VERSION = 1;
const HKDF_INFO = new TextEncoder().encode("keyden-team-key-wrap");

async function deriveWrapKey(ecdhSharedBits: ArrayBuffer, mlkemSharedSecret: Uint8Array): Promise<CryptoKey> {
  const combined = new Uint8Array(ecdhSharedBits.byteLength + mlkemSharedSecret.byteLength);
  combined.set(new Uint8Array(ecdhSharedBits), 0);
  combined.set(mlkemSharedSecret, ecdhSharedBits.byteLength);

  const hkdfKey = await crypto.subtle.importKey("raw", combined, "HKDF", false, ["deriveKey"]);
  return crypto.subtle.deriveKey(
    { name: "HKDF", hash: "SHA-256", salt: new Uint8Array(0), info: HKDF_INFO },
    hkdfKey,
    { name: "AES-GCM", length: 256 },
    false,
    ["encrypt", "decrypt"]
  );
}

function packWrappedTeamKey(ephemeralPublicKey: Uint8Array, kemCiphertext: Uint8Array, iv: Uint8Array, ciphertext: Uint8Array): string {
  const header = new Uint8Array(5);
  header[0] = TEAM_KEY_WRAP_VERSION;
  new DataView(header.buffer).setUint16(1, ephemeralPublicKey.length, false);
  new DataView(header.buffer).setUint16(3, kemCiphertext.length, false);

  const payload = new Uint8Array(header.length + ephemeralPublicKey.length + kemCiphertext.length + iv.length + ciphertext.length);
  let offset = 0;
  payload.set(header, offset); offset += header.length;
  payload.set(ephemeralPublicKey, offset); offset += ephemeralPublicKey.length;
  payload.set(kemCiphertext, offset); offset += kemCiphertext.length;
  payload.set(iv, offset); offset += iv.length;
  payload.set(ciphertext, offset);

  return bytesToBase64(payload);
}

function unpackWrappedTeamKey(payloadB64: string) {
  const payload = base64ToBytes(payloadB64);
  const view = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
  const version = payload[0];
  if (version !== TEAM_KEY_WRAP_VERSION) throw new Error(`Unsupported team key wrap version: ${version}`);
  const ephPubLen = view.getUint16(1, false);
  const kemCtLen = view.getUint16(3, false);

  let offset = 5;
  const ephemeralPublicKey = payload.slice(offset, offset + ephPubLen); offset += ephPubLen;
  const kemCiphertext = payload.slice(offset, offset + kemCtLen); offset += kemCtLen;
  const iv = payload.slice(offset, offset + 12); offset += 12;
  const ciphertext = payload.slice(offset);

  return { ephemeralPublicKey, kemCiphertext, iv, ciphertext };
}

// Hybrid EC+PQ wrap of a raw symmetric key (e.g. a team key), so only the
// holder of the matching EC+PQ private keys can unwrap it.
export async function wrapTeamKey(
  teamKeyRaw: Uint8Array,
  recipientPublicKeyEc: Uint8Array,
  recipientPublicKeyPq: Uint8Array
): Promise<string> {
  const ephemeralKeyPair = await crypto.subtle.generateKey({ name: "ECDH", namedCurve: "P-256" }, true, ["deriveBits"]);
  const recipientEcKey = await crypto.subtle.importKey("raw", recipientPublicKeyEc, { name: "ECDH", namedCurve: "P-256" }, false, []);
  const ecdhSharedBits = await crypto.subtle.deriveBits({ name: "ECDH", public: recipientEcKey }, ephemeralKeyPair.privateKey, 256);

  const kem = await createMlKem768();
  const [kemCiphertext, mlkemSharedSecret] = await kem.encap(recipientPublicKeyPq);

  const wrapKey = await deriveWrapKey(ecdhSharedBits, mlkemSharedSecret);

  const iv = crypto.getRandomValues(new Uint8Array(12));
  const ciphertext = new Uint8Array(await crypto.subtle.encrypt({ name: "AES-GCM", iv }, wrapKey, teamKeyRaw));

  const ephemeralPublicKey = new Uint8Array(await crypto.subtle.exportKey("raw", ephemeralKeyPair.publicKey));
  return packWrappedTeamKey(ephemeralPublicKey, kemCiphertext, iv, ciphertext);
}

// Inverse of wrapTeamKey: recovers the raw team key using this user's EC+PQ private keys.
export async function unwrapTeamKey(
  wrappedB64: string,
  privateKeyEc: Uint8Array,
  privateKeyPq: Uint8Array
): Promise<Uint8Array> {
  const { ephemeralPublicKey, kemCiphertext, iv, ciphertext } = unpackWrappedTeamKey(wrappedB64);

  const ecPrivateKey = await crypto.subtle.importKey("pkcs8", privateKeyEc, { name: "ECDH", namedCurve: "P-256" }, false, ["deriveBits"]);
  const ephemeralEcKey = await crypto.subtle.importKey("raw", ephemeralPublicKey, { name: "ECDH", namedCurve: "P-256" }, false, []);
  const ecdhSharedBits = await crypto.subtle.deriveBits({ name: "ECDH", public: ephemeralEcKey }, ecPrivateKey, 256);

  const kem = await createMlKem768();
  const mlkemSharedSecret = await kem.decap(kemCiphertext, privateKeyPq);

  const wrapKey = await deriveWrapKey(ecdhSharedBits, mlkemSharedSecret);
  return new Uint8Array(await crypto.subtle.decrypt({ name: "AES-GCM", iv }, wrapKey, ciphertext));
}