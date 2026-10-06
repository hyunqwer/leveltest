# -*- coding: utf-8 -*-
"""v12: 시작점 기준 영역 표기(큐·태그) 제거판. 1p·인쇄 상단 = 현행 서비스 마크업/CSS/Highcharts 옵션 그대로(레이아웃 동일), 내용만 교체.
2p 및 인쇄 하단 = v10 구성. 초4 전 영역 예시 학생 A.
   재생성: python gen_v12.py  → 1p.html / 2p.html / print.html / index.html"""
import os, json
HERE=os.path.dirname(os.path.abspath(__file__))
OUT=os.environ.get('OUT',os.path.expanduser('~/mnt/leveltest/진단평가리포트업글_codex/ys_report_mockups_v12_service'))
os.makedirs(OUT,exist_ok=True)
import v10parts as v10
NM=v10.NM; COL=v10.COL; BOX=v10.BOX
HOST=os.environ.get('HOST','https://leveltest.yoons.com')
LOCAL=os.environ.get('LOCAL')   # 로컬 렌더 검증용: CSS/JS 경로 치환
def css_links():
    if LOCAL: return LOCAL
    return ''.join(f'<link rel="stylesheet" href="{HOST}/css/{f}">' for f in ('common.css?v=1.0','w_reset.css?v=1.0','w_base.css?v=1.27','w_media.css?v=1.2'))
def hc_scripts():
    base=os.environ.get('HCBASE',HOST+'/Highcharts-6.0.3')
    return (f'<script src="{base}/highcharts.js"></script><script src="{base}/highcharts-more.js"></script><script src="{base}/modules/solid-gauge.js"></script>')
V11CSS=open(os.path.join(HERE,'v12.css'),encoding='utf-8').read()
# ---------- 샘플(영역 조합별) ----------
ptxt=v10.ptxt; band=v10.band
YES=['초1','초2','초3','초4','초5','초6','예비중','1','2','3','4','5','6','7','8','9']
PH_E=['알파벳','자음','단모음','장모음','기타자음','기타모음','Master']; PH_M=['Beginner','Intermediate','Advanced','Master']
def lvfix(s): return str(s).replace('All Star','All-Star')
def cell_of(level):
    s=lvfix(level)
    for k in YES[:7]:
        if s.endswith(k): return k
    return s.split()[-1]
# 학년 평균 단계(진단평가_학년별_영역평균SCALE.xlsx 학년별 평균 → v3 기준표 환산; 초4는 사용자 확인값, 그 외는 추정)
AVG_BY_GRADE={'초등 1':{'P':'장모음','L':'Rookie 초2','R':'Rookie 초2','G':'Rookie 초2'},
              '초등 3':{'P':'장모음','L':'Rising Star 초4','R':'Rising Star 초3','G':'Rising Star 초3'},
              '초등 4':{'P':'장모음','L':'All-Star 초5','R':'Rising Star 초4','G':'Rising Star 초4'},
              '초등 6':{'P':'자음','L':'MVP 예비중','R':'All-Star 초6','G':'All-Star 초6'},
              '중등 1':{'P':'Intermediate','L':'중고등 2','R':'중고등 1','G':'중고등 1'},
              '고등 1':{'P':'Intermediate','L':'중고등 5','R':'중고등 4','G':'중고등 2'}}
GR={'초등 1':'초1','초등 3':'초3','초등 4':'초4','초등 6':'초6','중등 1':'중1','고등 1':'고1'}
def convert(raw,key):
    """samples.json(v7 형식) → v10/v12 S 형식"""
    g=raw['grade']; mid=not g.startswith('초'); ph=PH_M if mid else PH_E
    area={}
    for a,x in raw['area'].items():
        if a=='P': cp=ph.index(x['stage'])+1
        else: cp=YES.index(cell_of(x['level']))+1
        area[a]={'stage':x['stage'],'level':lvfix(x.get('level','')),'score':x['score'],'k':x['k'],'n':x['n'],'pos':x['pos'],'cellpos':cp}
    st=raw['start']
    if st.get('by')=='P' and st.get('by2')=='G':   # 파닉스+문법 → 시작점은 문법 기준(파닉스 표 없음)
        start={'by':'G','level':lvfix(st['level2']),'cell':cell_of(st['level2'])}
    else:
        start={'by':st['by'],'level':lvfix(st['level'])}
        if st['by'] in ('L','R','G'): start['cell']=cell_of(st['level'])
    # 동단계: 듣말·읽쓰 둘 다 응시하고 정수 단계(YES4.0 칸)가 같으면 영역을 특정하지 않음(시스템 규칙: 그 단계 처음부터)
    start['tie']=('L' in area and 'R' in area and area['L']['cellpos']==area['R']['cellpos'])
    start['both']=('L' in area and 'R' in area)
    avg={}
    for a,lab in AVG_BY_GRADE[g].items():
        idx=(ph.index(lab) if a=='P' else YES.index(cell_of(lab)))
        avg[a]={'label':lab,'cellpos':idx+0.5}
    names={'e4_all':'예시 학생 A','e1_plr':'예시 학생 B','e6_all_low':'예시 학생 C','m1_lrg':'예시 학생 D','h1_all':'예시 학생 E','e3_p':'예시 학생 F','e4_pg':'예시 학생 G'}
    return {'key':key,'name':names.get(key,'예시 학생'),'grade':g,'gr':GR[g],'date':raw['date'],'combo':raw['combo'],'mid':mid,'ph':ph,'start':start,'area':area,'pos':raw['pos'],'pos_basis':raw.get('pos_basis','')},avg
SAMPLES=json.load(open(os.path.join(HERE,'samples.json'),encoding='utf-8'))
TABS=[('e4_all','초4 전 영역'),('e1_plr','초1 파닉스+듣말+읽쓰'),('e6_all_low','초6 전 영역·평균 이하'),('m1_lrg','중1 듣말+읽쓰+문법'),('h1_all','고1 전 영역'),('e3_p','초3 파닉스만'),('e4_pg','초4 파닉스+문법')]
S=None; AVG=None; pos=None; by=None; areas=None
def set_sample(key):
    global S,AVG,pos,by,areas
    S,AVG=convert(SAMPLES[key],key); v10.S=S; v10.AVG=AVG
    pos=S['pos']; by=S['start']['by']
    areas=[(a,NM[a],COL[a],S['area'][a]['score']) for a in 'PLRG' if a in S['area']]
set_sample('e4_all')
# ---------- 차트 JS (현행 옵션 복제 + 변경점) ----------
CHART_JS=r'''
(function(){
  var CURVE=[[0,6],[10,8],[20,16],[30,37],[40,80],[50,93],[60,80],[70,37],[80,16],[90,8],[100,6]]; // 현행 등급기준 곡선 데이터(고정)
  function yOn(x){ for(var i=1;i<CURVE.length;i++){ if(x<=CURVE[i][0]){ var a=CURVE[i-1],b=CURVE[i]; return a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0]); } } return CURVE[CURVE.length-1][1]; }
  window.v12Gauge=function(id,name,score,color){
    Highcharts.chart(id,{chart:{type:'solidgauge',backgroundColor:'transparent',animation:false,style:{fontFamily:'inherit'}},title:null,
      pane:{size:'100%',background:{borderWidth:10,backgroundColor:'#e6e6e6',shape:'arc',borderColor:'#e6e6e6',outerRadius:'90%',innerRadius:'90%'}},
      yAxis:{min:0,max:100,minColor:color,maxColor:color,lineWidth:0,tickWidth:0,minorTickLength:0,labels:{enabled:false}},
      plotOptions:{solidgauge:{borderColor:color,borderWidth:10,radius:90,innerRadius:'90%',dataLabels:{y:30,borderWidth:0,useHTML:true},animation:false}},
      credits:{enabled:false},tooltip:{enabled:false},exporting:{enabled:false},
      series:[{name:'',data:[score],dataLabels:{format:'<div style="width:60px;text-align:center"><span style="font-size:0.825rem;color:#666;">'+name+'</span><br/><span style="font-size:1.3rem;color:#333;line-height:29px">{y}점</span></div>'}}]});
  };
  // pos: 종합 위치(상위 %). 변경점: ① x축 눈금/라벨 등급→% ② Below/Average 경계선 80/20 ③ 80% 초과 시 마커 90 고정·"상위 80% 이하"
  window.v12Bell=function(id,pos){
    var x=Math.min(pos,90), lab=(pos>80)?'상위 80% 이하':'상위 '+Math.round(pos)+'%';
    Highcharts.chart(id,{chart:{alignTicks:false,animation:false,style:{fontFamily:'inherit'}},title:{text:null},credits:{enabled:false},tooltip:{enabled:false},legend:{enabled:false},exporting:{enabled:false},
      xAxis:[
        {title:{text:null},lineColor:'#cccccc',tickColor:'#cccccc',minPadding:0,maxPadding:0,tickPositions:[0,10,20,50,80,90,100],labels:{enabled:false},reversed:true,allowDecimals:true,min:0,max:100,
         plotLines:[{value:80,color:'#cccccc',width:1,zIndex:1},{value:20,color:'#cccccc',width:1,zIndex:1}]},             // ② 80/20 경계선
        {title:{text:null},opposite:true,gridLineWidth:0,tickWidth:0,lineWidth:0,reversed:true,min:0,max:100,tickPositions:[90,50,10],
         labels:{style:{color:'#999999',fontSize:'0.8rem'},formatter:function(){return {90:'Below Average',50:'Average',10:'Above Average'}[this.value]||'';}}},
        {title:{text:null},min:0,max:100,tickWidth:0,lineWidth:0,labels:{enabled:false},reversed:true,allowDecimals:true,plotBands:[{from:x,to:x,color:'#e64545'}]},
        {title:{text:null},tickWidth:0,lineWidth:0,minPadding:0,maxPadding:0,tickPositions:[90,80,50,20,10],min:0,max:100,reversed:true,allowDecimals:true,
         labels:{y:15,style:{color:'#666666',fontSize:'0.8rem'},formatter:function(){return this.value+'%';}}}],                     // ① % 눈금
      yAxis:[{title:{text:null},min:0,max:100,tickInterval:25,lineColor:'#cccccc',tickColor:'#cccccc',gridLineColor:'#cccccc',labels:{enabled:false},allowDecimals:false},
             {title:{text:null},opposite:true,min:0,gridLineWidth:0,lineColor:'#cccccc',tickColor:'#cccccc',labels:{enabled:false}},
             {title:{text:null},min:0,max:100,gridLineWidth:0,lineColor:'#cccccc',tickColor:'#cccccc',labels:{enabled:false}}],
      plotOptions:{series:{animation:false,states:{hover:{enabled:false}}}},
      series:[{name:'등급기준',type:'areaspline',fillColor:'rgba(204, 204, 204, 0.15)',lineColor:'#cccccc',marker:{enabled:false},xAxis:0,yAxis:0,enableMouseTracking:false,data:CURVE},
              {name:'라벨',type:'scatter',marker:{enabled:false},xAxis:1,yAxis:1,data:[[90,0],[50,0],[10,0]]},
              {name:'%',type:'scatter',marker:{enabled:false},xAxis:3,yAxis:0,data:[[90,0],[80,0],[50,0],[20,0],[10,0]]},
              {name:'나의 위치',type:'scatter',color:'#ff0000',marker:{symbol:'circle',lineWidth:2,lineColor:'#fff',fillColor:'#e64545'},xAxis:2,yAxis:2,data:[[x,yOn(x)]],
               dataLabels:{enabled:true,overflow:'none',crop:false,shape:'callout',backgroundColor:'#e64545',style:{textOutline:0},color:'#fff',borderWidth:0,borderRadius:15,y:-25,x:0,useHTML:true,formatter:function(){return lab;}}}]});
  };
})();'''
# ---------- 공통 조각 ----------
def yes_table(tid,cell=None):
    cell=cell or S["start"].get("cell")
    cells=[('Rookie초1','Rookie','초1','',1),('Rookie초2','Rookie','초2','borderright',0),('RisingStar초3','RisingStar','초3','',1),('RisingStar초4','RisingStar','초4','borderright',0),
           ('AllStar초5','AllStar','초5','',1),('AllStar초6','AllStar','초6','borderright',0),('MVP예비중','MVP','예비중','borderright',0)]+[(f'중고등{i}','중고등',str(i),'',1 if i<9 else 0) for i in range(1,10)]
    tds=''.join(f'<td data-level="{k}" class="{cls}{" bgred" if lv==cell else ""}" data-curri-stg="{stg}" data-curri-level="{lv}">{lv}{"<span></span>" if sp else ""}</td>' for k,stg,lv,cls,sp in cells)
    cols='<col width="*">'+''.join(f'<col width="{w}">' for w in ['5.8%']*6+['6%']+['5.8%']*9)
    return (f'<table data-1-level id="{tid}"><colgroup>{cols}</colgroup><tr><th rowspan="2" style="width: unset;">YES&nbsp;4.0</th><th colspan="2">Rookie</th><th colspan="2">Rising&nbsp;Star</th><th colspan="2">All-Star</th><th colspan="1">MVP</th><th colspan="9">중고등</th></tr>'
            f'<tr class="height30">{tds}</tr></table>')
def ph_table(tid,stage):
    ph=S['ph']
    w=f'{round(94/len(ph),1)}%'
    return (f'<table data-1-level id="{tid}" class="v12ph" style="table-layout:fixed;width:100%"><colgroup><col width="69px">'+''.join(f'<col width="{w}">' for _ in ph)+'</colgroup><tr><th rowspan="2" style="width: unset;">파닉스</th>'+''.join(f'<th>{x}</th>' for x in ph)+'</tr>'
            '<tr class="height30">'+''.join(f'<td class="{"bgred" if x==stage else ""}">{x}</td>' for x in ph)+'</tr></table>')
def start_parts(tid):
    """(배지들 HTML, 큐 텍스트, 표 HTML) — 응시 조합별"""
    st=S['start']; cue_other='메인 커리큘럼 레벨은 듣기/말하기·읽기/쓰기 응시 시 제공'
    if st['by'] in ('L','R','G'):
        return [st['level']], f'{NM[st["by"]]} 기준', yes_table(tid,st['cell'])
    return ['파닉스 '+st['level']], cue_other, ph_table(tid+'P',st['level'])
def start_sentence():
    """v11과 같은 문장 구조. 듣말·읽쓰 동단계일 때만 영역 언급 없이 '첫 교재부터'."""
    st=S['start']; b=st['by']; lv=st['level']
    if b=='P': return f'파닉스 <b>{lv}</b> 단계 교재부터 학습을 시작하세요.'
    if st.get('tie'): return f'<b>{lv}</b> 단계 첫 교재부터 학습을 시작하세요.'
    return f'<b>{lv}</b> 단계 <b>{NM[b]}</b> 영역 교재부터 학습을 시작하세요.'
def gauge_divs(prefix,h):
    out=''
    for i,(a,n,c,sc) in enumerate(areas,1):
        out+=f'<div class="v12g"><div id="{prefix}{i}" style="width:100%; height:{h}px;"></div></div>'
    return f'<div class="v12gs n{len(areas)}">{out}</div>'
def chart_init(prefix,bell_id):
    calls=''.join(f"v12Gauge('{prefix}{i}','{n}',{sc:g},'{c}');" for i,(a,n,c,sc) in enumerate(areas,1))
    return f'<script>{CHART_JS}</script><script>{calls}v12Bell("{bell_id}",{pos});</script>'
def summary():
    gr=S['gr']
    return (f'{gr} 응시자 중 <b>{ptxt(pos)}</b>로, <b>{band(pos)} 구간</b>이에요. '+start_sentence())
def header():
    return (f'<div id="header"><div class="yGnb_wrap yGnbreport_wrap" id="headerWrap"><div style="overflow:hidden"><h4 class="type_eval"></h4><div class="yGnb_common"><dl></dl></div></div>'
            f'<div class="reportInfo_wrap" id="headerReport"><div class="day" id="reportDate">{S["date"]}</div><div id="reportTitle">진단평가 리포트</div><div class="share"></div>'
            f'<dl><dd><span>이름</span><span id="reportName">{S["name"]}</span></dd><dd><span>학년</span><span id="reportYear">{S["grade"]}</span></dd></dl></div></div></div>')
# ---------- 1p (현행 마크업) ----------
def page1():
    badges,cue,tbl=start_parts('tblBEFLLevelTOBE')
    gbox=260; bell_h=260
    return ('<div class="rep"><div class="content"><div class="slide_pa">'
            '<div class="asidetop_wrap'+(' v12dual' if 'by2' in S['start'] else '')+'" id="levelBox"><div class="level_section"><dl><dt><span class="title visib" style="visibility: visible;">나에게 맞는 학습 시작점</span> '
            +''.join(f'<span class="level visib" style="width: unset; visibility: visible;">{b}</span>' for b in badges)+(f'<span class="v12cue">{cue}</span>' if by=='P' else '')+'</dt>'
            f'<dd><div class="tableLayout_wrap">{tbl}</div></dd></dl></div></div>'
            '<div class="asidebottom_wrap"><div class="achiev_section"><dl><dt><span class="title visib" style="visibility: visible;">나의 영역별 점수</span></dt><dd>'
            f'<div style="width:300px; height:{gbox}px;">{gauge_divs("divChartScore",130)}</div></dd></dl></div>'
            '<div class="position_section"><dl><dt><span class="title visib" style="visibility: visible;">동학년 대비 나의 위치</span></dt><dd>'
            f'<div class="graph_wrap" style="height:{bell_h+20}px"><div id="divPositionArea" style="width:100%;height:{bell_h}px;"></div></div>'
            f'<div class="arert_wrap visib" id="positionText" style="visibility: visible;"><span style="width: 31px;"></span>{summary()}</div></dd></dl></div></div>'
            '</div></div></div>'+chart_init('divChartScore','divPositionArea'))
# ---------- 인쇄용 (현행 인쇄 마크업 + 하단 v10) ----------
def cards_print():
    out=''
    for a in 'PLRG':
        if a not in S['area']:
            if a=='R' and 'L' not in S['area']: continue   # 듣말·읽쓰 둘 다 없으면 빈칸 하나(2칸 폭)
            span=2 if (a=='L' and 'R' not in S['area']) else 1
            out+=f'<div class="cd blankcol" style="grid-column:span {span}"><div class="blank"><img src="{HOST}/images/icon/blank_icon.png"><div>해당 영역에 응시하지 않았습니다.</div></div></div>'
            continue
        x=S['area'][a]; n=7 if a=='P' else 16; name=x['stage'] if a=='P' else x['level']
        fill=x['cellpos']/n*100; av=AVG[a]['cellpos']/n*100
        out+=(f'<div class="cd" style="--c:{COL[a]}"><div class="hd2">{NM[a]}</div><div class="lv">{name}</div>'
              f'<div class="mb"><i class="fill" style="width:{fill:.1f}%"></i><i class="av" style="left:{av:.1f}%"></i></div>'
              f'<div class="rw"><span>정답률</span><b>{x["score"]:g}%</b><small>{x["k"]} / {x["n"]}문항</small></div></div>')
    return out
def page_print():
    def has(k): return any(a in S['area'] for a in {'P':'P','LR':'LR','G':'G'}[k])
    boxes=''.join((f'<div class="info_area {cls}"><div>{BOX[k][0]}</div><div>{BOX[k][1]}</div></div>' if has(k) else f'<div class="info_area {cls} empty"></div>') for k,cls in (('P','orange'),('LR','green'),('G','purple')))
    return (f'<div class="wrap printerv3" id="printTest" style="overflow-x : hidden;"><div class="y_printer_area" style="display:none"></div>'
            f'<header><section class="header_1"><img src="{HOST}/images/icon/printer_logo_1.png" class="logo"><div class="title">윤선생 진단평가 리포트</div><div class="day" id="reportDate">{S["date"]}</div></section>'
            f'<section class="header_2"><dl class="center"><dt>센터</dt><dd id="headerBm">배플리</dd></dl><dl class="name"><dt>이름</dt><dd id="reportName">{S["name"]}</dd></dl><dl class="class"><dt>학년</dt><dd id="reportYear">{S["grade"]}</dd></dl></section></header>'
            '<section class="bodyarea">'
            # sec_1
            '<dl class="sec_1"><dt class="contitle">나에게 맞는 학습 시작점</dt><dd>'
            f'<div class="level" id="spnLevel" style="width: 20%; font-size: 117%;">{S["start"]["level"]}</div>'
            f'<div class="tableLayout_wrap" style="width: calc(80% - 10px);">{yes_table("tblBEFLLevelTOBE")}</div></dd></dl>'
            # sec_2
            '<dl class="sec_2"><dt class="contitle">나의 영역별 점수</dt><dd></dd>'
            f'<div style="width:250px; height:260px; padding-top:15px; float:left;">{gauge_divs("divChartScore",120)}</div>'
            '<div class="graph_wrap" style="width : calc(100% - 270px); margin-left : 10px; float : left;"><div id="divPositionArea" style="height : 230px; width : 100%;"></div></div>'
            '<dt class="contitle" style="left : 280px;">동학년 대비 나의 위치</dt><dd>'
            f'<div class="arert_wrap" id="positionText" style="font-size:12px; font-weight:700; height:auto; min-height:48px;"><span></span>{summary()}</div></dd></dl>'
            # sec_3 (v10 하단)
            '<dl class="sec_3 v12sec3"><dt class="contitle">영역별 진단·처방<span class="lg"><i class="me"></i>내 수준 <i class="av"></i>학년 평균</span></dt>'
            f'<div class="cds">{cards_print()}</div><div class="boxes">{boxes}</div></dl>'
            '</section></div>'+chart_init('divChartScore','divPositionArea'))
# ---------- 2p (v10 그대로) ----------
def page2():
    return v10.page2c()
# ---------- 파일 ----------
def nav(cur):
    items=[('1p.html','1페이지'),('2p.html','2페이지'),('print.html','인쇄용'),('index.html','탭 통합')]
    return ('<nav class="mk_bar"><strong>진단평가 리포트 · v12</strong>'+''.join(f'<a href="{h}" class="{"on" if h==cur else ""}">{t}</a>' for h,t in items)+
            '<span class="hint">초4 전 영역 · 2025.08.27 응시 · 점수·수준·위치 실제값 · 처방 문구는 현행 샘플(자리표시)</span></nav>')
def doc(title,body,extra_css='',cur=''):
    return (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=1024"><title>{title}</title>{css_links()}{hc_scripts()}<style>{V11CSS}{extra_css}</style></head><body>{nav(cur)}{body}</body></html>')
if __name__=='__main__':
    v10css=open(os.path.join(HERE,'v10.css'),encoding='utf-8').read()
    dots1='<div class="mk_dots"><i class="on"></i><i></i><i></i><i></i><i></i></div>'; dots2='<div class="mk_dots"><i></i><i class="on"></i><i></i><i></i><i></i></div>'
    pages={}
    for key,label in TABS:
        set_sample(key)
        p1=f'<section class="mk_page">{header()}{page1()}{dots1}</section>'.replace('divChartScore',f'c{key}_s').replace('divPositionArea',f'c{key}_pos').replace('id="tblBEFLLevelTOBE','id="t'+key)
        p2=f'<section class="mk_page">{v10.header(S["name"],S["grade"],S["date"])}{page2()}{dots2}</section>'
        pages[key]=(label,p1,p2)
    set_sample(os.environ.get('PRINT_KEY','e4_all'))   # 인쇄용은 초4 전 영역 1종 (검증용으로 PRINT_KEY 지정 가능)
    pr=f'<section class="mk_print">{page_print()}</section>'
    label,p1,p2=pages['e4_all']
    open(os.path.join(OUT,'1p.html'),'w',encoding='utf-8').write(doc('진단평가 리포트 v12 — 1p',p1,cur='1p.html'))
    open(os.path.join(OUT,'2p.html'),'w',encoding='utf-8').write(doc('진단평가 리포트 v12 — 2p',p2,v10css,cur='2p.html'))
    open(os.path.join(OUT,'print.html'),'w',encoding='utf-8').write(doc('진단평가 리포트 v12 — 인쇄용',pr,cur='print.html'))
    # 탭 통합: 샘플(영역 조합) × 페이지(1p/2p) + 인쇄용(초4 1종)
    sbtns=''.join(f'<a href="#" data-s="{k}" class="{"on" if i==0 else ""}">{l}</a>' for i,(k,l) in enumerate(TABS))
    bar=('<nav class="mk_bar"><strong>진단평가 리포트 · v12</strong><span class="grp">응시 조합</span>'+sbtns+'<span class="hint">점수·수준·위치 실제 응시 기록 · 처방 문구는 현행 샘플(자리표시)</span></nav>'
         '<nav class="mk_bar mk_bar2"><span class="grp">페이지</span><a href="#" data-t="p1" class="on">1페이지</a><a href="#" data-t="p2">2페이지</a><a href="#" data-t="pr">인쇄용 (A4 · 초4 전 영역)</a></nav>')
    secs=''.join(f'<div class="spane" data-s="{k}" style="{"" if i==0 else "display:none"}"><div class="tabpane" data-t="p1">{p1}</div><div class="tabpane" data-t="p2" style="display:none">{p2}</div></div>' for i,(k,(l,p1,p2)) in enumerate(pages.items()))
    secs+=f'<div class="tabpane" id="prpane" data-t="pr" style="display:none">{pr}</div>'
    js=("<script>var curS='e4_all',curT='p1';function show(){document.querySelectorAll('.spane').forEach(function(s){s.style.display=(s.dataset.s===curS&&curT!=='pr')?'':'none';});"
        "document.querySelectorAll('.spane .tabpane').forEach(function(t){t.style.display=t.dataset.t===curT?'':'none';});document.getElementById('prpane').style.display=curT==='pr'?'':'none';"
        "document.querySelectorAll('.mk_bar a[data-s]').forEach(function(a){a.classList.toggle('on',a.dataset.s===curS)});document.querySelectorAll('.mk_bar a[data-t]').forEach(function(a){a.classList.toggle('on',a.dataset.t===curT)});window.dispatchEvent(new Event('resize'));}"
        "document.querySelectorAll('.mk_bar a[data-s]').forEach(function(a){a.onclick=function(e){e.preventDefault();curS=a.dataset.s;if(curT==='pr')curT='p1';show();}});"
        "document.querySelectorAll('.mk_bar a[data-t]').forEach(function(a){a.onclick=function(e){e.preventDefault();curT=a.dataset.t;show();}});</script>")
    idx=(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=1024"><title>진단평가 리포트 v12</title>{css_links()}{hc_scripts()}<style>{V11CSS}{v10css}</style></head><body>{bar}{secs}{js}</body></html>')
    open(os.path.join(OUT,'index.html'),'w',encoding='utf-8').write(idx); print('v12 ok', len(pages))
