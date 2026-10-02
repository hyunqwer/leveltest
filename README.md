# 윤선생 진단평가 리포트 개선 시안

버전별 폴더로 관리. 최신은 `v9/`.

| 버전 | 위치 | 내용 |
|---|---|---|
| v7 | 저장소 루트 | 1p 시안, 샘플 7종 탭, Before/After 비교 |
| v9 | `v9/` | 1p · 2p · 인쇄용(A4 1장) 3종, 하이차트 스타일 벨커브, 초4 전 영역 1명 |

## v9 (`v9/`)

- `1p.html` / `2p.html` — 화면용 (1024×600, 서비스 CSS 웹 로드)
- `print.html` — 인쇄용 A4 세로 1장 (1p+2p 합본, 헤더는 현행 인쇄본 캡처)
- `gen_v9.py`, `gen_print9.py`, `v9.css`, `hdr.b64` — 재생성용 (`python gen_v9.py && python gen_print9.py`)
- `README.txt` — v8→v9 변경점·데이터

## v7 (루트)

진단평가 결과 리포트 첫 화면 개선안. `index.html`을 브라우저로 열면 상단 탭으로 샘플 7종(영역 조합·학년별)을 전환해 볼 수 있음.
서비스 CSS(leveltest.yoons.com)를 웹에서 불러오므로 인터넷 연결 필요.

- `index.html` — 시안 (초4 전 영역 / 초1 파닉스+L/R / 초6 전 영역·평균 이하 / 중1 L/R+문법 / 고1 전 영역 / 초3 파닉스만 / 초4 파닉스+문법)
- `compare_before_after.html` / `.png` — 현행(Before) vs v7(After) 비교, 초4 예시 학생 A (`gen_compare.py`로 재생성)
- `README.txt` — 구성·데이터·변경 내역·숙제
- `gen_v7.py`, `v7.css`, `samples7.json` — 재생성용 (python3 gen_v7.py)
- `pick7.py` — 샘플 추출 스크립트 (응시 데이터 필요, 저장소에는 미포함)

모든 수치는 실제 응시 기록·정답률 기준(이름 없음).
