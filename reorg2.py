"""Regroup new-research.css: all base rules first, then all @media blocks.
Verifies no media-vs-normal winner flip vs the original (pre-regroup) order.
"""
import re

PATH = 'research/static/research/css/new-research.css'
src = open(PATH, encoding='utf-8').read()

def segment(src):
    i, n = 0, len(src); segments = []; buf = []; depth = 0
    while i < n:
        if src.startswith('/*', i):
            j = src.find('*/', i + 2); j = n if j == -1 else j + 2
            buf.append(src[i:j]); i = j; continue
        c = src[i]
        if depth == 0 and c == '@':
            if ''.join(buf).strip(): segments.append(('chunk', ''.join(buf)))
            buf = []
            m = re.match(r'@([\w-]+)', src[i:]); name = m.group(1)
            j = i
            while j < n and src[j] not in '{;':
                if src.startswith('/*', j):
                    k = src.find('*/', j + 2); j = (n if k == -1 else k + 2); continue
                j += 1
            if j < n and src[j] == ';':
                segments.append(('media' if name == 'media' else 'chunk', src[i:j + 1])); i = j + 1; continue
            start = i; d = 0; k = j
            while k < n:
                if src.startswith('/*', k):
                    e = src.find('*/', k + 2); k = (n if e == -1 else e + 2); continue
                if src[k] == '{': d += 1
                elif src[k] == '}':
                    d -= 1
                    if d == 0: k += 1; break
                k += 1
            segments.append(('media' if name == 'media' else 'chunk', src[start:k])); i = k; continue
        buf.append(c)
        if c == '{': depth += 1
        elif c == '}': depth -= 1
        i += 1
    if ''.join(buf).strip(): segments.append(('chunk', ''.join(buf)))
    return segments

def strip_comments(s): return re.sub(r'/\*.*?\*/', '', s, flags=re.S)

def decls(body):
    """prop -> important? from a rule body"""
    out = {}
    for m in re.finditer(r'([\w-]+)\s*:\s*([^;]+);', body):
        out[m.group(1).strip()] = '!important' in m.group(2)
    return out

def normal_rules(text):
    out = []
    for m in re.finditer(r'([^{}]+)\{([^{}]*)\}', strip_comments(text)):
        sel = m.group(1).strip()
        if sel.startswith('@'): continue
        for s in re.split(r'\s*,\s*', sel):
            out.append((s, decls(m.group(2))))
    return out

def media_rules(text):
    t = strip_comments(text)
    inner = t[t.index('{') + 1: t.rindex('}')]
    return normal_rules(inner)

segs = segment(src)
chunks = [t for k, t in segs if k == 'chunk']
medias = [t for k, t in segs if k == 'media']
print(f"chunks: {len(chunks)}, media: {len(medias)}")

# ---- build new file ----
banner = "\n\n/* ========================================================================\n   RESPONSIVE / MOBILE STYLES\n   All @media rules are grouped here at the end of the file, in their\n   original order, so they keep overriding the base rules above.\n   ======================================================================== */\n\n"
new_src = '\n\n'.join(t.strip() for t in chunks) + banner + '\n\n'.join(t.strip() for t in medias) + '\n'

# ---- verification ----
# original file = current src but with 'body ' bumps undone (to model pre-regroup selectors+order)
orig = src.replace('body .', 'body .')  # selector text kept; order is what matters
def ordered_rules(segments):
    """list of (origin, pos, sel, prop, important)"""
    rules = []
    for pos, (k, t) in enumerate(segments):
        if k == 'chunk':
            for sel, d in normal_rules(t):
                for p, imp in d.items(): rules.append(('N', pos, sel, p, imp))
        else:
            for sel, d in media_rules(t):
                for p, imp in d.items(): rules.append(('M', pos, sel, p, imp))
    return rules

old_segs = segs  # pre-regroup order (selector bumps don't affect order)
new_segs = segment(new_src)
R_old = ordered_rules(old_segs)
R_new = ordered_rules(new_segs)

def winners(rules):
    """for each (sel,prop) with at least one M and one N decl, who wins (later pos; important always wins; higher-spec 'body X' beats 'X')"""
    groups = {}
    for o, pos, sel, p, imp in rules:
        eff = sel[5:] if sel.startswith('body ') else sel
        groups.setdefault((eff, p), []).append((o, pos, sel, imp))
    res = {}
    for key, lst in groups.items():
        if not any(o == 'M' for o, *_ in lst) or not any(o == 'N' for o, *_ in lst):
            continue
        # winner: important first; then higher spec (body prefix); then later pos
        def score(r):
            o, pos, sel, imp = r
            bumped = 1 if sel.startswith('body ') else 0
            return (1 if imp else 0, bumped, pos)
        w = max(lst, key=score)
        res[key] = w[0]
    return res

w_old = winners(R_old); w_new = winners(R_new)
flips = [(k, w_old.get(k), w_new.get(k)) for k in w_new if w_old.get(k) != w_new.get(k)]
print(f"winner flips: {len(flips)}")
for f in flips[:40]: print(' ', f)

if flips:
    print("NOT writing file — resolve flips first")
else:
    open(PATH, 'w', encoding='utf-8', newline='\n').write(new_src)
    print("written:", PATH, len(new_src), "chars")
