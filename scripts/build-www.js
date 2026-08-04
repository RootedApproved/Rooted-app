#!/usr/bin/env node
/**
 * ROOTED — stage the web app for Capacitor.
 *
 * Capacitor requires a directory containing a lowercase `index.html`. The website
 * lives as `Index.html` at the repo root and is served from there by Netlify, so
 * nothing about that can move. This script copies what the mobile shell needs into
 * `www/`, which is generated, gitignored, and never touched by hand.
 *
 * The website is the source of truth. `www/` is a build artifact. If they ever
 * disagree, delete `www/` and re-run this.
 *
 *   npm run build:www
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'www');

// Everything the app shell needs at runtime. Product data and listings live inside
// Index.html itself, so this list stays short by design.
const FILES = ['manifest.webmanifest', 'sw.js'];
const DIRS = ['icons'];

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const s = path.join(src, entry.name);
    const d = path.join(dest, entry.name);
    entry.isDirectory() ? copyDir(s, d) : fs.copyFileSync(s, d);
  }
}

function main() {
  const source = path.join(ROOT, 'Index.html');
  if (!fs.existsSync(source)) {
    console.error('ERROR: Index.html not found at repo root. Nothing to build.');
    process.exit(1);
  }

  // Rebuild from scratch every time so a deleted source file can never linger in www/.
  fs.rmSync(OUT, { recursive: true, force: true });
  fs.mkdirSync(OUT, { recursive: true });

  // Capacitor looks for a lowercase index.html specifically.
  fs.copyFileSync(source, path.join(OUT, 'index.html'));

  let copied = 1;
  for (const f of FILES) {
    const s = path.join(ROOT, f);
    if (fs.existsSync(s)) { fs.copyFileSync(s, path.join(OUT, f)); copied++; }
    else console.warn('  (skipped, not found: ' + f + ')');
  }
  for (const d of DIRS) {
    const s = path.join(ROOT, d);
    if (fs.existsSync(s)) { copyDir(s, path.join(OUT, d)); copied++; }
    else console.warn('  (skipped, not found: ' + d + ')');
  }

  const bytes = fs.statSync(path.join(OUT, 'index.html')).size;
  console.log('ROOTED: staged ' + copied + ' items into www/');
  console.log('  index.html  ' + (bytes / 1048576).toFixed(2) + ' MB');
}

main();
