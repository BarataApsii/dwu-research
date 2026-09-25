"""Split new-research.css into base rules and @media blocks, preserving order.
Reports conflicts: normal rules that originally came AFTER a media block and
target the same selector+property (their priority would flip if media moves
to the end of the file).
"""
import re, sys

PATH = 'research/static/research/css/new-research.css'
src = open(PATH, encoding='utf-8').read()

# --- tokenize top level: track brace depth, skip /* */ comments ---
def strip_comments(s):
    return re.sub(r'/\*.*?\*/', '', s, flags=re.S)

i, n = 0, len(src)
segments = []  # (kind, text) kind in {'chunk'(non-media incl comments), 'media'}
buf = []
depth = 0
in_comment = False
while i < n:
    if not in_comment and src.startswith('/*', i):
        j = src.find('*/', i + 2)
        j = n if j == -1 else j + 2
        buf.append(src[i:j]); i = j; continue
    c = src[i]
    if depth == 0 and c == '@':
        # top-level at-rule starts; flush buffer
        if ''.join(buf).strip():
            segments.append(('chunk', ''.join(buf)))
        buf = []
        # read at-rule name
        m = re.match(r'@([\w-]+)', src[i:])
        name = m.group(1)
        # find end: either ';' (no block) or balanced '{...}'
        j = i
        while j < n and src[j] not in '{;':
            # skip comments in prelude
            if src.startswith('/*', j):
                k = src.find('*/', j + 2); j = (n if k == -1 else k + 2); continue
            j += 1
        if j < n and src[j] == ';':
            at = src[i:j + 1]
            segments.append(('media' if name == 'media' else 'chunk', at))
            i = j + 1; continue
        # balanced block
        start = i
        d = 0; k = j
        while k < n:
            if src.startswith('/*', k):
                e = src.find('*/', k + 2); k = (n if e == -1 else e + 2); continue
            if src[k] == '{': d += 1
            elif src[k] == '}':
                d -= 1
                if d == 0: k += 1; break
            k += 1
        at = src[start:k]
        segments.append(('media' if name == 'media' else 'chunk', at))
        i = k; continue
    buf.append(c)
    if c == '{': depth += 1
    elif c == '}': depth -= 1
    i += 1
if ''.join(buf).strip():
    segments.append(('chunk', ''.join(buf)))

print(f"total top-level segments: {len(segments)}")
print(f"media blocks: {sum(1 for k,_ in segments if k=='media')}")

# --- index segments by position, extract selector->props ---
def selectors_of(rule_text):
    """yield (selector, prop) for 'sel{prop:val;...}' top level of a rule text"""
    # remove comments
    t = strip_comments(rule_text)
    for m in re.finditer(r'([^{}]+)\{([^{}]*)\}', t):
        sel = m.group(1).strip()
        body = m.group(2)
        props = set(re.findall(r'([\w-]+)\s*:', body))
        yield sel, props

def media_rules(text):
    """rules inside @media prelude {...}: need inner top-level rules"""
    t = strip_comments(text)
    inner = t[t.index('{') + 1: t.rindex('}')]
    out = []
    for m in re.finditer(r'([^{}]+)\{([^{}]*)\}', inner):
        sel = m.group(1).strip()
        props = set(re.findall(r'([\w-]+)\s*:', m.group(2)))
        out.append((sel, props))
    return out

# collect all normal rules with their segment index
normal = {}  # sel -> list of (seg_idx, props)
for idx, (kind, text) in enumerate(segments):
    if kind != 'chunk': continue
    for sel, props in selectors_of(text):
        normal.setdefault(sel, []).append((idx, props))

conflicts = []
for idx, (kind, text) in enumerate(segments):
    if kind != 'media': continue
    for sel, props in media_rules(text):
        for s2 in re.split(r'\s*,\s*', sel):
            if s2 in normal:
                for nidx, nprops in normal[s2]:
                    if nidx > idx and (props & nprops):
                        conflicts.append((sel, sorted(props & nprops), idx, nidx))

print(f"potential flips: {len(conflicts)}")
for c in conflicts[:60]:
    print(c)
