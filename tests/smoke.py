"""Compatibility entry point for the current Storm Island browser tests.

Run TEST_PART=390 python tests/smoke.py for a bounded mobile batch.
See browser.py and README.md for scope and dependency details.
The v0.2 quiz tests remain available in earlier commits.
"""
from pathlib import Path
import runpy

if __name__ == '__main__':
    runpy.run_path(str(Path(__file__).with_name('browser.py')), run_name='__main__')
