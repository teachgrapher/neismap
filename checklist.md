# 나이스 지도 ↔ 나이스 타임라인 연동 체크리스트

## 준비
- [x] 지도 데이터(part1~9의 PART 객체) 추출
- [x] 타임라인 카드 데이터(제목·어디서·누가) 추출

## 짝 맞추기
- [x] Section ↔ 타임라인 문서 대응 (가지 끝 항목의 짝에서 자동 계산)
- [x] 업무 항목 ↔ 업무카드 짝 판단 (쪽수는 쓰지 않음) → data/timeline-links.txt
- [x] 애매한 짝 10줄·카드 없음 4줄을 선생님께 확인받기 (5줄 연결 확정, 5줄 링크 빼기)
- [x] 확인 결과 반영 후 tools/build_timeline_links.py 다시 돌리기

## 지도 → 타임라인
- [x] part1~9 설명 패널에 "업무카드로 자세히 보기" 칸 (새 탭)
- [x] Section 선택 시 "이 Section을 업무카드로 보기" 문서 버튼

## 타임라인 → 지도
- [x] 카드마다 "나이스 지도에서 보기" 링크 (새 탭, neis_timeline/tools/patch_map_link.py)

## 검증
- [x] build_timeline_links.py 가 없는 항목·없는 카드를 잡아냄 (현재 오류 0)
- [x] 브라우저: 지도 항목 380개 버튼 수 일치, 파트별 3개씩 새 탭 도착 위치 확인
- [x] 브라우저: 타임라인 53편 634장 모두 지도 링크 있음, 표본 5개 지도 패널 도착 확인
- [x] 넓은 화면·휴대폰 폭(390px) 화면 확인, 가로 스크롤 없음
- [x] 커밋·브랜치 푸시 (neismap: link-neis-timeline, neis_timeline: link-neismap)
- [ ] 두 브랜치를 main 에 병합(병합하면 Vercel이 배포)
