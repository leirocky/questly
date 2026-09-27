/* Questly challenge collection v1. Original six levels still use the unchanged engine. */
(function(root){
'use strict';
const E=typeof module==='object'&&module.exports?require('./storm-engine.js'):root.QuestEngine;
const copy=x=>JSON.parse(JSON.stringify(x));
const catalog=[
 {id:'explorer',en:'First landing',zh:'初次登岛',tag:['Explorer','探索模式'],description:['Learn the three workshops.','认识三座工程站。'],titles:{cargo:['First supplies','第一批物资'],power:['A light in the harbor','港口亮灯'],robot:['Nova’s first route','Nova 初次出发']}},
 {id:'engineer',en:'Island engineer',zh:'小岛工程师',tag:['Engineer','工程师挑战'],description:['Tighter loads, branching wires and a repeat block.','规划载重、连接分支，试试循环。'],titles:{cargo:['Three voyages','三趟运输'],power:['Two stations','双站供电'],robot:['The stairway','阶梯路线']}},
 {id:'tides',en:'Tidal works',zh:'潮汐工坊',tag:['Challenge 1','进阶一'],description:['Link deliveries, split power three ways, finish beyond the loop.','串联运输顺序、三路供电，循环之后继续出发。'],titles:{cargo:['Build in order','按序施工'],power:['Three shore lights','三岸灯塔'],robot:['One more step','循环之外']}},
 {id:'ridge',en:'Ridge expedition',zh:'山脊探险',tag:['Challenge 2','进阶二'],description:['Only three crates fit. Plan junctions and a round trip.','每船最多三箱，规划多路电流与环岛路线。'],titles:{cargo:['A crowded deck','甲板有限'],power:['Ridge junctions','山脊岔路'],robot:['Around the lagoon','环绕潟湖']}},
 {id:'beacon',en:'Beacon network',zh:'灯塔网络',tag:['Challenge 3','进阶三'],description:['A four-stage build and a survey before the return to the lab.','四步建造顺序，巡查完成后返回中心实验室。'],titles:{cargo:['The relay delivery','接力运输'],power:['Across the estuary','河口连网'],robot:['Survey and return','巡查再返航']}},
 {id:'summit',en:'Summit challenge',zh:'巅峰挑战',tag:['Challenge 4','进阶四'],description:['Two dependency chains, a first-trip priority and reusable surveys.','两条建造链、首趟优先物资，复用两次巡查程序。'],titles:{cargo:['Everything has a place','环环相扣'],power:['The summit grid','山顶电网'],robot:['Two research camps','双营地巡查']}}
];
const ids=catalog.map(x=>x.id);
function info(mode){const value=catalog.find(x=>x.id===mode);if(!value)throw Error('Unknown collection');return value;}
function cargoConfig(mode){
 info(mode);
 const items=copy(E.cargo);
 const base={items,capacity:mode==='explorer'?12:10,maxTrips:mode==='explorer'?null:3,maxItems:null,before:[[0,1]],apart:[[2,3]],by:{}};
 if(['explorer','engineer'].includes(mode))return base;
 items.push({id:6,en:'Solar panels',zh:'太阳能板',weight:4,icon:'spark'},{id:7,en:'Tools',zh:'工具箱',weight:1,icon:'book'});
 base.before.push([1,6],[7,2]);
 if(mode==='tides')return base;
 items.push({id:8,en:'Pump',zh:'水泵',weight:5,icon:'sensor'});
 base.before=[[0,1],[1,6],[7,8],[8,3]];
 base.maxItems=3;
 if(mode==='ridge'){base.capacity=13;return base;}
 items.push({id:9,en:'Radio',zh:'电台',weight:3,icon:'bot'});
 base.maxTrips=4;base.before.push([6,9]);base.apart.push([8,9]);
 if(mode==='summit'){base.capacity=11;base.before.push([3,4]);base.by={5:1};}
 return base;
}
function cargoCheck(mode,load,delivered,trips=0){
 const c=cargoConfig(mode),bad=(reason,extra={})=>({ok:false,reason,...extra});
 if(c.maxTrips!==null&&trips>=c.maxTrips)return bad('voyages');
 if(!load.length)return bad('empty');
 if(load.some(i=>!Number.isInteger(i)||i<0||i>=c.items.length)||new Set(load).size!==load.length)return bad('invalid');
 if(load.some(i=>delivered.includes(i)))return bad('unavailable');
 const weight=load.reduce((sum,i)=>sum+c.items[i].weight,0);
 if(weight>c.capacity)return bad('overweight',{weight});
 const missing=c.before.find(([first,next])=>load.includes(next)&&!delivered.includes(first));
 if(missing)return bad(missing[0]===0&&missing[1]===1?'crane':'order',{weight,pair:missing});
 const conflict=c.apart.find(([a,b])=>load.includes(a)&&load.includes(b));
 if(conflict)return bad(conflict[0]===2&&conflict[1]===3?'water':'apart',{weight,pair:conflict});
 if(c.maxItems!==null&&load.length>c.maxItems)return bad('slots',{weight});
 const late=Object.entries(c.by).find(([id,by])=>!delivered.includes(Number(id))&&!load.includes(Number(id))&&trips+1>=by);
 if(late)return bad('priority',{weight,item:Number(late[0])});
 return {ok:true,weight};
}
// Paths describe the solved electrical topology. Player boards contain rotated pieces and decoys.
const circuits={
 tides:{n:6,source:30,targets:[5,11,35],fixed:[21],paths:[[30,24,18,19,20,14,8,2,3,4,5],[20,21,22,16,10,11],[22,28,34,35]],decoys:{1:6,7:10,12:6,13:9,25:6,26:12,31:3,32:9}},
 ridge:{n:6,source:12,targets:[0,5,35,30],fixed:[8,27],paths:[[12,13,14,8,2,1,0],[14,15,16,10,4,5],[16,22,28,34,35],[28,27,26,32,31,30]],decoys:{6:6,7:10,18:6,19:9,21:12,23:5,24:3,25:10,29:9}},
 beacon:{n:7,source:42,targets:[6,20,48,0],fixed:[23,39],paths:[[42,35,28,29,30,23,16,9,2,3,4,5,6],[30,31,32,25,18,19,20],[32,39,46,47,48],[16,15,14,7,0]],decoys:{8:6,10:10,11:12,21:6,22:9,26:5,36:6,37:12,43:3,44:9}},
 summit:{n:7,source:21,targets:[0,6,48,42],fixed:[17,37],paths:[[21,22,23,16,9,2,1,0],[23,24,25,18,11,4,5,6],[25,32,39,46,47,48],[39,38,37,36,35,42],[16,17,18]],decoys:{7:6,8:12,10:5,12:6,13:12,14:3,15:9,19:3,20:9,28:6,29:10,30:12,43:6,44:9,45:5}}
};
function powerConfig(mode){
 info(mode);
 if(!circuits[mode])return {...E.powerConfig(mode),fixed:[]};
 const data=circuits[mode],solution=Array(data.n**2).fill(0);
 for(const path of data.paths)for(let j=1;j<path.length;j++){
  const a=path[j-1],b=path[j],ar=Math.floor(a/data.n),ac=a%data.n,br=Math.floor(b/data.n),bc=b%data.n;
  const direction=E.directions.findIndex(([dr,dc])=>ar+dr===br&&ac+dc===bc);
  if(direction<0)throw Error('Nonadjacent authored circuit edge');
  solution[a]|=1<<direction;solution[b]|=1<<((direction+2)%4);
 }
 for(const [i,mask] of Object.entries(data.decoys)){
  if(solution[i])throw Error('Decoy overlaps circuit');solution[i]=mask;
 }
 const locked=[data.source,...data.targets,...data.fixed];
 const initial=solution.map((mask,i)=>locked.includes(i)?mask:E.turn(mask,(i*7+2)%3+1));
 return {n:data.n,source:data.source,targets:copy(data.targets),fixed:copy(data.fixed),initial,solution};
}
function perimeter(top,left,side){
 const road=[];
 for(let i=0;i<=side;i++)for(const p of [[top,left+i],[top+side,left+i],[top+i,left],[top+i,left+side]])if(!road.some(x=>x[0]===p[0]&&x[1]===p[1]))road.push(p);
 return road;
}
function robotConfig(mode){
 info(mode);
 if(mode==='explorer'||mode==='engineer')return E.robotConfig(mode);
 if(mode==='tides')return {n:8,start:[7,0,1],goal:[0,6],samples:[[5,2],[3,4],[1,6]],road:[[7,0],[7,1],[7,2],[6,2],[5,2],[5,3],[5,4],[4,4],[3,4],[3,5],[3,6],[2,6],[1,6],[0,6]],budget:10};
 if(mode==='ridge')return {n:7,start:[6,0,1],goal:[6,0],samples:[[6,6],[0,6],[0,0],[6,0]],road:perimeter(0,0,6),budget:9};
 if(mode==='beacon')return {n:7,start:[6,0,1],goal:[3,3],samples:[[6,3],[6,6],[3,6],[0,6],[0,3],[0,0],[3,0],[6,0]],road:[...perimeter(0,0,6),[3,1],[3,2],[3,3]],budget:18};
 return {n:9,start:[8,0,1],goal:[4,5],samples:[[8,3],[5,3],[5,0],[8,0],[8,8],[5,8],[5,5],[8,5]],road:[...perimeter(5,0,3),...perimeter(5,5,3),[8,4],[4,5]],budget:17};
}
function newCampaign(mode){const campaign=E.newCampaign(mode);campaign.power.masks=powerConfig(mode).initial;return campaign;}
const api={version:1,catalog,ids,info,cargoConfig,cargoCheck,powerConfig,robotConfig,newCampaign};
root.QuestLevels=api;
if(typeof module==='object'&&module.exports)module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
