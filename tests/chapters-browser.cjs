/* Final fresh-page UI audit. Navigation fixtures are synthetic completed saves, not play evidence. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const {chromium}=require('playwright');
const E=require('../storm-engine'),L=require('../storm-levels'),S=require('../storm-save');
const root=path.resolve(__dirname,'..'),out=path.join(root,'artifacts/web-v6'),results=[];
const rec=name=>{results.push({name,status:'PASS'});console.log('PASS',name);};
const server=http.createServer((req,res)=>{
 const name=new URL(req.url,'http://local').pathname;
 if(name==='/fixture'){res.end('<title>Isolated save fixture</title>');return;}
 const file=path.resolve(root,name==='/'?'index.html':name.slice(1));
 if(!file.startsWith(root+'/')||!fs.existsSync(file)){res.writeHead(404);res.end();return;}
 res.setHeader('Content-Type',file.endsWith('.js')?'application/javascript':file.endsWith('.css')?'text/css':'text/html');res.end(fs.readFileSync(file));
});
const click=(p,a,v)=>p.locator(`[data-action="${a}"]${v===undefined?'':`[data-value="${v}"]`}`).first().click();
async function run(){
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const url=`http://127.0.0.1:${server.address().port}`;
 const browser=await chromium.launch({headless:true,chromiumSandbox:true,executablePath:process.env.CHROMIUM_PATH||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 try{
  const p=await browser.newPage({viewport:{width:390,height:844},reducedMotion:'reduce'}),errors=[];p.on('pageerror',e=>errors.push(e.message));
  await p.goto(url);await p.waitForFunction(()=>QuestVisual?.version==='0.6.0');
  assert.equal(await p.evaluate(()=>QuestGame.getState().mode),'explorer');
  assert.deepEqual(await p.evaluate(()=>QuestLevels.ids),L.ids);rec('Final catalog order matches the published source; new players begin on level one');
  for(const lang of ['en','zh']){
   if(lang==='zh')await click(p,'lang');
   for(const stage of ['cargo','power','robot']){
    await click(p,'nav',stage);
    for(const id of L.ids){
     await p.selectOption('#level-select',id);
     for(let i=0;i<3;i++)await click(p,'hint',stage);
     const text=await p.locator('.hint').innerText();assert.ok(text.length>15);assert.ok(!/undefined|NaN/.test(await p.locator('#view').innerText()),id);
     if(stage==='cargo'){assert.equal(await p.locator('.q-cargo-art').count()>=L.cargoConfig(id).items.length,true);assert.ok(!/undefined/.test(await p.locator('.inventory').innerHTML()),id+' crate art');}
     assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,id);
    }
   }
   rec(lang+': all 90 mission screens expose three readable hints without missing art or horizontal page overflow');
  }
  await p.setViewportSize({width:1280,height:900});await click(p,'nav','map');await click(p,'chapter',5);await p.screenshot({path:path.join(out,'final-chapter6-zh-1280.png'),fullPage:true});
  await p.setViewportSize({width:390,height:844});await click(p,'level','islandheart:cargo');await p.screenshot({path:path.join(out,'final-cargo-zh-390.png'),fullPage:true});
  // Construct valid synthetic all-complete saves solely to exercise every next-link and chapter boundary.
  const state=S.fresh(),answers=JSON.parse(fs.readFileSync(path.join(out,'rules-report.json'))).solutions;
  for(const id of L.ids){const c=state.campaigns[id],s=answers[id];Object.assign(c.cargo,{trips:s.cargo,delivered:s.cargo.flat(),done:true});Object.assign(c.power,{masks:s.power,done:true});Object.assign(c.robot,s.robot,{done:true,best:E.codeSize(s.robot.main,s.robot.body)});}
  assert.ok(S.valid(state));await p.goto(url+'/fixture');await p.evaluate(s=>localStorage.setItem('questly-storm-v6',JSON.stringify(s)),state);await p.goto(url);
  for(const stage of ['cargo','power','robot']){
   await click(p,'nav',stage);await p.selectOption('#level-select',L.ids[0]);
   for(let i=1;i<L.ids.length;i++){await p.locator('.success [data-action="level"]').click();assert.equal(await p.evaluate(()=>QuestGame.getState().mode),L.ids[i]);}
   await p.locator('.success [data-action="nav"]').click();assert.equal(await p.evaluate(()=>QuestGame.getScreen()),'map');
  }
  rec('Synthetic completed-save navigation: all 87 next-level links cross chapters correctly; all three finales return to the map');
  assert.deepEqual(errors,[]);rec('No uncaught errors in final-file chapter/hint/navigation audit');
  fs.writeFileSync(path.join(out,'chapter-report.json'),JSON.stringify({testedAt:new Date().toISOString(),scope:'Sandboxed desktop Chrome, final fresh HTTP files, hint/art/layout audit; next-link checks use a validated synthetic completed-save fixture and do not count as gameplay completions',results,errors},null,2));
 }finally{await browser.close();await new Promise(resolve=>server.close(resolve));}
}
run().catch(e=>{console.error(e);server.close();process.exitCode=1;});
