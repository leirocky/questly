const assert=require('node:assert/strict');
const E=require('../storm-engine.js');
const results=[];
function test(name,fn){fn();results.push({name,status:'PASS'});}
test('Cargo: no empty, invalid or duplicate loads',()=>{
 assert.equal(E.cargoCheck([],[],10).reason,'empty');
 assert.equal(E.cargoCheck([0,0],[],10).reason,'invalid');
 assert.equal(E.cargoCheck([9],[],10).reason,'invalid');
});
test('Cargo: weight, arrival precedence, battery/water and delivered guard',()=>{
 assert.equal(E.cargoCheck([0,2],[],10).reason,'overweight');
 assert.equal(E.cargoCheck([1],[],10).reason,'crane');
 assert.equal(E.cargoCheck([2,3],[],10).reason,'water');
 assert.equal(E.cargoCheck([0],[0],10).reason,'unavailable');
 assert.equal(E.cargoCheck([1,2],[0],10).ok,true);
});
function searchCargo(cap){let queue=[{delivered:[],trips:[]}],seen=new Set(['']);for(let k=0;k<queue.length;k++){let x=queue[k];if(x.delivered.length===6)return x.trips;for(let bits=1;bits<64;bits++){let load=E.cargo.filter((_,i)=>bits&(1<<i)).map(v=>v.id);if(!E.cargoCheck(load,x.delivered,cap).ok)continue;let d=x.delivered.concat(load),key=d.slice().sort().join(',');if(!seen.has(key)){seen.add(key);queue.push({delivered:d,trips:x.trips.concat([load])});}}}return null;}
test('Cargo: exhaustive search finds 3-trip engineer and 2-trip explorer solutions',()=>{
 assert.equal(searchCargo(10).length,3);assert.equal(searchCargo(12).length,2);
});
test('Circuit: all 16 bit masks return after four turns',()=>{for(let mask=0;mask<16;mask++)assert.equal(E.turn(mask,4),mask);});
test('Circuit: both puzzles start unsolved and have a rotation-reachable solution',()=>{
 for(const mode of ['explorer','engineer']){const cfg=E.powerConfig(mode);assert.equal(E.circuit(cfg,cfg.initial).complete,false);assert.equal(E.circuit(cfg,cfg.solution).complete,true);cfg.solution.forEach((v,i)=>assert.ok([0,1,2,3].some(n=>E.turn(cfg.initial[i],n)===v)));}
});
test('Circuit: adjacency alone does not conduct; boundary never wraps',()=>{
 assert.deepEqual(E.circuit({n:2,source:1,targets:[2]},[0,2,8,0]).reached,[1]);
 assert.equal(E.circuit({n:2,source:0,targets:[1]},[2,2,0,0]).complete,false);
});
test('Circuit: closed loops terminate',()=>{assert.equal(E.circuit({n:2,source:0,targets:[3]},[6,12,3,9]).reached.length,4);});
test('Robot: missing code, empty loop and invalid repeat are safe',()=>{
 const cfg=E.robotConfig('engineer');assert.equal(E.simulate(cfg,[],[],2).reason,'noCode');assert.equal(E.simulate(cfg,['Q'],[],2).reason,'emptyLoop');assert.equal(E.simulate(cfg,['Q'],['F'],100).reason,'tooLong');
});
test('Robot: collision and missing pickup are distinguished',()=>{
 const c=E.robotConfig('explorer');assert.equal(E.simulate(c,['F','F','F'],[],2).reason,'wall');assert.equal(E.simulate(c,['P'],[],2).reason,'noSample');assert.equal(E.simulate(c,['F','F','L','F','F'],[],2).reason,'missing');
});
test('Robot: conditional turns only when front is blocked',()=>{
 const c=E.robotConfig('explorer');assert.equal(E.simulate(c,['I'],[],2).trace[0].d,1);assert.equal(E.simulate(c,['F','F','I'],[],2).trace[2].d,0);
});
test('Robot: explorer route solves with six commands',()=>{
 const r=E.simulate(E.robotConfig('explorer'),['F','F','L','F','F','P'],[],2);assert.equal(r.ok,true);assert.equal(r.blocks,6);assert.equal(r.efficient,true);
});
test('Robot: engineer repeat-and-condition route solves within 8 blocks',()=>{
 const r=E.simulate(E.robotConfig('engineer'),['Q'],['F','F','I','F','F','P','R'],2);assert.equal(r.ok,true);assert.equal(r.blocks,8);assert.equal(r.trace.length,14);assert.equal(r.efficient,true);assert.equal(r.trace.at(-1).bag.length,2);
});
test('Robot: an over-budget correct solution is still accepted',()=>{
 const r=E.simulate(E.robotConfig('engineer'),['F','F','L','F','F','P','R','F','F','L','F','F','P'],[],2);assert.equal(r.ok,true);assert.equal(r.efficient,false);
});
test('Campaign instances do not share mutable arrays',()=>{const a=E.newCampaign('engineer'),b=E.newCampaign('engineer');a.cargo.load.push(0);assert.deepEqual(b.cargo.load,[]);});
console.log(JSON.stringify({results,solutions:{engineer:searchCargo(10),explorer:searchCargo(12)}},null,2));
