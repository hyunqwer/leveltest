# -*- coding: utf-8 -*-
"""현행(Before) vs v7(After) 비교 — 초4 전 영역 예시 학생 A, 같은 실데이터."""
import os, json, math, importlib.util, sys
HERE=os.path.dirname(os.path.abspath(__file__))
OUT=os.environ.get('OUT',os.path.expanduser('~/mnt/leveltest/진단평가리포트업글_codex/ys_report_mockups_v7_service'))
spec=importlib.util.spec_from_file_location('g7',os.path.join(HERE,'gen_v7.py'))
os.environ.setdefault('OUT',OUT); g7=importlib.util.module_from_spec(spec); spec.loader.exec_module(g7)
S=g7.D['e4_all']; A=S['area']
# ---- 현행 위치: 결정값(낮은 영역 = 읽쓰 4.5단계) → 2022.11 기준표 초4 50.2% → 9등급 컷(4/11/23/40/60/77/89/96) → 5등급
CUR_POS=50.2
def grade9(p):
    cuts=[4,11,23,40,60,77,89,96]
    for i,c in enumerate(cuts):
        if p<=c: return i+1
    return 9
G9=grade9(CUR_POS)
COL=g7.COL; NM=g7.NM
def donut_old(a):
    x=A[a]; r=52; c=2*math.pi*r
    return (f'<div class="od"><svg viewBox="0 0 120 120" width="118" height="118"><circle cx="60" cy="60" r="{r}" fill="none" stroke="#e6e6e6" stroke-width="9"/>'
            f'<circle cx="60" cy="60" r="{r}" fill="none" stroke="{COL[a]}" stroke-width="9" stroke-dasharray="{c*x["score"]/100:.1f} {c:.1f}" transform="rotate(-90 60 60)"/></svg>'
            f'<div class="ctr"><span>{NM[a]}</span><strong>{x["score"]:g}점</strong></div></div>')
def bell():
    # 종 모양 곡선 + 9등급 축(왼쪽 9등급 → 오른쪽 1등급), 마커 = 상위 CUR_POS% → x = 100-CUR_POS
    W,H=620,200; pts=[]
    for i in range(0,W+1,4):
        x=i/W; y=math.exp(-((x-0.5)**2)/(2*0.17**2)); pts.append(f'{i},{H-20-y*(H-50)}')
    cuts=[4,11,23,40,60,77,89,96]  # 상위 % 경계
    vlines=''.join(f'<line x1="{(100-c)/100*W:.1f}" y1="0" x2="{(100-c)/100*W:.1f}" y2="{H-20}" stroke="#ddd"/>' for c in cuts)
    # 등급 라벨: 구간 중앙
    bounds=[100]+[c for c in reversed(cuts)]+[0]  # 100..96..4..0 → 왼쪽부터 9등급
    labels=''
    for gi in range(9):
        lo,hi=bounds[gi],bounds[gi+1]; cx=(100-(lo+hi)/2)/100*W
        labels+=f'<text x="{cx:.1f}" y="{H-4}" font-size="11" text-anchor="middle" fill="#555">{9-gi}등급</text>'
    mx=(100-CUR_POS)/100*W
    return (f'<svg class="bell" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{vlines}'
            f'<polyline points="{" ".join(pts)}" fill="none" stroke="#bbb" stroke-width="2"/>'
            f'<line x1="0" y1="{H-20}" x2="{W}" y2="{H-20}" stroke="#999"/>'
            f'<line x1="{mx:.1f}" y1="10" x2="{mx:.1f}" y2="{H-20}" stroke="#e64545" stroke-width="1.5"/>'
            f'<circle cx="{mx:.1f}" cy="{H-20}" r="4" fill="#e64545"/>'
            f'<rect x="{mx-38:.1f}" y="52" width="76" height="24" rx="4" fill="#e64545"/><text x="{mx:.1f}" y="69" font-size="12" font-weight="700" text-anchor="middle" fill="#fff">상위 {CUR_POS}%</text>'
            f'{labels}</svg>')
before=(f'<div class="rep rpt_old"><div class="content"><div class="slide_pa">'
 '<div class="asidetop_wrap"><div class="level_section"><dl><dt><span class="title">나의 레벨</span><span class="level">Rising Star 초4</span></dt><dd>'+g7.yes_table('초4').replace('All-Star','All Star')+'</dd></dl></div></div>'
 '<div class="obottom"><div class="oleft"><p class="otitle">영역별 성취도</p><div class="odn">'+''.join(donut_old(a) for a in 'PLRG')+'</div></div>'
 '<div class="oright"><p class="otitle">나의 위치</p><div class="bandlab"><span>Below Average</span><span>Average</span><span>Above Average</span></div>'+bell()+'</div></div>'
 f'<div class="arert_wrap oarert"><span></span>동학년 대비 상위 {CUR_POS}%로 평균 수준의 실력입니다. 꾸준한 학습으로 실력을 더 키워 보세요. <em>(총평 문구는 현행 템플릿 추정)</em></div>'
 '</div></div></div>')
after=g7.page_body(S)
CSS=g7.CSS+"""
/* 비교 페이지 */
.cmp_label{width:1024px;margin:26px auto 8px;font-size:15px;font-weight:800;color:#333;display:flex;align-items:center;gap:10px;}
.cmp_label b{display:inline-block;padding:2px 10px;border-radius:4px;color:#fff;font-size:12px;}
.cmp_label b.bf{background:#8a97a8;} .cmp_label b.af{background:#e64545;}
.cmp_label small{font-weight:400;color:#888;font-size:12px;margin-left:auto;}
.cmp_note{width:1024px;margin:10px auto 30px;padding:12px 18px;border:1px solid #e6e6e6;border-radius:5px;background:#fafafa;font-size:12px;color:#555;line-height:1.7;}
.cmp_note b{color:#e64545;}
/* 현행 모사 */
.rpt_old table{border-collapse:collapse;border-spacing:0;}
.rpt_old .obottom{display:flex;gap:30px;margin-top:26px;}
.rpt_old .oleft{flex:0 0 300px;} .rpt_old .oright{flex:1;min-width:0;}
.rpt_old .otitle{position:relative;padding-left:10px;font-size:12px;font-weight:800;color:#333;line-height:30px;}
.rpt_old .otitle::before{content:'';position:absolute;left:0;top:9px;width:3px;height:13px;background:#e64545;}
.rpt_old .odn{display:grid;grid-template-columns:1fr 1fr;gap:8px 0;margin-top:4px;}
.rpt_old .od{position:relative;width:118px;height:118px;margin:0 auto;}
.rpt_old .od .ctr{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;line-height:1.15;}
.rpt_old .od .ctr span{font-size:12px;color:#555;} .rpt_old .od .ctr strong{font-size:18px;font-weight:800;color:#333;}
.rpt_old .bandlab{display:flex;margin-top:6px;font-size:13px;color:#999;}
.rpt_old .bandlab span{flex:1;text-align:center;}
.rpt_old .bell{display:block;margin-top:4px;width:100%;height:auto;border:1px solid #ddd;}
.rpt_old .oarert{margin:26px 0 0 330px;width:calc(100% - 330px);float:none;line-height:20px;padding:8px 20px 8px 45px;font-size:12.5px;}
.rpt_old .oarert em{font-style:normal;color:#aaa;font-size:11px;}
"""
hdr=lambda name:(f'<div id="header"><div class="yGnb_wrap yGnbreport_wrap"><div><h4 class="type_eval"></h4></div><div class="reportInfo_wrap"><p class="day">{S["date"]}</p><div>진단평가 리포트</div><dl><dd><span>이름</span><span>{name}</span></dd><dd><span>학년</span><span>{S["grade"]}</span></dd></dl></div></div></div>')
html=(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>진단평가 1p — 현행 vs v7 (초4 전 영역, 예시 학생 A)</title>{g7.CSSLINKS}<style>{CSS}</style></head><body>'
 '<nav class="mk_bar"><strong>진단평가 리포트 1p · 현행 vs 개선안 v7</strong><span class="hint">같은 학생(초4 · 2025.08.27 응시 · 파닉스 75 · 듣말 84.6 · 읽쓰 60 · 문법 70)</span></nav>'
 f'<div class="cmp_label"><b class="bf">BEFORE</b>현행 리포트 1p<small>위치 = 낮은 영역(읽기/쓰기 4.5단계) 기준 · 2022.11 기준표 · 상위 {CUR_POS}% = {G9}등급</small></div>'
 f'<section class="mk_page">{hdr("예시 학생 A")}{before}</section>'
 f'<div class="cmp_label"><b class="af">AFTER</b>개선안 v7<small>위치 = 응시 4영역 합계 스케일 기준 · 최근 3년 창 · 상위 {S["pos"]}% · 평균 구간</small></div>'
 f'<section class="mk_page">{hdr("예시 학생 A")}<div class="rep rpt_v7"><div class="content"><div class="slide_pa">{after}</div></div></div></section>'
 '<div class="cmp_note"><b>같은 점수인데 달라지는 것</b><br>'
 '· 위치값: 현행은 듣말·읽쓰 중 낮은 읽기/쓰기(4.5단계) 하나로 50.2%, 개선안은 응시한 4영역을 합쳐 41.8%. 듣기/말하기(초6 수준)가 반영됨.<br>'
 '· 표기: 9등급 벨커브 → 3구간(평균 이하 / 평균 / 평균 이상) 눈금자. 상위 80% 초과는 수치 대신 "상위 80% 이하".<br>'
 '· 영역별: 점수만 → 점수 + 수준(도달 단계) + 동학년 위치. 강점·시작점 기준 라벨.<br>'
 '· 총평: 위치값 한 가지로 생성 → 위치 + 강점 + 시작 교재(단계·영역) 3문장.<br>'
 '· 레이아웃(시작점 위 / 성취도 좌 / 위치 우)과 단계표·원그래프는 그대로.</div>'
 '</body></html>')
open(os.path.join(OUT,'compare_before_after.html'),'w',encoding='utf-8').write(html); print('ok', G9)
