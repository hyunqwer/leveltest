# 윤선생 진단평가 리포트 개선 시안

버전별 폴더로 관리. GitHub Pages: https://hyunqwer.github.io/leveltest/ (주소 뒤에 `v7/`, `v8/`, `v9/`, `v10/`)
서비스 CSS(leveltest.yoons.com)를 웹에서 불러오므로 인터넷 연결 필요. 모든 수치는 실제 응시 기록·정답률 기준(이름 없음).

| 버전 | 폴더 | 내용 |
|---|---|---|
| v10 | `v10/` | **최신.** v9 기반. 2p 카드: 영역별 동학년 대비 삭제, 점수 → 정답률 % + 맞힌 문항 수, 카드 높이 확대·처방 박스 정리. 인쇄용 각주 삭제 |
| v9 | `v9/` | 1p · 2p · 인쇄용(A4 1장) 3종 + 탭 통합 `index.html`. 하이차트 스타일 벨커브, 2p 영역 카드 + 영역별 처방. 초4 전 영역 1명 |
| v8 | `v8/` | 1p + 2p 레이아웃 4안(A 닷플롯 / B 숫자표 / C1 카드+영역 박스 / C2 카드+종합 박스) 탭, 인쇄용 C1·C2 |
| v7 | `v7/` | 1p 시안, 영역 조합·학년별 샘플 7종 탭, 현행 vs v7 Before/After 비교 |

## 폴더별 파일

- **v10/** `index.html`(탭 통합), `1p.html`, `2p.html`, `print.html`, 재생성 `gen_v10.py` → `gen_print10.py`, `v10.css`, `hdr.b64`, `README.txt`

- **v9/** `index.html`(탭 통합), `1p.html`, `2p.html`, `print.html`, 재생성 `gen_v9.py` → `gen_print9.py`, `v9.css`, `hdr.b64`(인쇄 헤더 캡처), `README.txt`(변경점·데이터)
- **v8/** `index.html`, `print_c1.html`, `print_c2.html`, 재생성 `gen_v8.py` → `gen_print.py`, `v8.css`, `hdr.b64`, `README.txt`
- **v7/** `index.html`, `compare_before_after.html`/`.png`, 재생성 `gen_v7.py`, `v7.css`, `samples7.json`, `gen_compare.py`, `pick7.py`(응시 데이터 필요, 미포함), `README.txt`

재생성: 각 폴더에서 `python gen_v*.py` (인쇄용은 이어서 `python gen_print*.py`). 서비스 CSS는 HTML이 웹에서 로드.
