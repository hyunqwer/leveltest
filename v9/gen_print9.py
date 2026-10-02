# -*- coding: utf-8 -*-
"""인쇄(A4 세로 1장) 버전: v8 1p + 2p(C1 또는 C2). gen_v8의 마크업 함수를 재사용하고 .prt 범위 CSS로 축소 배치."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_v9 as g
OUT=g.OUT; S=g.S; NM=g.NM
HDR=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'hdr.b64')).read().strip()  # 현행 인쇄본 헤더 캡처(660×102)
PRT_CSS=r'''
@page{size:A4 portrait;margin:0}
body{background:#eee;margin:0}
.prt{box-sizing:border-box;width:794px;min-height:1123px;margin:0 auto;background:#fff;padding:0 67px 20px;font-family:"Noto Sans KR","Noto Sans CJK KR","Malgun Gothic",sans-serif;color:#333;position:relative}
@media print{body{background:#fff}.prt{margin:0;box-shadow:none}.mk_bar{display:none}}
.prt .bars{display:flex;justify-content:space-between;height:5px}
.prt .bars i{display:block;width:170px;height:5px;background:#ef7c00}.prt .bars i+i{background:#e64545;width:140px}
.prt .hd{position:relative;margin-top:6px;height:72px;background:#f4f4f4;border:1px solid #e3e3e3;border-radius:4px;overflow:hidden}
.prt .hd .yes{position:absolute;left:10px;top:-8px;font-size:66px;font-weight:900;color:#ddd;letter-spacing:-4px;font-family:Arial,sans-serif}
.prt .hd h1{position:absolute;left:0;right:0;top:0;line-height:72px;text-align:center;font-size:21px;font-weight:800;color:#333;margin:0}
.prt .hd .date{position:absolute;right:14px;top:8px;font-size:11px;color:#666}
.prt .info{display:flex;margin-top:6px;border:1px solid #e3e3e3;border-radius:4px;overflow:hidden}
.prt .info div{flex:1;height:30px;line-height:30px;font-size:12px;padding:0 10px;background:#fff}.prt .info div+div{border-left:1px solid #e3e3e3}
.prt .info span{color:#888;margin-right:8px;font-size:11px}.prt .info b{font-weight:700}
.prt .st{position:relative;margin:22px 0 8px;padding-left:9px;font-size:13px;font-weight:800;line-height:18px}
.prt .st::before{content:'';position:absolute;left:0;top:2px;width:3px;height:14px;background:#333}
.prt .st .level{display:inline-block;margin-left:10px;height:24px;line-height:21px;border:2px solid #e64545;border-radius:100px;color:#e64545;font-size:12.5px;padding:0 11px;vertical-align:middle}
.prt .st .cue{margin-left:8px;font-size:11px;color:#888;font-weight:400}
.prt .st .lg{float:right;font-size:10.5px;color:#777;font-weight:400}
.prt .st .lg i{display:inline-block;vertical-align:middle;margin:0 3px 0 8px}.prt .st .lg i.me{width:20px;height:8px;border-radius:0 4px 4px 0;background:linear-gradient(to right,#ef7c00 0 25%,#0a953d 25% 50%,#0078bf 50% 75%,#7b5aa3 75%)}.prt .st .lg i.av{width:0;height:0;border-left:4px solid transparent;border-right:4px solid transparent;border-top:8px solid #555}
.prt .hdimg{display:block;width:660px;height:auto;margin:0}
/* 시작점 표 */
.prt .ytb table{width:100%;table-layout:fixed;border-collapse:collapse;border-top:2px solid #293138}
.prt .ytb th{height:26px;font-size:11px;font-weight:700;background:#f7f7f7;border:1px solid #ddd;border-top:0;color:#333}
.prt .ytb td{height:28px;font-size:11.5px;text-align:center;border:1px solid #e3e3e3}
.prt .ytb td.bgred{background:#e64545;color:#fff;font-weight:700}
.prt .ytb col:first-child{width:52px}
/* 2단 */
.prt .two{display:flex;gap:18px;align-items:stretch}
.prt .colL{flex:0 0 250px}.prt .colR{flex:1;min-width:0;display:flex;flex-direction:column}
.prt .dns{display:grid;grid-template-columns:1fr 1fr;gap:4px 0;margin-top:2px}
.prt .dn{position:relative;display:flex;flex-direction:column;align-items:center;padding:20px 0 2px}
.prt .dn .tags{position:absolute;left:50%;top:6px;transform:translateX(-50%);z-index:2;white-space:nowrap}
.prt .dn .tg{display:inline-block;padding:0 5px;height:15px;line-height:12px;border-radius:3px;font-size:8.5px;font-weight:700;background:#fff;color:#e64545;border:1.5px solid #e64545}
.prt .dn .ring{position:relative;width:104px;height:104px}.prt .dn .ring svg{display:block;width:104px;height:104px}
.prt .dn .ctr{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;line-height:1.15}
.prt .dn .ctr .nm{font-size:12px;color:#555}.prt .dn .ctr strong{font-size:20px;font-weight:800;color:#333;letter-spacing:-.5px}
.prt .bell{display:block;width:100%;height:auto;margin-top:0}
.prt .arert{margin-top:auto;display:flex;gap:8px;align-items:flex-start;padding:10px 14px;border:1px solid #c9d3e0;border-radius:5px;background:#eef3fa;font-size:12.5px;line-height:19px}
.prt .arert b{color:#e64545;font-weight:700}
.prt .arert::before{content:'';flex:none;width:18px;height:18px;border-radius:50%;background:#333 url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path fill='%23fff' d='M9 21h6v-1H9v1zm3-19a7 7 0 0 0-4 12.7V17h8v-2.3A7 7 0 0 0 12 2z'/></svg>") center/12px no-repeat}
/* 카드 */
.prt .cds{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.prt .cd{padding:11px 10px 9px;border:1px solid #e0e0e0;border-top:3px solid var(--c);border-radius:4px}
.prt .cd .hd2{display:flex;align-items:center;font-size:11px;font-weight:700;color:var(--c);height:16px}
.prt .cd .tg{display:inline-block;margin-left:5px;padding:0 4px;height:14px;line-height:11px;border-radius:3px;font-size:8px;font-weight:700;background:#fff;color:#e64545;border:1.5px solid #e64545}
.prt .cd .lv{margin-top:7px;font-size:15.5px;font-weight:800;color:#333;letter-spacing:-.3px;white-space:nowrap}
.prt .cd .mb{position:relative;height:10px;margin:13px 0 4px;border-radius:0 5px 5px 0;background:#f1f1f1}
.prt .cd .mb .fill{position:absolute;left:0;top:0;height:100%;border-radius:0 5px 5px 0;background:var(--c);opacity:.9}
.prt .cd .mb .av{position:absolute;top:-4px;width:0;height:0;margin-left:-4px;border-left:4px solid transparent;border-right:4px solid transparent;border-top:8px solid #555}
.prt .cd .avl{margin-top:4px;font-size:9.5px;color:#888;white-space:nowrap}
.prt .cd .rw{display:flex;align-items:baseline;gap:4px;margin-top:8px;padding-top:8px;border-top:1px dashed #e6e6e6;font-size:10px;color:#888;white-space:nowrap}
.prt .cd .rw span{flex:none;min-width:26px;margin-right:2px}.prt .cd .rw b{font-size:14px;font-weight:800;color:#333}.prt .cd .rw b.pos{color:#e64545}.prt .cd .rw small{font-size:9.5px;color:#999}
/* 하단 박스 */
.prt .pboxes{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:14px}
.prt .pbox{padding:11px 12px;border:1.5px solid var(--bc);border-radius:5px;background:var(--bg);font-size:12px;line-height:1.7;color:#444}
.prt .pbox.c-lr{grid-column:span 2}.prt .pbox b{display:block;margin-bottom:3px;font-size:11.5px;color:var(--bc)}
.prt .c-p{--bc:#ef7c00;--bg:#fff7ee}.prt .c-lr{--bc:#2e9e5b;--bg:#eef9f1}.prt .c-g{--bc:#7b5aa3;--bg:#f3eef9}
.prt .sumbox{margin-top:14px;padding:14px 18px;border:1.5px solid #c9d3e0;border-radius:5px;background:#f4f7fb;font-size:12.5px;line-height:1.8;color:#444}
.prt .sumbox .sh{font-size:11px;font-weight:800;color:#345;margin:0 0 3px}.prt .sumbox p{margin:0}.prt .sumbox p b{font-weight:700;color:#333}
.prt .sumbox.one{margin-top:8px;padding:7px 14px 3px;background:#fafafa;border-color:#ddd;line-height:1.5}.prt .sumbox.one .sh{color:#333;margin-bottom:2px;font-size:11px}
.prt .sumbox .sr{display:flex;gap:10px;align-items:flex-start;padding:4px 0;border-top:1px dashed #e3e3e3;line-height:1.5;font-size:11px}
.prt .sumbox .sr:first-child{border-top:0;padding-top:1px}.prt .sumbox .sr .lab{flex:0 0 118px;font-size:11px;font-weight:800;color:var(--bc)}.prt .sumbox .sr .tx{flex:1;min-width:0}.prt .sumbox .sr .tx b{display:inline;color:#333;font-weight:700;margin-right:4px}.prt .sumbox .sr .tx p{display:inline;margin:0;color:#555}
.prt .foot{position:absolute;left:67px;right:67px;bottom:10px;font-size:9.5px;color:#aaa;text-align:center}
'''
def yes_table_p():
    cols=[('초1',0),('초2',1),('초3',0),('초4',1),('초5',0),('초6',1),('예비중',1)]+[(str(i),0) for i in range(1,10)]
    cells=''.join(f'<td class="{"bgred" if k==S["start"]["cell"] else ""}">{k}</td>' for k,br in cols)
    return ('<div class="ytb"><table><colgroup><col>'+'<col>'*16+'</colgroup>'
            '<tr><th rowspan="2">YES 4.0</th><th colspan="2">Rookie</th><th colspan="2">Rising Star</th><th colspan="2">All-Star</th><th>MVP</th><th colspan="9">중고등</th></tr>'
            f'<tr>{cells}</tr></table></div>')
def donuts_p():
    out=''
    for a in 'LRPG':
        x=S['area'][a]; tg='<b class="tg">시작점 기준</b>' if a==S['start']['by'] else ''
        out+=(f'<div class="dn"><span class="tags">{tg}</span><div class="ring">{g.donut(x["score"],g.COL[a],r=49,w=9)}<div class="ctr"><span class="nm">{NM[a]}</span><strong>{x["score"]:g}점</strong></div></div></div>')
    return f'<div class="dns">{out}</div>'
def card_p(a):
    x=S['area'][a]; n=7 if a=='P' else 16; name=x['stage'] if a=='P' else x['level']
    fill=x['cellpos']/n*100; av=g.AVG[a]['cellpos']/n*100
    tg='<b class="tg">시작점 기준</b>' if a==S['start']['by'] else ''
    return (f'<div class="cd" style="--c:{g.COL[a]}"><div class="hd2">{NM[a]}{tg}</div><div class="lv">{name}</div>'
            f'<div class="mb"><i class="fill" style="width:{fill:.1f}%"></i><i class="av" style="left:{av:.1f}%"></i></div>'
            f'<div class="rw"><span>점수</span><b>{x["score"]:g}점</b><small>{x["k"]} / {x["n"]}문항</small></div>'
            f'<div class="rw"><span>동학년 대비</span><b>{g.ptxt(x["pos"])}</b></div></div>')
def page(variant):
    gr=S['gr']; by=S['start']['by']
    if variant=='c1':
        bottom=('<div class="pboxes">'+''.join(f'<div class="pbox {cls}"><b>{g.BOX[k][0]}</b>{g.BOX[k][1]}</div>' for k,cls in (('P','c-p'),('LR','c-lr'),('G','c-g')))+'</div>')
    else:
        bottom=g.sumbox_c1()
    return (f'<div class="prt"><img class="hdimg" src="data:image/png;base64,{HDR}" alt="윤선생 진단평가 리포트">'
            f'<p class="st">나에게 맞는 학습 시작점<span class="level">{S["start"]["level"]}</span><span class="cue">{NM[by]} 기준</span></p>{yes_table_p()}'
            '<div class="two"><div class="colL"><p class="st">나의 영역별 점수</p>'+donuts_p()+'</div>'
            '<div class="colR"><p class="st">동학년 대비 나의 위치</p>'+g.bell(S['pos'])+
            f'<div class="arert"><span>{gr} 응시자 중 <b>{g.ptxt(S["pos"])}</b>로, <b>{g.band(S["pos"])} 구간</b>이에요. <b>{S["start"]["level"]}</b> 단계 <b>{NM[by]}</b> 영역 교재부터 학습을 시작하세요.</span></div></div></div>'
            '<p class="st">영역별 진단·처방<span class="lg"><i class="me"></i>내 수준 <i class="av"></i>학년 평균</span></p><div class="cds">'+''.join(card_p(a) for a in 'PLRG')+'</div>'
            +bottom+
            '<p class="foot">※ 동학년 대비 위치는 전국 동학년 응시자 기준이며, 2페이지 처방 문구는 '+('현행 샘플(자리표시)' if variant=='c1' else '현행 샘플(자리표시)')+'입니다.</p></div>')
for v,title in (('c1','v9'),):
    html=(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>진단평가 리포트 v9 — 인쇄용</title>'
          f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap"><style>{PRT_CSS}</style></head><body>{page(v)}</body></html>')
    open(os.path.join(OUT,'print.html'),'w',encoding='utf-8').write(html)
print('print ok')

# ---- index.html: 1p / 2p / 인쇄용 탭 하나로 ----
TABJS="<script>document.querySelectorAll('.mk_bar a[data-t]').forEach(a=>{a.onclick=e=>{e.preventDefault();document.querySelectorAll('.mk_bar a[data-t]').forEach(x=>x.classList.remove('on'));a.classList.add('on');document.querySelectorAll('section.mk_page').forEach(s=>s.style.display=s.id===a.dataset.t?'':'none');};});</script>"
dots='<div class="mk_dots"><i class="on"></i><i></i><i></i><i></i><i></i></div>'
secs=(f'<section class="mk_page" id="p1">{g.header(S["name"],S["grade"],S["date"])}{g.page1()}{dots}</section>'
      f'<section class="mk_page" id="p2" style="display:none">{g.header(S["name"],S["grade"],S["date"])}{g.page2c()}{dots}</section>'
      f'<section class="mk_page" id="pr" style="display:none">{page("c1")}</section>')
idx=(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>진단평가 리포트 v9</title>{g.CSSLINKS}'
     f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap"><style>{g.CSS}{PRT_CSS}'
     'body{background:#fff}.mk_bar a.on{border-color:#e64545;color:#e64545;font-weight:700}#pr{background:#eee;padding:20px 0}#pr .prt{box-shadow:0 2px 12px rgba(0,0,0,.12)}</style></head><body>'
     '<nav class="mk_bar"><strong>진단평가 리포트 · v9</strong><a href="#" data-t="p1" class="on">1페이지</a><a href="#" data-t="p2">2페이지</a><a href="#" data-t="pr">인쇄용 (A4)</a>'
     '<span class="hint">초4 전 영역 · 2025.08.27 응시 · 점수·수준·위치 실제값 · 2p 처방 문구는 현행 샘플(자리표시)</span></nav>'
     f'{secs}{TABJS}</body></html>')
open(os.path.join(OUT,'index.html'),'w',encoding='utf-8').write(idx); print('index ok')
