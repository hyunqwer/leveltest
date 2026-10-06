# -*- coding: utf-8 -*-
"""v11: 1p·인쇄 상단 = 현행 서비스 마크업/CSS/Highcharts 옵션 그대로(레이아웃 동일), 내용만 교체.
2p 및 인쇄 하단 = v10 구성. 초4 전 영역 예시 학생 A.
   재생성: python gen_v11.py  → 1p.html / 2p.html / print.html / index.html"""
import os, json
HERE=os.path.dirname(os.path.abspath(__file__))
OUT=os.environ.get('OUT',os.path.expanduser('~/mnt/leveltest/진단평가리포트업글_codex/ys_report_mockups_v11_service'))
os.makedirs(OUT,exist_ok=True)
import v10parts as v10
S=v10.S; NM=v10.NM; COL=v10.COL; BOX=v10.BOX; AVG=v10.AVG
HOST=os.environ.get('HOST','https://leveltest.yoons.com')
LOCAL=os.environ.get('LOCAL')   # 로컬 렌더 검증용: CSS/JS 경로 치환
def css_links():
    if LOCAL: return LOCAL
    return ''.join(f'<link rel="stylesheet" href="{HOST}/css/{f}">' for f in ('common.css?v=1.0','w_reset.css?v=1.0','w_base.css?v=1.27','w_media.css?v=1.2'))
def hc_scripts():
    base=os.environ.get('HCBASE',HOST+'/Highcharts-6.0.3')
    return (f'<script src="{base}/highcharts.js"></script><script src="{base}/highcharts-more.js"></script><script src="{base}/modules/solid-gauge.js"></script>')
V11CSS=open(os.path.join(HERE,'v11.css'),encoding='utf-8').read()
# ---------- 데이터 ----------
pos=S['pos']; by=S['start']['by']
ptxt=v10.ptxt; band=v10.band
pin=min(pos,90)
areas=[(a,NM[a],COL[a],S['area'][a]['score']) for a in 'PLRG']
# ---------- 차트 JS (현행 옵션 복제 + 변경점) ----------
CHART_JS=r'''
(function(){
  var CURVE=[[0,6],[10,8],[20,16],[30,37],[40,80],[50,93],[60,80],[70,37],[80,16],[90,8],[100,6]]; // 현행 등급기준 곡선 데이터(고정)
  function yOn(x){ for(var i=1;i<CURVE.length;i++){ if(x<=CURVE[i][0]){ var a=CURVE[i-1],b=CURVE[i]; return a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0]); } } return CURVE[CURVE.length-1][1]; }
  window.v11Gauge=function(id,name,score,color){
    Highcharts.chart(id,{chart:{type:'solidgauge',backgroundColor:'transparent',animation:false,style:{fontFamily:'inherit'}},title:null,
      pane:{size:'100%',background:{borderWidth:10,backgroundColor:'#e6e6e6',shape:'arc',borderColor:'#e6e6e6',outerRadius:'90%',innerRadius:'90%'}},
      yAxis:{min:0,max:100,minColor:color,maxColor:color,lineWidth:0,tickWidth:0,minorTickLength:0,labels:{enabled:false}},
      plotOptions:{solidgauge:{borderColor:color,borderWidth:10,radius:90,innerRadius:'90%',dataLabels:{y:30,borderWidth:0,useHTML:true},animation:false}},
      credits:{enabled:false},tooltip:{enabled:false},exporting:{enabled:false},
      series:[{name:'',data:[score],dataLabels:{format:'<div style="width:60px;text-align:center"><span style="font-size:0.825rem;color:#666;">'+name+'</span><br/><span style="font-size:1.3rem;color:#333;line-height:29px">{y}점</span></div>'}}]});
  };
  // pos: 종합 위치(상위 %). 변경점: ① x축 눈금/라벨 등급→% ② Below/Average 경계선 80/20 ③ 80% 초과 시 마커 90 고정·"상위 80% 이하"
  window.v11Bell=function(id,pos){
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
def yes_table(tid):
    cells=[('Rookie초1','Rookie','초1','',1),('Rookie초2','Rookie','초2','borderright',0),('RisingStar초3','RisingStar','초3','',1),('RisingStar초4','RisingStar','초4','borderright',0),
           ('AllStar초5','AllStar','초5','',1),('AllStar초6','AllStar','초6','borderright',0),('MVP예비중','MVP','예비중','borderright',0)]+[(f'중고등{i}','중고등',str(i),'',1 if i<9 else 0) for i in range(1,10)]
    tds=''.join(f'<td data-level="{k}" class="{cls}{" bgred" if lv==S["start"]["cell"] else ""}" data-curri-stg="{stg}" data-curri-level="{lv}">{lv}{"<span></span>" if sp else ""}</td>' for k,stg,lv,cls,sp in cells)
    cols='<col width="*">'+''.join(f'<col width="{w}">' for w in ['5.8%']*6+['6%']+['5.8%']*9)
    return (f'<table data-1-level id="{tid}"><colgroup>{cols}</colgroup><tr><th rowspan="2" style="width: unset;">YES&nbsp;4.0</th><th colspan="2">Rookie</th><th colspan="2">Rising&nbsp;Star</th><th colspan="2">All-Star</th><th colspan="1">MVP</th><th colspan="9">중고등</th></tr>'
            f'<tr class="height30">{tds}</tr></table>')
def gauge_divs(prefix,h):
    out=''
    for i,(a,n,c,sc) in enumerate(areas,1):
        tag='<b class="v11tag">시작점 기준</b>' if a==by else ''
        out+=f'<div class="v11g"><div id="{prefix}{i}" style="float:left; width:50%; height:{h}px;"></div>{tag}</div>' if tag else f'<div id="{prefix}{i}" style="float:left; width:50%; height:{h}px;"></div>'
    return out
def chart_init(prefix,bell_id):
    calls=''.join(f"v11Gauge('{prefix}{i}','{n}',{sc:g},'{c}');" for i,(a,n,c,sc) in enumerate(areas,1))
    return f'<script>{CHART_JS}</script><script>{calls}v11Bell("{bell_id}",{pos});</script>'
def summary():
    gr=S['gr']
    return (f'{gr} 응시자 중 <b>{ptxt(pos)}</b>로, <b>{band(pos)} 구간</b>이에요. <b>{S["start"]["level"]}</b> 단계 <b>{NM[by]}</b> 영역 교재부터 학습을 시작하세요.')
def header():
    return (f'<div id="header"><div class="yGnb_wrap yGnbreport_wrap" id="headerWrap"><div style="overflow:hidden"><h4 class="type_eval"></h4><div class="yGnb_common"><dl></dl></div></div>'
            f'<div class="reportInfo_wrap" id="headerReport"><div class="day" id="reportDate">{S["date"]}</div><div id="reportTitle">진단평가 리포트</div><div class="share"></div>'
            f'<dl><dd><span>이름</span><span id="reportName">{S["name"]}</span></dd><dd><span>학년</span><span id="reportYear">{S["grade"]}</span></dd></dl></div></div></div>')
# ---------- 1p (현행 마크업) ----------
def page1():
    return ('<div class="rep"><div class="content"><div class="slide_pa">'
            '<div class="asidetop_wrap" id="levelBox"><div class="level_section"><dl><dt><span class="title visib" style="visibility: visible;">나에게 맞는 학습 시작점</span> '
            f'<span class="level visib" id="spnLevel" style="width: unset; visibility: visible;">{S["start"]["level"]}</span><span class="v11cue">{NM[by]} 기준</span></dt>'
            f'<dd><div class="tableLayout_wrap">{yes_table("tblBEFLLevelTOBE")}</div></dd></dl></div></div>'
            '<div class="asidebottom_wrap"><div class="achiev_section"><dl><dt><span class="title visib" style="visibility: visible;">나의 영역별 점수</span></dt><dd>'
            f'<div style="width:300px; height:260px;">{gauge_divs("divChartScore",130)}</div></dd></dl></div>'
            '<div class="position_section"><dl><dt><span class="title visib" style="visibility: visible;">동학년 대비 나의 위치</span></dt><dd>'
            '<div class="graph_wrap"><div id="divPositionArea" style="width:100%;height:260px;"></div></div>'
            f'<div class="arert_wrap visib" id="positionText" style="visibility: visible;"><span style="width: 31px;"></span>{summary()}</div></dd></dl></div></div>'
            '</div></div></div>'+chart_init('divChartScore','divPositionArea'))
# ---------- 인쇄용 (현행 인쇄 마크업 + 하단 v10) ----------
def cards_print():
    out=''
    for a in 'PLRG':
        x=S['area'][a]; n=7 if a=='P' else 16; name=x['stage'] if a=='P' else x['level']
        fill=x['cellpos']/n*100; av=AVG[a]['cellpos']/n*100
        tg='<b class="tg">시작점 기준</b>' if a==by else ''
        out+=(f'<div class="cd" style="--c:{COL[a]}"><div class="hd2">{NM[a]}{tg}</div><div class="lv">{name}</div>'
              f'<div class="mb"><i class="fill" style="width:{fill:.1f}%"></i><i class="av" style="left:{av:.1f}%"></i></div>'
              f'<div class="rw"><span>정답률</span><b>{x["score"]:g}%</b><small>{x["k"]} / {x["n"]}문항</small></div></div>')
    return out
def page_print():
    boxes=''.join(f'<div class="info_area {cls}"><div>{BOX[k][0]}</div><div>{BOX[k][1]}</div></div>' for k,cls in (('P','orange'),('LR','green'),('G','purple')))
    return (f'<div class="wrap printerv3" id="printTest" style="overflow-x : hidden;"><div class="y_printer_area" style="display:none"></div>'
            f'<header><section class="header_1"><img src="{HOST}/images/icon/printer_logo_1.png" class="logo"><div class="title">윤선생 진단평가 리포트</div><div class="day" id="reportDate">{S["date"]}</div></section>'
            f'<section class="header_2"><dl class="center"><dt>센터</dt><dd id="headerBm">배플리</dd></dl><dl class="name"><dt>이름</dt><dd id="reportName">{S["name"]}</dd></dl><dl class="class"><dt>학년</dt><dd id="reportYear">{S["grade"]}</dd></dl></section></header>'
            '<section class="bodyarea">'
            # sec_1
            '<dl class="sec_1"><dt class="contitle">나에게 맞는 학습 시작점</dt><dd>'
            f'<div class="level" id="spnLevel" style="width: 20%; font-size: 117%;">{S["start"]["level"]}<small class="v11cue">{NM[by]} 기준</small></div>'
            f'<div class="tableLayout_wrap" style="width: calc(80% - 10px);">{yes_table("tblBEFLLevelTOBE")}</div></dd></dl>'
            # sec_2
            '<dl class="sec_2"><dt class="contitle">나의 영역별 점수</dt><dd></dd>'
            f'<div style="width:250px; height:260px; padding-top:15px; float:left;">{gauge_divs("divChartScore",120)}</div>'
            '<div class="graph_wrap" style="width : calc(100% - 270px); margin-left : 10px; float : left;"><div id="divPositionArea" style="height : 230px; width : 100%;"></div></div>'
            '<dt class="contitle" style="left : 280px;">동학년 대비 나의 위치</dt><dd>'
            f'<div class="arert_wrap" id="positionText" style="font-size:12px; font-weight:700; height:auto; min-height:48px;"><span></span>{summary()}</div></dd></dl>'
            # sec_3 (v10 하단)
            '<dl class="sec_3 v11sec3"><dt class="contitle">영역별 진단·처방<span class="lg"><i class="me"></i>내 수준 <i class="av"></i>학년 평균</span></dt>'
            f'<div class="cds">{cards_print()}</div><div class="boxes">{boxes}</div></dl>'
            '</section></div>'+chart_init('divChartScore','divPositionArea'))
# ---------- 2p (v10 그대로) ----------
def page2():
    return v10.page2c()
# ---------- 파일 ----------
def nav(cur):
    items=[('1p.html','1페이지'),('2p.html','2페이지'),('print.html','인쇄용'),('index.html','탭 통합')]
    return ('<nav class="mk_bar"><strong>진단평가 리포트 · v11</strong>'+''.join(f'<a href="{h}" class="{"on" if h==cur else ""}">{t}</a>' for h,t in items)+
            '<span class="hint">초4 전 영역 · 2025.08.27 응시 · 점수·수준·위치 실제값 · 처방 문구는 현행 샘플(자리표시)</span></nav>')
def doc(title,body,extra_css='',cur=''):
    return (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=1024"><title>{title}</title>{css_links()}{hc_scripts()}<style>{V11CSS}{extra_css}</style></head><body>{nav(cur)}{body}</body></html>')
if __name__=='__main__':
    v10css=open(os.path.join(HERE,'v10.css'),encoding='utf-8').read()
    p1=f'<section class="mk_page">{header()}{page1()}<div class="mk_dots"><i class="on"></i><i></i><i></i><i></i><i></i></div></section>'
    p2=f'<section class="mk_page">{v10.header(S["name"],S["grade"],S["date"])}{page2()}<div class="mk_dots"><i></i><i class="on"></i><i></i><i></i><i></i></div></section>'
    pr=f'<section class="mk_print">{page_print()}</section>'
    open(os.path.join(OUT,'1p.html'),'w',encoding='utf-8').write(doc('진단평가 리포트 v11 — 1p',p1,cur='1p.html'))
    open(os.path.join(OUT,'2p.html'),'w',encoding='utf-8').write(doc('진단평가 리포트 v11 — 2p',p2,v10css,cur='2p.html'))
    open(os.path.join(OUT,'print.html'),'w',encoding='utf-8').write(doc('진단평가 리포트 v11 — 인쇄용',pr,cur='print.html'))
    # 탭 통합 (차트 id 충돌 방지: 인쇄용 id에 접미사)
    pr2=pr.replace('divChartScore','pChartScore').replace('divPositionArea','pPositionArea').replace('id="spnLevel"','id="pSpnLevel"').replace('id="tblBEFLLevelTOBE"','id="pTbl"').replace('id="positionText"','id="pPositionText"')
    tabs=[('p1','1페이지',p1),('p2','2페이지',p2),('pr','인쇄용 (A4)',pr2)]
    bar=('<nav class="mk_bar"><strong>진단평가 리포트 · v11</strong>'+''.join(f'<a href="#" data-t="{k}" class="{"on" if i==0 else ""}">{t}</a>' for i,(k,t,_) in enumerate(tabs))+
         '<span class="hint">초4 전 영역 · 2025.08.27 응시 · 점수·수준·위치 실제값 · 처방 문구는 현행 샘플(자리표시)</span></nav>')
    secs=''.join(f'<div class="tabpane" id="{k}" style="{"" if i==0 else "display:none"}">{b}</div>' for i,(k,t,b) in enumerate(tabs))
    js=("<script>document.querySelectorAll('.mk_bar a[data-t]').forEach(function(a){a.onclick=function(e){e.preventDefault();document.querySelectorAll('.mk_bar a[data-t]').forEach(function(x){x.classList.remove('on')});a.classList.add('on');"
        "document.querySelectorAll('.tabpane').forEach(function(s){s.style.display=s.id===a.dataset.t?'':'none'});window.dispatchEvent(new Event('resize'));};});</script>")
    idx=(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=1024"><title>진단평가 리포트 v11</title>{css_links()}{hc_scripts()}<style>{V11CSS}{v10css}</style></head><body>{bar}{secs}{js}</body></html>')
    open(os.path.join(OUT,'index.html'),'w',encoding='utf-8').write(idx); print('v11 ok')
