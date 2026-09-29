#!/usr/bin/env python3
"""Kill only the isolated QE app after its first committed voyage; verify via XCTest.

Requires a current build-for-testing and DEVELOPER_DIR. Never reads normal player saves.
"""
import argparse
import base64
import json
import os
from pathlib import Path
import plistlib
import signal
import subprocess
import time
import uuid

p = argparse.ArgumentParser()
p.add_argument('--device', required=True)
p.add_argument('--products', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
a = p.parse_args()
a.products = a.products.resolve()
a.output = a.output.resolve()
a.output.mkdir(parents=True, exist_ok=True)
run_id = 'external-kill-' + str(uuid.uuid4())
source = next(a.products.glob('Questly_*.xctestrun'))
config = plistlib.loads(source.read_bytes())
config['QuestlyUITests']['EnvironmentVariables'].update({
    'QUESTLY_QE_EXTERNAL_KILL': '1', 'QUESTLY_QE_RUN_ID': run_id,
})
spec = a.products / (run_id + '.xctestrun')
spec.write_bytes(plistlib.dumps(config))
command = ['xcodebuild', 'test-without-building', '-xctestrun', str(spec),
           '-destination', 'platform=iOS Simulator,id=' + a.device,
           '-parallel-testing-enabled', 'NO', '-collect-test-diagnostics', 'never',
           '-only-testing:QuestlyUITests/QuestlyUITests/testExternalSIGKILLRestoresCommittedVoyage',
           '-resultBundlePath', str(a.output / 'kill.xcresult')]
report = {'device': a.device, 'runID': run_id, 'command': command, 'signal': 'SIGKILL',
          'result': 'NOT COMPLETED', 'scope': 'Isolated simulator app; not physical-device power-loss evidence'}
def sim(*args):
    return subprocess.check_output(['xcrun', 'simctl', *args], text=True, timeout=10).strip()

def verified_process(pid):
    process_path = subprocess.check_output(['ps', '-p', str(pid), '-o', 'args='], text=True, timeout=5)
    if a.device not in process_path or '/Questly.app/Questly' not in process_path:
        raise RuntimeError('Refusing to signal a process outside this isolated QE app')

process = None
try:
    device_list = json.loads(sim('list', 'devices', 'available', '--json'))
    device = next((d for group in device_list['devices'].values() for d in group if d['udid'] == a.device), None)
    if device is None or not device['name'].startswith('Questly-QE-'):
        raise RuntimeError('Use a dedicated Questly-QE-* simulator, not a personal device')
    report['deviceName'] = device['name']
    if (a.output / 'kill.xcresult').exists():
        raise RuntimeError('Choose a fresh output directory for the XCTest result bundle')
    with (a.output / 'kill.log').open('w') as log:
        process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT)
        deadline = time.monotonic() + 180
        folder = None
        killed = False
        while process.poll() is None and time.monotonic() < deadline:
            if folder is None or not folder.exists():
                try:
                    folder = Path(sim('get_app_container', a.device, 'com.questly.m1', 'data')) / 'Library/Application Support' / ('Questly-UITests-' + run_id)
                except subprocess.CalledProcessError:
                    time.sleep(0.2)
                    continue
            checkpoints = []
            for path in folder.glob('checkpoint-*.json'):
                try:
                    envelope = json.loads(path.read_bytes())
                    payload = json.loads(base64.b64decode(envelope['payload']))
                    checkpoints.append((envelope['generation'], payload, path))
                except (ValueError, KeyError):
                    continue
            if checkpoints:
                generation, payload, path = max(checkpoints, key=lambda c: c[0])
                fern = next(x for x in payload['profiles'] if x['id'] == 'fern')
                if fern['engineer']['trips'] == [[0, 3]]:
                    app_row = next(row for row in sim('spawn', a.device, 'launchctl', 'list').splitlines()
                                   if row.split()[-1].startswith('UIKitApplication:com.questly.m1['))
                    pid = int(app_row.split()[0])
                    verified_process(pid)
                    time.sleep(0.2)
                    sim('io', a.device, 'screenshot', str(a.output / 'before-sigkill.png'))
                    elapsed = (time.time_ns() - path.stat().st_mtime_ns) / 1e9
                    if not 0 <= elapsed < 1.6:
                        raise RuntimeError('Missed the 1.6-second voyage presentation window')
                    verified_process(pid)
                    os.kill(pid, signal.SIGKILL)
                    report.update({'killedPID': pid, 'checkpointGeneration': generation,
                                   'secondsAfterCheckpoint': elapsed, 'killedAtUnix': time.time()})
                    killed = True
                    break
            time.sleep(0.02)
        if not killed:
            if process.poll() is None:
                process.terminate()
            raise RuntimeError('No verified QE app was killed within the bounded wait')
        report['xcodebuildExitCode'] = process.wait(timeout=180)
        if report['xcodebuildExitCode'] != 0:
            raise RuntimeError('See kill.log for actual XCTest failures')
        report['result'] = 'PASS'
except BaseException as error:
    report['result'] = 'FAIL'
    report['error'] = str(error)
    raise
finally:
    if process is not None and process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=10)
    spec.unlink(missing_ok=True)
    (a.output / 'kill-report.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
