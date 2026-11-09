"""Loaded on startup, before hobbiesville_monitor.py starts checking.

The script hardcodes an 8-15 second gap and then idles until a round has lasted
60 seconds. This forces the faster pace. Delete this file to go back.
"""
import sys
import threading


def _patch(mod):
    if mod is None or getattr(mod, "_pace_patched", False):
        return
    if not hasattr(mod, "GAP_MIN") or not hasattr(mod, "MIN_SECONDS_PER_ROUND"):
        return
    mod.GAP_MIN = 3
    mod.GAP_MAX = 5
    mod.MIN_SECONDS_PER_ROUND = 3
    mod._pace_patched = True


def _watch():
    import time
    for _ in range(400):
        for name in ("__main__", "hobbiesville_monitor"):
            _patch(sys.modules.get(name))
        if getattr(sys.modules.get("__main__"), "_pace_patched", False):
            return
        time.sleep(0.05)


threading.Thread(target=_watch, daemon=True).start()
