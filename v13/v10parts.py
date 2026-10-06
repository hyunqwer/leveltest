# -*- coding: utf-8 -*-
"""v10: 1p(시작점 / 원그래프 점수 / 벨커브 종합 위치) + 2p(영역별 수준·점수·또래 위치 + 진단 처방). 초4 전 영역 예시 학생 A."""
import os, json, math
HERE=os.path.dirname(os.path.abspath(__file__))
OUT=os.environ.get('OUT',os.path.expanduser('~/mnt/leveltest/진단평가리포트업글_codex/ys_report_mockups_v10_service'))
CSSLINKS=os.environ.get('CSSLINKS','<link rel="stylesheet" href="https://leveltest.yoons.com/css/common.css?v=1.0"><link rel="stylesheet" href="https://leveltest.yoons.com/css/w_reset.css?v=1.0"><link rel="stylesheet" href="https://leveltest.yoons.com/css/w_base.css?v=1.27"><link rel="stylesheet" href="https://leveltest.yoons.com/css/w_media.css?v=1.2">')
os.makedirs(OUT,exist_ok=True)
CSS=open(os.path.join(HERE,'v10.css'),encoding='utf-8').read()
COL={'P':'#ef7c00','L':'#0a953d','R':'#0078bf','G':'#7b5aa3'}
NM={'P':'파닉스','L':'듣기/말하기','R':'읽기/쓰기','G':'문법'}
# ---- 실데이터: 통합 NO 195021 = 점수추가 2025.08.27 초4 (점수·정답수·SCALE 실제값)
S={'name':'예시 학생 A','grade':'초등 4','gr':'초4','date':'2025.08.27',
   'start':{'by':'R','level':'Rising Star 초4','cell':'초4'},
   'area':{'P':{'stage':'장모음','score':75.0,'k':9,'n':12,'pos':73.3,'cellpos':4.0},
           'L':{'level':'All-Star 초6','score':84.6,'k':11,'n':13,'pos':14.9,'cellpos':6.0},
           'R':{'level':'Rising Star 초4','score':60.0,'k':6,'n':10,'pos':43.9,'cellpos':4.0},
           'G':{'level':'All-Star 초5','score':70.0,'k':7,'n':10,'pos':43.8,'cellpos':5.0}},
   'pos':41.8}   # 버전B 4영역 합계 스케일 45 → 초4
# 초4 학년 평균 SCALE (실데이터, 진단평가_학년별_영역평균SCALE.xlsx 학년별 평균): P 11.3 / L 14.8 / R 11.4 / G 2.1
# → v3 기준표로 측정단계 환산 후 축 위치(칸 단위, 0 = 첫 칸 시작)로 보간
AVG={'P':{'label':'장모음','cellpos':3.6},       # 초4 파닉스 평균 = 장모음 (사용자 확인) → 장모음 칸 안
     'L':{'label':'All-Star 초5','cellpos':4.05},  # 14.8 → 측정단계 ≈4.95 ≈ 5.0 → 초5 칸 시작
     'R':{'label':'Rising Star 초4','cellpos':3.35}, # 11.4 → ≈4.35 → 초4 칸 안
     'G':{'label':'Rising Star 초4','cellpos':3.55}} # 2.1 → ≈4.55 → 초4 칸 안
def band(p): return '평균 이상' if p<=20 else ('평균' if p<=80 else '평균 이하')
def ptxt(p): return '상위 80% 이하' if p>80 else f'상위 {round(p)}%'
def pinpos(p): return min(p,90)
# ---------- 공통 ----------
def header(name,grade,date):
    return (f'<div id="header"><div class="yGnb_wrap yGnbreport_wrap"><div><h4 class="type_eval"></h4></div><div class="reportInfo_wrap"><p class="day">{date}</p><div>진단평가 리포트</div><dl><dd><span>이름</span><span>{name}</span></dd><dd><span>학년</span><span>{grade}</span></dd></dl></div></div></div>')
def yes_table(start_cell):
    cols=[('초1',0),('초2',1),('초3',0),('초4',1),('초5',0),('초6',1),('예비중',1)]+[(str(i),0) for i in range(1,10)]
    cells=''.join(f'<td class="{"bgred " if k==start_cell else ""}{"borderright" if br else ""}">{k}</td>' for k,br in cols)
    return ('<div class="tableLayout_wrap"><table style="width:100%;table-layout:fixed"><colgroup><col style="width:69px">'+'<col style="width:57px">'*16+'</colgroup>'
     '<tr><th rowspan="2">YES&nbsp;4.0</th><th colspan="2">Rookie</th><th colspan="2">Rising&nbsp;Star</th><th colspan="2">All-Star</th><th>MVP</th><th colspan="9">중고등</th></tr>'
     f'<tr class="height30">{cells}</tr></table></div>')
# ---------- 1p ----------
def donut(score,col,r=49,w=9):
    c=2*math.pi*r; return (f'<svg viewBox="0 0 118 118" width="118" height="118"><circle cx="59" cy="59" r="{r}" fill="none" stroke="#e9e9e9" stroke-width="{w}"/>'
     f'<circle cx="59" cy="59" r="{r}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-dasharray="{c*score/100:.1f} {c:.1f}" transform="rotate(-90 59 59)"/></svg>')
def donuts():
    out=''
    order='PLRG'   # 상단 파닉스/듣기말하기, 하단 읽기쓰기/문법
    for a in [k for k in order if k in S['area']]:
        x=S['area'][a]; tg=''  # v13: 시작점 기준 태그 삭제
        out+=(f'<div class="dn" style="--c:{COL[a]}"><span class="tags">{tg}</span><div class="ring">{donut(x["score"],COL[a])}<div class="ctr"><span class="nm">{NM[a]}</span><strong>{x["score"]:g}점</strong></div></div></div>')
    return f'<div class="dns">{out}</div>'
def bell(pos, W=600, H=230):
    """현행 리포트 하이차트 모사: 테두리+가로 그리드, 회색 영역 곡선, 80/20 세로 플롯라인, 빨간 마커(선+점+라벨). x축 = 상위% 선형(왼쪽 100% → 오른쪽 1%)"""
    L,R,T,B=10,10,30,36; pw=W-L-R; ph=H-T-B
    def X(p): return L+(100-p)/100*pw
    def Y(f): return T+ph-f*ph*0.86
    sig=0.21
    pts=[(X(100-i), Y(math.exp(-((i/100-0.5)**2)/(2*sig*sig)))) for i in range(0,101)]
    line=' '.join(f'{x:.1f},{y:.1f}' for x,y in pts)
    area=f'M{L},{T+ph} L'+line.replace(' ',' L')+f' L{L+pw},{T+ph} Z'
    grid=''.join(f'<line x1="{L}" y1="{T+ph*k/4:.1f}" x2="{L+pw}" y2="{T+ph*k/4:.1f}" stroke="#e6e6e6"/>' for k in range(0,4))
    plot=''.join(f'<line x1="{X(p):.1f}" y1="{T}" x2="{X(p):.1f}" y2="{T+ph}" stroke="#c8c8c8" stroke-width="1.2"/>' for p in (80,20))
    tk=''.join(f'<line x1="{X(p):.1f}" y1="{T+ph}" x2="{X(p):.1f}" y2="{T+ph+6}" stroke="#bbb"/><text x="{X(p):.1f}" y="{T+ph+19}" font-size="11" text-anchor="middle" fill="#666">{p}%</text>' for p in (90,80,50,20,10))
    labs=''.join(f'<text x="{X(c):.1f}" y="{T-11}" font-size="12.5" text-anchor="middle" fill="#888">{t}</text>' for c,t in ((90,'Below Average'),(50,'Average'),(10,'Above Average')))
    pp=pinpos(pos); mx=X(pp); my=Y(math.exp(-(((100-pp)/100-0.5)**2)/(2*sig*sig)))
    lab=ptxt(pos); bw=len(lab)*8.2+18; bh=24; by=T+ph*0.55
    bx=mx+10 if mx+10+bw<L+pw else mx-10-bw
    marker=(f'<line x1="{mx:.1f}" y1="{T}" x2="{mx:.1f}" y2="{T+ph}" stroke="#e8453c" stroke-width="1.5"/>'
            f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="4" fill="#e8453c" stroke="#fff" stroke-width="1.5"/>'
            f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bw:.1f}" height="{bh}" rx="3" fill="#e8453c"/>'
            f'<text x="{bx+bw/2:.1f}" y="{by+16.5:.1f}" font-size="12" font-weight="700" text-anchor="middle" fill="#fff">{lab}</text>')
    return (f'<svg class="bell" viewBox="0 0 {W} {H}" width="100%"><rect x="{L}" y="{T}" width="{pw}" height="{ph}" fill="#fff" stroke="#d9d9d9"/>{grid}'
            f'<path d="{area}" fill="#f1f1f1" stroke="none"/><polyline points="{line}" fill="none" stroke="#b9b9b9" stroke-width="1.6"/>{plot}'
            f'<line x1="{L}" y1="{T+ph}" x2="{L+pw}" y2="{T+ph}" stroke="#bbb"/>{tk}{labs}{marker}</svg>')
def page1():
    gr=S['gr']; by=S['start']['by']
    body=('<div class="sec3"><div class="level_section"><dl><dt><span class="title">나에게 맞는 학습 시작점</span><span class="level">'+S['start']['level']+'</span>'
          f'<span class="cue">{NM[by]} 기준</span></dt><dd>'+yes_table(S['start']['cell'])+'</dd></dl></div></div>'
          '<div class="two"><div class="colL"><dl><dt><span class="title">나의 영역별 점수</span></dt><dd>'+donuts()+'</dd></dl></div>'
          '<div class="colR"><dl><dt><span class="title">동학년 대비 나의 위치</span></dt><dd>'+bell(S['pos'])+
          f'<div class="arert_wrap"><span></span>{gr} 응시자 중 <b>{ptxt(S["pos"])}</b>로, <b>{band(S["pos"])} 구간</b>이에요. <b>{S["start"]["level"]}</b> 단계 <b>{NM[by]}</b> 영역 교재부터 학습을 시작하세요.</div></dd></dl></div></div>')
    return f'<div class="rep rpt_v10"><div class="content"><div class="slide_pa">{body}</div></div></div>'
# ---------- 2p ----------
YES=['초1','초2','초3','초4','초5','초6','예비중','1','2','3','4','5','6','7','8','9']
PH=['알파벳','자음','단모음','장모음','기타자음','기타모음','Master']
def ladder(a):
    x=S['area'][a]; av=AVG[a]; cells=PH if a=='P' else YES; n=len(cells)
    reach=x['stage'] if a=='P' else x['level']
    fill=(x['cellpos'])/n*100   # 도달 칸까지 채움 (cellpos = 도달 칸 번호, 1-base 끝)
    avx=av['cellpos']/n*100
    axis=''.join(f'<i>{c}</i>' for c in cells)
    tg=''  # v13: 시작점 기준 태그 삭제
    return (f'<div class="lad" style="--c:{COL[a]}"><div class="lhd"><span class="nm">{NM[a]}</span>{tg}<span class="lv">{reach}</span></div>'
            f'<div class="axis n{n}">{axis}</div>'
            f'<div class="track n{n}"><i class="fill" style="width:{fill:.2f}%"></i><i class="avg" style="left:{avx:.2f}%"></i></div>'
            f'<div class="avgl" style="left:{avx:.2f}%"><em>▲</em>학년 평균 {av["label"]}</div></div>')
def stat(a):
    x=S['area'][a]
    return (f'<div class="stat" style="--c:{COL[a]}"><span class="k">{NM[a]}</span>'
            f'<div class="c"><small>점수</small><b>{x["score"]:g}점</b><em>{x["k"]} / {x["n"]}문항</em></div>'
            f'<div class="c"><small>또래</small><b class="pos">{ptxt(x["pos"])}</b><em>{band(x["pos"])} 구간</em></div></div>')
BOX={'P':('장모음까지 잘 이해하고 있네요.','연속자음(fr, gr, br, pr, fl, gl, bl, pl)부터 파닉스 학습을 꾸준히 이어가세요.'),
     'LR':('공교육 기준 초등 4~5학년 수준으로, 듣기/말하기 실력은 우수하나 읽기/쓰기 능력이 다소 취약합니다.','다양한 이야기를 통해 읽기 유창성을 기르는 것이 필요합니다. 읽은 내용을 바탕으로 생각을 정리하고 논리적으로 글을 쓰는 훈련도 시작해보세요.'),
     'G':('초등 필수 문법을 완성하는 것이 필요합니다.','초등 문법의 기본기를 완성하여 읽기, 쓰기에 적용하는 능력을 길러보세요.')}
def page2():
    def col(title, areas, key, cls):
        return (f'<div class="pcol {cls}"><p class="ptitle">{title}</p>'+''.join(ladder(a) for a in areas)+'<div class="stats">'+''.join(stat(a) for a in areas)+'</div>'
                f'<div class="pbox"><b>{BOX[key][0]}</b><p>{BOX[key][1]}</p></div></div>')
    body=('<div class="p2"><div class="pcols">'+col('파닉스 진단',['P'],'P','c-p')+col('듣기/말하기, 읽기/쓰기 진단',['L','R'],'LR','c-lr')+col('문법 진단',['G'],'G','c-g')+'</div>'
          f'<p class="p2cap">막대 = 이번 진단에서 도달한 수준 · ▲ 학년 평균 = 전국 {S["gr"]} 응시자 평균(실데이터) · 또래 = 전국 {S["gr"]} 응시자 대비 상위 %<br><span class="legend"><i class="me"></i>내 수준 <i class="av"></i>학년 평균</span> · 진단 문구는 현행 샘플(자리표시)</p></div>')
    return f'<div class="rep rpt_v10 p2wrap"><div class="content"><div class="slide_pa">{body}</div></div></div>'

# ---------- 2p 레이아웃 3안 ----------
def boxes():
    return ('<div class="pboxes">'+''.join(f'<div class="pbox {cls}"><b>{BOX[k][0]}</b><p>{BOX[k][1]}</p></div>' for k,cls in (('P','c-p'),('LR','c-lr'),('G','c-g')))+'</div>')
def legend():
    return '<span class="lg"><i class="me"></i>내 수준 <i class="av"></i>학년 평균</span>'
def stat2(a):
    x=S['area'][a]
    return (f'<span class="sc"><b>{x["score"]:g}점</b><small>{x["k"]} / {x["n"]}문항</small></span>'
            f'<span class="pr"><b>{ptxt(x["pos"])}</b><small>{band(x["pos"])}</small></span>')
def dot_row(a,cells):
    x=S['area'][a]; n=len(cells); me=(x['cellpos']-0.5)/n*100; av=AVG[a]['cellpos']/n*100
    tg=''  # v13: 시작점 기준 태그 삭제
    name=x['stage'] if a=='P' else x['level']
    return (f'<div class="dprow" style="--c:{COL[a]}"><span class="nm">{NM[a]}{tg}</span>'
            f'<div class="ax n{n}"><i class="av" style="left:{av:.2f}%"></i><i class="me" style="left:{me:.2f}%"><em>{name}</em></i></div>{stat2(a)}</div>')
def page2a():
    yes_hdr=('<div class="dprow hdr"><span class="nm"></span><div class="ax n16 lab">'
             '<div class="grp"><b style="grid-column:span 2">Rookie</b><b style="grid-column:span 2">Rising Star</b><b style="grid-column:span 2">All-Star</b><b>MVP</b><b style="grid-column:span 9">중고등</b></div>'
             '<div class="cel">'+''.join(f'<b>{c}</b>' for c in YES)+'</div></div><span class="sc">점수</span><span class="pr">또래 위치</span></div>')
    ph_hdr=('<div class="dprow hdr ph"><span class="nm"></span><div class="ax n7 lab"><div class="cel">'+''.join(f'<b>{c}</b>' for c in PH)+'</div></div><span class="sc"></span><span class="pr"></span></div>')
    body=('<div class="p2 v2a"><dl><dt><span class="title">영역별 진단·처방</span>'+legend()+'</dt><dd><div class="dp">'
          +yes_hdr+dot_row('L',YES)+dot_row('R',YES)+dot_row('G',YES)+ph_hdr+dot_row('P',PH)+'</div></dd></dl>'+boxes()+'</div>')
    return f'<div class="rep rpt_v10 p2wrap"><div class="content"><div class="slide_pa">{body}</div></div></div>'
def page2b():
    rows=''
    for a in 'LRGP':
        x=S['area'][a]; name=x['stage'] if a=='P' else x['level']
        tg=''  # v13: 시작점 기준 태그 삭제
        cells=PH if a=='P' else YES; mi=int(round(x['cellpos']))-1; ai=cells.index(AVG[a]['label'].split()[-1]) if a!='P' else cells.index(AVG[a]['label'])
        cmp_='▲' if mi>ai else ('▼' if mi<ai else '＝')
        rows+=(f'<tr style="--c:{COL[a]}"><th>{NM[a]}{tg}</th><td class="lv"><b>{name}</b><i class="cmp">{cmp_}</i></td><td>{AVG[a]["label"]}</td>'
               f'<td><b>{x["score"]:g}점</b><small>{x["k"]} / {x["n"]}문항</small></td><td><b class="pos">{ptxt(x["pos"])}</b><small>{band(x["pos"])}</small></td></tr>')
    body=('<div class="p2 v2b"><dl><dt><span class="title">영역별 진단·처방</span><span class="cue">▲ 학년 평균보다 높음 · ＝ 비슷함 · ▼ 낮음</span></dt><dd>'
          '<table class="tb"><thead><tr><th>영역</th><th>내 수준</th><th>학년 평균</th><th>점수</th><th>또래 위치</th></tr></thead><tbody>'+rows+'</tbody></table></dd></dl>'+boxes()+'</div>')
    return f'<div class="rep rpt_v10 p2wrap"><div class="content"><div class="slide_pa">{body}</div></div></div>'
def cmp_idx(a):
    x=S['area'][a]; cells=PH if a=='P' else YES
    mi=int(round(x['cellpos']))-1
    ai=cells.index(AVG[a]['label']) if a=='P' else cells.index(AVG[a]['label'].split()[-1])
    return mi-ai
def summary_text():
    """1안: 룰 기반 3문장. ① 평균보다 앞선 영역 ② 평균·평균 이하 영역 + 보완 ③ 시작점 교재 + 상담 유도(고정)"""
    def lvl(a): x=S['area'][a]; return (x['stage']+'까지') if a=='P' else x['level']
    def avl(a): return AVG[a]['label']
    hi=[a for a in 'LRGP' if a in S['area'] and cmp_idx(a)>0]
    eq=[a for a in 'LRGP' if a in S['area'] and cmp_idx(a)==0]
    lo=[a for a in 'LRGP' if a in S['area'] and cmp_idx(a)<0]
    # ①
    if hi:
        a0=hi[0]; s1=f'<b>{NM[a0]}</b>는 {lvl(a0)} 수준으로 학년 평균({avl(a0)})보다 앞서 있'
        if len(hi)>1: s1+='고, '+'·'.join(NM[a] for a in hi[1:])+'도 평균보다 높아요.'
        else: s1+='어요.'
    elif eq: s1='·'.join(NM[a] for a in eq)+'은 또래 평균 수준이에요.'
    else: s1='이번 진단에서는 또래 평균보다 조금 뒤에 있는 영역이 많아요.'
    # ②
    parts=[]
    if eq: parts.append(', '.join(f'<b>{NM[a]}</b>는 {lvl(a)}로 평균 수준' for a in eq))
    if lo: parts.append(', '.join(f'<b>{NM[a]}</b>는 {lvl(a)} 익혀 평균({avl(a)})보다 조금 뒤에' for a in lo))
    weak=eq+lo
    if weak:
        s2='이고, '.join(parts)+(' 있어 ' if lo else '이라 ')+('이 영역을' if len(weak)==1 else f'이 {len(weak)}개 영역을')+' 보완하면 균형이 잡혀요.'
    else: s2='전 영역이 고르게 앞서 있어 지금 수준을 이어가면 돼요.'
    # ③
    by=S['start']['by']; strong=NM[hi[0]] if hi else None
    s3=f'<b>{S["start"]["level"]} {NM[by]}</b> 교재부터 시작하면 '+(f'{strong} 강점을 살리면서 ' if strong else '')+f'{NM[by].split("/")[0]}·{NM[by].split("/")[-1]}를 끌어올릴 수 있어요. 자세한 학습 계획은 선생님 상담에서 안내드려요.'
    return s1,s2,s3
def card(a):
    x=S['area'][a]; n=(4 if S.get('mid') else 7) if a=='P' else 16; name=x['stage'] if a=='P' else x['level']
    fill=x['cellpos']/n*100; av=AVG[a]['cellpos']/n*100
    tg=''  # v13: 시작점 기준 태그 삭제
    return (f'<div class="cd" style="--c:{COL[a]}"><div class="hd"><span class="nm">{NM[a]}</span>{tg}</div><div class="lv">{name}</div>'
            f'<div class="mb"><i class="fill" style="width:{fill:.1f}%"></i><i class="av" style="left:{av:.1f}%"></i></div>'
            f'<div class="rw"><span>정답률</span><b>{x["score"]:g}%</b><small>{x["k"]} / {x["n"]}문항</small></div></div>')
def page2c():
    """C1: 카드 파닉스→듣말→읽쓰→문법, 하단 박스 폭을 카드 폭에 맞춤(파닉스 1칸 / 듣말·읽쓰 2칸 / 문법 1칸)"""
    pres=[a for a in 'PLRG' if a in S['area']]; n=len(pres)
    cards=''.join(card(a) for a in pres)
    keys=[k for k,need in (('P',['P']),('LR',['L','R']),('G',['G'])) if any(a in S['area'] for a in need)]
    span={'P':1,'LR':sum(1 for a in 'LR' if a in S['area']),'G':1}
    cls={'P':'c-p','LR':'c-lr','G':'c-g'}
    narrow=('max-width:%dpx;margin-left:auto;margin-right:auto;'%(n*300+(14 if n==2 else 0))) if n<=2 else ''
    bx=(f'<div class="pboxes g4" style="grid-template-columns:repeat({n},1fr);{narrow}">'+''.join(f'<div class="pbox {cls[k]}" style="grid-column:span {span[k]}"><b>{BOX[k][0]}</b><p>{BOX[k][1]}</p></div>' for k in keys)+'</div>')
    body=(f'<div class="p2 v2c"><dl><dt><span class="title">영역별 진단·처방</span>'+legend()+f'</dt><dd><div class="cds" style="{narrow}">'+cards+'</div></dd></dl>'+bx+'</div>')
    return f'<div class="rep rpt_v10 p2wrap"><div class="content"><div class="slide_pa">{body}</div></div></div>'
def sumbox_c1():
    """C2: C1의 영역별 처방 3개를 한 박스에 행으로 정리(시작 교재 안내는 1p 총평에만 두고 여기선 반복하지 않음)"""
    rows=''.join(f'<div class="sr {cls}"><span class="lab">{lab}</span><div class="tx"><b>{g0}</b><p>{g1}</p></div></div>'
                 for (k,cls,lab),(g0,g1) in ((( 'P','c-p','파닉스'),BOX['P']),(('LR','c-lr','듣기/말하기<br>읽기/쓰기'),BOX['LR']),(('G','c-g','문법'),BOX['G'])))
    return f'<div class="sumbox one">{rows}</div>'
def page2c2():
    cards=''.join(card(a) for a in 'PLRG')
    body=('<div class="p2 v2c"><dl><dt><span class="title">영역별 진단·처방</span>'+legend()+'</dt><dd><div class="cds">'+cards+'</div></dd></dl>'+sumbox_c1()+'</div>')
    return f'<div class="rep rpt_v10 p2wrap"><div class="content"><div class="slide_pa">{body}</div></div></div>'


def wrap(title,body):
    return (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>{title}</title>{CSSLINKS}<style>{CSS}</style></head><body>'
            f'<nav class="mk_bar"><strong>진단평가 리포트 · v10</strong><a href="1p.html">1페이지</a><a href="2p.html">2페이지</a><a href="print.html">인쇄용</a>'
            f'<span class="hint">초4 전 영역 · 2025.08.27 응시 · 점수·수준·위치 실제값 · 2p 처방 문구는 현행 샘플(자리표시)</span></nav>'
            f'<section class="mk_page">{header(S["name"],S["grade"],S["date"])}{body}<div class="mk_dots"><i class="on"></i><i></i><i></i><i></i><i></i></div></section></body></html>')
if __name__=='__main__':
    open(os.path.join(OUT,'1p.html'),'w',encoding='utf-8').write(wrap('진단평가 리포트 v10 — 1p',page1()))
    open(os.path.join(OUT,'2p.html'),'w',encoding='utf-8').write(wrap('진단평가 리포트 v10 — 2p',page2c()))
    print('ok 1p/2p')
