# replace_use_container_width_safe.py
import pathlib
import re

ROOT = pathlib.Path('.').resolve()
TEXT_EXTS = {
    '.py', '.md', '.html', '.htm', '.css', '.js', '.json', '.txt',
    '.yml', '.yaml', '.ini', '.cfg', '.rst', '.ipynb', '.csv'
}
SKIP_DIRS = {'venv', '.venv', '.git', 'node_modules', '__pycache__'}

patterns = [
    (re.compile(r'use_container_width\s*=\s*True'), 'width="stretch"'),
    (re.compile(r'use_container_width\s*=\s*False'), 'width="content"'),
]

def should_skip(path: pathlib.Path) -> bool:
    for part in path.parts:
        if part in SKIP_DIRS:
            return True
    return False

patched = 0
for p in ROOT.rglob('*'):
    if p.is_file():
        if should_skip(p):
            continue
        if p.suffix.lower() not in TEXT_EXTS:
            continue
        try:
            raw = p.read_bytes()
            text = raw.decode('utf-8', errors='replace')
        except Exception:
            # fallback: try latin-1 decode
            try:
                text = raw.decode('latin-1', errors='replace')
            except Exception:
                continue

        new_text = text
        for pat, repl in patterns:
            new_text = pat.sub(repl, new_text)

        if new_text != text:
            p.write_text(new_text, encoding='utf-8')
            patched += 1
            print(f'Patched: {p}')
print(f'Done. Files patched: {patched}')