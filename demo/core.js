export const SAMPLE = '7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1';
export const ANOMALY = '1 2 3 4 1 2 5 1 2 3 4 5';
export function parseReferences(text) {
  const tokens = text.trim().split(/[\s,]+/);
  if (!text.trim() || tokens.length > 40 || tokens.some(x => !/^\d{1,4}$/.test(x))) throw new Error('Enter 1–40 page numbers from 0 to 9999, separated by spaces or commas.');
  return tokens.map(Number);
}
export function addressParts(text) {
  if (!/^\d{1,10}$/.test(text) || Number(text) > 0xffffffff) throw new Error('Use a decimal address from 0 to 4294967295.');
  const address = Number(text);
  return { address, page: Math.floor(address / 4096), offset: address % 4096 };
}
export function simulate(references, capacity, policy) {
  if (!Number.isInteger(capacity) || capacity < 1 || capacity > 10 || !['FIFO', 'LRU', 'OPT'].includes(policy)) throw new Error('Choose 1–10 frames and a supported policy.');
  if (!Array.isArray(references) || !references.length || references.length > 40 || references.some(x => !Number.isInteger(x) || x < 0 || x > 9999)) throw new Error('Invalid references.');
  const frames = [], usedAt = []; let cursor = 0, faults = 0;
  return references.map((page, index) => {
    let slot = frames.indexOf(page), evicted = null;
    const hit = slot >= 0;
    if (!hit) {
      faults++;
      if (frames.length < capacity) slot = frames.length;
      else {
        if (policy === 'FIFO') { slot = cursor; cursor = (cursor + 1) % capacity; }
        if (policy === 'LRU') slot = usedAt.indexOf(Math.min(...usedAt));
        if (policy === 'OPT') {
          const nextUses = frames.map(value => { const next = references.indexOf(value, index + 1); return next < 0 ? Infinity : next; });
          slot = nextUses.indexOf(Math.max(...nextUses));
        }
        evicted = frames[slot];
      }
      frames[slot] = page;
    }
    usedAt[slot] = index;
    return { step: index + 1, page, hit, faults, evicted, slot, frames: Array.from({ length: capacity }, (_, i) => frames[i] ?? null) };
  });
}
