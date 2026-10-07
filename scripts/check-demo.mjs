import { readdir, readFile, lstat } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
const entries = await readdir(new URL('../demo/', import.meta.url));
if (!entries.includes('index.html')) throw new Error('Missing demo entry');
for (const name of entries) {
  const path = new URL('../demo/' + name, import.meta.url);
  if (!(await lstat(path)).isFile() || !/^[a-z0-9-]+\.(html|css|js|json|svg)$/.test(name)) throw new Error('Unexpected demo asset: ' + name);
  const bytes = await readFile(path);
  if (!bytes.length || bytes.length > 100_000) throw new Error('Invalid demo asset size: ' + name);
  if (name.endsWith('.js') && spawnSync(process.execPath, ['--check', fileURLToPath(path)]).status !== 0) throw new Error('Invalid JavaScript');
}
console.log('Verified explicit demo artifact:', entries.join(', '));
