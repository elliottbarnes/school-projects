import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { SAMPLE, ANOMALY, simulate, parseReferences, addressParts } from '../demo/core.js';
test('known page fault totals and FIFO anomaly', () => {
  const input = parseReferences(SAMPLE);
  for (const [policy, faults] of [['FIFO', 15], ['LRU', 12], ['OPT', 9]]) assert.equal(simulate(input, 3, policy).at(-1).faults, faults);
  assert.equal(simulate(parseReferences(ANOMALY), 3, 'FIFO').at(-1).faults, 9);
  assert.equal(simulate(parseReferences(ANOMALY), 4, 'FIFO').at(-1).faults, 10);
  assert.equal(simulate([1, 2, 1, 3], 2, 'LRU').at(-1).evicted, 2);
});
test('rejects invalid inputs and handles address boundaries exactly', () => {
  for (const x of ['', '-1', '1.5', '1e3', '10000', Array(41).fill(1).join(' ')]) assert.throws(() => parseReferences(x));
  for (const x of ['-1', '4294967296', '1e3', '<script>', '']) assert.throws(() => addressParts(x));
  assert.deepEqual(addressParts('4294967295'), { address: 4294967295, page: 1048575, offset: 4095 });
  assert.deepEqual(addressParts('4096'), { address: 4096, page: 1, offset: 0 });
  for (const n of [0, -1, 1.1, 11, NaN]) assert.throws(() => simulate([1], n, 'FIFO'));
});
test('native C matches every browser trace row on deterministic inputs', () => {
  const dir = mkdtempSync(join(tmpdir(), 'coursework-test-'));
  try {
    for (const [name, source] of [['address', 'Assignment7/addresses.c'], ['replacement', 'Assignment8/q7.c']]) {
      const result = spawnSync('cc', ['-std=c11', '-Wall', '-Wextra', '-Werror', '-o', join(dir, name), 'projects/c-programming/' + source], { encoding: 'utf8' });
      assert.equal(result.status, 0, result.stderr);
    }
    let seed = 417;
    const random = n => { seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0; return seed % n; };
    const cases = [[3, parseReferences(SAMPLE)], [3, parseReferences(ANOMALY)], [4, parseReferences(ANOMALY)], [1, [0, 0, 1, 1]], [10, [9, 9, 0]]];
    for (let i = 0; i < 25; i++) cases.push([1 + random(10), Array.from({ length: 1 + random(40) }, () => random(15))]);
    for (const [capacity, refs] of cases) {
      const native = spawnSync(join(dir, 'replacement'), [capacity, ...refs].map(String), { encoding: 'utf8', timeout: 2000 });
      assert.equal(native.status, 0, native.stderr);
      for (const policy of ['FIFO', 'LRU', 'OPT']) {
        const rows = native.stdout.split('\n').filter(x => x.startsWith(policy + ' step '));
        const expected = simulate(refs, capacity, policy);
        assert.equal(rows.length, expected.length);
        rows.forEach((row, i) => { const state = expected[i]; assert.equal(row, `${policy} step ${i + 1}: ${state.page} ${state.hit ? 'hit' : 'fault'} | ${state.frames.map(x => x ?? -1).join(' ')}`); });
        assert.ok(native.stdout.includes(`Page Faults (${policy}): ${expected.at(-1).faults}\n`));
      }
    }
    for (const value of ['0', '4095', '4096', '4294967295']) {
      const native = spawnSync(join(dir, 'address'), [value], { encoding: 'utf8' });
      const result = addressParts(value); assert.equal(native.status, 0);
      assert.ok(native.stdout.includes(`Page Number = ${result.page}\nOffset = ${result.offset}`));
    }
    for (const value of ['-1', '4294967296', '1e3', 'x', '']) assert.notEqual(spawnSync(join(dir, 'address'), [value]).status, 0);
    for (const args of [['0'], ['11'], ['3', '-1'], ['3', ...Array(41).fill('1')]]) assert.notEqual(spawnSync(join(dir, 'replacement'), args).status, 0);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});
