/* Interaction layer. All state stays on this device; no accounts, payments, telemetry or AI calls. */
(function(){
'use strict';
const E=window.QuestEngine,L=window.QuestLevels,S=window.QuestSaves,KEY='questly-storm-v5',LEGACY_KEY='questly-storm-v3';
const paths={
 spark:'M12 2l2.7 6.9L22 12l-7.3 2.6L12 22l-2.8-7.4L2 12l7.2-3.1z',
 boat:'M3 14h18l-4 6H7z M8 14V9h8v5 M12 9V3l5 4h-5 M2 22q3-3 6 0q3-3 6 0q3-3 8 0',
 bolt:'M14 2L5 14h7l-2 8 10-13h-7z',
 bot:'M7 6h10a3 3 0 0 1 3 3v9H4V9a3 3 0 0 1 3-3 M12 6V2 M9 11v2 M15 11v2 M8 18v3 M16 18v3 M2 10v6 M22 10v6',
 crane:'M5 21V3h13 M5 3l8 6H5 M18 3v8l-2 2 2 2 2-2 M2 21h8',
 beams:'M3 7l14-4 4 4-14 4z M3 7v5l4 4 14-4V7 M3 15v3l4 4 14-4v-3 M7 11v5 M7 19v3',
 drop:'M12 2C8 8 5 10 5 15a7 7 0 0 0 14 0c0-5-4-9-7-13z M8 15q0 4 4 4',
 leaf:'M20 3C6 1 2 9 7 15c7 6 14 0 13-12z M3 22L17 7',
 medical:'M9 6V3h6v3 M4 6h16v15H4z M12 10v7 M8.5 13.5h7',
 home:'M3 11l9-8 9 8 M6 9v12h12V9 M10 21v-7h4v7',
 flag:'M5 22V3 M5 3h13l-3 4 3 4H5',
 arrow:'M4 12h16 M14 6l6 6-6 6',
 forward:'M12 21V3 M5 10l7-7 7 7',
 left:'M19 21V10H4 M10 4l-6 6 6 6',
 right:'M5 21V10h15 M14 4l6 6-6 6',
 loop:'M4 9V5h14l3 4 M21 15v4H7l-3-4 M1 8l3 3 3-3 M18 16l3-3 3 3',
 sensor:'M4 21V11h12 M11 6l5 5-5 5 M20 3v5 M20 12v1',
 check:'M4 12l5 5L20 6',
 reset:'M3 10a9 9 0 1 1 1 8 M3 4v6h6',
 undo:'M9 4l-6 6 6 6 M3 10h10q7 0 7 8v3',
 light:'M8 17a7 7 0 1 1 8 0v3H8z M9 23h6 M12 1V0',
 play:'M7 3l14 9-14 9z',
 stop:'M5 5h14v14H5z',
 book:'M12 5Q7 1 2 4v16q5-3 10 1q5-4 10-1V4q-5-3-10 1z M12 5v16',
 lock:'M5 11h14v11H5z M8 11V6a4 4 0 0 1 8 0v5',
 close:'M5 5l14 14 M19 5L5 19'
};
const icon=(name,cls='')=>`<svg class="icon ${cls}" viewBox="0 0 24 24" aria-hidden="true"><path d="${paths[name]||paths.spark}"/></svg>`;
const t=(en,zh)=>state.lang==='zh'?zh:en;
const btn=(label,action,value='',cls='btn',disabled=false)=>`<button class="${cls}" data-action="${action}" data-value="${value}" ${disabled?'disabled':''}>${label}</button>`;
let state=S.fresh(),screen='map',storageOK=true,storageNotice=null,saveWritable=true,notice=null,hintText='',busy=false,epoch=0,editor='main',runner=null,powerResult=null,cargoSailing=false;
function parseSave(text){if(text===null)return null;try{return JSON.parse(text)??{invalid:true};}catch(_){return {invalid:true};}}
try{
 const restored=S.restore(parseSave(localStorage.getItem(KEY)),parseSave(localStorage.getItem(LEGACY_KEY)));
 state=restored.state;storageNotice=restored.notice;saveWritable=restored.writable;
 if(!saveWritable)storageOK=false;
}catch(_){storageOK=false;storageNotice='unavailable';}
function save(){
 if(!saveWritable){storageOK=false;return;}
 try{localStorage.setItem(KEY,JSON.stringify(state));storageOK=true;}catch(_){storageOK=false;storageNotice='unavailable';}
}
const cargoConfig=()=>L.cargoConfig(state.mode);
const levelInfo=()=>L.info(state.mode);
const localized=pair=>pair[state.lang==='zh'?1:0];
const itemName=(id,cfg=cargoConfig())=>state.lang==='zh'?cfg.items[id].zh:cfg.items[id].en;
const campaign=()=>state.campaigns[state.mode];
const names=()=>({cargo:t('Supply run','运送物资'),power:t('Restore power','修复电路'),robot:t('Program Nova','编程小车')});
const hard=()=>state.mode==='engineer';
function say(en,zh,type='neutral'){notice={text:t(en,zh),type};document.getElementById('live').textContent=notice.text;}
function flash(){return notice?`<div id="feedback" class="feedback ${notice.type}" role="status">${notice.text}</div>`:'';}
function hints(){return hintText?`<p class="hint">${icon('light')} ${hintText}</p>`:'';}
function cancel(){epoch++;busy=false;cargoSailing=false;runner=null;}
function navigate(to){cancel();screen=to;notice=null;hintText='';powerResult=null;render();window.scrollTo(0,0);document.getElementById('view').focus({preventScroll:true});}
function completeBanner(stage){
 if(!campaign()[stage].done)return '';
 const next=L.ids[L.ids.indexOf(state.mode)+1];
 return `<div class="success"><div><h3>${icon('check')} ${t('Station restored','站点修复成功')}</h3><p>${t('Your plan worked. Try the next challenge, or revisit this one.','你的方案成功了。试试下一关，或继续改进这一关。')}</p></div>${next?btn(t('Next challenge','下一关')+' '+icon('arrow'),'level',next+':'+stage):btn(t('All 18 missions','全部 18 关'),'nav','map')}</div>`;
}
function missionSummary(stage){
 if(stage==='power'){const cfg=L.powerConfig(state.mode);return t(`${cfg.n} × ${cfg.n} board · ${cfg.targets.length} stations. Follow every branch.`,`${cfg.n} × ${cfg.n} 电路板，${cfg.targets.length} 个站点，追踪每条支路。`);}
 if(stage==='robot'){const cfg=L.robotConfig(state.mode);return state.mode==='ridge'?t('The lab is also your start. Collect every sample before returning.','起点也是实验室，收齐所有样本后再回到这里。'):t(`${cfg.samples.length} samples. Plan the repeated route, then the way to the lab.`,`${cfg.samples.length} 个样本，规划重复路线和去实验室的路。`);}
 return localized(levelInfo().description);
}
function levelPicker(stage){
 const completed=L.ids.filter(id=>state.campaigns[id][stage].done).length;
 return `<section class="level-picker" aria-label="${t('Choose a mission','选择关卡')}"><label><span>${t('Mission','关卡')}</span><select id="level-select" data-stage="${stage}">${L.catalog.map((level,i)=>`<option value="${level.id}" ${state.mode===level.id?'selected':''}>${i+1}. ${localized(level.titles[stage])}${state.campaigns[level.id][stage].done?' ✓':''}</option>`).join('')}</select></label><span class="fine">${completed}/6 ${t('completed','已完成')}</span>${btn(t('All missions','全部关卡'),'nav','map','ghost')}<p>${missionSummary(stage)}</p></section>`;
}
function library(){
 const completed=L.ids.reduce((total,id)=>total+['cargo','power','robot'].filter(stage=>state.campaigns[id][stage].done).length,0);
 return `<section class="mission-library" id="missions"><div class="library-heading"><div><div class="eyebrow">${t('The adventure continues','冒险继续')}</div><h2>${t('18 missions. More possibilities.','18 个关卡，更多可能。')}</h2><p>${t('Six missions in each workshop. Start anywhere; every mission keeps its own progress.','每种玩法六关，任意选择，每关进度独立保存。')}</p></div><span class="pill">${completed}/18 ${t('restored','已修复')}</span></div><div class="mission-columns">${['cargo','power','robot'].map((stage,i)=>`<section class="mission-column"><h3>${icon(['boat','bolt','bot'][i])} ${names()[stage]}</h3>${L.catalog.map((level,j)=>btn(`<span class="mission-index">${state.campaigns[level.id][stage].done?'✓':String(j+1).padStart(2,'0')}</span><span><strong>${localized(level.titles[stage])}</strong><small>${localized(level.tag)}</small></span>${icon('arrow')}`,'level',level.id+':'+stage,`mission-choice ${state.campaigns[level.id][stage].done?'solved':''} ${state.mode===level.id?'current':''}`)).join('')}</section>`).join('')}</div></section>`;
}
function storageBanner(){
 if(storageNotice==='protected')return `<div class="feedback error">${t('This saved file needs a compatible version or recovery. It is preserved. You can play here, but this session will not replace it.','已有存档需要兼容版本或恢复，原文件已保留。仍可试玩，但本次进度不会覆盖它。')}</div>`;
 if(!storageOK)return `<div class="feedback error">${t('Storage is unavailable. Progress lasts only while this page stays open.','存储不可用，进度仅保留到本页面关闭。')}</div>`;
 if(storageNotice==='migrated')return `<div class="feedback neutral">${t('Your original six missions are here. Twelve new challenges are ready; the original save is preserved.','原来六关的进度已带过来，十二个新挑战已开放，旧存档也已保留。')}</div>`;
 if(storageNotice==='legacyInvalid')return `<div class="feedback neutral">${t('The old save could not be read. It is preserved; this collection starts a separate save.','旧存档无法读取，原文件已保留；本关卡册将使用独立新存档。')}</div>`;
 return '';
}
function header(){return `<nav class="nav" aria-label="${t('Main navigation','主导航')}">${btn(`<span class="brand-mark">${icon('spark')}</span>Questly`,'nav','map','brand')}<div class="nav-actions">${btn(state.lang==='en'?'中文':'EN','lang','','ghost')}${btn(icon('book')+' '+t('For parents','家长记录'),'nav','parents','ghost')}</div></nav>`;}
function tabs(){return `<nav class="stage-nav" aria-label="${t('Stations','站点')}">${['cargo','power','robot'].map((s,i)=>btn(`<span class="num">${campaign()[s].done?'✓':i+1}</span>${names()[s]}`,'nav',s,screen===s?'active':'')).join('')}</nav>`;}
function footer(){return `<footer class="footer"><span>QUESTLY · STORM ISLAND · v0.5.0</span><span>${t('Review prototype · No ads, payments or cloud data','试玩原型 · 无广告、付费或云端数据')}${storageOK?'':t(' · Storage unavailable',' · 存储不可用')}</span></footer>`;}
function home(){const c=campaign(),total=['cargo','power','robot'].filter(k=>c[k].done).length;return `<section class="home-grid"><div class="home-copy"><div class="eyebrow">${t('Chapter 01 / Storm Island','第一章 / 暴风雨后的岛屿')}</div><h1>${t('Small engineer.<br><em>Big ideas.</em>','小小工程师。<br><em>大大的想法。</em>')}</h1><p class="lead">${t('The storm has passed. The island needs you. Pack a boat, reconnect the power, and teach Nova the way home.','暴风雨停了，小岛需要你的帮助。装好船、接通电路，再教 Nova 小车找到回家的路。')}</p>${btn(t(total?'Return to the island':'Let’s rebuild the island',total?'继续修复小岛':'开始修复小岛')+' '+icon('arrow'),'nav',['cargo','power','robot'].find(k=>!c[k].done)||'cargo','btn gold')}${btn(t('Choose from all 18 missions','选择全部 18 个关卡')+' '+icon('arrow'),'library','','ghost library-jump')}<div class="mode-box"><span class="fine">${t('The original two challenges are still here. Find all 18 missions below.','原有两档仍然保留，下方可选全部 18 关。')}</span><div class="seg">${btn(t('Explorer','探索模式'),'mode','explorer',state.mode==='explorer'?'active':'')}${btn(t('Engineer','工程师挑战'),'mode','engineer',state.mode==='engineer'?'active':'')}</div><p class="fine">${localized(levelInfo().description)}</p></div></div><div class="world-map" aria-label="${t('Interactive island map','可交互的小岛地图')}"><span class="map-label">NOVA ISLAND / 01</span><span class="map-compass">N ${icon('forward')}</span><div class="map-island"></div><svg class="map-road" viewBox="0 0 500 440" preserveAspectRatio="none" aria-hidden="true"><path d="M123 293Q137 163 270 122Q337 135 371 292" fill="none" stroke="#e8dcbb" stroke-width="21" stroke-linecap="round"/><path d="M123 293Q137 163 270 122Q337 135 371 292" fill="none" stroke="#aa9d76" stroke-width="2" stroke-dasharray="4 11"/></svg><i class="tree t1"></i><i class="tree t2"></i><i class="tree t3"></i><i class="tree t4"></i><i class="cloud c1"></i><i class="cloud c2"></i>${['cargo','power','robot'].map((s,i)=>btn(`<span class="building">${icon(c[s].done?'check':['boat','bolt','bot'][i])}</span><strong>${i+1}. ${names()[s]}</strong>`,'nav',s,`map-station ${s} ${c[s].done?'done':''}`)).join('')}<span class="map-footer">${total}/3 ${t('stations restored · Tap any station','站点已修复 · 点击任意站点')}</span></div></section><section class="chapter-cards">${['cargo','power','robot'].map((s,i)=>btn(`<span class="badge">${icon(['boat','bolt','bot'][i])}</span><div><strong>0${i+1} / ${names()[s]}</strong><p>${[t('Plan the load. Every trip matters.','规划装载，每一趟都很重要。'),t('Turn the pieces. Follow the current.','转动线路，观察电流走向。'),t('Build a program. Watch it run.','编排指令，看它如何行动。')][i]}</p></div>`,'nav',s,'chapter-card')).join('')}</section>${library()}${total===3?`<div class="success"><div><h3>${t('The island is back!','小岛恢复运转了！')}</h3><p>${t('A good place to stop. Show someone how your designs work.','现在可以休息啦。向家人展示你的设计是怎样工作的吧。')}</p></div>${btn(t('See field notes','查看工程记录'),'nav','parents','btn light')}</div>`:''}`;}
function missionTitle(num,title,desc){
 const stage=['cargo','power','robot'][Number(num)-1];
 if(stage&&L.ids.indexOf(state.mode)>1)title=localized(levelInfo().titles[stage]);
 return `<header class="mission-title"><div><div class="eyebrow">${t('Station','站点')} ${num} / 03</div><h2>${title}</h2><p class="lead">${desc}</p></div><span class="pill">${localized(levelInfo().tag)}</span></header>${stage?levelPicker(stage):''}`;
}
function cargoView(){
 const a=campaign().cargo,cfg=cargoConfig(),cap=cfg.capacity,weight=a.load.reduce((n,i)=>n+cfg.items[i].weight,0);
 const rules=[
  ...cfg.before.map(([first,next])=>[cfg.items[first].icon,t(`${itemName(first,cfg)} must arrive before ${itemName(next,cfg)}. Separate trips.`,`${itemName(first,cfg)}必须先于${itemName(next,cfg)}到达，不能同一趟运输。`)]),
  ...cfg.apart.map(([first,next])=>['drop',t(`${itemName(first,cfg)} and ${itemName(next,cfg)} need separate trips.`,`${itemName(first,cfg)}和${itemName(next,cfg)}不能同船运输。`)]),
  ['flag',cfg.maxTrips?t(`Only ${cfg.maxTrips} voyages. Use the space wisely.`,`最多 ${cfg.maxTrips} 趟，规划好每一趟。`):t('No voyage limit. Try different combinations.','不限制航次，自由尝试搭配。')],
  ...(cfg.maxItems?[['boat',t(`Only ${cfg.maxItems} crates fit on deck, even if the weight is lower.`,`甲板最多放 ${cfg.maxItems} 箱，即使载重没满也不能多放。`)]]:[]),
  ...Object.entries(cfg.by).map(([id,trip])=>['medical',t(`${itemName(Number(id),cfg)} must arrive by voyage ${trip}.`,`${itemName(Number(id),cfg)}必须在第 ${trip} 趟送达。`)])
 ];
 return missionTitle('01',t('The right cargo. The right order.','装什么？先运什么？'),t(`Deliver all ${cfg.items.length} supplies. Tap a card to load or unload it, then launch your boat.`,`送达全部 ${cfg.items.length} 件物资。点击卡片装船或卸下，再让船出发。`))+completeBanner('cargo')+`
 <section class="workspace cargo-workspace"><div class="panel"><div class="panel-head"><h3>${icon('boat')} ${t('Your boat','你的运输船')}</h3><span class="fine">${t('Voyages','已用航次')} ${a.trips.length}${cfg.maxTrips?' / '+cfg.maxTrips:''}</span></div>
 <div class="harbor"><div class="dock left"><span>${t('DEPOT','仓库')}</span></div><div class="dock right"><span>${t('ISLAND','小岛')}</span></div><div class="boat ${cargoSailing?'sailing':''}"><div class="boat-deck">${a.load.map(i=>icon(cfg.items[i].icon)).join('')||icon('boat')}</div><div class="hull"></div></div></div>
 <div class="weight-line"><span>${t('Cargo weight','载重')}</span><span><b>${weight}</b> / ${cap}</span></div><div class="weight-meter ${weight>cap?'over':''}"><i style="width:${Math.min(100,weight/cap*100)}%"></i></div><p class="program-caption">${t('Tap supplies to load / unload.','点击物资来装船或卸下。')}${cfg.maxItems?' '+t(`Deck: ${a.load.length} / ${cfg.maxItems} crates.`,`甲板：${a.load.length} / ${cfg.maxItems} 箱。`):''}</p>
 <div class="inventory">${cfg.items.map(item=>btn(`${icon(item.icon)}<strong>${itemName(item.id,cfg)}</strong><small>${item.weight} ${t('units','载重单位')}</small>${a.delivered.includes(item.id)?'<span class="tick">✓</span>':a.load.includes(item.id)?'<span class="tick">＋</span>':''}`,'cargo',item.id,`cargo-item ${a.load.includes(item.id)?'selected':''} ${a.delivered.includes(item.id)?'delivered':''}`,busy||a.delivered.includes(item.id))).join('')}</div>
 <div class="actions">${btn(icon('play')+' '+t('Launch boat','让船出发'),'launch','','btn',busy||a.done)}${btn(icon('undo')+' '+t('Undo trip','撤回一趟'),'undoCargo','','ghost',busy||!a.trips.length)}</div>${flash()}${hints()}</div>
 <div class="panel"><div class="panel-head"><h3>${t('Plan your voyages','规划你的航次')}</h3><span class="fine">${a.delivered.length}/${cfg.items.length} ${t('delivered','已送达')}</span></div><div class="rule-list">${rules.map(([symbol,text])=>`<div class="rule">${icon(symbol)}<span>${text}</span></div>`).join('')}</div>
 <div class="actions">${btn(icon('light')+' '+t('A small hint','一点提示'),'hint','cargo','ghost')}${btn(icon('reset')+' '+t('Start over','重新规划'),'reset','cargo','ghost',busy)}</div><div style="margin-top:20px"><h3 style="font-size:13px">${t('Trip log','航次记录')}</h3>${a.trips.length?a.trips.map((trip,i)=>`<div class="trip-row"><span>0${i+1}</span><span>${trip.map(j=>itemName(j,cfg)).join(' + ')}</span><b>${trip.reduce((n,j)=>n+cfg.items[j].weight,0)} / ${cap}</b></div>`).join(''):`<p class="fine" style="margin-top:8px">${t('Your first delivery will appear here. Empty returns do not count as voyages.','第一趟成功送达后会显示在这里，空船返程不计航次。')}</p>`}</div></div></section>`;
}
function wire(mask,source,target){const ends=[[50,0],[100,50],[50,100],[0,50]];return `<svg viewBox="0 0 100 100" aria-hidden="true">${ends.map(([x,y],i)=>mask&(1<<i)?`<path d="M50 50L${x} ${y}" fill="none" stroke="currentColor" stroke-width="13"/>`:'').join('')}<circle class="wire-center" cx="50" cy="50" r="${source||target?20:10}" fill="${source?'#eab759':target?'#d0dee3':'currentColor'}" stroke="currentColor" stroke-width="3"/>${source?'<path d="M54 34L42 51H51L46 67L60 47H51Z" fill="#17343e"/>':target?'<path d="M42 45L50 39L58 45V59H42Z" fill="#17343e"/>':''}</svg>`;}
function powerView(){const p=campaign().power,cfg=L.powerConfig(state.mode),res=powerResult||(p.done?E.circuit(cfg,p.masks):null),lit=res?res.lit.length:0;return missionTitle('02',t('Make the island glow.','让小岛亮起来。'),t('Tap a wire tile to turn it clockwise. Join the generator to every station, then test the circuit.','点击线路块顺时针旋转。将发电机连接到所有站点，再测试通电。'))+completeBanner('power')+`<section class="workspace"><div class="panel"><div class="panel-head"><h3>${icon('bolt')} ${t('Circuit board','电路板')}</h3><span class="fine">${cfg.n} × ${cfg.n}</span></div><div class="board-wrap"><div class="power-grid" style="grid-template-columns:repeat(${cfg.n},1fr);min-width:${cfg.n*44+(cfg.n-1)*5+18}px">${p.masks.map((m,i)=>{const src=i===cfg.source,target=cfg.targets.includes(i),fixed=cfg.fixed.includes(i);return `<button class="wire ${!m?'empty':''} ${src?'source':''} ${target?'target':''} ${res&&res.reached.includes(i)?'lit':''}" data-action="wire" data-value="${i}" ${!m||src||target||fixed?'disabled':''} aria-label="${t('Tile','线路块')} ${i+1}${src?t(' generator',' 发电机'):target?t(' station',' 站点'):fixed?t(' fixed relay',' 固定接点'):''}" title="${t('Turn clockwise','顺时针旋转')}">${m?wire(m,src,target):''}${src||target||fixed?`<span class="wire-label">${src?'G':fixed?'●':cfg.targets.indexOf(i)+1}</span>`:''}</button>`;}).join('')}</div></div><p class="board-scroll-note fine">${t('On a small screen, swipe the board sideways to see every tile.','小屏幕可在棋盘上左右滑动，查看所有线路块。')}</p><div class="legend"><span><i class="dot"></i>G = ${t('generator','发电机')}</span><span><i class="dot blue"></i>${t('Stations and ● relays are fixed','站点与 ● 接点方向固定')}</span></div><div class="actions">${btn(icon('bolt')+' '+t('Test power','测试通电'),'testPower','','btn gold')}${btn(icon('reset')+' '+t('Reset','重置'),'reset','power','ghost')}</div>${flash()}</div><div class="panel"><div class="eyebrow">${t('Power check','供电检查')}</div><div class="power-score">${lit}<small> / ${cfg.targets.length} ${t('stations','站点')}</small></div><div class="rule-list"><div class="rule">${icon('bolt')}<span>${t('Power flows only where <strong>both ends meet</strong>. A piece nearby is not enough.','只有线路的<strong>两端正确相接</strong>才会通电，靠近并不等于连接。')}</span></div><div class="rule">${icon('light')}<span>${cfg.targets.length>1?t('Use the junctions to reach every station. Some pieces are decoys.','利用分岔接头为所有站点供电，有些线路是干扰项。'):t('Trace a route from G. You do not need every tile.','从 G 出发寻找路径，不需要用上每一块线路。')}</span></div></div><p class="fine">${t('Testing lights up the connected part, so you can see where your route breaks.','测试时会点亮已经连接的部分，方便你找到断点。')}</p><div class="actions">${btn(icon('light')+' '+t('A small hint','一点提示'),'hint','power','ghost')}</div>${hints()}</div></section>`;}
const commandNames=()=>({F:[t('Forward','前进'),'forward'],L:[t('Left','左转'),'left'],R:[t('Right','右转'),'right'],P:[t('Pick up','拾取'),'leaf'],I:[t('If blocked: left','遇障碍左转'),'sensor'],Q:[t('Repeat','重复'),'loop']});
function robotBoard(){const cfg=L.robotConfig(state.mode),snap=runner&&runner.snap,at=snap?[snap.r,snap.c,snap.d]:cfg.start,bag=snap?snap.bag:[],visited=runner?runner.result.trace.slice(0,runner.cursor).map(f=>f.r+','+f.c):[];const road=new Set(cfg.road.map(p=>p.join(',')));return `<div class="robot-grid" style="grid-template-columns:repeat(${cfg.n},1fr);min-width:${cfg.n*28+(cfg.n-1)*4+18}px">${Array.from({length:cfg.n*cfg.n},(_,i)=>{const r=Math.floor(i/cfg.n),c=i%cfg.n,k=r+','+c,isGoal=cfg.goal.join(',')===k,isStart=cfg.start.slice(0,2).join(',')===k,sample=cfg.samples.some(v=>v.join(',')===k)&&!bag.includes(k);return `<div class="cell ${road.has(k)?'road':''} ${isGoal?'goal':''} ${isStart?'start':''} ${visited.includes(k)?'visited':''}">${sample?icon('leaf','sample'):''}${at[0]===r&&at[1]===c?`<div class="rover" data-rover="${k}" aria-label="${t('Nova facing','Nova 朝向')} ${['N','E','S','W'][at[2]]}"><svg viewBox="0 0 24 24" class="icon" style="transform:rotate(${at[2]*90}deg)"><path d="M12 3l-7 9h4v8h6v-8h4z" fill="#17343e" stroke="none"/></svg></div>`:''}${isGoal||isStart?`<span class="cell-label">${isGoal&&isStart?t('START / LAB','起点 / 实验室'):isGoal?t('LAB','实验室'):t('START','起点')}</span>`:''}</div>`;}).join('')}</div><div class="robot-state"><span>${t('Samples','样本')} ${bag.length}/${cfg.samples.length}</span><span>${t('Facing','朝向')} ${['↑ N','→ E','↓ S','← W'][at[2]]}</span><span>${t('Step','步骤')} ${runner?runner.cursor:0}</span></div>`;}
function robotView(){const r=campaign().robot,cfg=L.robotConfig(state.mode),labels=commandNames(),commands=r[editor];return missionTitle('03',t('Teach Nova a clever route.','教 Nova 走一条聪明的路线。'),t('Collect every seed sample and finish at the lab. Plan the moves, run your program, then improve it.','收集全部种子样本，并停在实验室。规划指令、运行程序，再改进你的方案。'))+completeBanner('robot')+`<section class="workspace robot-workspace ${cfg.n>6?'large-board':''}"><div class="panel"><div class="panel-head"><h3>${icon('bot')} ${t('Nova’s route','Nova 的路线')}</h3><span class="fine">${t('Arrow = facing','箭头 = 朝向')}</span></div><div id="robot-board" class="board-wrap">${robotBoard()}</div><div class="rule-list"><div class="rule">${icon('forward')}<span>${t('<strong>Forward</strong> moves one tile in the direction Nova faces. Turning does not move Nova.','<strong>前进</strong>是沿着 Nova 当前朝向走一格，转弯本身不会移动。')}</span></div><div class="rule">${icon('leaf')}<span>${t('<strong>Pick up</strong> works only while standing on an uncollected sample.','只有站在还没收集的样本上，<strong>拾取</strong>才有效。')}</span></div></div><div class="actions">${btn(icon('play')+' '+t('Run','运行'),'runRobot','','btn gold',busy)}${btn(t('Step','单步'),'stepRobot','','ghost',busy)}${btn(icon('stop')+' '+t('Stop','停止'),'stopRobot','','ghost',!runner)}</div>${flash()}${hints()}</div><div class="panel"><div class="panel-head"><h3>${t('Program builder','程序工作台')}</h3><span class="fine" id="blocks">${E.codeSize(r.main,r.body)} ${t('blocks','块指令')}</span></div><div class="editor-tabs">${btn(t('Main program','主程序')+` (${r.main.length})`,'editor','main',editor==='main'?'active':'',busy)}${btn(t('Repeat body','循环内容')+` (${r.body.length})`,'editor','body',editor==='body'?'active':'',busy)}</div><div class="code-box" id="code-box">${commands.length?commands.map((cmd,i)=>btn(`<b>${i+1}</b> ${labels[cmd][0]}${cmd==='Q'?' ×'+r.repeat:''}`,'remove',i,`code-token ${cmd} ${runner&&runner.snap&&(editor==='main'?runner.snap.index===i:runner.snap.sub===i)?'executing':''}`,busy)).join(''):`<span class="empty-text">${editor==='main'?t('Tap a command below to add it here. Tap a block above to remove it.','点击下面的指令来添加，点击已添加的指令可删除。'):t('These commands will repeat. Add a Repeat block to the main program to use them.','这里的指令会重复执行。需要在主程序中添加“重复”指令。')}</span>`}</div><div class="palette">${Object.keys(labels).map(cmd=>btn(icon(labels[cmd][1])+labels[cmd][0],'add',cmd,'command',busy||(cmd==='Q'&&editor==='body'))).join('')}</div><div class="loop-controls"><span>${t('Repeat body','循环内容')}</span><label>${t('Repeat','重复')} <select id="repeat-count" aria-label="${t('Repeat count','重复次数')}" ${busy?'disabled':''}>${[2,3,4].map(n=>`<option value="${n}" ${n===r.repeat?'selected':''}>${n} ×</option>`).join('')}</select></label></div><p class="program-caption">${t('If blocked: left → turns left only when the tile ahead is not a road. Otherwise it does nothing.','遇障碍左转 → 只有前方不是道路时才左转，否则不行动。')}</p><div class="feedback neutral">${t('First, make it work. Bonus: use','先完成任务，再试着优化到')} <strong style="display:inline">≤ ${cfg.budget} ${t('blocks','块指令')}</strong>${t(' including the repeat body. This is a design goal, not a speed test.','（包含循环内容）。不计时、不催促。')}</div><div class="actions">${btn(icon('light')+' '+t('A small hint','一点提示'),'hint','robot','ghost')}${btn(icon('reset')+' '+t('Clear code','清空程序'),'reset','robot','ghost',busy)}</div></div></section>`;}
function parents(){const c=campaign();return missionTitle('—',t('The engineer’s field notes.','小小工程师的记录。'),t('Observed actions from this device, not a diagnosis or a mastery score.','这里只记录本设备上的实际操作，不是能力诊断，也不生成掌握度评分。'))+`<div class="report-intro">${t('Ask: “What did you change after your first test?” The conversation matters more than a perfect run. Current mode:','可以问：“第一次测试之后，你改了什么？”比起一次成功，这段讨论更有价值。当前模式：')} <b>${localized(levelInfo().tag)}</b></div><section class="report-grid">${['cargo','power','robot'].map((s,i)=>{const v=c[s],fields=s==='cargo'?[[t('Successful trips','成功航次'),v.trips.length],[t('Launches rejected','发船被阻止'),v.rejected],[t('Hints opened','查看提示'),v.hints]]:s==='power'?[[t('Tile rotations','转动次数'),v.turns],[t('Power tests','通电测试'),v.tests],[t('Hints opened','查看提示'),v.hints]]:[[t('Program runs','运行次数'),v.runs],[t('Best working program','最短成功程序'),v.best===null?'—':v.best],[t('Hints opened','查看提示'),v.hints]];return `<article class="report-card">${icon(['boat','bolt','bot'][i])}<h3>${names()[s]}</h3><p style="margin-top:6px">${v.done?t('✓ Restored','✓ 已修复'):t('Still exploring','仍在探索')}</p><dl>${fields.map(([k,val])=>`<div><dt>${k}</dt><dd>${val}</dd></div>`).join('')}</dl><p>${[t('Try together: why can’t the crane and beams travel on the same boat?','一起讨论：为什么起重机和木梁不能同船到达？'),hard()?t('Try together: show where the power splits into two routes.','一起讨论：电流在哪里分成两条路线？'):t('Try together: follow the current from G to the station.','一起讨论：沿着电流从 G 走到站点。'),t('Try together: which part of the route repeats? Could you reuse it?','一起讨论：哪一段路线重复出现了？能不能复用？')][i]}</p></article>`;}).join('')}</section><p class="fine">${storageOK?t('Saved on this browser only. Reloading can restore your progress here; there is no cross-device sync.','仅保存在当前浏览器，没有账号或跨设备同步。'):t('Browser storage is unavailable. Progress lasts only while this page stays open.','浏览器存储不可用，进度只会保留到本页面关闭。')} ${t('No names, recordings or child data are sent to a server. Resetting a station resets its counters.','不会把姓名、录音或儿童数据上传服务器。重置某站点会清除该站点的计数。')}</p><div class="settings-row">${btn(icon('home')+' '+t('Back to the island','返回小岛'),'nav','map')}${btn(t('Reset this mode','重置当前模式'),'resetAll','','ghost')}</div>`;}
function render(){
 const active=document.activeElement,focus=active&&active.dataset?{a:active.dataset.action,v:active.dataset.value}:null;
 document.documentElement.lang=state.lang==='zh'?'zh-CN':'en';
 document.getElementById('app').innerHTML=`<div class="shell">${header()}${!['map','parents'].includes(screen)?tabs():''}<main id="view" class="screen" tabindex="-1">${storageBanner()}${screen==='map'?home():screen==='cargo'?cargoView():screen==='power'?powerView():screen==='robot'?robotView():parents()}</main>${footer()}</div>`;
 if(focus&&focus.a){const match=Array.from(document.querySelectorAll('button[data-action]')).find(b=>b.dataset.action===focus.a&&b.dataset.value===focus.v&&!b.disabled);if(match)match.focus({preventScroll:true});}
}
function launch(){
 const a=campaign().cargo,cfg=cargoConfig();if(busy||a.done)return;
 const result=L.cargoCheck(state.mode,a.load,a.delivered,a.trips.length);
 if(!result.ok){
  if(result.reason!=='voyages')a.rejected++;
  const pair=result.pair||[];
  const msg={
   empty:['Your boat is empty. Tap supplies to load it.','船上还没有物资，点击物资装船吧。'],
   overweight:['Too heavy. Remove something or try another combination.','超过载重了。卸下一些物资，或试试别的搭配。'],
   crane:['The crane must already be on the island before beams can travel.','要先把起重机送到岛上，木梁才能出发。'],
   water:['Water and a battery cannot share this boat. Split them across trips.','清水和电池不能同船，请分开运输。'],
   voyages:['No voyages left. Undo a trip and regroup the supplies.','没有航次了。撤回一趟，重新搭配物资。'],
   slots:[`Only ${cfg.maxItems} crates fit on deck. Unload a crate.`,`甲板最多放 ${cfg.maxItems} 箱，请卸下一箱。`]
  };
  if(result.reason==='order')msg.order=[`${itemName(pair[0],cfg)} must arrive before ${itemName(pair[1],cfg)}.`,`${itemName(pair[0],cfg)}必须先到达，才能运送${itemName(pair[1],cfg)}。`];
  if(result.reason==='apart')msg.apart=[`${itemName(pair[0],cfg)} and ${itemName(pair[1],cfg)} need separate trips.`,`${itemName(pair[0],cfg)}与${itemName(pair[1],cfg)}需要分开运输。`];
  if(result.reason==='priority')msg.priority=[`Load ${itemName(result.item,cfg)} now: it must arrive on this voyage.`,`这趟请装上${itemName(result.item,cfg)}，它必须优先送达。`];
  say(...(msg[result.reason]||['Check your cargo.','请检查物资。']),'error');save();render();return;
 }
 busy=true;const token=++epoch;notice=null;render();setTimeout(()=>{if(token!==epoch)return;cargoSailing=true;render();},30);
 setTimeout(()=>{
  if(token!==epoch)return;
  const load=a.load.slice();a.trips.push(load);a.delivered.push(...load);a.load=[];a.done=a.delivered.length===cfg.items.length;busy=false;cargoSailing=false;
  if(a.done)say(`All ${cfg.items.length} supplies delivered. Your island can start rebuilding!`,`全部 ${cfg.items.length} 件物资送达，小岛可以开始修复啦！`,'good');
  else if(cfg.maxTrips&&a.trips.length===cfg.maxTrips)say('Voyages used, but supplies remain. Undo a trip and redesign the loads.','航次用完了，但还有物资。撤回一趟，重新规划装载。','error');
  else say('Delivered! Plan the next load.','送达成功！规划下一趟吧。','good');save();render();
 },760);
}
function testPower(){const p=campaign().power;powerResult=E.circuit(L.powerConfig(state.mode),p.masks);p.tests++;p.done=powerResult.complete;if(p.done)say('Every station is powered. You made the connections work!','全部站点都通电了！你的连接方案成功了！','good');else say(`Only ${powerResult.lit.length} stations are powered. Follow the gold path to its last connected tile.`,`目前 ${powerResult.lit.length} 个站点通电。沿着金色线路，找找最后一个接通的格子。`,'neutral');save();render();}
function buildRunner(){const r=campaign().robot;r.runs++;const cfg=L.robotConfig(state.mode),result=E.simulate(cfg,r.main,r.body,r.repeat);runner={result,cursor:0,snap:{r:cfg.start[0],c:cfg.start[1],d:cfg.start[2],bag:[]}};notice=null;save();return result;}
function finishRunner(){const r=campaign().robot,result=runner.result;busy=false;if(result.ok){r.done=true;r.best=r.best===null?result.blocks:Math.min(r.best,result.blocks);say(result.efficient?'Nova delivered every sample — and met the compact-program goal!':'Nova delivered every sample! Can you use a repeat block to make the program smaller?',result.efficient?'Nova 送达了所有样本，也完成了精简程序目标！':'Nova 送达了所有样本！能不能用循环再减少指令数量？','good');}else{const messages={noCode:['Add commands before running.','先添加指令再运行。'],emptyLoop:['The Repeat block has no body. Switch to Repeat body and add commands.','重复指令还没有内容，切换到“循环内容”添加指令。'],wall:['Nova reached the edge of the road. Check its facing direction at this step.','Nova 走到了道路边缘，看看这一步的朝向是否正确。'],noSample:['There is no new sample here. Move to a seed before using Pick up.','这里没有新的样本，走到种子上再拾取。'],unfinished:['The program ended before Nova reached the lab. Add or rearrange a few moves.','程序结束了，但 Nova 还没到实验室。再加几步，或调整顺序。'],missing:['Nova reached the lab, but left a sample behind. Add a Pick up at each seed.','Nova 到达了实验室，但漏掉了样本。记得在每颗种子上拾取。']};say(...(messages[result.reason]||['The program needs a little adjustment.','程序还需要调整。']),'error');}save();render();}
function frame(){if(!runner)return;const f=runner.result.trace[runner.cursor];if(f){runner.snap=f;runner.cursor++;editor=f.sub>=0?'body':'main';}if(runner.cursor>=runner.result.trace.length){finishRunner();return;}render();}
function runRobot(){if(busy)return;cancel();buildRunner();busy=true;const token=++epoch;render();if(!runner.result.trace.length){finishRunner();return;}const tick=()=>{if(token!==epoch||!runner)return;frame();if(busy)setTimeout(tick,330);};setTimeout(tick,220);}
function stepRobot(){if(busy)return;if(!runner||runner.cursor>=runner.result.trace.length){cancel();buildRunner();}frame();}
function advancedHints(stage){
 if(stage==='cargo'){
  const plans={tides:[[0,7,4],[1,2],[3,5,6]],ridge:[[0,7,2],[1,8,5],[3,4,6]],beacon:[[0,7,5],[1,2],[6,8],[9,3,4]],summit:[[0,7,5],[1,8],[6,3],[9,4,2]]};
  return [t('Draw the arrival chains first. Which supplies must go on the first voyage?','先画出到达顺序链。哪些物资必须第一趟就出发？'),t('Reserve space for the middle of each chain before packing the small crates.','先为每条链中间的物资留出空间，再安排小箱子。'),t('One plan: ','一种方案：')+plans[state.mode].map(trip=>trip.map(id=>itemName(id)).join(' + ')).join(' → ')];
 }
 if(stage==='power')return [t('Trace from G to the nearest junction. Test to see the exact break.','从 G 走到最近的分岔接头，测试看看具体断在哪里。'),t('● relays cannot turn. Plan the wire on each side of a relay before extending a branch.','● 接点不能旋转。先规划它两侧的线路，再延伸支路。'),t('Work outward from G, connecting one station at a time. Leave lit junctions in place while repairing a different branch.','从 G 向外逐步连接站点。修复另一条支路时，先保留已通电的分岔方向。')];
 const programs={
  tides:[['Repeat the stair three times, then leave the stairs for the lab.','先走三段阶梯，完成循环后还要继续去实验室。'],['Body: F F L F F P R ×3. Main: Q L F.','循环：前进 前进 左转 前进 前进 拾取 右转，重复 3 次。主程序：循环 左转 前进。']],
  ridge:[['Each side has six moves. Pick up at each corner, including the starting corner when you return.','每条边走六步，在每个角拾取，起点的样本留到回到起点时拿。'],['Body: F F F F F F P L ×4. Main: Q.','循环：前进六次 拾取 左转，重复 4 次。主程序：循环。']],
  beacon:[['Pick up halfway along each side and at each corner. The journey to the central lab belongs after the loop.','每条边的中点和拐角都要拾取，去中心实验室的路放在循环后面。'],['Body: F F F P F F F P L ×4. Main: Q L F F F R F F F.','循环：前进三次 拾取 前进三次 拾取 左转，重复 4 次。主程序：循环 左转 前进三次 右转 前进三次。']],
  summit:[['Both camps have the same shape. Use the same repeat block twice, with the connecting path between them.','两个营地形状一样。复用同一个循环两次，中间插入连接道路。'],['Body: F F F P L ×4. Main: Q, five F, Q, L, four F.','循环：前进三次 拾取 左转，重复 4 次。主程序：循环 前进五次 循环 左转 前进四次。']]
 };
 return [t('Separate the repeated survey from the journey between places. Turning changes facing, not position.','把重复巡查和地点间的移动分开，转弯只改变朝向。'),localized(programs[state.mode][0]),localized(programs[state.mode][1])];
}
function showHint(stage){const c=campaign()[stage];c.hints++;let list;
 if(L.ids.indexOf(state.mode)>1){list=advancedHints(stage);hintText=list[Math.min(c.hints-1,list.length-1)];save();render();return;}
 if(stage==='cargo')list=[t('Start with the item that unlocks another item. Is there room for something else beside it?','先运能解锁其他物资的东西，它旁边还有没有空位？'),t('The 6-unit beams fit beside the 4-unit battery. What must arrive first?','6 单位的木梁能和 4 单位的电池同船，什么必须先到？'),t('One plan: crane + water; then beams + battery; then seeds + medicine.','一种方案：起重机＋清水；木梁＋电池；种子＋药箱。')];
 else if(stage==='power')list=[t('Start at G. A wire must point toward the next tile, and that tile must point back.','从 G 开始，线路要朝向下一格，而下一格也要朝回来。'),hard()?t('The central three-way piece needs one arm toward G, one up, and one down.','中央三岔接头需要一端朝向 G，一端向上，一端向下。'):t('From G, go right twice, up twice, then right to the station.','从 G 向右两格，再向上两格，最后向右到站点。'),hard()?t('From the junction: up → right → right → up. The second branch goes down → right → right → down.','从三岔接头：上→右→右→上；另一支：下→右→右→下。'):t('Test after each change to see how far the current travels.','每改一处就测试一次，看看电流走了多远。')];
 else list=[t('Look for a repeated shape in the road. Turning changes direction, not position.','观察道路里重复的形状。转弯只改变朝向，不会移动。'),hard()?t('Each stair-shaped section uses: two forward, left, two forward, pick up, right.','每一段阶梯都能用：前进两次、左转、前进两次、拾取、右转。'):t('Try: Forward, Forward, Left, Forward, Forward, Pick up.','试试：前进、前进、左转、前进、前进、拾取。'),hard()?t('Put F, F, If blocked: left, F, F, Pick up, Right in Repeat body. Put one Repeat ×2 in Main.','循环内容放：前进、前进、遇障碍左转、前进、前进、拾取、右转。主程序只放“重复 ×2”。'):t('Tap a code block to remove it. Run again to test your change.','点击指令块可以删除，重新运行来测试修改。')];
 hintText=list[Math.min(c.hints-1,list.length-1)];save();render();}
function resetStage(stage){cancel();campaign()[stage]=L.newCampaign(state.mode)[stage];notice=null;hintText='';powerResult=null;save();render();}
document.addEventListener('click',event=>{const b=event.target.closest('button[data-action]');if(!b||b.disabled)return;const {action,value}=b.dataset;const c=campaign();
 switch(action){
 case 'nav':navigate(value);break;
 case 'library':document.getElementById('missions')?.scrollIntoView({block:'start'});break;
 case 'lang':state.lang=state.lang==='en'?'zh':'en';notice=null;hintText='';save();render();break;
 case 'mode':if(L.ids.includes(value)){cancel();state.mode=value;notice=null;hintText='';powerResult=null;editor='main';save();render();}break;
 case 'level':{const [mode,stage]=value.split(':');if(L.ids.includes(mode)&&['cargo','power','robot'].includes(stage)){state.mode=mode;editor='main';save();navigate(stage);}break;}
 case 'cargo':{if(busy||c.cargo.done)return;const i=Number(value);if(!Number.isInteger(i)||!cargoConfig().items[i]||c.cargo.delivered.includes(i))return;const load=c.cargo.load;c.cargo.load=load.includes(i)?load.filter(x=>x!==i):load.concat(i);notice=null;save();render();break;}
 case 'launch':launch();break;
 case 'undoCargo':if(!busy&&c.cargo.trips.length){const trip=c.cargo.trips.pop();c.cargo.delivered=c.cargo.delivered.filter(i=>!trip.includes(i));c.cargo.load=[];c.cargo.done=false;notice=null;save();render();}break;
 case 'wire':{const i=Number(value),cfg=L.powerConfig(state.mode);if(i===cfg.source||cfg.targets.includes(i)||cfg.fixed.includes(i)||!c.power.masks[i])return;c.power.masks[i]=E.rotate(c.power.masks[i]);c.power.turns++;c.power.done=false;powerResult=null;notice=null;save();render();break;}
 case 'testPower':testPower();break;
 case 'editor':editor=value;render();break;
 case 'add':if(!busy){cancel();if(c.robot[editor].length>=(editor==='main'?24:12)){say('This program tray is full. Try a repeat block.','指令区已满，试试循环指令。','error');render();break;}c.robot[editor].push(value);notice=null;save();render();}break;
 case 'remove':if(!busy){cancel();c.robot[editor].splice(Number(value),1);notice=null;save();render();}break;
 case 'runRobot':runRobot();break;
 case 'stepRobot':stepRobot();break;
 case 'stopRobot':c.robot.stops++;cancel();say('Stopped. Your code is still here to edit.','已停止，可以继续修改程序。');save();render();break;
 case 'hint':showHint(value);break;
 case 'reset':resetStage(value);break;
 case 'resetAll':if(window.confirm(t('Reset all three stations in this collection? Other collections are kept.','清除当前关卡组的三个站点进度？其他关卡组不会受到影响。'))){state.campaigns[state.mode]=L.newCampaign(state.mode);save();navigate('map');}break;
 }
});
document.addEventListener('change',event=>{if(event.target.id==='level-select'){const mode=event.target.value;if(L.ids.includes(mode)){state.mode=mode;editor='main';save();navigate(event.target.dataset.stage);}return;}if(event.target.id==='repeat-count'){cancel();campaign().robot.repeat=Number(event.target.value);save();render();}});
document.addEventListener('visibilitychange',()=>{if(document.hidden){cancel();save();render();}});
window.QuestGame={getCargoConfig:cargoConfig,getState:()=>JSON.parse(JSON.stringify(state)),getScreen:()=>screen,storageKey:KEY};
render();
})();
