import os
from pathlib import Path
from functools import wraps
import pickle

def memoize(fn):
    """Caches previous calls to the function."""
    memo = {}

    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not memoize.disabled:
            key = pickle.dumps((args, kwargs))
            if key not in memo:
                memo[key] = fn(*args, **kwargs)
            value = memo[key]
        else:
            # Memoize is disabled, call the function
            value = fn(*args, **kwargs)

        return value

    return wrapper

memoize.disabled = False

def get_alias():
    return os.environ.get('UF_ALIAS', 'fix')

@memoize
def get_all_executables():
    from . import shell

    def _safe(fn, fallback):
        try:
            return fn()
        except OSError:
            return fallback

    uf_alias = get_alias()
    uf_entry_points = ['thefuck', 'fuck']

    bins = [exe.name for path in os.environ.get('PATH', '').split(os.pathsep)
            for exe in _safe(lambda: list(Path(path).iterdir()), [])
            if not _safe(exe.is_dir, True)
            and exe.name not in uf_entry_points]
    aliases = [alias for alias in shell.get_aliases() if alias != uf_alias]

    return bins + aliases