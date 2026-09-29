"""Real Chromium DOM clicks with set_content, not an online navigation test.
Storage is simulated for recovery tests. No browser security policy is bypassed.
Run: python tests/browser.py (pip install playwright; CHROMIUM_PATH selects the browser)
"""
from pathlib import Path
import json,os
from datetime import datetime,timezone
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'artifacts'/'web-v6-legacy'
OUTPUT.mkdir(parents=True,exist_ok=True)
import re
html=(ROOT/'index.html').read_text()
html=re.sub(r'<link rel="stylesheet" href="([^"?]+)(?:\?[^\"]*)?">',lambda m:'<style>'+(ROOT/m.group(1)).read_text()+'</style>',html)
html=re.sub(r'<script src="([^"?]+)(?:\?[^\"]*)?"></script>',lambda m:'<script>'+(ROOT/m.group(1)).read_text()+'</script>',html)
PART=os.environ.get("TEST_PART","all");results=[];errors=[]
def rec(name): results.append({'name':name,'status':'PASS'});print('PASS',name,flush=True)
def load(b,width=390,store=None,denied=False):
 ctx=b.new_context(viewport={'width':width,'height':844 if width<800 else 900},has_touch=width<800)
 page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 if denied:page.evaluate("Object.defineProperty(window,'localStorage',{configurable:true,get(){throw new Error('Storage unavailable')}})")
 else:page.evaluate("""data=>{window.testStore={...data};Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem(k){return window.testStore[k]??null},setItem(k,v){window.testStore[k]=String(v)}}})}""",store or {})
 page.set_content(html,wait_until='load');page.locator('[data-action="mode"][data-value="engineer"]').click();return ctx,page

def click(p,a,v=None):
 q=f'[data-action="{a}"]'+(f'[data-value="{v}"]' if v is not None else '')
 p.locator(q).first.click(timeout=5000)
def state(p):return p.evaluate('QuestGame.getState()')
def nooverflow(p):assert p.evaluate('document.documentElement.scrollWidth<=innerWidth'),p.evaluate('document.documentElement.scrollWidth')
def voyage(p,ids,n,mode='engineer'):
 for i in ids:click(p,'cargo',i)
 click(p,'launch');p.wait_for_function('(x)=>QuestGame.getState().campaigns[x.mode].cargo.trips.length===x.n',arg={'mode':mode,'n':n},timeout=4000)
def solvepower(p,mode):
 click(p,'nav','power');click(p,'testPower');expect(p.locator('#feedback')).to_contain_text('Only 0')
 cfg=p.evaluate(f"QuestEngine.powerConfig('{mode}')")
 for i,target in enumerate(cfg['solution']):
  if i==cfg['source'] or i in cfg['targets']:continue
  for _ in range(4):
   if state(p)['campaigns'][mode]['power']['masks'][i]==target:break
   click(p,'wire',i)
 click(p,'testPower');assert state(p)['campaigns'][mode]['power']['done']
def solvebot(p,mode):
 click(p,'nav','robot');click(p,'runRobot');expect(p.locator('#feedback')).to_contain_text('Add commands')
 click(p,'add','F');click(p,'add','F');click(p,'add','F');click(p,'runRobot')
 p.wait_for_function("document.querySelector('#feedback')?.textContent.includes('edge')",timeout=4000)
 click(p,'reset','robot')
 if mode=='engineer':
  click(p,'editor','body')
  for cmd in ['F','F','I','F','F','P','R']:click(p,'add',cmd)
  click(p,'editor','main');click(p,'add','Q')
 else:
  click(p,'editor','main')
  for cmd in ['F','F','L','F','F','P']:click(p,'add',cmd)
 click(p,'runRobot')
 p.wait_for_function(f"QuestGame.getState().campaigns.{mode}.robot.done",timeout=12000)
 assert state(p)['campaigns'][mode]['robot']['best']==(8 if mode=='engineer' else 6)
 nooverflow(p)

with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,chromium_sandbox=True,timeout=15000)
 version=b.version
 for width in ([int(PART)] if PART in ['390','1280'] else [390,1280] if PART=='all' else []):
  ctx,p=load(b,width);nooverflow(p);p.screenshot(path=str(OUTPUT/f'map-{width}.png'),full_page=True)
  click(p,'nav','cargo');click(p,'launch');expect(p.locator('#feedback')).to_contain_text('empty')
  click(p,'cargo',1);click(p,'launch');expect(p.locator('#feedback')).to_contain_text('crane must');click(p,'cargo',1)
  for i in [0,2]:click(p,'cargo',i)
  click(p,'launch');expect(p.locator('#feedback')).to_contain_text('Too heavy')
  for i in [0,2]:click(p,'cargo',i)
  for i in [2,3]:click(p,'cargo',i)
  click(p,'launch');expect(p.locator('#feedback')).to_contain_text('cannot share')
  for i in [2,3]:click(p,'cargo',i)
  rec(f'{width}px cargo: empty, precedence, overload and incompatible cargo rejected')
  voyage(p,[0,3],1);voyage(p,[1,2],2);voyage(p,[4,5],3)
  assert state(p)['campaigns']['engineer']['cargo']['done'];nooverflow(p)
  rec(f'{width}px cargo: all supplies delivered in three voyages')
  click(p,'undoCargo');assert not state(p)['campaigns']['engineer']['cargo']['done'];voyage(p,[4,5],3)
  rec(f'{width}px cargo: successful voyage undo and retry')
  solvepower(p,'engineer');p.screenshot(path=str(OUTPUT/f'power-{width}.png'),full_page=True)
  rec(f'{width}px power: rotate through DOM clicks, test both targets')
  solvebot(p,'engineer');p.screenshot(path=str(OUTPUT/f'robot-{width}.png'),full_page=True)
  rec(f'{width}px robot: empty program, collision, loop+condition success with 8 blocks')
  click(p,'nav','map');expect(p.locator('.map-footer')).to_contain_text('3/3');nooverflow(p)
  click(p,'nav','parents');assert p.locator('.report-card').count()==3;nooverflow(p)
  rec(f'{width}px completion map and actual parent counters')
  stored=p.evaluate('window.testStore');ctx.close()
  ctx,p=load(b,width,store=stored);assert all(state(p)['campaigns']['engineer'][k]['done'] for k in ['cargo','power','robot'])
  click(p,'mode','explorer');assert not state(p)['campaigns']['explorer']['cargo']['done'];click(p,'mode','engineer');assert state(p)['campaigns']['engineer']['cargo']['done']
  click(p,'lang');assert p.locator('html').get_attribute('lang')=='zh-CN'
  for stage in ['cargo','power','robot','parents','map']:click(p,'nav',stage);nooverflow(p)
  rec(f'{width}px simulated storage recovery, independent modes and Chinese screens')
  ctx.close()
 if PART in ['all','explorer']:
  # Simpler level, actual click flow.
  ctx,p=load(b);click(p,'mode','explorer');click(p,'nav','cargo');voyage(p,[0,3,4],1,'explorer');voyage(p,[1,2,5],2,'explorer');solvepower(p,'explorer');solvebot(p,'explorer')
  rec('Explorer: two-voyage cargo, single-target circuit, six-command robot completion');ctx.close()
 if PART in ['all','extra']:
  # Trip budget, cancel while animating, hint progression.
  ctx,p=load(b);click(p,'nav','cargo');voyage(p,[0],1);voyage(p,[1],2);voyage(p,[2],3);click(p,'cargo',3);click(p,'launch');expect(p.locator('#feedback')).to_contain_text('No voyages');click(p,'undoCargo');assert len(state(p)['campaigns']['engineer']['cargo']['trips'])==2
  for _ in range(3):click(p,'hint','cargo')
  expect(p.locator('.hint')).to_contain_text('One plan');rec('Three-voyage limit, recoverable planning failure and progressive hints')
  click(p,'reset','cargo');click(p,'cargo',0);click(p,'launch');click(p,'nav','robot');p.wait_for_timeout(900);assert not state(p)['campaigns']['engineer']['cargo']['trips'];rec('Navigation cancels in-flight voyage without hidden completion')
  click(p,'add','F');click(p,'add','F');click(p,'stepRobot');assert p.locator('[data-rover="5,1"]').count()==1;click(p,'stepRobot');assert p.locator('[data-rover="5,2"]').count()==1
  click(p,'runRobot');click(p,'stopRobot');p.wait_for_timeout(750);assert p.locator('[data-rover="5,0"]').count()==1
  rec('Robot: single-step, rerun and stop cancel pending animation');ctx.close()
 if PART in ['all','storage']:
  # Storage errors must not prevent interaction.
  ctx,p=load(b,denied=True);click(p,'nav','cargo');voyage(p,[0,3],1);click(p,'nav','parents');expect(p.locator('#view')).to_contain_text('storage is unavailable');rec('Storage denied: game works with explicit non-persistence notice');ctx.close()
  for stored in [{'questly-storm-v3':'not json'},{'questly-storm-v3':'{"version":3,"lang":"en","mode":"engineer","campaigns":{}}'}]:
   ctx,p=load(b,store=stored);assert state(p)['version']==6;click(p,'nav','robot');nooverflow(p);assert p.evaluate('window.testStore["questly-storm-v3"]')==stored['questly-storm-v3'];ctx.close()
  rec('Malformed and structurally invalid legacy saves are preserved while a separate new game works')
  ctx,p=load(b,320)
  for stage in ['cargo','power','robot','parents','map']:click(p,'nav',stage);nooverflow(p)
  rec('320px viewport: no horizontal overflow on every screen');ctx.close()
 assert not errors,errors
 rec('No uncaught JavaScript errors in all exercised browser cases')
 b.close()
report={'tested_at_utc':datetime.now(timezone.utc).isoformat(),'browser':'Chromium '+version,'scope':'Real Chromium DOM clicks with set_content; storage explicitly simulated; sizes 320, 390 and 1280 CSS pixels. Not a physical device or real-origin storage test.','not_verified':['iPhone Safari / WebKit','Live HTTPS browser clicking','Real-origin storage across browser restarts'],'results':results,'errors':errors}
(OUTPUT/f'browser-results-{PART}.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'passed':len(results),'errors':errors}))
