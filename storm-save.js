/* Versioned web save validation and one-time v3 migration. No storage access in this module. */
(function(root){
'use strict';
const node=typeof module==='object'&&module.exports;
const E=node?require('./storm-engine.js'):root.QuestEngine,L=node?require('./storm-levels.js'):root.QuestLevels;
const count=n=>Number.isInteger(n)&&n>=0&&n<100000;
const fresh=()=>({version:5,contentVersion:1,lang:'en',mode:'engineer',campaigns:Object.fromEntries(L.ids.map(id=>[id,L.newCampaign(id)]))});
function validCampaign(c,mode){
 if(!c||!c.cargo||!c.power||!c.robot)return false;
 const a=c.cargo,p=c.power,r=c.robot,cargo=L.cargoConfig(mode);
 const ids=x=>Array.isArray(x)&&x.every(i=>Number.isInteger(i)&&i>=0&&i<cargo.items.length)&&new Set(x).size===x.length;
 if(!ids(a.load)||!ids(a.delivered)||a.load.some(i=>a.delivered.includes(i))||!Array.isArray(a.trips)||a.trips.length>(cargo.maxTrips??cargo.items.length)||!a.trips.every(ids))return false;
 let delivered=[];
 for(const [i,trip] of a.trips.entries()){
  if(!L.cargoCheck(mode,trip,delivered,i).ok)return false;delivered=delivered.concat(trip);
 }
 if(JSON.stringify(delivered)!==JSON.stringify(a.delivered)||a.done!==(delivered.length===cargo.items.length))return false;
 const cfg=L.powerConfig(mode),locked=[cfg.source,...cfg.targets,...cfg.fixed];
 if(!Array.isArray(p.masks)||p.masks.length!==cfg.n**2||!p.masks.every(v=>Number.isInteger(v)&&v>=0&&v<=15))return false;
 if(!p.masks.every((v,i)=>[0,1,2,3].some(k=>E.turn(cfg.initial[i],k)===v)))return false;
 if(locked.some(i=>p.masks[i]!==cfg.initial[i]))return false;
 if(typeof p.done!=='boolean'||(p.done&&!E.circuit(cfg,p.masks).complete))return false;
 if(!Array.isArray(r.main)||r.main.length>24||!r.main.every(x=>['F','L','R','P','I','Q'].includes(x)))return false;
 if(!Array.isArray(r.body)||r.body.length>12||!r.body.every(x=>['F','L','R','P','I'].includes(x))||![2,3,4].includes(r.repeat))return false;
 // A completion badge records an earlier successful run, even if code was subsequently edited.
 return [a.rejected,a.hints,p.turns,p.tests,p.hints,r.runs,r.stops,r.hints].every(count)&&typeof r.done==='boolean'&&(r.best===null||count(r.best))&&(!r.done||r.best!==null);
}
function valid(state){return !!state&&state.version===5&&state.contentVersion===1&&['en','zh'].includes(state.lang)&&L.ids.includes(state.mode)&&!!state.campaigns&&L.ids.every(id=>validCampaign(state.campaigns[id],id));}
function restore(current,legacy){
 const result=fresh();
 if(current!==null&&current!==undefined){
  if(valid(current))return {state:current,notice:null,writable:true};
  // Preserve future saves and invalid saves; do not silently replace them with an empty campaign.
  return {state:result,notice:'protected',writable:false};
 }
 if(legacy&&legacy.version===3&&['en','zh'].includes(legacy.lang)&&['explorer','engineer'].includes(legacy.mode)&&legacy.campaigns){
  if(['explorer','engineer'].every(id=>validCampaign(legacy.campaigns[id],id))){
   result.lang=legacy.lang;result.mode=legacy.mode;
   for(const id of ['explorer','engineer'])result.campaigns[id]=JSON.parse(JSON.stringify(legacy.campaigns[id]));
   return {state:result,notice:'migrated',writable:true};
  }
  return {state:result,notice:'legacyInvalid',writable:true};
 }
 return {state:result,notice:legacy?'legacyInvalid':null,writable:true};
}
const api={fresh,valid,validCampaign,restore};root.QuestSaves=api;if(node)module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
