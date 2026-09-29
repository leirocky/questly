/* Deterministic offline authoring tool. Commits static data; no random puzzles at runtime. */
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const E=require('../storm-engine');
const p=(main,body='',times=2)=>({main:main.split(''),body:body.split(''),repeat:times});
const chapters=[['Harbor apprentice','港湾学徒'],['Coastal planner','海岸规划师'],['Tidal workshop','潮汐工坊'],['Ridge expedition','山脊探险'],['Beacon network','灯塔网络'],['Island master','全岛总工程师']];
const titles=[
 ['harbor','Room on board','留一点船位','Jetty light','码头灯光','Two seed stops','两次采样'],
 ['cove','Balance the boat','平衡运输','Cove cable','海湾电缆','Turn at the cove','海湾转弯'],
 ['garden','Garden supplies','花园补给','Garden lamps','花园灯串','Garden zigzag','花园折线'],
 ['quay','Last crate','最后一箱','Quay junction','码头分岔','Return to the jetty','返回码头'],
 ['orchard','Orchard order','果园顺序','Orchard split','果园分流','Short stairs','短阶梯'],
 ['canal','Canal convoy','运河船队','Canal crossing','运河交汇','Wide stairs','宽阶梯'],
 ['cliff','Cliff crane','悬崖起重机','Cliff relays','崖边接点','Narrow ascent','窄路攀登'],
 ['bridge','Bridge builders','搭桥工队','Bridge lights','桥头灯光','Three landings','三段平台'],
 ['marsh','Marsh pump','湿地水泵','Marsh branches','湿地支路','Small survey','小环巡查'],
 ['delta','Delta deliveries','三角洲运送','Delta network','三角洲网络','Long rectangle','长方形巡查'],
 ['grove','Grove relay','林地接力','Grove stations','林间站点','Two sides at once','两边一组'],
 ['inlet','Inlet priority','海口优先','Inlet switches','海口转接','Survey checkpoints','沿途采样'],
 ['terrace','Terrace sequence','梯田工序','Terrace current','梯田电流','Survey then dock','巡查后停靠'],
 ['ravine','Ravine deck','峡谷甲板','Ravine forks','峡谷分岔','Return to the center','回到中心'],
 ['plateau','Plateau relay','高原接力','Plateau grid','高原电网','Samples on every side','每边都采样'],
 ['waterfall','Waterfall works','瀑布工程','Waterfall lights','瀑布灯网','The side laboratory','侧边实验室'],
 ['observatory','Observatory cargo','观测台补给','Observatory link','观测台连线','Twin outposts','双前哨巡查'],
 ['estuary','Estuary schedule','河口调度','Estuary relays','河口接力','Wide twin camps','宽营地巡查'],
 ['lighthouse','Lighthouse chain','灯塔建造链','Lighthouse mesh','灯塔联通','Two rectangular camps','双矩形营地'],
 ['reservoir','Reservoir plan','水库规划','Reservoir branches','水库分支','Return from two camps','双营地返航'],
 ['citadel','Citadel convoy','堡垒船队','Citadel power','堡垒电路','Survey and climb','巡查再攀登'],
 ['aurora','Aurora expedition','极光远征','Aurora network','极光网络','Conditional corners','条件转弯'],
 ['horizon','Horizon logistics','天际调度','Horizon current','天际电流','Two surveys and a detour','双巡查与绕行'],
 ['islandheart','Island lifeline','全岛生命线','Island power web','全岛电网','The final sample','最后的样本']
];
// Each tuple authors cargo size, capacity slack, deck slots, precedence pattern and deadline.
const specs=[
 [6,2,null,0,0],[6,1,3,0,0],[6,0,3,1,0],[7,1,3,1,0],
 [7,0,3,2,0],[8,1,3,2,0],[8,0,3,3,0],[8,0,3,3,1],
 [9,1,3,3,0],[9,0,3,4,0],[9,0,3,4,1],[9,0,3,5,1],
 [10,1,3,4,0],[10,0,3,5,0],[10,0,3,5,1],[10,0,3,6,1],
 [11,1,3,5,1],[11,0,3,6,1],[11,0,3,7,1],[11,0,3,7,2],
 [12,1,3,6,1],[12,0,3,7,1],[12,0,3,8,2],[12,0,3,9,2]
];
const items=[...E.cargo,{id:6,en:'Solar panels',zh:'太阳能板',weight:4,icon:'spark'},{id:7,en:'Tools',zh:'工具箱',weight:1,icon:'book'},{id:8,en:'Pump',zh:'水泵',weight:5,icon:'sensor'},{id:9,en:'Radio',zh:'电台',weight:3,icon:'bot'},{id:10,en:'Cable',zh:'电缆',weight:2,icon:'bolt'},{id:11,en:'Antenna',zh:'天线',weight:4,icon:'sensor'}];
function cargo(i){
 const [n,slack,slots,pattern,priority]=specs[i];
 const goods=items.slice(0,n).map(x=>({...x}));
 // Named parcels have explicitly versioned, visible weights; patterns vary packing as well as order.
 if(i%4===1)goods[4].weight=3;
 if(i%4===2)goods[2].weight=5;
 if(i%4===3)goods[5].weight=3;
 let plan=n===6?[[0,3],[1,2],[4,5]]:n===7?[[0,3],[1,4],[6,2,5]]:n===8?[[0,7,5],[1,2],[6,3,4]]:n===9?[[0,7,2],[1,8,5],[3,4,6]]:n===10?[[0,7,5],[1,8],[6,3],[9,4,2]]:n===11?[[0,7,5],[1,8,10],[6,3],[9,4,2]]:[[0,7,5],[1,8],[6,3,11],[9,10],[4,2]];
 const before=[[0,1]],apart=[[2,3]],by={};
 if(pattern>=1)before.push([0,4]);
 if(pattern>=2)before.push([1,6]);
 if(pattern>=3&&n>=9)before.push([7,8],[8,3]);
 else if(pattern>=3)before.push([7,2]);
 if(pattern>=4)before.push([1,3]);
 if(pattern>=5&&n>=10)before.push([6,9]);
 if(pattern>=6)before.push([3,4]);
 if(pattern>=7)before.push([7,10]);
 if(pattern>=8)before.push([11,10]);
 if(pattern>=9)before.push([3,10],[10,4],[6,2]);
 if(n>=10)apart.push([8,9]);
 if(pattern>=7)apart.push([2,10]);
 if(pattern>=7&&n>11)apart.push([6,9]);
 if(priority)by[n===9?2:5]=1;
 if(priority===2)by[8]=2;
 const capacity=Math.max(...plan.map(load=>load.reduce((s,id)=>s+goods[id].weight,0)))+slack;
 return {config:{items:goods,capacity,maxTrips:plan.length+(i===0?1:0),maxItems:slots,before,apart,by},plan};
}
const recipes=[
 p('FFPLFFP'),p('FFLFP RFFP'.replaceAll(' ','')),p('FFLFP RFFLFP'.replaceAll(' ','')),p('FFFP LLFFFRFFP'.replaceAll(' ','')),
 p('Q','FLFPR',2),p('QLF','FFLFFPR',2),p('Q','FLFFPR',3),p('QLFP','FFLFPR',3),
 p('Q','FFPL',4),p('Q','FFFPLFFPL',2),p('Q','FFFFPLFPL',2),p('Q','FPFFPL',4),
 p('QLFRFP','FFFPL',4),p('QLFFRFFP','FFFFPL',4),p('QLFRFFP','FFPFFPL',4),p('QLFFRFP','FFFFFPL',4),
 p('QFFFFQ','FFPL',4),p('QFFFFFQ','FFFPL',4),p('QFFFFFQ','FFFPLFFPL',2),p('QFFFFQ LFRFP'.replaceAll(' ',''),'FFPL',4),
 p('QFFFFFQLFFFFP','FFFPL',4),p('Q','FFPFFFPL',4),p('QFFFFFQLFRFFP','FFFPLFFPL',2),p('QFFFFQ LFFRFP'.replaceAll(' ',''),'FFPLFFFPL',2)
];
function robot(index){
 const code=JSON.parse(JSON.stringify(recipes[index]));
 let r=0,c=0,d=1;const road=new Map([['0,0',[0,0]]]),samples=[];
 const flat=code.main.flatMap(op=>op==='Q'?Array(code.repeat).fill(code.body).flat():[op]);
 for(const op of flat){
  if(op==='F'){r+=E.directions[d][0];c+=E.directions[d][1];road.set([r,c].join(','),[r,c]);}
  if(op==='L')d=(d+3)%4;if(op==='R')d=(d+1)%4;
  if(op==='P'){assert(!samples.some(p=>p[0]===r&&p[1]===c),'duplicate sample '+index);samples.push([r,c]);}
 }
 const cells=[...road.values()],minR=Math.min(...cells.map(p=>p[0])),minC=Math.min(...cells.map(p=>p[1]));
 const shift=p=>[p[0]-minR,p[1]-minC],shifted=cells.map(shift);
 const config={n:Math.max(5,...shifted.flat().map(x=>x+1)),start:[-minR,-minC,1],goal:shift([r,c]),samples:samples.map(shift),road:shifted,budget:E.codeSize(code.main,code.body)};
 if(index===21){code.body=code.body.map(op=>op==='L'?'I':op);assert(E.simulate(config,code.main,code.body,code.repeat).ok);}
 assert(config.n<=9);assert(E.simulate(config,code.main,code.body,code.repeat).ok,'robot '+index);
 return {config,code};
}
function rng(seed){return ()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296;};}
function circuit(i){
 const chapter=Math.floor(i/4),n=[4,5,6,6,7,8][chapter],random=rng(901+i*173),source=Math.floor(n/2)*n;
 const targetSets=[[n-1],[n-1,n*n-1],[0,n-1,n*n-1],[0,n-1,n*n-1,n*(n-1)],[0,n-1,n*n-1,n*(n-1)],[0,n-1,n*n-1,n*(n-1),Math.floor(n/2)*n+n-1]];
 const targets=targetSets[chapter],parents=new Map([[source,null]]),front=[source];
 // Randomized growth creates reproducible authored branching networks; prune unused branches.
 while(front.length){
  const pick=Math.floor(random()*front.length),a=front[pick],r=Math.floor(a/n),c=a%n;
  const next=E.directions.map(([dr,dc])=>[r+dr,c+dc]).filter(([r,c])=>r>=0&&r<n&&c>=0&&c<n).map(([r,c])=>r*n+c).filter(b=>!parents.has(b));
  if(!next.length){front.splice(pick,1);continue;}
  const b=next[Math.floor(random()*next.length)];parents.set(b,a);front.push(b);
 }
 const solution=Array(n*n).fill(0);
 for(const target of targets){let b=target;while(parents.get(b)!==null){const a=parents.get(b),dr=Math.floor(b/n)-Math.floor(a/n),dc=b%n-a%n,dir=E.directions.findIndex(v=>v[0]===dr&&v[1]===dc);solution[a]|=1<<dir;solution[b]|=1<<((dir+2)%4);b=a;}}
 const fixed=solution.map((mask,id)=>({mask,id})).filter(({mask,id})=>mask&&id!==source&&!targets.includes(id)).filter((_,j)=>j%7===3).slice(0,Math.max(0,chapter-1)).map(x=>x.id);
 for(let id=0;id<solution.length;id++)if(!solution[id]&&random()<.15+chapter*.065)solution[id]=[3,5,6,10,12][Math.floor(random()*5)];
 const locked=[source,...targets,...fixed];let initial;
 do{initial=solution.map((mask,id)=>locked.includes(id)?mask:E.turn(mask,1+Math.floor(random()*3)));}while(E.circuit({n,source,targets},initial).complete);
 return {n,source,targets,fixed,initial,solution};
}
const levels={},witnesses={};
for(let i=0;i<24;i++){
 const [id,...names]=titles[i],cg=cargo(i),rb=robot(i),chapter=Math.floor(i/4);
 for(const pair of cg.config.apart)assert.equal(pair.length,2);
 levels[id]={info:{id,en:names[0],zh:names[1],tag:chapters[chapter],description:[`Chapter ${chapter+1}: plan, test and revise. Every mission has an optional hint.`,`第 ${chapter+1} 章：规划、测试、改进。每关都有可选提示。`],titles:{cargo:names.slice(0,2),power:names.slice(2,4),robot:names.slice(4,6)}},cargo:cg.config,power:circuit(i),robot:rb.config,hints:{cargo:cg.plan,robot:rb.code}};
 witnesses[id]=rb.code;
}
const root=path.resolve(__dirname,'..');
const output='/* Static, versioned web content. Reproduce: node scripts/build-web-content.cjs */\n(function(root){\nconst data='+JSON.stringify({version:2,chapters,levels},null,1)+';\nroot.QuestContent=data;if(typeof module!==\'undefined\'&&module.exports)module.exports=data;\n})(typeof window!==\'undefined\'?window:globalThis);\n';
if(process.argv.includes('--check'))assert.equal(fs.readFileSync(path.join(root,'storm-content.js'),'utf8'),output);
else fs.writeFileSync(path.join(root,'storm-content.js'),output);
console.log('24 new collections authored deterministically; all robot witnesses execute.');
