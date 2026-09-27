"""Presentation regression. set_content is not an HTTPS/Safari test; storage is simulated."""
from pathlib import Path
import json,re,os
from datetime import datetime,timezone
from playwright.sync_api import sync_playwright,expect
R=Path(__file__).resolve().parents[1]
OUTPUT=R/'artifacts'/'web-v5-legacy'
OUTPUT.mkdir(parents=True,exist_ok=True)
h=(R/'index.html').read_text()
h=re.sub(r'<link rel="stylesheet" href="([^"?]+)(?:\?[^\"]*)?">',lambda m:'<style>'+(R/m.group(1)).read_text()+'</style>',h)
h=re.sub(r'<script src="([^"?]+)(?:\?[^\"]*)?"></script>',lambda m:'<script>'+(R/m.group(1)).read_text()+'</script>',h)
results=[];errors=[]
def rec(n):results.append({'name':n,'status':'PASS'});print('PASS',n,flush=True)
def boot(b,width=390,store=None,reduce=False):
 c=b.new_context(viewport={'width':width,'height':844},reduced_motion='reduce' if reduce else 'no-preference')
 p=c.new_page();p.on('pageerror',lambda e:errors.append(str(e)))
 p.evaluate("""d=>{window.testStore={...d};Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem(k){return testStore[k]??null},setItem(k,v){testStore[k]=String(v)}}});}""",store or {})
 p.set_content(h);p.wait_for_function("window.QuestVisual?.version==='0.5.0'");return c,p

def nav(p,s):p.locator(f'[data-action="nav"][data-value="{s}"]').first.click()
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,chromium_sandbox=True)
 c,p=boot(b)
 assert not p.evaluate('QuestVisual.hasAudioContext()');assert not p.evaluate('QuestVisual.getPreferences().sound')
 rec('Sound starts off; no AudioContext is created without opt-in')
 original=p.evaluate('QuestGame.getState()')
 for i in range(6):p.locator('[data-visual="motion"]').click()
 assert p.locator('.q-island-art').count()==1;assert p.locator('.q-buddy').count()==1;assert p.locator('.q-toolbar').count()==1
 assert p.evaluate('QuestGame.getState()')==original
 rec('Repeated animation toggles do not duplicate artwork or modify campaign state')
 p.locator('[data-visual="sound"]').click();p.wait_for_timeout(220)
 assert p.evaluate('QuestVisual.hasAudioContext()');assert p.evaluate('QuestVisual.getPreferences().sound')
 p.locator('[data-visual="sound"]').click();assert not p.evaluate('QuestVisual.getPreferences().sound')
 rec('Sound control opts into local synthesis, then mutes; no external audio asset')
 p.locator('[data-visual="motion"]').click();assert p.locator('body').evaluate("e=>e.classList.contains('q-reduce')")
 rec('Animation opt-out sets reduced mode without blocking interaction')
 saved=p.evaluate('window.testStore');c.close();c,p=boot(b,store=saved)
 assert not p.evaluate('QuestVisual.getPreferences().motion');nav(p,'cargo')
 p.locator('[data-action="cargo"][data-value="0"]').click();p.locator('[data-action="launch"]').click()
 p.wait_for_function('QuestGame.getState().campaigns.engineer.cargo.trips.length===1')
 rec('Visual preferences restore from simulated storage; a voyage still completes with motion off')
 nav(p,'power');p.locator('[data-action="testPower"]').click();assert p.locator('.q-power-unit').count()==2
 assert p.locator('.q-power-unit.online').count()==p.locator('.wire.target.lit').count()
 for i in range(4):p.locator('[data-visual="motion"]').click()
 assert p.locator('.q-power-units').count()==1
 rec('Power preview follows tested connectivity; toggles cannot duplicate station panels')
 c.close();c,p=boot(b,reduce=True)
 expect(p.locator('[data-visual="motion"]')).to_be_disabled();assert p.evaluate('QuestVisual.getPreferences().reducedBySystem')
 assert p.locator('.q-turbine').evaluate("e=>getComputedStyle(e).animationName")=='none'
 nav(p,'robot');p.locator('[data-action="add"][data-value="F"]').click();p.locator('[data-action="stepRobot"]').click();assert p.locator('[data-rover="5,1"]').count()==1
 rec('System reduced-motion is respected; robot single-step remains functional');c.close()
 for width in [320,390,768,1280]:
  c,p=boot(b,width)
  for lang in ['en','zh']:
   if lang=='zh':p.locator('[data-action="lang"]').click()
   for stage in ['map','cargo','power','robot','parents']:
    nav(p,stage)
    assert p.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,lang,stage)
    assert p.locator('.q-toolbar').count()==1
  rec(f'{width}px English and Chinese: all five screens fit without horizontal overflow')
  if width in [390,1280]:
   nav(p,'map');p.wait_for_timeout(400);p.screenshot(path=str(OUTPUT/f'visual-map-zh-{width}.png'),full_page=True)
   p.locator('[data-action="lang"]').click()
   for stage in ['map','cargo','power','robot']:
    nav(p,stage);p.wait_for_timeout(400);p.screenshot(path=str(OUTPUT/f'visual-{stage}-{width}.png'),full_page=True)
  c.close()
 assert not errors,errors;rec('No uncaught JavaScript errors during visual and accessibility checks')
 b.close()
(OUTPUT/'visual-results.json').write_text(json.dumps({'tested_at_utc':datetime.now(timezone.utc).isoformat(),'scope':'Sandboxed Chromium DOM tests; simulated storage; no real iPhone or live HTTPS navigation','results':results,'errors':errors},indent=2))
