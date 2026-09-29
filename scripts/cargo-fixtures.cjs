// Run with node. The shipped JS engine remains read-only.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const E = require('../storm-engine.js');
const root = path.resolve(__dirname, '..');
const cases = [];
const ids = bits => E.cargo.filter((_, i) => bits & (1 << i)).map(x => x.id);
for (const capacity of [10, 12]) {
  for (let delivered = 0; delivered < 64; delivered++) {
    for (let load = 0; load < 64; load++) {
      const input = {load: ids(load), delivered: ids(delivered), capacity};
      cases.push({...input, expected: E.cargoCheck(input.load, input.delivered, capacity)});
    }
  }
  for (const load of [[0, 0], [-1], [6], [1, 0], [3, 2], [999], [0, 0, 1]]) {
    cases.push({load, delivered: [], capacity, expected: E.cargoCheck(load, [], capacity)});
  }
}
const report = {reference: 'storm-engine.js', sha256: crypto.createHash('sha256').update(fs.readFileSync(path.join(root, 'storm-engine.js'))).digest('hex'), cases};
const fixture = JSON.stringify(report) + '\n';
const content = fs.readFileSync(path.join(root, 'content/cargo-v1.json'));
const catalog = JSON.parse(content);
if (JSON.stringify(catalog.items.map(({id,en,zh,weight}) => ({id,en,zh,weight}))) !== JSON.stringify(E.cargo.map(({id,en,zh,weight}) => ({id,en,zh,weight})))) throw Error('Cargo content differs from JS');
const files = [
  ['fixtures/cargo-contract.json', fixture],
  ['packages/QuestCore/Sources/QuestCore/Resources/cargo-v1.json', content]
];
for (const [file, data] of files) {
  const target = path.join(root, file);
  if (process.argv.includes('--check')) {
    if (!fs.existsSync(target) || !Buffer.from(data).equals(fs.readFileSync(target))) throw Error(`Stale generated file: ${file}`);
  } else fs.writeFileSync(target, data);
}
console.log(`${process.argv.includes('--check') ? 'Verified' : 'Generated'} ${cases.length} JS cargo cases and bundled content.`);
