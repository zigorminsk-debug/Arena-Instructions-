/* Автотест клиентского пути (то же, что делает браузер).
   Проверяет на живом сервере: /api/check -> PBKDF2 -> разворачивание ключа ->
   скачивание content/content.bin -> расшифровка -> совпадение страниц.

   Запуск:  node tools/selftest_client.mjs http://127.0.0.1:8000 user001 ПАРОЛЬ
            node tools/selftest_client.mjs http://127.0.0.1:8000 --owner
            (пароль владельца берётся из private/users_plain.json) */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createHash } from "node:crypto";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.dirname(HERE);
const [base = "http://127.0.0.1:8000", user = "user001", passArg] = process.argv.slice(2);

const plain = JSON.parse(fs.readFileSync(path.join(ROOT, "private", "users_plain.json"), "utf-8"));
const pass = passArg || (user === "--owner" ? plain.users.developer.pass : null);
if (!pass) {
  console.error("укажите логин и пароль: node tools/selftest_client.mjs <url> <логин> <пароль>");
  process.exit(2);
}
const login = user === "--owner" ? "developer" : user;

const b64d = (s) => Uint8Array.from(Buffer.from(s, "base64"));
const enc = new TextEncoder();
const hex = (b) => createHash("sha256").update(b).digest("hex");

const t0 = Date.now();
const res = await fetch(base + "/api/check", {
  method: "POST", headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ user: login, pass })
});
const j = await res.json();
console.log("check:", res.status, JSON.stringify({ ...j, wrapped_ck: j.wrapped_ck && "…", salt_k: j.salt_k && "…" }));
if (!j.ok) { console.error("ОШИБКА: сервер не пустил"); process.exit(1); }

const kekBits = await crypto.subtle.deriveBits(
  { name: "PBKDF2", hash: "SHA-256", salt: b64d(j.salt_k), iterations: j.iter },
  await crypto.subtle.importKey("raw", enc.encode(pass), "PBKDF2", false, ["deriveBits"]), 256);
const kek = await crypto.subtle.importKey("raw", new Uint8Array(kekBits), "AES-GCM", false, ["decrypt"]);
const wrapped = b64d(j.wrapped_ck);
const ckRaw = await crypto.subtle.decrypt(
  { name: "AES-GCM", iv: wrapped.slice(0, 12), additionalData: enc.encode("arena-ck-v1") },
  kek, wrapped.slice(12));
const ck = await crypto.subtle.importKey("raw", ckRaw, "AES-GCM", false, ["decrypt"]);

const bundle = new Uint8Array(await (await fetch(base + "/content/content.bin")).arrayBuffer());
const pt = new Uint8Array(await crypto.subtle.decrypt(
  { name: "AES-GCM", iv: bundle.slice(0, 12), additionalData: enc.encode("arena-bundle-v1") },
  ck, bundle.slice(12)));

const magic = String.fromCharCode(...pt.slice(0, 8));
const n = new DataView(pt.buffer, pt.byteOffset).getUint32(8);
const sizes = []; let off = 12 + 4 * n;
for (let i = 0; i < n; i++) sizes.push(new DataView(pt.buffer, pt.byteOffset).getUint32(12 + 4 * i));
const ours = [];
for (const s of sizes) { ours.push(hex(pt.slice(off, off + s))); off += s; }

const refDir = path.join(ROOT, "private", "pages");
const files = fs.readdirSync(refDir).filter((f) => f.endsWith(".jpg")).sort();
const ref = files.map((f) => hex(fs.readFileSync(path.join(refDir, f))));

const okMagic = magic === "ARENAPG1";
const okCount = n === ref.length;
const okPages = okCount && ours.every((h, i) => h === ref[i]);
console.log(`magic=${magic} страниц=${n}/${ref.length} совпадение=${okPages}`);
console.log(`${okMagic && okPages ? "ТЕСТ ПРОЙДЕН" : "ТЕСТ НЕ ПРОЙДЕН"} за ${Date.now() - t0} мс`);
process.exit(okMagic && okPages ? 0 : 1);
