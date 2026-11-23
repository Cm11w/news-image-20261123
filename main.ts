// main.ts — entrypoint for the news-image-20261123 make.fun entry.
// Takes the generated newspaper image (entry.png) sitting beside this
// script and drops a copy into the grading output directory.
// Node 22, standard library only.

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const imagePath = join(scriptDir, "entry.png");

if (!existsSync(imagePath)) {
  console.error(`error: entry.png is missing from ${scriptDir}`);
  process.exit(1);
}

const targetDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(targetDir, { recursive: true });

const targetPath = resolve(join(targetDir, "entry.png"));
copyFileSync(imagePath, targetPath);
console.log(`entry.png copied to ${targetPath}`);
