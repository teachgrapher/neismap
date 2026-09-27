# 지도↔타임라인 연결표(data/timeline-links.txt)를 검사하고 두 사이트의 링크 파일을 만드는 스크립트
#
# 쓰는 법.  neismap 저장소 뿌리에서
#   python3 tools/build_timeline_links.py [neis_timeline 저장소 경로]
# 경로를 생략하면 ../neis_timeline 을 쓴다.
#
# 만드는 파일.
#   neismap/timeline-links.js        지도 설명 패널의 '업무카드로 자세히 보기' 칸이 읽는 자료
#   neis_timeline/map-links.js       타임라인 카드의 '지도에서 위치 보기' 링크가 읽는 자료
#
# 연결표를 고친 뒤, 또는 타임라인 카드를 고치고 cards.js 를 다시 만든 뒤에 돌린다.
# 없는 항목·없는 카드를 가리키면 멈추고 알려 준다.

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TL = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else (ROOT.parent / 'neis_timeline')
SRC = ROOT / 'data' / 'timeline-links.txt'

TL_URL = 'https://neis-timeline.vercel.app/pages/'
MAP_URL = 'https://neismap.vercel.app/'

NODE = re.compile(r"\{id:'([A-Za-z0-9_]+)',\s*(?:(?:side|no):'[^']*',\s*)?label:'((?:[^'\\]|\\.)*)'")


def read_map(p):
    """part 파일에서 가지 끝 항목과 그 소속 Section을 순서대로 읽는다."""
    s = (ROOT / f'part{p}.html').read_text(encoding='utf-8')
    a = s.index('const PART')
    b = s.index('flows:', a)
    block = s[a:b]
    part_label = re.search(r"label:'([^']*)'", block).group(1)
    secs, leaves, cur = {}, {}, None
    for m in NODE.finditer(block):
        nid, label = m.group(1), m.group(2).replace("\\'", "'")
        if nid == 'root' or re.fullmatch(r'[A-Z]', nid):
            continue
        if re.fullmatch(r'S\d+', nid):
            cur = nid
            secs[nid] = {'label': label}
            continue
        leaves[nid] = {'label': label, 'sec': cur}
    return part_label, secs, leaves


def read_cards():
    s = (TL / 'cards.js').read_text(encoding='utf-8')
    data = json.loads(s[s.index('{'):s.rindex('}') + 1])
    docs = data['docs']
    cards = {}
    for c in data['cards']:
        cards[(docs[c['d']]['f'], c['i'])] = c
    return docs, cards


def read_src():
    alias, parts, p = {}, {}, None
    for no, raw in enumerate(SRC.read_text(encoding='utf-8').split('\n'), 1):
        line = raw.strip()
        if not line or (line.startswith('#') and not line.startswith('## part')):
            continue
        if line.startswith('## part'):
            p = int(line.split()[-1])
            parts[p] = {}
            continue
        if line.startswith('@'):
            k, f = line[1:].split(' ', 1)
            alias[k] = f.strip()
            continue
        note = ''
        if '?' in line:
            line, note = line.split('?', 1)
        leaf, *refs = line.split()
        if leaf in parts[p]:
            raise SystemExit(f'{no}번째 줄 · part {p} 항목 {leaf} 이 두 번 나옴')
        parts[p][leaf] = {'refs': [r for r in refs if r != '-'], 'note': note.strip(), 'line': no}
    return alias, parts


def main():
    docs, cards = read_cards()
    doc_idx = {d['f']: i for i, d in enumerate(docs)}
    alias, src = read_src()
    errors, warns = [], []
    used = set()
    tl_links = {}        # part → 항목id → [[문서idx, 카드id, 번호, 제목], ...]
    tl_secs = {}         # part → Section id → [문서idx, ...]
    back = {}            # 문서파일 → 카드id → [[part, 항목id, 항목이름, Section이름], ...]
    maps = {}

    for p in range(1, 10):
        part_label, secs, leaves = read_map(p)
        maps[p] = (part_label, secs)
        got = src.get(p, {})
        for leaf in leaves:
            if leaf not in got:
                errors.append(f'part {p} · 연결표에 없는 지도 항목 {leaf}({leaves[leaf]["label"]})')
        out, per_sec = {}, {}
        for leaf, row in got.items():
            if leaf not in leaves:
                errors.append(f'{row["line"]}번째 줄 · part {p} 지도에 없는 항목 {leaf}')
                continue
            if row['note']:
                warns.append(f'part {p} {leaf} {leaves[leaf]["label"]} · {row["note"]}')
            lst = []
            for r in row['refs']:
                k, cid = r.split(':')
                f = alias.get(k)
                if f is None:
                    errors.append(f'{row["line"]}번째 줄 · 정의되지 않은 문서번호 @{k}')
                    continue
                c = cards.get((f, cid))
                if c is None:
                    errors.append(f'{row["line"]}번째 줄 · {f} 에 카드 {cid} 가 없음')
                    continue
                di = doc_idx[f]
                used.add((f, cid))
                lst.append([di, cid, c['n'], c['t']])
                sec = leaves[leaf]['sec']
                if docs[di]['p'].split()[1] == str(p):
                    per_sec.setdefault(sec, {}).setdefault(di, 0)
                    per_sec[sec][di] += 1
                back.setdefault(f, {}).setdefault(cid, []).append(
                    [p, leaf, leaves[leaf]['label'], secs[sec]['label']])
            if lst:
                out[leaf] = lst
        tl_links[p] = out
        tl_secs[p] = {s: [d for d, _ in sorted(v.items(), key=lambda x: (-x[1], x[0]))] for s, v in per_sec.items()}

    unused = [k for k in cards if k not in used]
    for f, cid in unused:
        warns.append(f'지도와 연결되지 않은 카드 · {f} #{cid} {cards[(f, cid)]["t"]}')

    if errors:
        print('\n'.join(errors))
        raise SystemExit(f'오류 {len(errors)}건 · 파일을 만들지 않음')

    tl_js = ('// 지도 항목→타임라인 업무카드 연결 자료. 손으로 고치지 말고 tools/build_timeline_links.py 로 만든다\n'
             'window.TL_LINKS = ' + json.dumps({
                 'base': TL_URL,
                 'docs': [[d['f'], d['t']] for d in docs],
                 'links': tl_links,
                 'secs': tl_secs,
             }, ensure_ascii=False, separators=(',', ':')) + ';\n'
             + (ROOT / 'tools' / 'timeline-links.tail.js').read_text(encoding='utf-8'))
    (ROOT / 'timeline-links.js').write_text(tl_js, encoding='utf-8')

    map_js = ('// 업무카드→나이스 지도 항목 연결 자료. neismap 저장소의 tools/build_timeline_links.py 가 만든다(손으로 고치지 않음)\n'
              'window.MAP_LINKS = ' + json.dumps({
                  'base': MAP_URL,
                  'parts': {p: maps[p][0] for p in maps},
                  'cards': back,
              }, ensure_ascii=False, separators=(',', ':')) + ';\n')
    (TL / 'map-links.js').write_text(map_js, encoding='utf-8')

    n_leaf = sum(len(v) for v in tl_links.values())
    n_link = sum(len(x) for v in tl_links.values() for x in v.values())
    print(f'지도 항목 {n_leaf}개 → 카드 링크 {n_link}개 · 연결된 카드 {len(used)}/{len(cards)}장')
    if warns:
        print(f'확인할 것 {len(warns)}건')
        print('  ' + '\n  '.join(warns))
    return 0


if __name__ == '__main__':
    sys.exit(main())
