// Entry point for the news-image-20261126 make.fun entry.
//
// Reads the rendered front page (entry.png) sitting next to this file,
// sanity-checks that it really is a PNG and small enough to submit,
// then copies it into the output directory the harness provides.
import { copyFile, mkdir, readFile, stat } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1024 * 1024;
const IMAGE_NAME = "entry.png";

function fail(message: string): never {
  console.error(`error: ${message}`);
  process.exit(1);
}

async function main(): Promise<void> {
  const here = dirname(fileURLToPath(import.meta.url));
  const sourcePath = join(here, IMAGE_NAME);

  let info;
  try {
    info = await stat(sourcePath);
  } catch {
    fail(`could not find ${IMAGE_NAME} next to main.ts (${sourcePath})`);
  }

  if (!info.isFile()) {
    fail(`${IMAGE_NAME} exists but is not a regular file`);
  }
  const bytes = await readFile(sourcePath);
  if (bytes.length === 0) {
    fail(`${IMAGE_NAME} is empty (0 bytes)`);
  }
  if (bytes.length > MAX_BYTES) {
    fail(
      `${IMAGE_NAME} is ${bytes.length} bytes, over the 1 MiB limit (${MAX_BYTES} bytes)`
    );
  }
  if (!bytes.subarray(0, PNG_SIGNATURE.length).equals(PNG_SIGNATURE)) {
    fail(`${IMAGE_NAME} does not start with the PNG magic bytes — not a valid PNG file`);
  }

  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  await mkdir(outDir, { recursive: true });
  const targetPath = join(outDir, IMAGE_NAME);
  await copyFile(sourcePath, targetPath);
  console.log(`copied ${IMAGE_NAME} (${info.size} bytes) -> ${targetPath}`);
}

await main();
