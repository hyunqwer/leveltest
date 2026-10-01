import pandas as pd, numpy as np, json
d=pd.read_pickle('score.pkl'); t=pd.read_pickle('기준표_신규v3_테이블.pkl'); comp,Lt,Rt=pd.read_pickle('tables.pkl')
B={k:pd.read_excel('mnt/leveltest/진단평가_리포트개선_v1/나의위치값_버전B_영역조합합계_2018.02-2026.09기반_260930.xlsx',sheet_name=k).set_index('합계스케일') for k in ['B_LS+RW','B_LS+RW+P','B_LS+RW+P+G','B_P+G']}
sc={'P':'파닉스_SCALE','L':'듣기말하기_SCALE','R':'읽기쓰기_SCALE','G':'문법_SCALE'}
for c in sc.values(): d[c]=pd.to_numeric(d[c],errors='coerce')
d['combo']=d.apply(lambda r:''.join(k for k,c in sc.items() if pd.notna(r[c])),axis=1)
d['lvok']=d.응시수준.str.replace(' ','')==d.학년.str.replace(' ','')
trk={'초등 1':'예비초등','초등 2':'초등','초등 3':'초등','초등 4':'초등','초등 5':'예비중등','초등 6':'예비중등'}
def lk(area,scale,grade):
    r=t[(t.영역==area)&(t.스케일==scale)]
    if area=='P': r=r[r.학령==trk.get(grade,'중등')]
    r=r.iloc[0]; return r['측정 단계'], r['(교실_나의레벨)'], float(r[grade])
def build(r):
    g=r.학년; o={'date':r.응시일자,'grade':g,'combo':r.combo,'level_raw':r['나의 레벨'],'area':{}}
    sco={'P':('파닉스점수','파닉스_정답수'),'L':('듣말점수','듣말_정답수'),'R':('읽쓰점수','읽쓰_정답수'),'G':('문법점수','문법_정답수')}
    for a in r.combo:
        s=int(r[sc[a]]); s=min(s,41) if a=='L' else (min(s,44) if a=='R' else s); st,lv,p=lk({'P':'P','L':'LS','R':'RW','G':'G'}[a],s,g)
        score=float(r[sco[a][0]]); k=int(r[sco[a][1]]); n=round(k/score*100) if score>0 else None
        if a=='L': p=float(Lt.loc[float(st),g])
        if a=='R': p=float(Rt.loc[float(st),g])
        o['area'][a]={'scale':s,'stage':st if a=='P' else float(st),'level':lv,'pos':round(p,1),'score':score,'k':k,'n':n}
    A=o['area']
    if 'L' in A and 'R' in A:
        by='R' if float(A['R']['stage'])<float(A['L']['stage']) else 'L'
        o['start']={'by':by,'level':A[by]['level']}
        key={'LR':'B_LS+RW','PLR':'B_LS+RW+P','PLRG':'B_LS+RW+P+G','LRG':None}[r.combo] if r.combo in ('LR','PLR','PLRG','LRG') else None
        if key: o['pos']=float(B[key].loc[sum(A[a]['scale'] for a in r.combo),g]); o['pos_basis']=key
        else: o['pos']=float(B['B_LS+RW'].loc[A['L']['scale']+A['R']['scale'],g]); o['pos_basis']='B_LS+RW(문법 제외·임시)'
    elif r.combo=='PG':
        o['start']={'by':'P','level':A['P']['stage'],'by2':'G','level2':A['G']['level']}
        o['pos']=float(B['B_P+G'].loc[A['P']['scale']+A['G']['scale'],g]); o['pos_basis']='B_P+G'
    elif r.combo=='P':
        o['start']={'by':'P','level':A['P']['stage']}; o['pos']=A['P']['pos']; o['pos_basis']='P단독(v3)'
    elif r.combo=='G':
        o['start']={'by':'G','level':A['G']['level']}; o['pos']=A['G']['pos']; o['pos_basis']='G단독(v3)'
    return o
out={}
# 1 초4 전영역 (기존)
out['e4_all']=build(d[(d.응시일자=='2025.08.27')&(d.학년=='초등 4')&(d.파닉스_SCALE==9)&(d.듣기말하기_SCALE==20)].iloc[0])
def pick(g,combo,cond=None,seed=1,want=None):
    s=d[(d.학년==g)&(d.combo==combo)&d.lvok&(d.응시일자>='2025.01')]
    if cond is not None: s=s[cond(s)]
    if len(s)<5: s=d[(d.학년==g)&(d.combo==combo)]
    rows=[build(r) for _,r in s.sample(min(300,len(s)),random_state=seed).iterrows()]
    if want: rows=[o for o in rows if want(o)]
    return rows[0]
out['e1_plr']=pick('초등 1','PLR',lambda s:(s.듣기말하기_SCALE>s.읽기쓰기_SCALE)&(s.읽기쓰기_SCALE>=2),want=lambda o:o['pos'] and 30<o['pos']<70)
out['e6_all_low']=pick('초등 6','PLRG',want=lambda o:o['pos'] and 85<o['pos']<97 and all(x['score']>0 for x in o['area'].values()))
out['m1_lrg']=pick('중등 1','LRG',want=lambda o:True)   # LRG는 버전B 조합 없음 → 아래서 처리
out['h1_all']=pick('고등 1','PLRG',want=lambda o:o['pos'] and 10<o['pos']<90)
out['e3_p']=pick('초등 3','P',want=lambda o:30<o['pos']<70)
out['e4_pg']=pick('초등 4','PG',want=lambda o:15<o['pos']<85)
json.dump(out,open('samples7.json','w'),ensure_ascii=False,indent=1,default=str)
for k,v in out.items(): print(k,v['grade'],v['combo'],v['date'],v.get('pos'),v.get('pos_basis'),{a:(x['level'] if a!='P' else x['stage'],x['pos'],x['score']) for a,x in v['area'].items()},v['start'])
