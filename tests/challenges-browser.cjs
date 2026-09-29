/* Real HTTP navigation and real-origin localStorage in sandboxed Chrome. No injected game mutations. */
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const http=require('node:http');
const crypto=require('node:crypto');
const {chromium}=require('playwright');
const E=require('../storm-engine.js'),L=require('../storm-levels.js'),S=require('../storm-save.js');
const {searchCargo,robotPrograms}=require('./challenges.test.cjs');
const root=path.resolve(__dirname,'..'),output=path.join(root,'artifacts/web-v6');
fs.mkdirSync(output,{recursive:true});
const results=[],errors=[];
const record=name=>{results.push({name,status:'PASS'});console.log('PASS',name);};
const server=http.createServer((request,response)=>{
 const url=new URL(request.url,'http://localhost');
 if(url.pathname==='/storage-fixture'){response.setHeader('Content-Type','text/html');response.end('<!doctype html><title>Storage fixture</title>');return;}
 const relative=url.pathname==='/'?'index.html':decodeURIComponent(url.pathname.slice(1));
 const file=path.resolve(root,relative);
 if(!file.startsWith(root+path.sep)||!fs.existsSync(file)||!fs.statSync(file).isFile()){response.writeHead(404);response.end();return;}
 response.setHeader('Content-Type',file.endsWith('.js')?'text/javascript; charset=utf-8':file.endsWith('.css')?'text/css; charset=utf-8':'text/html; charset=utf-8');
 response.setHeader('Cache-Control','no-store');response.end(fs.readFileSync(file));
});
const click=(p,action,value)=>p.locator(`[data-action="${action}"]${value===undefined?'':`[data-value="${value}"]`}`).first().click();
const state=p=>p.evaluate(()=>QuestGame.getState());
async function select(p,mode,stage){await click(p,'nav','map');await click(p,'chapter',Math.floor(L.ids.indexOf(mode)/5));await click(p,'level',mode+':'+stage);}
async function noOverflow(p){assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);}
async function screen(p,name){await p.screenshot({path:path.join(output,name+'.png'),fullPage:true});}
async function ready(p){await p.waitForFunction(()=>window.QuestVisual?.version==='0.6.0');}
async function solveCargo(p,mode){
 await select(p,mode,'cargo');const trips=searchCargo(L.cargoConfig(mode));
 for(const [index,trip] of trips.entries()){
  for(const id of trip)await click(p,'cargo',id);
  await click(p,'launch');await p.waitForFunction(({mode,count})=>QuestGame.getState().campaigns[mode].cargo.trips.length===count,{mode,count:index+1});
 }
 assert.equal((await state(p)).campaigns[mode].cargo.done,true);await noOverflow(p);
}
async function solvePower(p,mode){
 await select(p,mode,'power');const cfg=L.powerConfig(mode);
 await click(p,'testPower');
 for(let id=0;id<cfg.solution.length;id++){
  let mask=(await state(p)).campaigns[mode].power.masks[id];
  for(let turn=0;mask!==cfg.solution[id]&&turn<4;turn++){
   await click(p,'wire',id);mask=E.rotate(mask);
  }
 }
 await click(p,'testPower');assert.equal((await state(p)).campaigns[mode].power.done,true);await noOverflow(p);
}
async function solveRobot(p,mode){
 await select(p,mode,'robot');const code=robotPrograms[mode];
 if(code.body.length){await click(p,'editor','body');for(const op of code.body)await click(p,'add',op);}
 await click(p,'editor','main');for(const op of code.main)await click(p,'add',op);
 await p.selectOption('#repeat-count',String(code.repeat));
 await click(p,'runRobot');await p.waitForFunction(mode=>QuestGame.getState().campaigns[mode].robot.done,mode,{timeout:60000});
 assert.equal((await state(p)).campaigns[mode].robot.best,E.codeSize(code.main,code.body));await noOverflow(p);
}
async function main(){
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 const origin=`http://127.0.0.1:${server.address().port}`;
 const options={headless:true,chromiumSandbox:true,executablePath:process.env.CHROMIUM_PATH||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'};
 let browser=await chromium.launch(options);
 const attach=p=>p.on('pageerror',error=>errors.push(error.message));
 try{
  const context=await browser.newContext({viewport:{width:390,height:844},hasTouch:true}),p=await context.newPage();attach(p);
  await p.goto(origin);await ready(p);
  assert.equal(await p.locator('.mission-choice').count(),90);
  await click(p,'library');assert.ok(await p.locator('#missions').evaluate(el=>Math.abs(el.getBoundingClientRect().top)<2));
  await screen(p,'missions-en-390');record('HTTP home presents all 90 mission entries in six chapters with a direct library shortcut on phone');
  for(const chapter of [0,1,2,3,4,5]){await click(p,'chapter',chapter);assert.equal(await p.locator('.mission-choice:visible').count(),15);}
  record('Six ordered chapters each expose five missions per workshop, all freely selectable');
  for(const mode of L.ids){
   await solveCargo(p,mode);record(`${mode}: cargo completed using real buttons`);
   await solvePower(p,mode);record(`${mode}: circuit completed by rotating real tiles`);
   await solveRobot(p,mode);record(`${mode}: robot program built and run through real controls`);
  }
  await select(p,'summit','cargo');await click(p,'undoCargo');assert.equal((await state(p)).campaigns.summit.cargo.done,false);
  assert.equal((await state(p)).campaigns.beacon.cargo.done,true);
  await p.selectOption('#level-select','beacon');assert.equal((await state(p)).campaigns.beacon.cargo.done,true);
  record('Undo and mission selector isolate progress between challenges');
  await select(p,'summit','cargo');await screen(p,'summit-cargo-en-390');
  await click(p,'lang');await screen(p,'summit-cargo-zh-390');
  await select(p,'summit','power');await screen(p,'summit-power-zh-390');
  await select(p,'summit','robot');await screen(p,'summit-robot-zh-390');
  await click(p,'nav','map');await screen(p,'missions-zh-390');
  const before=await state(p);await p.reload();await ready(p);assert.deepEqual(await state(p),before);
  record('Real localStorage restores all mission histories and language after HTTP reload');
  await context.close();
  // A persistent Chrome profile verifies a full browser shutdown/relaunch, not storage-state injection.
  await browser.close();browser=null;
  const profile=fs.mkdtempSync(path.join(output,'profile-'));
  let disk=await chromium.launchPersistentContext(profile,{...options,viewport:{width:390,height:844}});
  let page=await disk.newPage();attach(page);await page.goto(origin);await ready(page);
  await select(page,'tides','cargo');await click(page,'cargo',7);await click(page,'lang');
  const persisted=await state(page);await disk.close();
  disk=await chromium.launchPersistentContext(profile,{...options,viewport:{width:390,height:844}});
  page=await disk.newPage();attach(page);await page.goto(origin);await ready(page);assert.deepEqual(await state(page),persisted);
  await disk.close();fs.rmSync(profile,{recursive:true,force:true});
  record('Entire Chrome process closes/reopens with real-origin saved selection, mission and Chinese intact');
  browser=await chromium.launch(options);
  // Seed only storage fixtures. All gameplay remains DOM-driven.
  // Seed on a blank same-origin page: hiding a running game intentionally flushes its current save.
  const legacyContext=await browser.newContext(),legacyPage=await legacyContext.newPage();attach(legacyPage);await legacyPage.goto(origin+'/storage-fixture');
  const legacy={version:3,lang:'zh',mode:'engineer',campaigns:{explorer:E.newCampaign('explorer'),engineer:E.newCampaign('engineer')}};
  legacy.campaigns.engineer.cargo.load=[0,3];const original=JSON.stringify(legacy);
  await legacyPage.evaluate(text=>{localStorage.clear();localStorage.setItem('questly-storm-v3',text);},original);
  await legacyPage.goto(origin);await ready(legacyPage);
  assert.deepEqual((await state(legacyPage)).campaigns.engineer.cargo.load,[0,3]);
  await select(legacyPage,'tides','cargo');await click(legacyPage,'cargo',7);
  assert.equal(await legacyPage.evaluate(()=>localStorage.getItem('questly-storm-v3')),original);
  assert.deepEqual((await state(legacyPage)).campaigns.engineer.cargo.load,[0,3]);
  record('Original v3 storage migrates without altering its bytes; new mission actions preserve legacy progress');
  for(const invalid of ['broken-json','null']){
   await legacyPage.goto(origin+'/storage-fixture');
   await legacyPage.evaluate(text=>localStorage.setItem('questly-storm-v6',text),invalid);
   await legacyPage.goto(origin);await ready(legacyPage);await select(legacyPage,'tides','cargo');await click(legacyPage,'cargo',7);
   assert.equal(await legacyPage.evaluate(()=>localStorage.getItem('questly-storm-v6')),invalid);
  }
  record('Malformed current save is visibly protected and never overwritten during session play');
  await legacyPage.goto(origin+'/storage-fixture');
  const previousText=JSON.stringify(require('./fixtures/web-v5.json').save);
  await legacyPage.evaluate(text=>{localStorage.clear();localStorage.setItem('questly-storm-v5',text);},previousText);
  await legacyPage.goto(origin);await ready(legacyPage);
  assert.equal((await state(legacyPage)).version,6);
  for(const id of ['explorer','engineer','tides','ridge','beacon','summit'])for(const stage of ['cargo','power','robot'])assert.equal((await state(legacyPage)).campaigns[id][stage].done,true);
  await select(legacyPage,'islandheart','cargo');await click(legacyPage,'cargo',0);
  assert.equal(await legacyPage.evaluate(()=>localStorage.getItem('questly-storm-v5')),previousText);
  await legacyPage.reload();await ready(legacyPage);assert.deepEqual((await state(legacyPage)).campaigns.islandheart.cargo.load,[0]);
  assert.equal((await state(legacyPage)).campaigns.summit.robot.done,true);
  record('Released v5 save preserves all 18 completions byte-for-byte while a new mission survives reload');
  await legacyContext.close();
  // In-flight cancellation must not complete in a different collection or after Stop.
  const cancelContext=await browser.newContext(),cancelPage=await cancelContext.newPage();attach(cancelPage);await cancelPage.goto(origin);await ready(cancelPage);
  await select(cancelPage,'tides','cargo');await click(cancelPage,'cargo',0);await click(cancelPage,'launch');
  await cancelPage.selectOption('#level-select','ridge');await cancelPage.waitForTimeout(900);
  assert.equal((await state(cancelPage)).campaigns.tides.cargo.trips.length,0);
  await select(cancelPage,'tides','robot');await click(cancelPage,'add','F');await click(cancelPage,'runRobot');await click(cancelPage,'stopRobot');await cancelPage.waitForTimeout(500);
  assert.equal(await cancelPage.locator('[data-rover="7,0"]').count(),1);
  record('Changing a mission cancels pending voyage; robot Stop cancels the runner');
  await cancelContext.close();
  // Responsive/localization/motion matrix includes the largest new boards in both languages.
  for(const width of [320,390,768,1280]){
   const ctx=await browser.newContext({viewport:{width,height:900},reducedMotion:'reduce'}),view=await ctx.newPage();attach(view);await view.goto(origin);await ready(view);
   assert.equal(await view.locator('[data-visual="motion"]').isDisabled(),true);
   assert.equal(await view.evaluate(()=>QuestVisual.hasAudioContext()),false);
   for(const language of ['en','zh']){
    if(language==='zh')await click(view,'lang');
    for(const stage of ['map','cargo','power','robot','parents']){
     if(stage==='map'||stage==='parents')await click(view,'nav',stage);else await select(view,stage==='power'?'islandheart':'summit',stage);
     await noOverflow(view);
     assert.equal(await view.locator('.q-toolbar').count(),1);
     if(stage==='power'){
      const tiles=await view.locator('.wire:not(:disabled)').evaluateAll(elements=>elements.map(e=>e.getBoundingClientRect().width));
      assert.ok(tiles.every(size=>size>=43.9),'Rotatable tiles remain at least 44 CSS px wide');
     }
    }
   }
   await select(view,'islandheart','cargo');for(let hint=0;hint<3;hint++)await click(view,'hint','cargo');assert.ok((await view.locator('.hint').innerText()).length>30);
   await select(view,'horizon','robot');for(let hint=0;hint<3;hint++)await click(view,'hint','robot');assert.ok((await view.locator('.hint').innerText()).length>30);await noOverflow(view);
   if(width===390){await select(view,'islandheart','power');await screen(view,'chapter6-power-zh-390');await select(view,'islandheart','cargo');await screen(view,'chapter6-cargo-zh-390');await select(view,'horizon','robot');await screen(view,'chapter6-robot-zh-390');}
   if(width===1280){await click(view,'nav','map');await screen(view,'missions-zh-1280');await select(view,'summit','power');await screen(view,'summit-power-zh-1280');}
   record(`${width}px: both languages, all screens fit, 44px wire targets, reduced motion and sound-off default`);
   await ctx.close();
  }
  assert.deepEqual(errors,[]);record('No uncaught page errors across exercised HTTP flows');
 }finally{if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}
 const hashes=Object.fromEntries(['storm-content.js','index.html','storm-engine.js','storm-levels.js','storm-save.js','storm-app.js','storm.css','storm-visual.js','storm-visual.css'].map(file=>[file,crypto.createHash('sha256').update(fs.readFileSync(path.join(root,file))).digest('hex')]));
 fs.writeFileSync(path.join(output,'browser-report.json'),JSON.stringify({testedAt:new Date().toISOString(),scope:'Sandboxed desktop Chrome via HTTP, real-origin storage and real process relaunch; CSS viewports are not physical iPhone/iPad evidence',results,errors,hashes},null,2));
 console.log(JSON.stringify({passed:results.length,output}));
}
main().catch(error=>{console.error(error);server.close();process.exitCode=1;});
