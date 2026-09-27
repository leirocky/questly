"""Browser DOM click tests. HTTP/HTTPS navigation is NOT tested by this suite.
Storage is explicitly simulated for persistence/rehydration cases.
Requires: pip install playwright; a Chromium executable.
Run: CHROMIUM_PATH=/path/to/chromium python tests/smoke.py
"""
from pathlib import Path
from datetime import datetime, timezone
import json, os
from playwright.sync_api import sync_playwright, expect
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'index.html').read_text()
results=[]
errors=[]

def load(context, storage=None, denied=False):
    page=context.new_page()
    page.on('pageerror',lambda e:errors.append(str(e)))
    if denied:
        page.evaluate("Object.defineProperty(window,'localStorage',{configurable:true,get(){throw new Error('Storage unavailable')}})")
    else:
        page.evaluate("""data=>{window.testStore={...data};Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem(k){return window.testStore[k]??null},setItem(k,v){window.testStore[k]=String(v)},removeItem(k){delete window.testStore[k]}}})}""",storage or {})
    page.set_content(HTML,wait_until='load')
    return page

def no_overflow(page):
    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), 'Horizontal overflow'

def play(page,retry=False):
    page.get_by_role('button',name='Try the first mission').click()
    expect(page.locator('#setup')).to_be_visible()
    page.get_by_role('button',name='Grade 1').click()
    page.get_by_role('button',name='Start 3-question warm-up').click()
    for answer in [1,2,0]:
        page.locator('#da button').nth(answer).click()
        expect(page.locator('#dnext')).to_be_visible()
        page.evaluate(f'doD({answer})')  # Deliberate duplicate handler invocation.
        page.get_by_role('button',name='Continue →',exact=True).click()
    expect(page.locator('#quest')).to_be_visible()
    no_overflow(page)
    for i,answer in enumerate([1,2,1,0]):
        if i==0 and retry:
            page.locator('#qa button').nth(0).click()
            expect(page.locator('#qf')).to_contain_text('Make 10 first')
            expect(page.locator('#qa button').nth(0)).to_be_disabled()
        page.locator('#qa button').nth(answer).click()
        expect(page.locator('#qnext')).to_be_visible()
        page.evaluate(f'doQ({answer})')
        page.locator('#qnext').click()
    expect(page.locator('#parent')).to_be_visible()
    expect(page.locator('#warm-result')).to_have_text('3/3')
    expect(page.locator('#first-result')).to_have_text('3/4' if retry else '4/4')
    expect(page.locator('#retry-result')).to_have_text('1' if retry else '0')
    no_overflow(page)

with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,
        args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu'],timeout=15000)
    version=browser.version
    for size in [{'width':390,'height':844},{'width':1280,'height':900}]:
        context=browser.new_context(viewport=size,has_touch=size['width']<600)
        page=load(context)
        no_overflow(page)
        page.get_by_role('button',name='Parent preview').click()
        expect(page.locator('#brief-title')).to_have_text('No session yet')
        page.get_by_role('button',name='← Home').click()
        page.screenshot(path=str(ROOT/'tests'/f"home-{size['width']}.png"),full_page=True)
        play(page,retry=True)
        results.append({'test':f"{size['width']}px: empty state, full click flow, hint, duplicate event guard, overflow",'status':'PASS'})
        page.screenshot(path=str(ROOT/'tests'/f"brief-{size['width']}.png"),full_page=True)
        stored=page.evaluate('window.testStore')
        page.close()
        page=load(context,storage=stored)
        page.get_by_role('button',name='Parent preview').click()
        expect(page.locator('#first-result')).to_have_text('3/4')
        results.append({'test':f"{size['width']}px: rehydrate a completed session from SIMULATED storage",'status':'PASS'})
        page.get_by_role('button',name='Preview family plan').click()
        no_overflow(page)
        page.get_by_role('button',name='Preview trial confirmation').click()
        expect(page.locator('#payment-note')).to_contain_text('No trial started')
        page.get_by_role('button',name='← Back to parent brief').click()
        expect(page.locator('#parent')).to_be_visible()
        results.append({'test':f"{size['width']}px: non-charging paywall preview and return",'status':'PASS'})
        context.close()
    context=browser.new_context(viewport={'width':390,'height':844})
    page=load(context,denied=True)
    play(page)
    expect(page.locator('#save-status')).to_contain_text('storage is unavailable')
    results.append({'test':'Storage denied: full click flow reaches parent brief','status':'PASS'})
    context.close()
    context=browser.new_context(viewport={'width':390,'height':844})
    page=load(context,storage={'questly-review-v2':'{malformed'})
    page.get_by_role('button',name='Parent preview').click()
    expect(page.locator('#brief-title')).to_have_text('No session yet')
    results.append({'test':'Malformed saved JSON does not break app','status':'PASS'})
    context.close()
    assert not errors,errors
    results.append({'test':'No uncaught JavaScript errors in exercised cases','status':'PASS'})
    browser.close()
report={'tested_at_utc':datetime.now(timezone.utc).isoformat(),'browser':'Chromium '+version,
    'scope':'HTML loaded into Chromium via set_content. Real browser clicks, mobile viewport emulation. localStorage simulated for persistence tests.',
    'not_verified':['Live HTTPS deployment','Physical iPhone','Safari/WebKit','Real origin-backed storage across browser refresh'],
    'environment_note':'Local HTTP navigation attempt was blocked with ERR_BLOCKED_BY_ADMINISTRATOR. No browser policy was changed. DOM tests use supplied HTML without network navigation.',
    'results':results,'javascript_errors':errors}
(ROOT/'tests'/'results.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
