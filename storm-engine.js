/* Questly Storm Island v0.3 — deterministic game rules, no network or AI. */
(function (root) {
  'use strict';
  const cargo = [
    {id:0, en:'Crane', zh:'起重机', weight:7, icon:'crane'},
    {id:1, en:'Beams', zh:'木梁', weight:6, icon:'beams'},
    {id:2, en:'Battery', zh:'电池', weight:4, icon:'bolt'},
    {id:3, en:'Water', zh:'清水', weight:3, icon:'drop'},
    {id:4, en:'Seeds', zh:'种子', weight:2, icon:'leaf'},
    {id:5, en:'Medicine', zh:'药箱', weight:2, icon:'medical'}
  ];
  const directions = [[-1,0],[0,1],[1,0],[0,-1]];
  const rotate = mask => ((mask << 1) & 15) | ((mask >> 3) & 1);
  function turn(mask, n) { for(let i=0;i<n;i++) mask=rotate(mask); return mask; }
  function powerConfig(mode) {
    const hard=mode==='engineer', n=hard?5:4;
    const solved=hard ? {0:6,1:10,2:12,4:4,7:6,8:10,9:9,10:2,11:10,12:13,13:5,14:9,17:3,18:10,19:12,23:3,24:1}
      : {0:6,1:12,2:6,3:8,4:5,6:5,8:2,9:10,10:9,12:3,13:10,15:9};
    const source=hard?10:8, targets=hard?[4,24]:[3];
    const initial=Array(n*n).fill(0), solution=initial.slice();
    Object.keys(solved).forEach(key=>{const i=Number(key); solution[i]=solved[i]; initial[i]=(i===source||targets.includes(i))?solved[i]:turn(solved[i],i%3+1);});
    return {n,source,targets,initial,solution};
  }
  function circuit(config,masks) {
    const reached=new Set([config.source]), queue=[config.source];
    for(let at=0;at<queue.length;at++){
      const i=queue[at], r=Math.floor(i/config.n), c=i%config.n;
      directions.forEach(([dr,dc],d)=>{
        if(!(masks[i] & (1<<d)))return;
        const nr=r+dr,nc=c+dc;
        if(nr<0||nc<0||nr>=config.n||nc>=config.n)return;
        const j=nr*config.n+nc;
        if((masks[j] & (1<<((d+2)%4)))&&!reached.has(j)){reached.add(j);queue.push(j);}
      });
    }
    return {reached:Array.from(reached),lit:config.targets.filter(i=>reached.has(i)),complete:config.targets.every(i=>reached.has(i))};
  }
  function cargoCheck(load,delivered,capacity) {
    if(!load.length)return {ok:false,reason:'empty'};
    if(load.some(i=>!Number.isInteger(i)||i<0||i>=cargo.length)||new Set(load).size!==load.length)return {ok:false,reason:'invalid'};
    if(load.some(i=>delivered.includes(i)))return {ok:false,reason:'unavailable'};
    const weight=load.reduce((sum,i)=>sum+cargo[i].weight,0);
    if(weight>capacity)return {ok:false,reason:'overweight',weight};
    if(load.includes(1)&&!delivered.includes(0))return {ok:false,reason:'crane',weight};
    if(load.includes(2)&&load.includes(3))return {ok:false,reason:'water',weight};
    return {ok:true,weight};
  }
  function robotConfig(mode){
    const hard=mode==='engineer';
    return hard ? {n:6,start:[5,0,1],goal:[1,4],samples:[[3,2],[1,4]],road:[[5,0],[5,1],[5,2],[4,2],[3,2],[3,3],[3,4],[2,4],[1,4]],budget:8}
      : {n:5,start:[4,0,1],goal:[2,2],samples:[[2,2]],road:[[4,0],[4,1],[4,2],[3,2],[2,2]],budget:6};
  }
  const commands=['F','L','R','P','I'];
  function codeSize(main,body){return main.length+(main.includes('Q')?body.length:0);}
  function simulate(config,main,body,repeat){
    const trace=[], fail=reason=>({ok:false,reason,trace,blocks:codeSize(main,body)});
    if(!main.length)return fail('noCode');
    if(main.length>24||body.length>12||![2,3,4].includes(repeat))return fail('tooLong');
    if(main.some(a=>!commands.concat('Q').includes(a))||body.some(a=>!commands.includes(a)))return fail('invalidCode');
    if(main.includes('Q')&&!body.length)return fail('emptyLoop');
    const flat=[];
    main.forEach((a,index)=>{if(a==='Q'){for(let round=0;round<repeat;round++)body.forEach((b,sub)=>flat.push({a:b,index,sub,round}));}else flat.push({a,index,sub:-1,round:0});});
    if(flat.length>160)return fail('tooLong');
    const road=new Set(config.road.map(p=>p.join(','))),samples=new Set(config.samples.map(p=>p.join(',')));
    let [r,c,d]=config.start;const bag=new Set();
    const snapshot=(item,event)=>({r,c,d,bag:Array.from(bag),...item,event});
    for(const item of flat){
      const [dr,dc]=directions[d], ahead=road.has([r+dr,c+dc].join(','));
      if(item.a==='F'){
        if(!ahead){trace.push(snapshot(item,'wall'));return fail('wall');}r+=dr;c+=dc;
      }else if(item.a==='L')d=(d+3)%4;
      else if(item.a==='R')d=(d+1)%4;
      else if(item.a==='I'){if(!ahead)d=(d+3)%4;}
      else if(item.a==='P'){
        const key=[r,c].join(',');
        if(!samples.has(key)||bag.has(key)){trace.push(snapshot(item,'noSample'));return fail('noSample');}bag.add(key);
      }
      trace.push(snapshot(item,'ok'));
    }
    if(r!==config.goal[0]||c!==config.goal[1])return fail('unfinished');
    if(bag.size!==samples.size)return fail('missing');
    return {ok:true,reason:'done',trace,blocks:codeSize(main,body),efficient:codeSize(main,body)<=config.budget};
  }
  function newCampaign(mode){
    return {
      cargo:{load:[],delivered:[],trips:[],rejected:0,hints:0,done:false},
      power:{masks:powerConfig(mode).initial.slice(),turns:0,tests:0,hints:0,done:false},
      robot:{main:[],body:[],repeat:2,runs:0,stops:0,hints:0,done:false,best:null}
    };
  }
  root.QuestEngine={cargo,directions,rotate,turn,powerConfig,circuit,cargoCheck,robotConfig,codeSize,simulate,newCampaign};
  if(typeof module!=='undefined'&&module.exports)module.exports=root.QuestEngine;
})(typeof window!=='undefined'?window:globalThis);
