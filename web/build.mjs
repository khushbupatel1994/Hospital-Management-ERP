import { cpSync, mkdirSync, rmSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname);
const source = resolve(root, "public");
const output = resolve(root, "dist");
const apiBaseUrl = (process.env.ERP_API_URL || "").replace(/\/+$/, "");

rmSync(output, { recursive: true, force: true });
mkdirSync(output, { recursive: true });
cpSync(source, output, { recursive: true });
writeFileSync(
  resolve(output, "config.js"),
  `window.ERP_CONFIG = ${JSON.stringify({ apiBaseUrl })};\n`,
  "utf8",
);

console.log(`Built Hospital ERP web client. API: ${apiBaseUrl || "same-origin"}`);
