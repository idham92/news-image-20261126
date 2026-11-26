import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");

// Validate before copying: entry.png must be a real PNG (magic bytes)
// and at most 1 MiB, so a bad or oversized file fails loudly here.
const bytes = readFileSync(src);
const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (bytes.length < 8 || !bytes.subarray(0, 8).equals(pngMagic)) {
  throw new Error("entry.png is not a valid PNG file");
}
const MAX_BYTES = 1024 * 1024;
if (bytes.length > MAX_BYTES) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}
copyFileSync(src, join(outDir, "entry.png"));
