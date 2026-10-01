# -*- coding: utf-8 -*-
"""v7: v6f를 기준으로 영역 조합·학년 샘플을 탭으로 모은 목업. 데이터는 samples7.json(실제 응시 기록·정답률)."""
import os, json, math
OUT=os.environ.get('OUT',os.path.expanduser('~/mnt/leveltest/진단평가리포트업글_codex/ys_report_mockups_v7_service'))
CSSLINKS=os.environ.get('CSSLINKS','<link rel="stylesheet" href="https://leveltest.yoons.com/css/common.css?v=1.0"><link rel="stylesheet" href="https://leveltest.yoons.com/css/w_reset.css?v=1.0"><link rel="stylesheet" href="https://leveltest.yoons.com/css/w_base.css?v=1.27"><link rel="stylesheet" href="https://leveltest.yoons.com/css/w_media.css?v=1.2">')
HERE=os.path.dirname(os.path.abspath(__file__))
SAMPLES=os.environ.get('SAMPLES',os.path.join(HERE,'samples7.json'))
os.makedirs(OUT,exist_ok=True)
CSS=open(os.path.join(HERE,'v7.css'),encoding='utf-8').read()
COL={'P':'#ef7c00','L':'#0a953d','R':'#0078bf','G':'#7b5aa3'}
NM={'P':'파닉스','L':'듣기/말하기','R':'읽기/쓰기','G':'문법'}
GR={'초등 1':'초1','초등 2':'초2','초등 3':'초3','초등 4':'초4','초등 5':'초5','초등 6':'초6','중등 1':'중1','중등 2':'중2','중등 3':'중3','고등 1':'고1','고등 2':'고2','고등 3':'고3'}
TABS=[('e4_all','초4 · 전 영역','예시 학생 A'),('e1_plr','초1 · 파닉스+L/R','예시 학생 B'),('e6_all_low','초6 · 전 영역 (평균 이하)','예시 학생 C'),
      ('m1_lrg','중1 · L/R+문법','예시 학생 D'),('h1_all','고1 · 전 영역','예시 학생 E'),('e3_p','초3 · 파닉스만','예시 학생 F'),('e4_pg','초4 · 파닉스+문법','예시 학생 G')]
def lv(s): return str(s).replace('All Star','All-Star')
def band(p): return '평균 이상' if p<=20 else ('평균' if p<=80 else '평균 이하')
def ptxt(p): return '상위 80% 이하' if p>80 else f'상위 {round(p)}%'
def pinpos(p): return min(p,90)
def tag(p): return ('강점','hi') if p<=20 else (('취약','lo') if p>80 else ('',''))
def cell_of(level):
    s=level.replace('All Star','All-Star')
    for k in ['초1','초2','초3','초4','초5','초6','예비중']:
        if s.endswith(k): return k
    return s.split()[-1]  # 중고등 N
def yes_table(start_cell):
    cols=[('초1',0),('초2',1),('초3',0),('초4',1),('초5',0),('초6',1),('예비중',1)]+[(str(i),0) for i in range(1,10)]
    cells=''.join(f'<td class="{"bgred " if k==start_cell else ""}{"borderright" if br else ""}">{k}</td>' for k,br in cols)
    return ('<div class="tableLayout_wrap"><table style="width:100%;table-layout:fixed"><colgroup><col style="width:69px">'+'<col style="width:57px">'*16+'</colgroup>'
     '<tr><th rowspan="2">YES&nbsp;4.0</th><th colspan="2">Rookie</th><th colspan="2">Rising&nbsp;Star</th><th colspan="2">All-Star</th><th>MVP</th><th colspan="9">중고등</th></tr>'
     f'<tr class="height30">{cells}</tr></table></div>')
def phonics_table(stage, grade):
    st=['Beginner','Intermediate','Advanced','Master'] if grade.startswith('중') or grade.startswith('고') else ['알파벳','자음','단모음','장모음','기타자음','기타모음','Master']
    return ('<div class="tableLayout_wrap ph_table"><table style="width:100%;table-layout:fixed"><colgroup><col style="width:69px"></colgroup><tr><th rowspan="2">파닉스</th>'+''.join(f'<th>{x}</th>' for x in st)+'</tr><tr class="height30">'+''.join(f'<td class="{"bgred" if x==stage else ""}">{x}</td>' for x in st)+'</tr></table></div>')
def donut(score,col,r=44,w=9):
    c=2*math.pi*r; return (f'<svg viewBox="0 0 110 110" width="96" height="96"><circle cx="55" cy="55" r="{r}" fill="none" stroke="#e9e9e9" stroke-width="{w}"/>'
     f'<circle cx="55" cy="55" r="{r}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-dasharray="{c*score/100:.1f} {c:.1f}" transform="rotate(-90 55 55)"/></svg>')
def donuts(S):
    A=S['area']; bys={S['start'].get('by'),S['start'].get('by2')}; out=''
    for a in ('P','L','R','G'):
        if a not in A: continue
        x=A[a]; t,tc=tag(x['pos'])
        tg=(f'<b class="tg {tc}">{t}</b>' if t else '')+('<b class="tg st">시작점 기준</b>' if a in bys else '')
        reach=x['stage'] if a=='P' else lv(x['level'])
        out+=(f'<div class="dn" style="--c:{COL[a]}"><span class="tags">{tg}</span><div class="ring">{donut(x["score"],COL[a])}<div class="ctr"><span class="nm">{NM[a]}</span><strong>{x["score"]:g}점</strong></div></div>'
              f'<div class="rw"><span>수준</span><b>{reach}</b></div><div class="rw"><span>위치</span><b>{ptxt(x["pos"])}</b></div></div>')
    n=len(A); return f'<div class="dns n{n}">{out}</div>'
def ruler(S):
    pos=S['pos']; b=band(pos); lab=f'{ptxt(pos)} · {b}' if pos<=80 else ptxt(pos)
    pin=f'<div class="pin" style="left:{100-pinpos(pos)}%"><div class="tip">{lab}</div><div class="stem"></div></div>'
    n=len(S['area']); names=' · '.join(NM[a] for a in 'PLRG' if a in S['area'])
    cap=(f'{names} 기준' if n==1 else f'{names} 종합')+f'<br>전국 {GR[S["grade"]]} 응시자 기준'
    return (f'<div class="ruler_col"><div class="ruler">{pin}<div class="bands"><span class="lo">평균 이하</span><span class="mid">평균</span><span class="hi">평균 이상</span></div>'
            '<div class="ticks"><span class="l" style="left:0">100%</span><span style="left:20%">80%</span><span style="left:80%">20%</span><span class="r" style="left:100%">1%</span></div></div>'
            f'<p class="cap">{cap}</p></div>')
def strength_sentence(A):
    hi=[NM[a] for a in 'PLRG' if a in A and A[a]['pos']<=20]; lo=[NM[a] for a in 'PLRG' if a in A and A[a]['pos']>80]
    if hi and lo: return f'{"·".join(hi)}가 강점이고, {"·".join(lo)}는 보완이 필요해요. '
    if hi: return f'{"·".join(hi)}가 강점이에요. '
    if lo: return f'{"·".join(lo)}는 보완이 필요해요. '
    return ''
def start_sentence(S):
    st=S['start']; by=st['by']
    if by in ('L','R'): return f'<b>{lv(st["level"])}</b> 단계 <b>{NM[by]}</b> 영역 교재부터 학습을 시작하세요.'
    if by=='P' and 'by2' in st: return f'파닉스 <b>{st["level"]}</b> 단계, 문법 <b>{lv(st["level2"])}</b> 단계 교재부터 학습을 시작하세요.'
    if by=='P': return f'파닉스 <b>{st["level"]}</b> 단계 교재부터 학습을 시작하세요.'
    return f'문법 <b>{lv(st["level"])}</b> 단계 교재부터 학습을 시작하세요.'
def start_section(S):
    st=S['start']; g=S['grade']
    if st['by'] in ('L','R'):
        return ('<div class="sec3"><div class="level_section"><dl><dt><span class="title">나에게 맞는 학습 시작점</span><span class="level">'+lv(st['level'])+'</span>'
                f'<span class="cue">{NM[st["by"]]} 기준</span></dt><dd>'+yes_table(cell_of(st['level']))+'</dd></dl></div></div>')
    if st['by']=='P' and 'by2' in st:
        return ('<div class="sec3 dual"><div class="level_section"><dl><dt><span class="title">나에게 맞는 학습 시작점</span><span class="level">파닉스 '+st['level']+'</span><span class="level">문법 '+lv(st['level2'])+'</span>'
                '<span class="cue">메인 커리큘럼 레벨은 듣기/말하기·읽기/쓰기 응시 시 제공</span></dt><dd>'+phonics_table(st['level'],g)+yes_table(cell_of(st['level2']))+'</dd></dl></div></div>')
    if st['by']=='P':
        return ('<div class="sec3"><div class="level_section"><dl><dt><span class="title">나에게 맞는 학습 시작점</span><span class="level">파닉스 '+st['level']+'</span>'
                '<span class="cue">메인 커리큘럼 레벨은 듣기/말하기·읽기/쓰기 응시 시 제공</span></dt><dd>'+phonics_table(st['level'],g)+'</dd></dl></div></div>')
    return ('<div class="sec3"><div class="level_section"><dl><dt><span class="title">나에게 맞는 학습 시작점</span><span class="level">문법 '+lv(st['level'])+'</span>'
            '<span class="cue">메인 커리큘럼 레벨은 듣기/말하기·읽기/쓰기 응시 시 제공</span></dt><dd>'+yes_table(cell_of(st['level']))+'</dd></dl></div></div>')
def page_body(S):
    gr=GR[S['grade']]
    return (start_section(S)+
     '<div class="two"><div class="colL"><dl><dt><span class="title">나의 영역별 성취수준</span></dt><dd>'+donuts(S)+'</dd></dl></div>'
     '<div class="colR"><dl><dt><span class="title">동학년 대비 나의 위치</span></dt><dd>'+ruler(S)+
     f'<div class="arert_wrap"><span></span>{gr} 응시자 중 <b>{ptxt(S["pos"])}</b>로, <b>{band(S["pos"])} 구간</b>이에요. {strength_sentence(S["area"])}{start_sentence(S)}</div></dd></dl></div></div>')
D=json.load(open(SAMPLES,encoding='utf-8'))
secs=''; btns=''
for i,(key,label,name) in enumerate(TABS):
    S=D[key]
    btns+=f'<a href="#" data-t="{key}" class="{"on" if i==0 else ""}">{label}</a>'
    secs+=(f'<section class="mk_page" id="{key}" style="{"" if i==0 else "display:none"}"><div id="header"><div class="yGnb_wrap yGnbreport_wrap"><div><h4 class="type_eval"></h4></div><div class="reportInfo_wrap"><p class="day">{S["date"]}</p><div>진단평가 리포트</div><dl><dd><span>이름</span><span>{name}</span></dd><dd><span>학년</span><span>{S["grade"]}</span></dd></dl></div></div></div>'
           f'<div class="rep rpt_v7"><div class="content"><div class="slide_pa">{page_body(S)}</div></div></div><div class="mk_dots"><i class="on"></i><i></i><i></i><i></i><i></i></div>'
           f'<p class="mk_tag">응시 {S["date"]} · 조합 {S["combo"]} · 종합 위치 {S["pos"]}% ({S["pos_basis"]}) · 모든 수치 실제값</p></section>')
JS='''<script>document.querySelectorAll('.mk_bar a[data-t]').forEach(a=>{a.onclick=e=>{e.preventDefault();document.querySelectorAll('.mk_bar a[data-t]').forEach(x=>x.classList.remove('on'));a.classList.add('on');document.querySelectorAll('section.mk_page').forEach(s=>s.style.display=s.id===a.dataset.t?'':'none');};});</script>'''
html=(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>진단평가 1p v7 — 조합·학년 샘플</title>{CSSLINKS}<style>{CSS}</style></head><body>'
      f'<nav class="mk_bar"><strong>진단평가 리포트 1p · v7</strong>{btns}<span class="hint">v6f 기준 · 실제 응시 기록·정답률</span></nav>{secs}{JS}</body></html>')
open(os.path.join(OUT,'index.html'),'w',encoding='utf-8').write(html); print('ok')
