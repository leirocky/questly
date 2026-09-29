// Re-run against deployed Pages; the reference directory must contain the tested web v0.6 tree.
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),os=require('node:os'),crypto=require('node:crypto');
const {chromium}=require('playwright');
const root=path.resolve(process.argv[2]),out=path.resolve(process.argv[3]),url='https://leirocky.github.io/questly/';
const E=require(path.join(root,'storm-engine.js')),L=require(path.join(root,'storm-levels.js'));
const {searchCargo,robotPrograms}=require(path.join(root,'tests/challenges.test.cjs'));
fs.mkdirSync(out,{recursive:true});
const results=[],errors=[],failedResponses=[],hashes={};
const record=name=>{results.push({name,status:'PASS'});console.log('PASS',name);};
const click=(p,action,value)=>p.locator(`[data-action="${action}"]${value===undefined?'':`[data-value="${value}"]`}`).first().click();
const state=p=>p.evaluate(()=>QuestGame.getState());
const ready=p=>p.waitForFunction(()=>window.QuestVisual?.version==='0.6.0');
async function select(p,mode,stage){await click(p,'nav','map');await click(p,'chapter',Math.floor(L.ids.indexOf(mode)/5));await click(p,'level',mode+':'+stage);}
async function run(){
 const profile=fs.mkdtempSync(path.join(os.tmpdir(),'questly-pages-test-'));
 const options={headless:true,chromiumSandbox:true,executablePath:process.env.CHROMIUM_PATH||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',viewport:{width:390,height:844},reducedMotion:'reduce'};
 let ctx;
 try{
  ctx=await chromium.launchPersistentContext(profile,options);
  const p=await ctx.newPage();p.on('pageerror',e=>errors.push(e.message));p.on('response',r=>{if(r.status()>=400)failedResponses.push({url:r.url(),status:r.status()});});
  await p.goto(url,{waitUntil:'networkidle'});await ready(p);
  for(const file of ['storm-content.js','index.html','storm-engine.js','storm-levels.js','storm-save.js','storm-app.js','storm.css','storm-visual.js','storm-visual.css']){
   const res=await ctx.request.get(new URL(file,url).href);assert.equal(res.status(),200);
   const deployed=crypto.createHash('sha256').update(await res.body()).digest('hex');
   const local=crypto.createHash('sha256').update(fs.readFileSync(path.join(root,file))).digest('hex');
   assert.equal(deployed,local,file+' differs from tested tree');hashes[file]=deployed;
  }
  record('All nine deployed frontend files return HTTP 200 and match tested SHA-256 hashes');
  assert.equal(await p.locator('.mission-choice').count(),90);record('Live HTTPS home has 90 playable entries');
  for(const mode of L.ids){
   await select(p,mode,'cargo');
   for(const [index,trip] of searchCargo(L.cargoConfig(mode)).entries()){
    for(const id of trip)await click(p,'cargo',id);
    await click(p,'launch');await p.waitForFunction(({mode,count})=>QuestGame.getState().campaigns[mode].cargo.trips.length===count,{mode,count:index+1});
   }
   assert.equal((await state(p)).campaigns[mode].cargo.done,true);record(mode+': live cargo completed through buttons');
   await select(p,mode,'power');const cfg=L.powerConfig(mode);
   for(let id=0;id<cfg.solution.length;id++){
    let mask=(await state(p)).campaigns[mode].power.masks[id];
    for(let turn=0;mask!==cfg.solution[id]&&turn<4;turn++){await click(p,'wire',id);mask=E.rotate(mask);}
   }
   await click(p,'testPower');assert.equal((await state(p)).campaigns[mode].power.done,true);record(mode+': live circuit completed through tiles');
   await select(p,mode,'robot');const code=robotPrograms[mode];
   if(code.body.length){await click(p,'editor','body');for(const op of code.body)await click(p,'add',op);}
   await click(p,'editor','main');for(const op of code.main)await click(p,'add',op);
   await p.selectOption('#repeat-count',String(code.repeat));
   const autoplay=L.ids.indexOf(mode)%5===4;
   if(autoplay){await click(p,'runRobot');await p.waitForFunction(mode=>QuestGame.getState().campaigns[mode].robot.done,mode,{timeout:60000});}
   else{const steps=E.simulate(L.robotConfig(mode),code.main,code.body,code.repeat).trace.length;for(let step=0;step<steps;step++)await click(p,'stepRobot');assert.equal((await state(p)).campaigns[mode].robot.done,true);}
   record(mode+': live robot completed through '+(autoplay?'Run':'Step')+' controls');
  }
  await click(p,'lang');await select(p,'islandheart','cargo');
  assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
  await p.screenshot({path:path.join(out,'live-finale-zh-390.png'),fullPage:true});
  const saved=await state(p);await p.reload();await ready(p);assert.deepEqual(await state(p),saved);record('All 90 completions and Chinese survive live HTTPS reload');
  await ctx.close();ctx=await chromium.launchPersistentContext(profile,options);
  const reopened=await ctx.newPage();reopened.on('pageerror',e=>errors.push(e.message));await reopened.goto(url,{waitUntil:'networkidle'});await ready(reopened);
  assert.deepEqual(await state(reopened),saved);record('Real Chrome shutdown/relaunch restores all 90 completions, mission and language on public origin');
  await reopened.setViewportSize({width:1280,height:900});await click(reopened,'nav','map');
  await reopened.screenshot({path:path.join(out,'live-missions-zh-1280.png'),fullPage:true});
  assert.deepEqual(errors,[]);assert.deepEqual(failedResponses,[]);record('No uncaught page errors or failed HTTP responses during exercised live flows');
  fs.writeFileSync(path.join(out,'live-report.json'),JSON.stringify({testedAt:new Date().toISOString(),url,mergeCommit:process.env.RELEASE_COMMIT||'not supplied',node:process.version,browser:await ctx.browser().version(),scope:'Sandboxed desktop Chrome over public HTTPS; isolated real disk profile; not physical-device or Safari evidence',results,errors,failedResponses,hashes},null,2));
 }finally{if(ctx)await ctx.close();fs.rmSync(profile,{recursive:true,force:true});}
 console.log(JSON.stringify({passed:results.length,out}));
}
run().catch(e=>{console.error(e);process.exitCode=1;});
