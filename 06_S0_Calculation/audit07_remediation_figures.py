"""Pre-writing figures. Separate assets; never replace the archived manuscript figures.
Run after audit06_remediation.mjs and audit06_road_remediation.mjs.
All publication figures are 15 cm wide at native size, text >= 8 pt.
"""
import csv, math
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Patch
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.text import Text

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"02_Cleaned_Data"
F=ROOT/"09_Paper_Draft"/"figures_final"/"remediation"
F.mkdir(parents=True,exist_ok=True)
W=15/2.54
ICE="#496783"; NMC="#C56D88"; LFP="#82ADD0"; PHEV="#9B8AB8"; BUS="#D3A16F"
ENERGY="#4E6D8A"; MATERIAL="#8DB6D8"; PARTS="#5C8DB6"; DIST="#CCD6E0"
DARK="#263849"; BEV="#497C79"; GREY="#B7BEC5"; LIGHT="#EDF1F4"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":9,"axes.labelsize":9,"axes.titlesize":10,"axes.titleweight":"semibold","xtick.labelsize":8.5,"ytick.labelsize":8.5,"legend.fontsize":8.5,"axes.spines.top":False,"axes.spines.right":False,"axes.edgecolor":"#8492A0","text.color":DARK,"axes.labelcolor":DARK,"xtick.color":DARK,"ytick.color":DARK,"figure.facecolor":"white","axes.facecolor":"white","savefig.facecolor":"white","svg.fonttype":"none","hatch.linewidth":.65})
SS=["S-1","S0","S1","S2","S3","S4"]; SL=["S−1","S0","S1","S2","S3","S4"]; XX=np.arange(6)
manifest=[]; qa=[]
def read(n):
    with (D/n).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def one(rows,**kw):return next(r for r in rows if all(r[k]==v for k,v in kw.items()))
def num(r,k):return float(r[k])
def vals(rows,k):return np.array([num(r,k) for r in rows])
def make(h,rows=1,cols=1,**kwargs):return plt.subplots(rows,cols,figsize=(W,h),layout="constrained",**kwargs)
def axis(ax,y=None,x=None):
    if y:ax.set_ylabel(y)
    if x:ax.set_xlabel(x)
    ax.grid(axis="y",color="#D9E1E8",lw=.5);ax.set_axisbelow(True)
def ticks(ax):ax.set_xticks(XX,SL);ax.set_xlim(-.55,5.55)
def save(fig,name,source,caption,domain="contest"):
    fig.canvas.draw();rend=fig.canvas.get_renderer()
    boxes=[];font=[]
    for t in fig.findobj(Text):
        if not t.get_visible() or not t.get_text().strip():continue
        font.append(t.get_fontsize())
        box=t.get_window_extent(rend)
        if box.x0 < -2 or box.y0 < -2 or box.x1 > fig.bbox.width+2 or box.y1 > fig.bbox.height+2:
            boxes.append(t.get_text().replace("\n"," "))
    if min(font,default=9)<8:raise ValueError("font below 8 pt: "+name)
    for ext in ("svg","png","pdf"):
        fig.savefig(F/(name+"."+ext),dpi=300 if ext=="png" else 96,metadata={"Date":None} if ext=="svg" else None)
    qa.append([name,round(W*2.54,2),min(font,default=9),len(boxes)," | ".join(boxes),"PENDING human print-size review"])
    manifest.append([name+".svg",name+".png",name+".pdf",domain,source,caption])
    plt.close(fig)
def block(ax,x,y,w,h,head,body,color=LIGHT):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.008,rounding_size=0.018",facecolor=color,edgecolor=ICE,lw=.8))
    ax.text(x+w/2,y+h*.70,head,ha="center",va="center",weight="bold",fontsize=9)
    ax.text(x+w/2,y+h*.29,body,ha="center",va="center",fontsize=8.5,linespacing=1.3)
def arrow(ax,x,y,u,v):
    ax.annotate("",xy=(u,v),xytext=(x,y),arrowprops={"arrowstyle":"-|>","color":ICE,"lw":1})
def diagram(h):
    f,ax=make(h);ax.set(xlim=(0,1),ylim=(0,1));ax.axis("off");return f,ax
A=read("R9_7A_SIX_SCENARIO_VKT.csv")
a0=one(A,scenario="S0")
E=[r for r in read("R9_7B_SIX_SCENARIO_ENERGY_WTW.csv") if r["case"]=="base"]
G=read("R9_7C_PARTIAL_LCA_GWP_SCENARIOS.csv")
P=[r for r in read("R9_7E_ROAD_POLLUTANT_SCENARIOS.csv") if r["case"]=="V_reference"]
PM=[r for r in read("R9_7AUDIT04_WEAR_SCENARIOS.csv") if r["case"]=="EEA_equal"]
N=read("R9_7F_NESTED_ENVELOPE.csv")
FIX=read("R9_7FIX_SENSITIVITY_ENVELOPE.csv")
WIT=read("R9_7FIX_REVERSAL_WITNESSES.csv")
T=read("R9_7F_TRANSFER_GRID.csv")
D0=read("R9_7D_SERVICE_SENSITIVITY.csv")
PK=read("R9_7FIX_CALIBRATED_PKM.csv")
B=read("R9_7AUDIT04_BATTERY_RECIPE.csv")
C=read("R9_7FIX_STAGE_COVERAGE.csv")
params={r["parameter"]:float(r["value"]) for r in read("R9_7B_ENERGY_INPUTS.csv")}
prod=read("R9_7C_MANUFACTURING_FACTOR_REGISTER.csv")
gref=vals(G,"partial_LCA_GWP_t_y")/1000
red=100*(1-gref/gref[1])
# F01: complete independent domains.
f,ax=diagram(5.0)
block(ax,.13,.83,.74,.13,"Beijing evidence","Population, stock, travel and energy",LIGHT)
block(ax,.13,.62,.74,.13,"Million-resident representative city","Mode VKT, propulsion mix and six scenarios","#DDEBF5")
arrow(ax,.5,.83,.5,.75)
for i,(head,body,col) in enumerate([("Climate","Production + WTW\nFinal energy","#DDEBF5"),("Road ecology","Combustion exhaust\nTyre, brake, road wear","#F4E4E8"),("Battery LCIA","11 separate indicators\nNot added to GWP","#E8E3F0")]):
    x=.012+i*.33
    block(ax,x,.36,.31,.18,head,body,col);arrow(ax,.5,.62,x+.155,.54);arrow(ax,x+.155,.36,.5,.29)
block(ax,.10,.15,.80,.14,"Paired tests and transfer","VKT/PKM, grid, lifetime, replacement",LIGHT)
arrow(ax,.5,.15,.5,.10)
ax.text(.5,.055,"Conditional environmental decisions",ha="center",weight="bold",fontsize=10)
save(f,"F01_Framework","R9.7A–F; Audit-04; R9_7FIX_*","Representative city of one million residents; 2022 activity and pre-contest evidence; distinct climate, road and private-battery domains. PKM conditional; no aggregation across unlike indicators.")
# F02: activity and propulsion.
f,axs=make(4.8,2,1)
for ax,keys,labels,colors,total,title in [
 (axs[0],["private_ICEV_vkt_km","private_BEV_vkt_km","private_PHEV_vkt_km"],["ICEV","BEV (unspecified chemistry)","PHEV"],[ICE,BEV,PHEV],"private_total_vkt_km","(a) Private cars"),
 (axs[1],["bus_diesel_vkt_km","bus_natural_gas_vkt_km","bus_mixed_nonBEV_vkt_km","bus_BEV_vkt_km","bus_unclassified_vkt_km"],["Diesel","Natural gas","Mixed non-BEV","BEV","Unknown"],[ICE,BUS,PHEV,BEV,GREY],"bus_total_vkt_km","(b) Public buses")]:
    bottom=np.zeros(6);den=vals(A,total)
    for k,label,col,hatch in zip(keys,labels,colors,["","//","..","xx","\\\\"]):
        z=vals(A,k)/den*100;ax.bar(XX,z,bottom=bottom,color=col,edgecolor="white",lw=.35,label=label,hatch=hatch);bottom+=z
    assert np.allclose(bottom,100)
    ticks(ax);ax.set_ylim(0,100);axis(ax,"VKT share (%)")
    ax.set_title(f"{title} | {den[0]/1e6:,.2f} million km/year",loc="left")
    ax.legend(loc="upper center",bbox_to_anchor=(.5,-.17),ncol=2,frameon=False)
save(f,"F02_Activity","R9_7A_SIX_SCENARIO_VKT.csv","2022 activity anchor; April 2023 propulsion snapshot. Annual private and bus VKT are fixed within mode. Shares are conditional allocations, not observed propulsion-specific mileage.")
# F03: boundaries and limits.
f,ax=diagram(4.4)
block(ax,.04,.76,.92,.18,"Annual included-stage climate GWP","Source-specific production / replacements + energy WTW","#DDEBF5")
block(ax,.04,.50,.44,.19,"Road combustion","CO, VOCs, NOx,\nPM2.5, PM10","#F4E4E8")
block(ax,.52,.50,.44,.19,"Road wear","Brake, tyre, surface\nPM2.5 and PM10","#F4E4E8")
block(ax,.04,.25,.44,.18,"Private battery LCIA","Independent NCM622\nrecycling scenarios","#E8E3F0")
block(ax,.52,.25,.44,.18,"Replacement stress","Extra private packs;\nbus replacement NA","#E8E3F0")
block(ax,.04,.02,.92,.16,"Not fully quantified","Full maintenance, EOL, dust, infrastructure, noise",LIGHT)
save(f,"F03_Boundary","R9_7FIX_STAGE_COVERAGE.csv; R9_7AUDIT04_WEAR_SCENARIOS.csv; R9_7AUDIT04_BATTERY_RECIPE.csv","Included production (Qiao includes selected consumable replacements) + WTW is not complete cradle-to-grave LCA. Road wear and private battery LCIA are separate modules; some stages remain NA. Detailed 128-cell ledger in A05.")
# F04 energy and separate GWP panels.
f=plt.figure(figsize=(W,5.0),layout="constrained");gs=f.add_gridspec(2,2,height_ratios=[1,1.15]);ax=f.add_subplot(gs[0,:]);axs=[f.add_subplot(gs[1,0]),f.add_subplot(gs[1,1])]
bottom=np.zeros(6)
for label,z,col,h in [("Gasoline",vals(E,"gasoline_L")*params["gasoline_mj_l"]/1e9,ICE,""),("Diesel",vals(E,"diesel_MJ")/1e9,"#74899B","//"),("Natural gas",vals(E,"natural_gas_MJ")/1e9,BUS,".."),("Car electricity",vals(E,"private_electricity_kWh")*3.6/1e9,BEV,"xx"),("Bus electricity",vals(E,"bus_electricity_kWh")*3.6/1e9,PHEV,"\\\\")]:
    ax.bar(XX,z,bottom=bottom,color=col,edgecolor="white",lw=.3,label=label,hatch=h);bottom+=z
assert np.allclose(bottom,vals(E,"final_energy_MJ")/1e9)
ticks(ax);axis(ax,"Final energy (PJ/year)");ax.set_ylim(0,6.5);ax.set_title("(a) Energy demand by carrier",loc="left");ax.legend(ncol=3,frameon=False,loc="upper right")
for j,z in enumerate(bottom):ax.text(j,z+.07,f"{z:.2f}",fontsize=8.5,ha="center")
for ax,k,title,key in zip(axs,["private","bus"],["(b) Private cars","(c) Buses"],["private_vehicle_production_GWP_t_y","bus_manufacturing_GWP_t_y"]):
    w=vals(E,k+"_WTW_tCO2e")/1000;m=vals(G,key)/1000
    ax.bar(XX,w,color=ENERGY,label="WTW")
    ax.bar(XX,m,bottom=w,color=MATERIAL,edgecolor=ICE,hatch="//",lw=.35,label="Production")
    ticks(ax);axis(ax,"GWP (kt CO₂e/year)");ax.set_title(title,loc="left");ax.set_ylim(0,max(w+m)*1.30)
    ax.legend(frameon=False,loc="upper right",fontsize=8.5)
save(f,"F04_Energy_GWP","R9_7B_SIX_SCENARIO_ENERGY_WTW.csv; R9_7C_PARTIAL_LCA_GWP_SCENARIOS.csv","Million-resident annual reference: final energy in PJ/year and annualized production + WTW in kt CO2e/year. Separate mode scales. S3 and S4 energy identical; S4 changes electricity emissions only.")
# F05 pollutants. PM shows combustion + wear, no double counting or summing size classes.
f,axs=make(6.5,3,2)
for ax,k,lab in zip(axs.flat,["CO","VOCs","NOx","PM2_5","PM10"],["CO","VOCs","NOₓ","PM₂.₅","PM₁₀"]):
    r=[one(P,scenario=s,pollutant=k) for s in SS]
    c=vals(r,"private_t_y");b=vals(r,"bus_t_y")
    ax.bar(XX,c,color=ICE);ax.bar(XX,b,bottom=c,color=BUS,edgecolor=DARK,hatch="//",lw=.3)
    if k.startswith("PM"):
        a=[one(PM,scenario=s,pollutant=k) for s in SS];w=vals(a,"private_wear_t_y");v=vals(a,"bus_wear_t_y")
        ax.bar(XX,w,bottom=c+b,color="#A9C7DD",edgecolor=ICE,hatch="..",lw=.3)
        ax.bar(XX,v,bottom=c+b+w,color="#E5C7A6",edgecolor=DARK,hatch="xx",lw=.3)
        assert np.allclose(c+b+w+v,vals(a,"covered_road_PM_t_y"))
    ticks(ax);axis(ax,"t/year");ax.set_title(lab,loc="left")
axs.flat[5].axis("off")
axs.flat[5].legend(handles=[Patch(facecolor=ICE,label="Car exhaust"),Patch(facecolor=BUS,edgecolor=DARK,hatch="//",label="Bus exhaust"),Patch(facecolor="#A9C7DD",edgecolor=ICE,hatch="..",label="Car wear (PM)"),Patch(facecolor="#E5C7A6",edgecolor=DARK,hatch="xx",label="Bus wear (PM)")],loc="center",frameon=False)
save(f,"F05_Road_Pollutants","R9_7E_ROAD_POLLUTANT_SCENARIOS.csv; R9_7AUDIT04_WEAR_SCENARIOS.csv","2022 anchor, illustrative China V draft factors, EEA generic wear. PM panels include tyre/brake/surface wear; gas panels only combustion. Dust and secondary PM excluded. Independent panel scales; PM size categories overlap.")
# F06 decision trade-off.
f,ax=make(3.2)
nox=np.array([num(one(P,scenario=s,pollutant="NOx"),"total_t_y") for s in SS]);nr=100*(1-nox/nox[1])
for i,col,marker,offset in [(1,GREY,"s",(4,4)),(2,BUS,"^",(5,-12)),(3,ICE,"s",(5,4)),(4,NMC,"o",(-32,-17)),(5,BEV,"D",(5,-17))]:
    ax.scatter(red[i],nr[i],s=65,c=col,marker=marker,edgecolor=DARK,zorder=3);ax.annotate(SL[i],(red[i],nr[i]),xytext=offset,textcoords="offset points",fontsize=9)
ax.set(xlim=(-3,50),ylim=(-5,108));ax.set_xticks([0,10,20,30,40,50]);ax.set_yticks([0,20,40,60,80,100]);axis(ax,"NOₓ exhaust reduction (%)","Included-stage GWP reduction (%)")
ax.axhline(0,color=DARK,lw=.7);ax.axvline(0,color=DARK,lw=.7)
save(f,"F06_Policy_Tradeoff","R9_7C_PARTIAL_LCA_GWP_SCENARIOS.csv; R9_7E_ROAD_POLLUTANT_SCENARIOS.csv","Reference S0–S4 reductions, relative to S0; climate and road NOx objectives differ. This is not a cost-constrained Pareto frontier or a forecast.")
# F07 comparison of deterministic envelopes.
f,ax=make(3.9)
for j,s in enumerate(SS):
    old=one(N,scenario=s,indicator="partial_GWP_t");new=one(FIX,design="remediation_25_packages",scenario=s)
    ax.hlines(j-.14,num(old,"min_reduction_pct"),num(old,"max_reduction_pct"),lw=3,color="#A0A0A0")
    ax.hlines(j+.14,num(new,"min_reduction_pct"),num(new,"max_reduction_pct"),lw=3.7,color=ICE)
    ax.scatter(red[j],j+.14,c=NMC,edgecolor=DARK,s=25,zorder=4)
ax.set_yticks(XX,SL);ax.invert_yaxis();ax.set_xlim(-33,66);ax.set_xticks([-30,-20,-10,0,10,20,30,40,50,60]);ax.set_xlabel("Reduction relative to paired S0 (%)");ax.grid(axis="x",color="#D9E1E8",lw=.5);ax.axvline(0,color=DARK,ls="--",lw=.9)
ax.legend(handles=[plt.Line2D([0],[0],color="#A0A0A0",lw=3,label="Original: 14,580"),plt.Line2D([0],[0],color=ICE,lw=3,label="Extended: 328,050"),plt.Line2D([0],[0],marker="o",color=NMC,ls="",label="Reference")],loc="upper right",frameon=False)
w=one(WIT,design="remediation_25_packages",scenario="S4")
ax.annotate(f"S4 min {float(w['red']):.3f}%",(float(w["red"]),5.14),xytext=(13,9),textcoords="offset points",fontsize=8.5,arrowprops={"arrowstyle":"-","color":DARK})
save(f,"F07_Paired_Envelope","R9_7F_NESTED_ENVELOPE.csv; R9_7FIX_SENSITIVITY_ENVELOPE.csv; R9_7FIX_REVERSAL_WITNESSES.csv","Deterministic designs, not probabilities or confidence intervals; original and extended designs are not strict subsets. S4 near-zero negative witness under joint adverse assumptions. 2022 activity anchor; paired S0 in each set.")
# F08 private car break-even with additional private NMC pack.
mi=num(one(prod,source_id="QIAO17_ICE"),"factor_value")*1000
mb=num(one(prod,source_id="QIAO17_BEV_NMC"),"factor_value")*1000
bf=num(one(B,scenario="S3",recycling_case="no_credit",indicator="GWP100"),"factor_per_kWh")
ll=np.linspace(100000,300000,150)
f,axs=make(5.0,2,1)
for ax,gas,eta,title in [(axs[0],params["gasoline_l100"],1,"(a) Reference fuel / delivered electricity"),(axs[1],6,.9,"(b) Low fuel use / conditional charging loss")]:
    for n,col,ls in [(0,ICE,"-"),(.5,PHEV,"--"),(1,NMC,"-.")]:
        y=((mi-mb-n*40*bf)/ll+gas/100*params["gasoline_mj_l"]*params["gasoline_ef"]/1000)/(params["car_e"]/eta)
        ax.plot(ll/1000,y,color=col,ls=ls,lw=1.7,label=f"{n:g} extra packs")
    ax.axhline(params["grid_ef"],color=DARK,ls=":",label="Reference grid")
    ax.axhline(params["grid_ef"]*.5,color=BEV,ls=":",label="Half factor")
    ax.set_ylim(0,1.15);ax.set_xticks([100,150,200,250,300]);axis(ax,"Threshold (kg CO₂e/kWh)","Lifetime (thousand km)");ax.set_title(title,loc="left")
axs[0].legend(ncol=2,frameon=True,facecolor="white",framealpha=1,edgecolor="none",loc="lower right")
save(f,"F08_Threshold","R9_7B_ENERGY_INPUTS.csv; R9_7C_MANUFACTURING_FACTOR_REGISTER.csv; R9_7AUDIT04_BATTERY_RECIPE.csv","Private gasoline versus NMC BEV, matched lifetime and production + WTW boundary. Extra 40 kWh NMC packs at Sun proxy 124.48 kg CO2e/kWh. Curves are conditional; below threshold BEV has lower GWP. Not city-wide threshold.")
# A01 transfer (no retrospective inputs).
f,axs=make(2.9,1,3);levels=[.8,1,1.2];tr=[r for r in T if r["scenario"]=="S3"];vv=vals(tr,"reduction_vs_paired_S0_pct")
for ax,b in zip(axs,levels):
    mat=np.array([[next(num(r,"reduction_vs_paired_S0_pct") for r in tr if np.allclose([num(r,k) for k in ["g_ownership","m_mileage","b_bus_supply"]],[g,m,b])) for m in levels] for g in levels])
    im=ax.imshow(mat,vmin=min(vv),vmax=max(vv),cmap="Blues",aspect="equal")
    for i,j in np.ndindex(mat.shape):ax.text(j,i,f"{mat[i,j]:.2f}",ha="center",va="center",fontsize=8.5,color="white" if mat[i,j]>(min(vv)+max(vv))/2 else DARK)
    ax.set_xticks(range(3),["0.8","1","1.2"]);ax.set_yticks(range(3),["0.8","1","1.2"]);ax.set_xlabel("Mileage m");ax.set_title(f"Bus b={b:g}",fontsize=9)
axs[0].set_ylabel("Ownership g");f.colorbar(im,ax=axs,label="S3 reduction (%)",shrink=.65)
save(f,"A01_Transfer","R9_7F_TRANSFER_GRID.csv","27 reference-intensity transfer settings; common color scale. No actual Jinhua VKT. Retrospective Jinhua diagnostic table remains separately labelled.")
# A02 conditional passenger service.
f,axs=make(4.4,2,1);r=[one(D0,case="reference",scenario=s) for s in SS]
axs[0].bar(XX-.18,vals(r,"car_partial_GWP_g_per_PKM"),.36,color=ICE,label="Cars");axs[0].bar(XX+.18,vals(r,"bus_partial_GWP_g_per_PKM"),.36,color=BUS,edgecolor=DARK,hatch="//",label="Buses")
ticks(axs[0]);axis(axs[0],"g CO₂e/PKM");axs[0].legend(frameon=False);axs[0].set_title("(a) Conditional intensity",loc="left")
z=vals(PK,"S3_GWP_kt")
axs[1].bar(range(3),z,color=[NMC,LFP,BEV],edgecolor=DARK,lw=.4);axs[1].axhline(gref[1],color=DARK,ls="--",label="Paired S0")
axs[1].set_xticks(range(3),["Lower","Reference","Higher"]);axis(axs[1],"GWP (kt CO₂e/year)");axs[1].set_title("(b) Equal S0 passenger service",loc="left");axs[1].set_ylim(0,700);axs[1].legend(frameon=False,loc="upper right")
save(f,"A02_PKM","R9_7D_SERVICE_SENSITIVITY.csv; R9_7FIX_CALIBRATED_PKM.csv","Proxy 10.9 km per bus boarding and 1.24 car occupants; not observed PKM. Equal-service stresses recalibrate each S0 to common conditional service volumes; annual GWP unchanged by calibration.")
# A03 meter.
f,ax=diagram(2.6)
block(ax,.02,.58,.28,.29,"Grid input","WTW factor\nQgrid","#DDEBF5");block(ax,.36,.58,.28,.29,"Charger","Loss if outside\nreported meter",LIGHT);block(ax,.70,.58,.28,.29,"Battery","Meter may be\nhere or upstream","#DDEBF5")
arrow(ax,.30,.73,.36,.73);arrow(ax,.64,.73,.70,.73)
ax.text(.5,.36,"Delivered interpretation: use reported kWh",ha="center",fontsize=9)
ax.text(.5,.21,"Battery-side interpretation: Qgrid = Qreported / η",ha="center",fontsize=9)
ax.text(.5,.07,"Historical bus proxy: test both interpretations",ha="center",weight="bold",fontsize=8.5)
save(f,"A03_Meter","R9_7B_ENERGY_INPUTS.csv; R9_7FIX_TECH_PACKAGES.csv","Meter position is unresolved. Apply charger loss only when excluded from recorded quantity. Historical high bus electricity use tested both delivered and battery-side; no claim measured losses.")
# A04 battery-only LCIA.
f,ax=make(4.9)
r=[x for x in B if x["scenario"]=="S3" and x["recycling_case"]=="no_credit"]
names=[x["indicator"] for x in r];labels=[x.replace("_"," ").replace("GWP100","GWP100") for x in names]
z=[]
for x in r:
    old=num(x,"factor_per_kWh");new=num(one(B,scenario="S3",indicator=x["indicator"],recycling_case="source_100pct_recycling"),"factor_per_kWh")
    z.append((new/old-1)*100 if old!=0 else np.nan)
for i,v in enumerate(z):
    if not np.isfinite(v):ax.text(0,i,"NA",fontsize=8.5);continue
    ax.barh(i,v,color=NMC if v>0 else ICE,edgecolor=DARK,lw=.3,hatch="//" if v>0 else "")
    if abs(v)<1e-12:ax.text(1,i,"≈0",va="center",fontsize=8.5)
ax.set_yticks(range(len(labels)),labels);ax.set_xlim(-100,40);ax.set_xticks([-100,-75,-50,-25,0,25,40]);ax.invert_yaxis();ax.axvline(0,color=DARK,lw=.8);ax.set_xlabel("Change within each category (%)");ax.grid(axis="x",color="#D9E1E8",lw=.5);ax.set_axisbelow(True)
save(f,"A04_Battery_LCIA","R9_7AUDIT04_BATTERY_RECIPE.csv","S3 hypothetical private NCM622 battery only, Sun 2020 ReCiPe Midpoint(H), reported 100% recycling compared with no-credit material + production. Rounded factors limit precision. Categories not summed, not added to whole-vehicle GWP.")
# A05 actual 8x16 coverage matrix.
f,ax=make(6.1)
vehicles=list(dict.fromkeys(x["vehicle"] for x in C));stages=list(dict.fromkeys(x["stage"] for x in C));assert len(vehicles)==8 and len(stages)==16 and len(C)==128
status={"INCLUDED_PARTIAL_CONSUMABLES":("I*",0),"INCLUDED_AGGREGATE_PROXY":("I",0),"INCLUDED_WTW_PROXY":("W",0),"ALLOCATED_PROXY":("A",1),"SUPPLEMENTARY_PROXY":("P",1),"CONDITIONAL_SERVICE":("C",1),"SEPARATE_LCIA":("L",2),"SEPARATE_HISTORICAL_PHYSICAL":("H",2),"NA":("NA",3),"NOT_APPLICABLE":("—",4)}
mat=np.zeros((16,8));codes={}
for i,s in enumerate(stages):
    for j,v in enumerate(vehicles):
        k=one(C,vehicle=v,stage=s)["coverage"];codes[i,j],mat[i,j]=status[k]
colors=[ICE,BUS,PHEV,"#E8DFE4","#E8EDF0"]
ax.imshow(mat,aspect="auto",cmap=ListedColormap(colors),norm=BoundaryNorm(np.arange(-.5,5.5),5))
for (i,j),c in codes.items():ax.text(j,i,c,ha="center",va="center",fontsize=8.5,color="white" if mat[i,j]==0 else DARK)
ax.set_xticks(range(8),[v.replace("private_","Car ").replace("bus_","Bus ").replace("_"," ") for v in vehicles],rotation=48,ha="right")
ax.set_yticks(range(16),[s.replace("_"," ") for s in stages]);ax.tick_params(length=0)
ax.set_xticks(np.arange(-.5,8,1),minor=True);ax.set_yticks(np.arange(-.5,16,1),minor=True);ax.grid(which="minor",color="white",lw=.8)
save(f,"A05_Coverage","R9_7FIX_STAGE_COVERAGE.csv","128 actual ledger cells. I aggregate production; I* selected consumable replacements already in aggregate; W joint WTW; A allocated proxy; P supplementary proxy; C conditional service; L separate LCIA; H historical physical; NA unidentified; — not applicable. Cell counts do not measure impact coverage.")
for name,header,rows in [("MANIFEST.csv",["svg","png","pdf","domain","source","caption"],manifest),("LAYOUT_QA.csv",["figure","native_width_cm","min_font_pt","out_of_canvas_text_count","text_outside","visual_gate"],qa)]:
    with (F/name).open("w",encoding="utf-8",newline="") as o:
        w=csv.writer(o,lineterminator="\n");w.writerow(header);w.writerows(rows)
print("Generated",len(manifest),"SVG/PNG/PDF triples; human visual approval remains separate.")
