from pathlib import Path
import math, json, csv
import xlsxwriter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

ROOT=Path('/workspace/assignment1')
OUT=ROOT/'deliverables'
OUT.mkdir(exist_ok=True)
DATE='2026-10-16'
SOURCES=json.loads((ROOT/'tools/sources_config.json').read_text())
(OUT/'sources.json').write_text(json.dumps(SOURCES,indent=2),encoding='utf-8')
with (OUT/'sources.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=list(SOURCES[0]),lineterminator="\n");w.writeheader();w.writerows(SOURCES)

# All monetary, behavioural and workforce parameters are illustrative assumptions.
inputs=[
('employees',200,'users','Constant licensed users, 2026-2030.'),
('years',5,'years','Finite operational horizon; no terminal value.'),
('first_year',2026,'year','Cash costs start at opening of 2026.'),
('clients',10,'enterprise accounts','Each supplier acquires this many accounts.'),
('exchange_acq',70000,'USD','Illustrative gross/net acquisition budget.'),
('google_gross_acq',70000,'USD','Hypothetical common gross campaign cost.'),
('ecosystem_credit',30000,'USD','Illustrative adjacent-business funding; allocation only.'),
('annual_gp',6000,'USD/account/year','Standardized contribution before operating-risk haircut.'),
('risk_loss',.05,'fraction/year','Expected contribution loss, distinct from churn.'),
('discount',.10,'fraction/year','Annual end-of-year discount rate.'),
('churn_base',.18,'fraction/year','Illustrative churn at n=0; not fitted to data.'),
('churn_beta',.10,'per integration','Illustrative exponential decay coefficient.'),
('base_n',4,'integrations','Baseline active material API/workflow integrations.'),
('hardware',32000,'USD, once','Two servers plus storage; planning allowance.'),
('deployment',9000,'USD, once','Exchange implementation at opening of 2026.'),
('licensing',12000,'USD/year','Exchange/SA and underlying OS/CAL allowance; quote needed.'),
('loaded_fte',80000,'USD/FTE/year','Implied by USD 24,000 at 0.30 FTE.'),
('exchange_fte',.30,'FTE','Baseline incremental annual administration.'),
('facilities',7000,'USD/year','Incremental on-premises facilities/network/maintenance.'),
('backup',5000,'USD/year/option','Incremental backup and security in both options.'),
('migration',15000,'USD, once','Cloud migration and training at opening of 2026.'),
('google_price',7,'USD/user/month','Illustrative flat 2026-2030 scenario; not a current quote.'),
('google_admin',8000,'USD/year','Cloud administration allowance.'),
('stress_price',14,'USD/user/month','Higher-subscription sensitivity scenario.'),
('low_fte',.15,'FTE','Lower on-premises staffing sensitivity scenario.')]
V={k:v for k,v,u,d in inputs}
c=V['churn_base']*math.exp(-V['churn_beta']*V['base_n'])
def ltv(churn,shift=1):return sum(V['annual_gp']*(1-V['risk_loss'])*(1-churn)**(t-shift)/(1+V['discount'])**t for t in range(1,6))
L=ltv(c)
EX=V['hardware']+V['deployment']+5*(V['licensing']+V['loaded_fte']*V['exchange_fte']+V['facilities']+V['backup'])
GW=V['migration']+5*(V['employees']*V['google_price']*12+V['google_admin']+V['backup'])
M={'baseline_churn':c,'ltv':L,'ltv_after_churn':ltv(c,0),'exchange_tco':EX,'google_tco':GW,'saving':EX-GW,'saving_pct':(EX-GW)/EX,'churn_scenarios':[],'sensitivity':[]}
for n in [0,2,4,6,8]:
 cn=V['churn_base']*math.exp(-V['churn_beta']*n)
 M['churn_scenarios'].append({'n':n,'churn':cn,'retention5':(1-cn)**5,'ltv':ltv(cn)})
for p in [7,14]:
 for fte in [.3,.15]:
  et=41000+5*(12000+80000*fte+7000+5000);gt=15000+5*(200*p*12+8000+5000)
  M['sensitivity'].append({'price':p,'fte':fte,'exchange':et,'google':gt,'saving':et-gt})
(OUT/'model_results.json').write_text(json.dumps(M,indent=2))

# Publication figures: scenario x-axis, explicitly not a time series.
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
blue='#183B56';teal='#007F86';orange='#C65E21'
fig,ax=plt.subplots(figsize=(3.55,2.8),layout='constrained')
ns=[s['n'] for s in M['churn_scenarios']];cs=[s['churn'] for s in M['churn_scenarios']]
ax.plot(ns,cs,color=teal,marker='o',linewidth=2)
for n,cv in zip(ns,cs):ax.annotate(f'{cv:.1%}',(n,cv),xytext=(0,7),textcoords='offset points',ha='center',fontsize=9)
ax.set(xlabel='Material integrations, n (count)',ylabel='Annual churn (%)',xticks=ns,ylim=(0,.215))
ax.yaxis.set_major_formatter(PercentFormatter(1));ax.grid(axis='y',alpha=.18)
ax.set_title('Churn by integration scenario',loc='left',fontweight='bold',fontsize=10,color=blue,pad=10)

fig.subplots_adjust if False else None
for ext in ['png','pdf','svg']:fig.savefig(OUT/f'churn_chart.{ext}',dpi=240,bbox_inches='tight')
svg=OUT/'churn_chart.svg';svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
plt.close(fig)
fig,ax=plt.subplots(figsize=(3.55,2.8),layout='constrained')
bar=ax.bar(['Exchange SE\non-premises','Google\nWorkspace'],[EX/1000,GW/1000],color=[blue,teal],width=.52)
for b,val in zip(bar,[EX,GW]):ax.text(b.get_x()+b.get_width()/2,b.get_height()+7,f'{val/1000:,.0f}',ha='center',fontweight='bold',fontsize=10)
ax.set(ylabel='Nominal TCO (USD thousands)',ylim=(0,335));ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True)
ax.set_title('200 users | 2026–2030',loc='left',fontweight='bold',fontsize=10,color=blue,pad=10)

for ext in ['png','pdf','svg']:fig.savefig(OUT/f'tco_chart.{ext}',dpi=240,bbox_inches='tight')
svg=OUT/'tco_chart.svg';svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
plt.close(fig)

# Formula workbook, cached results supplied explicitly for non-calculating readers.
wb=xlsxwriter.Workbook(OUT/'assignment1_models.xlsx')
wb.set_properties({'title':'Assignment 1 — Exchange SE vs Google Workspace','subject':'Illustrative strategic and quantitative models, 2026–2030','author':'','comments':'No vendor CAC, churn or cost observations are claimed.'})
wb.set_calc_mode('auto')
fmt={
 'title':wb.add_format({'font_name':'Arial','font_size':17,'bold':True,'font_color':blue}),
 'head':wb.add_format({'font_name':'Arial','bold':True,'bg_color':blue,'font_color':'white','text_wrap':True,'valign':'vcenter','border':1}),
 'label':wb.add_format({'font_name':'Arial','font_size':10,'text_wrap':True,'valign':'top'}),
 'input':wb.add_format({'font_name':'Arial','font_color':'#145B9B','bg_color':'#EAF4FC','num_format':'#,##0.00'}),
 'num':wb.add_format({'font_name':'Arial','num_format':'#,##0.00','font_size':10}),
 'usd':wb.add_format({'font_name':'Arial','num_format':'"$"#,##0.00','font_size':10}),
 'pct':wb.add_format({'font_name':'Arial','num_format':'0.00%','font_size':10}),
 'good':wb.add_format({'font_name':'Arial','bg_color':'#E0F2E9','font_color':'#166245'}),
 'note':wb.add_format({'font_name':'Arial','font_color':'#5D6570','italic':True,'text_wrap':True,'valign':'top','font_size':10})}
S={name:wb.add_worksheet(name) for name in ['Guide','Inputs','CAC_LTV','Churn','TCO','Sensitivity','Charts','Sources','Checks']}
for sh in S.values():
 sh.hide_gridlines(2);sh.freeze_panes(3,1);sh.set_default_row(22);sh.set_column('A:A',35);sh.set_column('B:H',19);sh.set_landscape();sh.set_paper(9);sh.fit_to_pages(1,0)
 sh.set_footer('&LAssignment 1 | Illustrative assumptions&RPage &P of &N')
def title(sh,s):sh.merge_range('A1:H1',s,fmt['title'])
def headers(sh,row,labels):
 for col,s in enumerate(labels):sh.write(row,col,s,fmt['head'])
 sh.set_row(row,32)
def formula(sh,row,col,s,val,style='num'):sh.write_formula(row,col,s,fmt[style],val)
def note(sh,row,s):sh.merge_range(row,0,row+1,7,s,fmt['note']);sh.set_row(row,25);sh.set_row(row+1,25)
sh=S['Guide'];title(sh,'Assignment 1 | Model guide and scope')
notes=[
 'Purpose: compare a hypothetical 200-user SME’s Exchange SE and Google Workspace options over 2026–2030, while separating supplier CAC/LTV from buyer TCO.',
 'All numeric commercial, cost, risk and churn inputs are ILLUSTRATIVE ASSUMPTIONS supplied or explicitly derived from the case. No vendor customer cohort or empirical fit is represented.',
 'Blue cells on Inputs are editable; other sheets use Excel formulas. Changing baseline n updates B1 through the Churn sheet. Charts on Charts update with their linked data.',
 'LTV timing: an account active at the start of a year earns that year’s contribution; churn occurs at year-end. Cash is discounted at year-end. Thus survival exponent is t−1, not t.',
 'Risk loss is a 5% haircut to contribution, not a second churn probability. Annual churn is independent and held constant within each scenario; no terminal value is used.',
 'Cross-subsidy is a hypothetical USD 30,000 credit against USD 70,000 gross acquisition spending. Net allocated CAC falls, but ecosystem-wide resource cost remains USD 7,000/account. No actual Google transfer is claimed.',
 'TCO: nominal USD cash costs, opening-2026 one-off payments, five annual recurring payments. 200 seats, fixed prices, no tax/inflation/discount, zero residual value. Common connectivity and endpoints are excluded equally.',
 'Sensitivity varies only Google subscription price and Exchange FTE at USD 80,000/FTE/year. A USD 14 plan is a cost stress, not an assertion of equal plan features.',
 'Sources maps the official documentation to specific claims and records publication/revision dates. Licensing, staffing and hardware inputs are planning assumptions; procurement requires current entitlements and comparable quotations.',
 'Model validation: see Checks. Cached values are included; open in Excel/LibreOffice to recalculate after changing inputs. External PNG/PDF/SVG figures represent the original baseline and do not auto-refresh.',
]
for i,s in enumerate(notes):note(sh,3+3*i,s)
sh=S['Inputs'];title(sh,'Inputs | All numbers are illustrative assumptions');headers(sh,2,['Parameter','Value','Units','Definition / boundary'])
sh.set_column('A:A',25);sh.set_column('C:C',27);sh.set_column('D:D',79)
R={}
for i,(k,val,unit,desc) in enumerate(inputs,3):
 R[k]=i+1;sh.write(i,0,k,fmt['label']);sh.write_number(i,1,val,fmt['input']);sh.write(i,2,unit,fmt['label']);sh.write(i,3,desc,fmt['label']);sh.set_row(i,32)
 sh.data_validation(i,1,i,1,{'validate':'decimal','criteria':'>=','value':0})
for k in ['risk_loss','discount','churn_base']:
 sh.write_number(R[k]-1,1,V[k],wb.add_format({'font_name':'Arial','bg_color':'#EAF4FC','font_color':'#145B9B','num_format':'0.00%'}))
sh.data_validation(R['base_n']-1,1,R['base_n']-1,1,{'validate':'list','source':[0,2,4,6,8]})
for k in ['risk_loss','churn_base']:
 sh.data_validation(R[k]-1,1,R[k]-1,1,{'validate':'decimal','criteria':'between','minimum':0,'maximum':1})
# Horizon is deliberately 5 years, matching explicit year rows and report.
sh.write_comment(R['years']-1,1,'This assignment model has five explicit annual rows. Keep this input at 5; extend all year rows and formulas for a different horizon.')
sh.data_validation(R['years']-1,1,R['years']-1,1,{'validate':'integer','criteria':'equal to','value':5})
def I(k):return f'Inputs!$B${R[k]}'

sh=S['Churn'];title(sh,'B2 | Integration scenarios and retained customers');headers(sh,2,['n (count)','Annual churn','End-2030 retention','5-year LTV (USD)','Exchange LTV/CAC','Google LTV/CAC'])
for i,s in enumerate(M['churn_scenarios'],3):
 row=i+1;n=s['n'];sh.write_number(i,0,n,fmt['num'])
 formula(sh,i,1,f'={I("churn_base")}*EXP(-{I("churn_beta")}*A{row})',s['churn'],'pct')
 formula(sh,i,2,f'=(1-B{row})^{I("years")}',s['retention5'],'pct')
 formula(sh,i,3,'='+ '+'.join(f'{I("annual_gp")}*(1-{I("risk_loss")})*(1-B{row})^{t-1}/(1+{I("discount")})^{t}' for t in range(1,6)),s['ltv'],'usd')
 formula(sh,i,4,f'=D{row}/CAC_LTV!$B$7',s['ltv']/7000)
 formula(sh,i,5,f'=D{row}/CAC_LTV!$C$7',s['ltv']/4000)
note(sh,10,'Scenarios are alternative integration counts, not successive calendar years. Within each scenario, churn and n remain constant through 2026–2030. Retention=(1−c)^5, conditional on presence at opening-2026.')
note(sh,13,'No causal estimate is claimed. Data quality, usability, customer mix and portability could change the sign or magnitude of an observed relationship. API availability alone does not prove retention.')

sh=S['CAC_LTV'];title(sh,'B1 | Supplier-level CAC and risk-adjusted LTV');headers(sh,2,['Metric','Exchange SE','Google Workspace'])
labels=['Gross acquisition spending','Ecosystem funding credit','Net allocated acquisition cost','CAC per acquired account','5-year risk-adjusted LTV','LTV / net allocated CAC','Gross resource CAC (no funding credit)','LTV / gross resource CAC']
for i,l in enumerate(labels,3):sh.write(i,0,l,fmt['label']);sh.set_row(i,31)
for row,form,val in [(3,'='+I('exchange_acq'),70000),(4,'=0',0),(5,'=B4-B5',70000),(6,f'=B6/{I("clients")}',7000),(7,'=SUM(G18:G22)',L),(8,'=B8/B7',L/7000),(9,f'=B4/{I("clients")}',7000),(10,'=B8/B10',L/7000)]:formula(sh,row,1,form,val,'num' if row in [8,10] else 'usd')
for row,form,val in [(3,'='+I('google_gross_acq'),70000),(4,'='+I('ecosystem_credit'),30000),(5,'=C4-C5',40000),(6,f'=C6/{I("clients")}',4000),(7,'=SUM(G18:G22)',L),(8,'=C8/C7',L/4000),(9,f'=C4/{I("clients")}',7000),(10,'=C8/C10',L/7000)]:formula(sh,row,2,form,val,'num' if row in [8,10] else 'usd')
sh.write('A13','Selected baseline n',fmt['label']);formula(sh,12,1,'='+I('base_n'),4)
sh.write('A14','Linked baseline annual churn',fmt['label']);formula(sh,13,1,'=INDEX(Churn!B4:B8,MATCH(B13,Churn!A4:A8,0))',c,'pct')
headers(sh,16,['Year t','Calendar year','Start-year survival','End-year retention','Risk-adjusted GP','Discount factor','Present value'])
for i,t in enumerate(range(1,6),17):
 row=i+1;sh.write_number(i,0,t,fmt['num']);formula(sh,i,1,f'={I("first_year")}+A{row}-1',2025+t)
 formula(sh,i,2,f'=(1-$B$14)^(A{row}-1)',(1-c)**(t-1),'pct')
 formula(sh,i,3,f'=(1-$B$14)^A{row}',(1-c)**t,'pct')
 gp=6000*.95*(1-c)**(t-1)
 formula(sh,i,4,f'={I("annual_gp")}*(1-{I("risk_loss")})*C{row}',gp,'usd')
 formula(sh,i,5,f'=1/(1+{I("discount")})^A{row}',1/1.1**t)
 formula(sh,i,6,f'=E{row}*F{row}',gp/1.1**t,'usd')
sh.write('A24','Alternative timing LTV',fmt['label']);formula(sh,23,1,'=B8*(1-B14)',ltv(c,0),'usd')
note(sh,26,'The report presents the formal LTV equation. This sheet sums five discounted annual contributions, weighted by start-year survival. Alternative timing requires survival through year 1; neither convention includes a terminal value.')
note(sh,29,'Funding credit changes the cost assigned to the focal product, not total ecosystem resource use. This is a transparent hypothetical cross-subsidy mechanism, not observed Google or Microsoft financial performance.')

sh=S['TCO'];title(sh,'B3 | Buyer-level nominal cash costs, 2026–2030');headers(sh,2,['Cash cost category','Exchange SE (USD)','Google (USD)','Timing / scope'])
sh.set_column('A:A',35);sh.set_column('D:D',60)
costs=[('Hardware / storage',f'={I("hardware")}',32000,'=0',0,'Opening-2026; zero residual value'),('Deployment / migration',f'={I("deployment")}',9000,f'={I("migration")}',15000,'Opening-2026; cloud includes training'),('Total one-off','=SUM(B4:B5)',41000,'=SUM(C4:C5)',15000,'Do not add again to recurring expenses'),('Licensing / subscriptions',f'={I("licensing")}',12000,f'={I("employees")}*{I("google_price")}*12',16800,'Annual; illustrative licensing allowance / price'),('Administration',f'={I("loaded_fte")}*{I("exchange_fte")}',24000,f'={I("google_admin")}',8000,'Annual; USD 80,000/FTE/year for Exchange'),('Facilities/network/maintenance',f'={I("facilities")}',7000,'=0',0,'Annual incremental on-premises allowance'),('Backup / added security',f'={I("backup")}',5000,f'={I("backup")}',5000,'Annual incremental control allowance'),('Total annual recurring','=SUM(B7:B10)',48000,'=SUM(C7:C10)',29800,'Five recurring payments'),('Five-year TCO',f'=B6+{I("years")}*B11',EX,f'=C6+{I("years")}*C11',GW,'Nominal USD; no discounting')]
for row,(label,ef,ev,gf,gv,scope) in enumerate(costs,3):
 sh.write(row,0,label,fmt['label']);formula(sh,row,1,ef,ev,'usd');formula(sh,row,2,gf,gv,'usd');sh.write(row,3,scope,fmt['label']);sh.set_row(row,32)
sh.write('A14','Google savings (USD)',fmt['label']);formula(sh,13,1,'=B12-C12',EX-GW,'usd')
sh.write('A15','Savings / Exchange TCO',fmt['label']);formula(sh,14,1,'=B14/B12',(EX-GW)/EX,'pct')
headers(sh,17,['Cash year','Exchange SE','Google Workspace','Cumulative Exchange','Cumulative Google'])
for i,year in enumerate(range(2026,2031),18):
 r=i+1;sh.write_number(i,0,year,fmt['num'])
 formula(sh,i,1,'=$B$11'+('+$B$6' if year==2026 else ''),48000+(41000 if year==2026 else 0),'usd')
 formula(sh,i,2,'=$C$11'+('+$C$6' if year==2026 else ''),29800+(15000 if year==2026 else 0),'usd')
 formula(sh,i,3,f'=SUM(B19:B{r})',41000+(year-2025)*48000,'usd')
 formula(sh,i,4,f'=SUM(C19:C{r})',15000+(year-2025)*29800,'usd')
note(sh,25,'The two-server allowance is a cost scenario, not a validated resilient architecture. Existing directory/DNS capacity is assumed reusable. Required OS/CAL/SE entitlements and backup design must be checked with current official terms and a reseller quote.')
note(sh,28,'Excluded symmetrically: common endpoints/internet, tax, inflation, financing, productivity valuation and outage losses. No hardware refresh or decommissioning cost is modeled; prices and users stay constant. Feature equivalence and regulatory suitability are not established.')

sh=S['Sensitivity'];title(sh,'Sensitivity | Two-variable cost reversal test');headers(sh,2,['Google USD/user/month','Exchange FTE','Exchange TCO','Google TCO','Google savings','Preferred by cost'])
for i,s in enumerate(M['sensitivity'],3):
 row=i+1;formula(sh,i,0,'='+I('google_price' if s['price']==7 else 'stress_price'),s['price'],'usd');formula(sh,i,1,'='+I('exchange_fte' if s['fte']==.3 else 'low_fte'),s['fte'])
 formula(sh,i,2,f'={I("hardware")}+{I("deployment")}+{I("years")}*({I("licensing")}+{I("loaded_fte")}*B{row}+{I("facilities")}+{I("backup")})',s['exchange'],'usd')
 formula(sh,i,3,f'={I("migration")}+{I("years")}*({I("employees")}*A{row}*12+{I("google_admin")}+{I("backup")})',s['google'],'usd')
 formula(sh,i,4,f'=C{row}-D{row}',s['saving'],'usd');formula(sh,i,5,f'=IF(E{row}>0,"Google",IF(E{row}<0,"Exchange","Tie"))','Google' if s['saving']>0 else 'Exchange','label')
headers(sh,9,['Exchange FTE','Break-even Google price','Units'])
for i,fte in enumerate([.3,.15],10):
 row=i+1;formula(sh,i,0,'='+I('exchange_fte' if fte==.3 else 'low_fte'),fte)
 et=41000+5*(12000+80000*fte+7000+5000)
 formula(sh,i,1,f'=({I("hardware")}+{I("deployment")}+{I("years")}*({I("licensing")}+{I("loaded_fte")}*A{row}+{I("facilities")}+{I("backup")})-{I("migration")}-{I("years")}*({I("google_admin")}+{I("backup")}))/({I("years")}*{I("employees")}*12)',(et-15000-5*13000)/12000,'usd')
 sh.write(i,2,'USD/user/month',fmt['label'])
note(sh,14,'Positive savings favour Google. At USD 14/user/month and 0.15 Exchange FTE, Exchange is USD 27,000 cheaper. This does not prove either plan meets the same functional or compliance requirements.')

sh=S['Charts'];title(sh,'Figures | Linked Excel charts')
chart=wb.add_chart({'type':'scatter','subtype':'straight_with_markers'})
chart.add_series({'name':'Annual churn (illustrative)','categories':'=Churn!$A$4:$A$8','values':'=Churn!$B$4:$B$8','line':{'color':teal},'marker':{'type':'circle','size':7},'data_labels':{'value':True,'num_format':'0.00%'}})
chart.set_title({'name':'Annual churn by integration count | 2026–2030 scenarios'})
chart.set_x_axis({'name':'Active material integrations, n (count)','min':0,'max':8,'major_unit':2})
chart.set_y_axis({'name':'Annual customer churn (%)','num_format':'0%','min':0,'max':.22});chart.set_legend({'none':True});chart.set_size({'width':720,'height':420});sh.insert_chart('A4',chart)
chart=wb.add_chart({'type':'column'})
chart.add_series({'name':'Five-year TCO (nominal USD)','categories':'=TCO!$B$3:$C$3','values':'=TCO!$B$12:$C$12','points':[{'fill':{'color':blue}},{'fill':{'color':teal}}],'data_labels':{'value':True,'num_format':'$#,##0'}})
chart.set_title({'name':'200 users | 2026–2030 | Illustrative assumptions'});chart.set_y_axis({'name':'Five-year nominal TCO (USD)','num_format':'$#,##0'});chart.set_legend({'none':True});chart.set_size({'width':720,'height':420});sh.insert_chart('A26',chart)
note(sh,48,'Baseline TCO: USD 7/user/month and 0.30 Exchange FTE. The line chart uses integration scenarios, not calendar time. External figure files are static exports of the initial baseline.')

sh=S['Sources'];title(sh,'Official sources | Claim mapping and access audit');headers(sh,2,['ID','Organization / date','Title','Official URL','Supported use','Verification status','Official GitHub source','Citation date basis'])
sh.set_column('A:A',8);sh.set_column('B:B',22);sh.set_column('C:C',35);sh.set_column('D:H',52)
for i,s in enumerate(SOURCES,3):
 vals=[s['id'],s['author']+' ('+s['date']+')',s['title'],s['url'],s['supports'],s['status'],s['mirror'],(s.get('revision_date') or 'Undated')+' — '+s['date_basis']]
 for j,v in enumerate(vals):sh.write(i,j,v,fmt['label'])
 sh.set_row(i,95)
note(sh,18,'Access audit date: 16 October 2026. A verified GitHub sample supports only the stated API/documentation claim. It is not a live API test, a product-price verification or evidence of vendor churn/CAC.')

sh=S['Checks'];title(sh,'Validation | Formula identities and scenario checks');headers(sh,2,['Check','Result','Expected / rationale'])
checks=[
 ('Baseline CAC, Exchange','=IF(ABS(CAC_LTV!B7-7000)<0.000001,"PASS","FAIL")','USD 7,000'),
 ('Baseline CAC, Google','=IF(ABS(CAC_LTV!C7-4000)<0.000001,"PASS","FAIL")','USD 4,000'),
 ('Linked churn, n=4','=IF(ABS(CAC_LTV!B14-0.18*EXP(-0.4))<0.000000001,"PASS","FAIL")','Unrounded baseline used throughout'),
 ('Finite-horizon baseline LTV','=IF(ABS(CAC_LTV!B8-17398.8668944561)<0.00001,"PASS","FAIL")','End-year cash; start-year survival'),
 ('Scenario n=4 links to B1','=IF(ABS(Churn!D6-CAC_LTV!B8)<0.00001,"PASS","FAIL")','Same provider-normalized LTV'),
 ('Exchange 5-year TCO','=IF(ABS(TCO!B12-281000)<0.00001,"PASS","FAIL")','USD 41,000 + 5 × USD 48,000'),
 ('Google 5-year TCO','=IF(ABS(TCO!C12-164000)<0.00001,"PASS","FAIL")','USD 15,000 + 5 × USD 29,800'),
 ('Annual schedule reconciliation','=IF(AND(ABS(SUM(TCO!B19:B23)-TCO!B12)<0.00001,ABS(SUM(TCO!C19:C23)-TCO!C12)<0.00001),"PASS","FAIL")','Five annual rows reconcile'),
 ('High-price / low-FTE reversal','=IF(ABS(Sensitivity!E7+27000)<0.00001,"PASS","FAIL")','Google savings = −USD 27,000'),
 ('Churn and retention direction','=IF(AND(Churn!B4>Churn!B8,Churn!C4<Churn!C8),"PASS","FAIL")','Illustrative monotonic model'),
 ('First-year contribution timing','=IF(ABS(CAC_LTV!G18-5700/1.1)<0.00001,"PASS","FAIL")','No churn before year-1 contribution'),
 ('Alternative-timing identity','=IF(ABS(CAC_LTV!B24-CAC_LTV!B8*(1-CAC_LTV!B14))<0.00001,"PASS","FAIL")','About USD 15,300'),
 ('All baseline assumptions unchanged',f'=IF(AND({I("base_n")}=4,{I("google_price")}=7,{I("exchange_fte")}=0.3,{I("years")}=5),"PASS","CHANGED")','Baseline checkpoints intentionally flag edits')]
for i,(label,ff,expected) in enumerate(checks,3):
 sh.write(i,0,label,fmt['label']);formula(sh,i,1,ff,'PASS','good');sh.write(i,2,expected,fmt['label']);sh.set_row(i,35)
sh.set_column('C:C',58)
note(sh,19,'Baseline checks compare against the report values and will flag legitimate input changes. They are reconciliation checks, not an empirical validation of the behavioural model or evidence that a real deployment meets requirements.')
wb.close()
print(json.dumps(M,indent=2))
print('Wrote workbook, charts and source ledger to',OUT)
