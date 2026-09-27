// (build_timeline_links.py 가 이 조각을 timeline-links.js 끝에 붙인다) 설명 패널에 타임라인 링크 칸을 그리는 함수
window.tlBlock = function (n) {
  var T = window.TL_LINKS, m = location.pathname.match(/part(\d)/);
  if (!T || !m || !n) return '';
  var p = m[1], e = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var url = function (d, id) { return T.base + encodeURIComponent(T.docs[d][0]) + (id ? '#' + id : ''); };
  var btn = function (href, sm, b, arr) {
    return '<a class="gobtn" href="' + e(href) + '" target="_blank" rel="noopener"><span><small>' + e(sm) +
      '</small><b>' + e(b) + '</b></span><span class="arr">' + arr + '</span></a>';
  };
  var rows = [], h = '';
  if (n.type === 'section') {
    (T.secs[p] && T.secs[p][n.id] || []).forEach(function (d) {
      rows.push(btn(url(d), '나이스 타임라인 문서', T.docs[d][1], '문서 열기 ↗'));
    });
    h = '이 Section을 업무카드로 보기';
  } else {
    (T.links[p] && T.links[p][n.id] || []).forEach(function (c) {
      rows.push(btn(url(c[0], c[1]), T.docs[c[0]][1] + ' · 업무카드 ' + c[2], c[3], '새 탭 ↗'));
    });
    h = '업무카드로 자세히 보기';
  }
  return rows.length ? '<section class="goto tlbox"><h3>' + h + '</h3>' + rows.join('') + '</section>' : '';
};
