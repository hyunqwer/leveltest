# 윤선생 진단평가 리포트 개선 시안

버전별 폴더로 관리. GitHub Pages: https://hyunqwer.github.io/leveltest/ (주소 뒤에 `v7/` ~ `v11/`)
서비스 CSS(leveltest.yoons.com)를 웹에서 불러오므로 인터넷 연결 필요. 모든 수치는 실제 응시 기록·정답률 기준(이름 없음).

| 버전 | 폴더 | 내용 |
|---|---|---|
| v11 | `v11/` | **최신.** 현행 레이아웃 복제판: 1p·인쇄 상단은 현행 마크업·CSS·Highcharts 옵션 그대로(위치·간격 동일), 섹션명·시작점 큐·태그·벨커브 눈금(80/20, %)·총평만 교체. 2p·인쇄 하단은 v10 구성 |
| v10 | `v10/` | v9 기반. 2p 카드: 영역별 동학년 대비 삭제, 점수 → 정답률 % + 맞힌 문항 수, 카드 높이 확대·처방 박스 정리. 인쇄용 각주 삭제 |
| v9 | `v9/` | 1p · 2p · 인쇄용(A4 1장) 3종 + 탭 통합 `index.html`. 하이차트 스타일 벨커브, 2p 영역 카드 + 영역별 처방. 초4 전 영역 1명 |
| v8 | `v8/` | 1p + 2p 레이아웃 4안(A 닷플롯 / B 숫자표 / C1 카드+영역 박스 / C2 카드+종합 박스) 탭, 인쇄용 C1·C2 |
| v7 | `v7/` | 1p 시안, 영역 조합·학년별 샘플 7종 탭, 현행 vs v7 Before/After 비교 |

## 폴더별 파일

- **v11/** `index.html`(탭 통합), `1p.html`, `2p.html`, `print.html`, 재생성 `gen_v11.py`(한 번에 4개 생성), `v11.css`, `v10parts.py`/`v10.css`(2p용), `README.txt`

- **v10/** `index.html`(탭 통합), `1p.html`, `2p.html`, `print.html`, 재생성 `gen_v10.py` → `gen_print10.py`, `v10.css`, `hdr.b64`, `README.txt`

- **v9/** `index.html`(탭 통합), `1p.html`, `2p.html`, `print.html`, 재생성 `gen_v9.py` → `gen_print9.py`, `v9.css`, `hdr.b64`(인쇄 헤더 캡처), `README.txt`(변경점·데이터)
- **v8/** `index.html`, `print_c1.html`, `print_c2.html`, 재생성 `gen_v8.py` → `gen_print.py`, `v8.css`, `hdr.b64`, `README.txt`
- **v7/** `index.html`, `compare_before_after.html`/`.png`, 재생성 `gen_v7.py`, `v7.css`, `samples7.json`, `gen_compare.py`, `pick7.py`(응시 데이터 필요, 미포함), `README.txt`

재생성: 각 폴더에서 `python gen_v*.py` (인쇄용은 이어서 `python gen_print*.py`). 서비스 CSS는 HTML이 웹에서 로드.
