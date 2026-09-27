const assert=require('node:assert/strict');
const fs=require('node:fs');
const crypto=require('node:crypto');
const path=require('node:path');
const E=require('../storm-engine.js'),L=require('../storm-levels.js'),S=require('../storm-save.js');
const results=[],solutions={};
function test(name,run){run();results.push({name,status:'PASS'});}
// This search uses authored constraints directly, never L.cargoCheck to select a move.
function searchCargo(cfg){
 const all=(1<<cfg.items.length)-1,queue=[{mask:0,trips:[]}],seen=new Set(['0:0']);
 const candidates=[];
 for(let mask=1;mask<=all;mask++){
  const ids=cfg.items.filter(x=>mask&(1<<x.id)).map(x=>x.id);
  if(ids.reduce((n,id)=>n+cfg.items[id].weight,0)>cfg.capacity)continue;
  if(cfg.maxItems&&ids.length>cfg.maxItems)continue;
  if(cfg.apart.some(([a,b])=>ids.includes(a)&&ids.includes(b)))continue;
  candidates.push({mask,ids});
 }
 for(let at=0;at<queue.length;at++){
  const state=queue[at];if(state.mask===all)return state.trips;
  if(cfg.maxTrips&&state.trips.length>=cfg.maxTrips)continue;
  for(const cargo of candidates){
   if(cargo.mask&state.mask)continue;
   if(cfg.before.some(([a,b])=>(cargo.mask&(1<<b))&&!(state.mask&(1<<a))))continue;
   if(Object.entries(cfg.by).some(([id,by])=>state.trips.length+1>=by&&!((state.mask|cargo.mask)&(1<<Number(id)))))continue;
   const next={mask:state.mask|cargo.mask,trips:[...state.trips,cargo.ids]},key=next.mask+':'+next.trips.length;
   if(!seen.has(key)){seen.add(key);queue.push(next);}
  }
 }
 return null;
}
function independentCircuit(config,masks){
 const seen=new Set([config.source]),queue=[config.source];
 while(queue.length){
  const id=queue.shift(),r=Math.floor(id/config.n),c=id%config.n;
  for(const [dr,dc,bit,opposite] of [[-1,0,1,4],[0,1,2,8],[1,0,4,1],[0,-1,8,2]]){
   const nr=r+dr,nc=c+dc;if(nr<0||nr>=config.n||nc<0||nc>=config.n)continue;
   const neighbor=nr*config.n+nc;
   if((masks[id]&bit)&&(masks[neighbor]&opposite)&&!seen.has(neighbor)){seen.add(neighbor);queue.push(neighbor);}
  }
 }
 return config.targets.every(id=>seen.has(id));
}
const robotPrograms={
 explorer:{main:['F','F','L','F','F','P'],body:[],repeat:2},
 engineer:{main:['Q'],body:['F','F','I','F','F','P','R'],repeat:2},
 tides:{main:['Q','L','F'],body:['F','F','L','F','F','P','R'],repeat:3},
 ridge:{main:['Q'],body:['F','F','F','F','F','F','P','L'],repeat:4},
 beacon:{main:['Q','L','F','F','F','R','F','F','F'],body:['F','F','F','P','F','F','F','P','L'],repeat:4},
 summit:{main:['Q','F','F','F','F','F','Q','L','F','F','F','F'],body:['F','F','F','P','L'],repeat:4}
};
function independentRobot(cfg,program){
 let [r,c,d]=cfg.start;const bag=new Set(),road=new Set(cfg.road.map(x=>x.join(','))),samples=new Set(cfg.samples.map(x=>x.join(',')));
 const flat=program.main.flatMap(x=>x==='Q'?Array.from({length:program.repeat},()=>program.body).flat():[x]);
 for(const op of flat){
  const dr=[-1,0,1,0][d],dc=[0,1,0,-1][d],ahead=road.has([r+dr,c+dc].join(','));
  if(op==='F'){if(!ahead)return false;r+=dr;c+=dc;}
  if(op==='L'||op==='I'&&!ahead)d=(d+3)%4;
  if(op==='R')d=(d+1)%4;
  if(op==='P'){const key=[r,c].join(',');if(!samples.has(key)||bag.has(key))return false;bag.add(key);}
 }
 return r===cfg.goal[0]&&c===cfg.goal[1]&&bag.size===samples.size;
}
function run(){
 test('18 independently selectable missions, stable IDs and isolated initial state',()=>{
  assert.equal(L.ids.length*3,18);assert.equal(new Set(L.ids).size,6);
 const state=S.fresh();assert.ok(S.valid(state));
  state.campaigns.tides.cargo.load.push(7);assert.deepEqual(state.campaigns.ridge.cargo.load,[]);
 });
 test('Original six configurations and 8,192 cargo acceptance/rejection cases match the unchanged engine',()=>{
  for(const mode of ['explorer','engineer']){
   const cfg=L.cargoConfig(mode),{fixed,...power}=L.powerConfig(mode);
   assert.deepEqual(cfg.items,E.cargo);assert.deepEqual(power,E.powerConfig(mode));assert.deepEqual(L.robotConfig(mode),E.robotConfig(mode));
   for(let loadMask=0;loadMask<64;loadMask++)for(let deliveredMask=0;deliveredMask<64;deliveredMask++){
    const load=E.cargo.filter(x=>loadMask&(1<<x.id)).map(x=>x.id),delivered=E.cargo.filter(x=>deliveredMask&(1<<x.id)).map(x=>x.id);
    const original=E.cargoCheck(load,delivered,cfg.capacity),actual=L.cargoCheck(mode,load,delivered,0);
    assert.equal(actual.ok,original.ok);assert.equal(actual.reason,original.reason);assert.equal(actual.weight,original.weight);
   }
  }
 });
 for(const mode of L.ids){
  test(`${mode}: independent cargo BFS finds a legal solution within its voyage limit`,()=>{
   const config=L.cargoConfig(mode),trips=searchCargo(config);assert.ok(trips);let delivered=[];
   trips.forEach((load,index)=>{assert.equal(L.cargoCheck(mode,load,delivered,index).ok,true);delivered.push(...load);});
   assert.equal(delivered.length,config.items.length);
   solutions[mode]={cargo:trips};
  });
  test(`${mode}: circuit starts unsolved; a rotation-reachable solution independently powers every target`,()=>{
   const cfg=L.powerConfig(mode);assert.equal(independentCircuit(cfg,cfg.initial),false);
   assert.equal(independentCircuit(cfg,cfg.solution),true);assert.equal(E.circuit(cfg,cfg.solution).complete,true);
   cfg.solution.forEach((mask,id)=>assert.ok([0,1,2,3].some(turns=>E.turn(cfg.initial[id],turns)===mask)));
   for(const id of [cfg.source,...cfg.targets,...cfg.fixed])assert.equal(cfg.initial[id],cfg.solution[id]);
   solutions[mode].power=cfg.solution;
  });
  test(`${mode}: independent robot interpreter verifies the authored loop plan and optional block target`,()=>{
   const cfg=L.robotConfig(mode),p=robotPrograms[mode];assert.equal(independentRobot(cfg,p),true);
   const result=E.simulate(cfg,p.main,p.body,p.repeat);assert.equal(result.ok,true);assert.equal(result.efficient,true);
   const slow={...p,main:['L','R',...p.main]};assert.equal(independentRobot(cfg,slow),true);
   assert.equal(E.simulate(cfg,slow.main,slow.body,slow.repeat).ok,true);
   solutions[mode].robot=p;
  });
 }
 test('New cargo precedence, deck slots, priority and trip budget reject without time pressure',()=>{
  assert.equal(L.cargoCheck('tides',[6],[0],1).reason,'order');
  assert.equal(L.cargoCheck('ridge',[2,4,5,7],[],0).reason,'slots');
  assert.equal(L.cargoCheck('summit',[0,7],[],0).reason,'priority');
  assert.equal(L.cargoCheck('summit',[0,7,5],[],0).ok,true);
  assert.equal(L.cargoCheck('beacon',[4],[],4).reason,'voyages');
  assert.equal(L.cargoCheck('tides',[7,7],[],0).reason,'invalid');
 });
 test('All displayed cargo hint plans satisfy the independently authored constraints',()=>{
  const hints={tides:[[0,7,4],[1,2],[3,5,6]],ridge:[[0,7,2],[1,8,5],[3,4,6]],beacon:[[0,7,5],[1,2],[6,8],[9,3,4]],summit:[[0,7,5],[1,8],[6,3],[9,4,2]]};
  for(const [mode,trips] of Object.entries(hints)){let delivered=[];trips.forEach((load,i)=>{assert.equal(L.cargoCheck(mode,load,delivered,i).ok,true,mode);delivered.push(...load);});assert.equal(delivered.length,L.cargoConfig(mode).items.length);}
 });
 test('Legacy migration preserves original six mission states without mutating the input',()=>{
  const old={version:3,lang:'zh',mode:'engineer',campaigns:{explorer:E.newCampaign('explorer'),engineer:E.newCampaign('engineer')}};
  old.campaigns.engineer.cargo.load=[0,3];
  old.campaigns.explorer.power.masks=E.powerConfig('explorer').solution;old.campaigns.explorer.power.done=true;
  const before=JSON.stringify(old),result=S.restore(null,old);
  assert.equal(result.notice,'migrated');assert.ok(S.valid(result.state));
  assert.deepEqual(result.state.campaigns.engineer,old.campaigns.engineer);
  assert.deepEqual(result.state.campaigns.explorer,old.campaigns.explorer);
  result.state.campaigns.engineer.cargo.load=[];assert.equal(JSON.stringify(old),before);
 });
 test('All 18 completed states survive JSON roundtrip; clearing one mission leaves the other 17 intact',()=>{
  const state=S.fresh();
  for(const mode of L.ids){const c=state.campaigns[mode],answer=solutions[mode];c.cargo.trips=answer.cargo;c.cargo.delivered=answer.cargo.flat();c.cargo.done=true;c.power.masks=answer.power;c.power.done=true;Object.assign(c.robot,answer.robot,{done:true,best:E.codeSize(answer.robot.main,answer.robot.body)});}
  assert.ok(S.valid(state));const restored=S.restore(JSON.parse(JSON.stringify(state)),null).state;assert.deepEqual(restored,state);
  restored.campaigns.summit.cargo=L.newCampaign('summit').cargo;
  assert.equal(L.ids.reduce((n,id)=>n+['cargo','power','robot'].filter(stage=>restored.campaigns[id][stage].done).length,0),17);
 });
 test('Malformed/future saves are preserved and cannot silently overwrite valid legacy progress',()=>{
  for(const broken of [{version:99},{invalid:true},{...S.fresh(),contentVersion:2}])assert.equal(S.restore(broken,null).writable,false);
  const state=S.fresh();state.campaigns.summit.cargo.trips=[[0]];state.campaigns.summit.cargo.delivered=[0];
  assert.equal(S.valid(state),false);assert.equal(S.restore(state,null).writable,false);
  assert.equal(S.restore(null,{version:3}).notice,'legacyInvalid');
 });
 test('Fixed circuit pieces and impossible cargo histories cannot be loaded',()=>{
  const state=S.fresh(),cfg=L.powerConfig('summit');
  state.campaigns.summit.power.masks[cfg.fixed[0]]=0;assert.equal(S.valid(state),false);
  const bad=S.fresh();bad.campaigns.tides.cargo.trips=[[1]];bad.campaigns.tides.cargo.delivered=[1];assert.equal(S.valid(bad),false);
 });
 const files=['index.html','storm-engine.js','storm-levels.js','storm-save.js','storm-app.js','storm.css','storm-visual.js','storm-visual.css'];
 const hashes=Object.fromEntries(files.map(name=>[name,crypto.createHash('sha256').update(fs.readFileSync(path.join(__dirname,'..',name))).digest('hex')]));
 const report={testedAt:new Date().toISOString(),environment:process.version,scope:'Node rules/content/migration tests; no browser or device claim',results,solutions,hashes};
 console.log(JSON.stringify(report,null,2));return report;
}
if(require.main===module)run();
module.exports={run,robotPrograms,searchCargo,independentCircuit,independentRobot};
