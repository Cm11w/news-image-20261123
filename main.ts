// main.ts — entry point for the news-image-20261123 make.fun entry.
// Copies entry.png (sitting next to this file) into MAKEFUN_OUTPUT_DIR
// (default /output). Node 22, stdlib only.

import { copyFileSync, mkdirSync, existsSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");

if (!existsSync(source)) {
  console.error(`entry.png not found next to main.ts (${here})`);
  process.exit(1);
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });

const dest = join(resolve(outDir), "entry.png");
copyFileSync(source, dest);
console.log(`copied entry.png -> ${dest}`);
