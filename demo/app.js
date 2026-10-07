import { SAMPLE, ANOMALY, parseReferences, simulate, addressParts } from './core.js';
const $ = id => document.getElementById(id);
let steps = [], current = 0;
const explanations = { FIFO: 'Evict the page loaded earliest. A hit does not change the queue.', LRU: 'Evict the page whose most recent use is furthest in the past.', OPT: 'Evict the page whose next use is furthest in the future. This is a hindsight benchmark, not an online strategy.' };
function show() {
  const row = steps[current]; if (!row) return;
  $('step-label').textContent = `Reference ${row.step} / ${steps.length}: page ${row.page} — ${row.hit ? 'hit' : 'fault'}${row.evicted === null ? '' : `; evict page ${row.evicted}`}`;
  $('frames').replaceChildren(...row.frames.map((page, i) => { const el = document.createElement('span'); el.className = 'frame' + (i === row.slot ? ' changed' : ''); el.textContent = page ?? '—'; return el; }));
  $('progress').textContent = `${row.faults} fault${row.faults === 1 ? '' : 's'} so far`;
  $('previous').disabled = current === 0; $('next').disabled = current === steps.length - 1;
  document.querySelectorAll('#trace tr').forEach((tr, i) => tr.classList.toggle('selected', i === current));
}
function run() {
  try {
    const refs = parseReferences($('references').value), capacity = Number($('capacity').value), policy = $('policy').value;
    steps = simulate(refs, capacity, policy); current = 0;
    $('error').textContent = ''; $('explanation').textContent = explanations[policy];
    for (const p of ['FIFO', 'LRU', 'OPT']) $(p.toLowerCase() + '-count').textContent = simulate(refs, capacity, p).at(-1).faults;
    $('trace').replaceChildren(...steps.map(row => { const tr = document.createElement('tr'); for (const value of [row.step, row.page, row.hit ? 'Hit' : 'Fault', row.frames.map(x => x ?? '—').join(' · '), row.faults]) { const td = document.createElement('td'); td.textContent = value; tr.append(td); } return tr; }));
    $('result').hidden = false; show();
  } catch (e) { $('error').textContent = e.message; $('result').hidden = true; }
}
$('simulate').addEventListener('submit', e => { e.preventDefault(); run(); });
$('previous').addEventListener('click', () => { if (current > 0) current--; show(); });
$('next').addEventListener('click', () => { if (current < steps.length - 1) current++; show(); });
$('reset').addEventListener('click', () => { current = 0; show(); });
$('finish').addEventListener('click', () => { current = steps.length - 1; show(); });
$('anomaly').addEventListener('click', () => { $('references').value = ANOMALY; $('capacity').value = '3'; $('policy').value = 'FIFO'; run(); });
$('address-form').addEventListener('submit', e => { e.preventDefault(); try { const r = addressParts($('address').value); $('address-result').textContent = `Page ${r.page} · offset ${r.offset}. ${r.page} × 4096 + ${r.offset} = ${r.address}.`; } catch (error) { $('address-result').textContent = error.message; } });
for (const id of ['references', 'capacity', 'policy']) $(id).addEventListener('input', () => { $('result').hidden = true; $('error').textContent = 'Inputs changed. Run the simulation to update results.'; });
$('references').value = SAMPLE; run(); $('address-form').requestSubmit();
