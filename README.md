# 나이스 지도

2026년 하반기 나이스 교무업무 사용자 설명서(고등학교용)를 파트별 마인드맵과 연수자료 PDF로 정리한 정적 웹사이트입니다. 2026.9.11. 기능개선 내용을 반영했습니다.

나이스(NEIS) 공식 자료가 아니며, 교사 연수용으로 설명서를 다시 정리한 것입니다.

## 폴더 구성

| 경로 | 내용 |
|---|---|
| `index.html` | 첫 화면(포털). 파트별 지도와 PDF로 들어가는 카드 |
| `part1.html` ~ `part8.html` | 파트별 마인드맵 |
| `pdf/part1.pdf` ~ `pdf/part8.pdf` | 파트별 인쇄용 연수자료 |
| `pages/`, `pages4/`, `pages7/`, `pages8/` | ‘매뉴얼 원문’ 탭에 뜨는 설명서 쪽 이미지(Part 1·4·7·8) |
| `timeline-links.js` | 설명 패널의 ‘업무카드로 자세히 보기’ 링크 자료(자동 생성, 손으로 고치지 않음) |
| `data/timeline-links.txt` | 지도 항목 ↔ 나이스 타임라인 업무카드 연결표(사람이 고치는 원본) |
| `tools/build_timeline_links.py` | 연결표를 검사하고 두 사이트의 링크 파일을 만드는 스크립트 |
| `vercel.json` | 주소에서 `.html` 생략, 이미지·PDF 캐시 설정 |

빌드 과정이 없는 정적 사이트라서 Vercel에서 Framework Preset을 **Other**로 두고 그대로 배포하면 됩니다.

## 고칠 때

파일을 바꿔 GitHub에 올리면(commit·push) Vercel이 1~2분 안에 자동으로 다시 배포합니다.

## 나이스 타임라인과 연결

지도에서 항목을 누르면 설명 패널 아래 ‘업무카드로 자세히 보기’ 버튼이 나오고, 누르면 [나이스 타임라인](https://neis-timeline.vercel.app)의 해당 업무카드가 새 탭으로 열립니다. 타임라인 카드 끝에는 반대로 ‘나이스 지도에서 보기’ 링크가 붙어 있습니다.

짝을 바꾸려면 `data/timeline-links.txt`에서 해당 줄을 고친 뒤, 두 저장소를 나란히 받아 둔 상태에서 다음을 실행합니다.

```
python3 tools/build_timeline_links.py ../neis_timeline
```

`timeline-links.js`(이 저장소)와 `map-links.js`(타임라인 저장소)가 다시 만들어집니다. 두 저장소 모두 커밋·푸시해야 양쪽에 반영됩니다. 없는 항목이나 카드를 가리키면 스크립트가 멈추고 알려 줍니다.
