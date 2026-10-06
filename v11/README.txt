진단평가 리포트 시안 v11 — 현행 레이아웃 복제판 (초4 전 영역 예시 학생 A)
===========================================================================
목적: 1p와 인쇄용 상단은 현행 서비스의 마크업·CSS·Highcharts 옵션을 그대로 써서 요소 위치·간격·높이를
      기존과 동일하게 유지하고, 내용(섹션명·시작점 큐·태그·눈금·총평)만 교체. 2p와 인쇄 하단은 v10 구성.

파일
 - index.html   1p / 2p / 인쇄용 탭 통합 (GitHub Pages: https://hyunqwer.github.io/leveltest/v11/)
 - 1p.html / 2p.html / print.html   개별 파일
 - gen_v11.py   생성 스크립트 (python gen_v11.py 한 번으로 4개 파일 생성)
 - v11.css      추가 CSS(변경 요소 + 인쇄 하단 v10 구성)  ·  v10parts.py / v10.css  2p용(v10 그대로)
 - 서비스 리소스는 웹에서 로드: /css/common.css, w_reset.css, w_base.css, w_media.css, /Highcharts-6.0.3/*, /images/icon/printer_logo_1.png

1p (현행 PagePanel RS 마크업 그대로: asidetop_wrap/level_section, asidebottom_wrap/achiev_section·position_section)
 1. 섹션명: 나의 레벨 → 나에게 맞는 학습 시작점 / 영역별 성취도 → 나의 영역별 점수 / 나의 위치 → 동학년 대비 나의 위치
 2. 시작점 배지 옆 회색 큐 "읽기/쓰기 기준" (.v11cue)
 3. 읽기/쓰기 원그래프 위 "시작점 기준" 태그 (.v11g 래퍼 + .v11tag, 차트 div 크기 변경 없음)
 4. YES4.0 표 "All Star" → "All-Star"
 5. 원그래프: 현행 solidgauge 옵션 그대로(색·크기·라벨 포맷 동일)
 6. 벨커브: 현행 areaspline 옵션 그대로 + 변경 3가지
    ① xAxis[0] tickPositions 등급컷 → [0,10,20,50,80,90,100], xAxis[3] 라벨 "9등급…" → "90% 80% 50% 20% 10%"
    ② Below/Average/Above 경계선: 카테고리 3등분 → xAxis[0] plotLines 80·20, 라벨은 xAxis[1] tickPositions [90,50,10]
    ③ 80% 초과: 마커 x=90 고정, 라벨 "상위 80% 이하"
 7. 총평(.arert_wrap): 두 줄 허용, 예시 2문장(문구 세트는 추후)

인쇄용 (현행 evaluationPrintPreview 마크업: .wrap.printerv3 > header(header_1/header_2) > .bodyarea > dl.sec_1 / sec_2)
 - 상단 sec_1·sec_2는 현행 그대로(폭 860, 레벨 20% + 표 80%, 게이지 250×260, 벨커브 230px). 큐는 레벨명 아래 작은 글씨.
 - #positionText height 48px 고정 → auto(min 48)로 두 줄 허용.
 - sec_3: 현행 3열 막대차트 → v10 구성(카드 4장 + 처방 박스 3개). 처방 박스는 현행 .info_area orange/green/purple 클래스 사용.
 - sec_4(추천 교재)·sec_5(커리큘럼)는 범위 밖(미포함).
 - 인쇄 버튼 영역(.y_printer_area)은 시안에서 숨김.

2p: v10과 동일 (영역 카드 + 영역별 처방, 정답률 % + 문항 수, 동학년 대비 없음).

개발 참고
 - 시안은 서버 API 없이 학생 A 데이터를 마크업에 직접 넣고 Highcharts 옵션으로 그린 것. 실제 적용 시 evaluationResult_001.js /
   evaluationPrintPreview.js의 차트 옵션에서 위 ①②③만 바꾸면 됨.
 - 데이터: 파닉스 75%(9/12) 장모음 / 듣말 84.6%(11/13) All-Star 초6 / 읽쓰 60%(6/10) Rising Star 초4 / 문법 70%(7/10) All-Star 초5
   종합 상위 41.8%(B_LS+RW+P+G) / 학년 평균(초4): 장모음 / All-Star 초5 / Rising Star 초4 / Rising Star 초4
