"""Publication figures. Read live repository CSVs; never mix contest and retrospective ledgers."""
import csv, math, re, hashlib
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Patch
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.ticker import MaxNLocator
R=Path(__file__).resolve().parents[1]; D=R/"02_Cleaned_Data"; L=R/"07_LCA_LCIA"; P=R/"09_Paper_Draft"
F=P/"figures_final"; H=P/"figures_diagnostic"
for p in (F,H): p.mkdir(exist_ok=True)
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":9,"axes.labelsize":9,"axes.titlesize":10,"axes.titleweight":"semibold","legend.fontsize":8,"xtick.labelsize":8,"ytick.labelsize":8,"axes.spines.top":False,"axes.spines.right":False,"axes.edgecolor":"#687987","axes.labelcolor":"#263849","xtick.color":"#263849","ytick.color":"#263849","text.color":"#263849","axes.grid":False,"figure.facecolor":"white","axes.facecolor":"white","savefig.facecolor":"white","svg.fonttype":"none","hatch.linewidth":0.65})
ICE="#496783"; NMC="#C56D88"; LFP="#82ADD0"; PHEV="#9B8AB8"; BUS="#D3A16F"; DARK="#283E50"
C={"ICEV":ICE,"BEV_NMC":NMC,"BEV_LFP":LFP,"BEV":LFP,"PHEV":PHEV,"bus_diesel":BUS,"bus_assumed_BEV":"#4C988C","bus_natural_gas":"#B1A580","bus_unassigned_nonBEV":"#9095A5","bus_unclassified":"#B7BEC5"}
VLAB={"ICEV":"ICEV","BEV":"BEV","PHEV":"PHEV","BEV_NMC":"BEV-NMC","BEV_LFP":"BEV-LFP","bus_diesel":"Diesel bus","bus_assumed_BEV":"Assumed BEV bus","bus_natural_gas":"Gas bus","bus_unassigned_nonBEV":"Mixed bus","bus_unclassified":"Unknown bus"}
SS=["S-1","S0","S1","S2","S3","S4"]; SL=["S−1",*SS[1:]]; xx=np.arange(6)
manifest=[]
def read(folder,name):
    with (folder/name).open(encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))
def val(r,k):
    x=r[k].strip()
    return float(x) if x not in ("NA","","N/A") else np.nan
def get(rows,**kw): return next(r for r in rows if all(r[k]==v for k,v in kw.items()))
def nums(rows,key): return np.array([val(r,key) for r in rows])
def fig(size=(7.2,3.5),nrows=1,ncols=1,**kw): return plt.subplots(nrows,ncols,figsize=size,layout="constrained",**kw)
def axis(ax,yl=None,xl=None):
    if yl: ax.set_ylabel(yl)
    if xl: ax.set_xlabel(xl)
    ax.grid(axis="y",color="#D9E1E8",lw=.55); ax.set_axisbelow(True)
def scenarios(ax):
    ax.set_xticks(xx,SL); ax.set_xlim(-.55,5.55)
def legend(ax,**kw): ax.legend(frameon=False,**kw)
def save(f,folder,name,source,caption):
    for ext in ("svg","png"):
        path=folder/(name+"."+ext)
        f.savefig(path,dpi=240 if ext=="png" else 96,metadata={"Date":None} if ext=="svg" else None)
    plt.close(f)
    manifest.append([folder.name+"/"+name+".svg",folder.name+"/"+name+".png","contest" if folder==F else "retrospective_diagnostic",source,caption])
def block(ax,x,y,w,h,heading,body,color):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.012,rounding_size=0.022",facecolor=color,edgecolor=DARK,linewidth=.8))
    ax.text(x+w/2,y+h*.72,heading,ha="center",va="center",weight="bold",fontsize=9)
    ax.text(x+w/2,y+h*.32,body,ha="center",va="center",fontsize=8,linespacing=1.35)
def arrow(ax,x,y,x2,y2):
    ax.annotate("",xy=(x2,y2),xytext=(x,y),arrowprops=dict(arrowstyle="-|>",lw=1.15,color=DARK))
def common(ax): ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis("off")
def series(ax,x,y,vehicle):
    sty={"ICEV":("-", "s"),"BEV_NMC":("-", "o"),"BEV_LFP":("--","^")}
    ls,mark=sty[vehicle]; ax.plot(x,y,ls=ls,marker=mark,ms=4,lw=1.9,color=C[vehicle],markeredgecolor=DARK,markeredgewidth=.45,label=VLAB[vehicle])
def diffpanel(ax,x,delta,xlabel):
    ax.bar(x,delta,color=LFP,edgecolor=ICE,width=(min(np.diff(x))*.38 if len(x)>1 else .1))
    ax.set_ylim(0,max(delta)*1.45);ax.set_ylabel("LFP − NMC\n(g CO₂e/km)");ax.set_xlabel(xlabel);axis(ax)
    for xi,yi in zip(x,delta):ax.text(xi,yi+.04*max(delta),f"{yi:.2f}",ha="center",fontsize=8)
    ax.set_title("Difference (separate scale)",loc="left")

# Contest-facing figures: 2022 activity + pre-contest factors.
a=read(D,"R9_7A_SIX_SCENARIO_VKT.csv"); a0=get(a,scenario="S0")
e=[r for r in read(D,"R9_7B_SIX_SCENARIO_ENERGY_WTW.csv") if r["case"]=="base"]
m=read(D,"R9_7C_PARTIAL_LCA_GWP_SCENARIOS.csv")
q=read(D,"R9_7E_ENVIRONMENTAL_MATRIX.csv"); q0=get(q,scenario="S0")
p=[r for r in read(D,"R9_7E_ROAD_POLLUTANT_SCENARIOS.csv") if r["case"]=="V_reference"]
d=read(D,"R9_7D_SERVICE_SENSITIVITY.csv")
n=read(D,"R9_7F_NESTED_ENVELOPE.csv")
t=read(D,"R9_7F_TRANSFER_GRID.csv")
params={r["parameter"]:val(r,"value") for r in read(D,"R9_7B_ENERGY_INPUTS.csv")}
prod=read(D,"R9_7C_MANUFACTURING_FACTOR_REGISTER.csv")
# Figure 1: model flow
f,ax=fig((7.2,3.6));common(ax)
block(ax,.04,.71,.27,.21,"Reference evidence","Population · stock\nTravel · energy", "#E8EFF5")
block(ax,.365,.71,.27,.21,"Activity model","1 million residents\nVKT by mode", "#E8EFF5")
block(ax,.69,.71,.27,.21,"Six scenarios","Propulsion allocation\nFixed mode VKT", "#E8EFF5")
arrow(ax,.31,.815,.365,.815);arrow(ax,.635,.815,.69,.815)
block(ax,.04,.39,.27,.21,"Production + WTW","Annualized GWP\nFinal energy", "#DDEBF5")
block(ax,.365,.39,.27,.21,"Road exhaust","Five pollutant masses\nSeparate units", "#F4E4E8")
block(ax,.69,.39,.27,.21,"Passenger service","Conditional PKM\nEqual-service test", "#E8E3F0")
arrow(ax,.825,.71,.825,.60);arrow(ax,.825,.675,.50,.60);arrow(ax,.825,.675,.175,.60)
block(ax,.16,.065,.68,.20,"Decision and robustness","Paired S0 comparison · transfer stress · lifetime and grid thresholds", "#EDF0F3")
for x in (.175,.5,.825):arrow(ax,x,.39,.5,.265)
save(f,F,"Figure_01_Framework","Q5 manuscript model equations","Model structure; data anchor is not target geography.")
# Figure 2: boundary
f,ax=fig((7.2,3.0));common(ax)
block(ax,.035,.59,.26,.25,"Production","Materials, assembly\nInitial traction battery", "#DDEBF5")
block(ax,.37,.59,.26,.25,"Operation (WTW)","Fuel / electricity chain\nVehicle operation", "#DDEBF5")
block(ax,.705,.59,.26,.25,"Road exhaust","CO, VOCs, NOx,\nPM₂.₅ and PM₁₀", "#F4E4E8")
arrow(ax,.295,.715,.37,.715);arrow(ax,.63,.715,.705,.715)
ax.text(.5,.48,"Included-stage climate GWP     |     Road exhaust reported separately",ha="center",fontsize=9,weight="bold")
block(ax,.035,.13,.43,.24,"Unquantified in main totals","Maintenance · end-of-life\nInfrastructure · non-exhaust", "#F1F2F4")
block(ax,.535,.13,.43,.24,"Separate battery LCIA","Do not add to vehicle GWP\nDo not sum impact categories", "#E8E3F0")
save(f,F,"Figure_02_System_Boundary","R9.7C/E scope; R9.4 battery domain","Included and missing stages; no double counting.")
# Figure 3: mode/stage bars
f,axs=fig((7.2,3.5),1,2)
for ax,k,title in zip(axs,["private","bus"],["(a) Private cars","(b) Buses"]):
    w=nums(e,k+"_WTW_tCO2e")/1000; u=nums(m,"private_vehicle_production_GWP_t_y" if k=="private" else "bus_manufacturing_GWP_t_y")/1000
    ax.bar(xx,w,color=ICE,label="WTW operation");ax.bar(xx,u,bottom=w,color=LFP,edgecolor=ICE,linewidth=.45,hatch="//",label="Production")
    ax.set_ylim(0,max(w+u)*1.18);scenarios(ax);axis(ax,"GWP (kt CO₂e/year)");ax.set_title(title,loc="left")
    for j,z in enumerate(w+u):ax.text(j,z+max(w+u)*.018,f"{z:.1f}",ha="center",fontsize=7)
    legend(ax,loc="upper right")
save(f,F,"Figure_03_Scenario_GWP","R9_7B_SIX_SCENARIO_ENERGY_WTW.csv; R9_7C_PARTIAL_LCA_GWP_SCENARIOS.csv","2022 activity anchor; annual production plus WTW, separate scales by mode.")
# Figure 4: road pollutant small multiples
f,axs=fig((7.2,6.0),3,2); labels=["CO","VOCs","NOx","PM2_5","PM10"]
for ax,k,lab in zip(axs.flat,labels,["CO","VOCs","NOₓ","PM₂.₅","PM₁₀"]):
    r=[get(p,scenario=s,pollutant=k) for s in SS]; c=nums(r,"private_t_y");b=nums(r,"bus_t_y")
    ax.bar(xx,c,color=ICE,label="Cars");ax.bar(xx,b,bottom=c,color=BUS,edgecolor=DARK,lw=.35,hatch="//",label="Buses")
    scenarios(ax);axis(ax,"t/year");ax.set_title(lab,loc="left");ax.set_ylim(0,max(c+b)*1.13)
axs.flat[5].axis("off");axs.flat[5].legend(handles=[Patch(color=ICE,label="Private cars"),Patch(facecolor=BUS,edgecolor=DARK,hatch="//",label="Buses")],loc="center",frameon=False)
axs.flat[5].text(.5,.22,"Combustion exhaust only\nIndependent panel scales",ha="center",va="center",transform=axs.flat[5].transAxes,fontsize=8)
save(f,F,"Figure_04_Road_Exhaust","R9_7E_ROAD_POLLUTANT_SCENARIOS.csv","China V illustrative reference; modeled exhaust only.")
# Figure 5: paired reduction envelopes
f,ax=fig((7.2,3.2)); rows=[get(n,scenario=s,indicator="partial_GWP_t") for s in SS]; lo=nums(rows,"min_reduction_pct");hi=nums(rows,"max_reduction_pct");z=val(q0,"partial_GWP_kt_y");ref=100*(1-nums(q,"partial_GWP_kt_y")/z)
ax.axvline(0,color=DARK,ls="--",lw=1,label="No change")
ax.hlines(xx,lo,hi,color=ICE,lw=4,label="Stress envelope");ax.scatter(ref,xx,color=NMC,edgecolor=DARK,zorder=3,s=35,label="Reference")
ax.set_yticks(xx,SL);ax.invert_yaxis();ax.set_xlabel("Reduction relative to paired S0 (%)");ax.grid(axis="x",color="#D9E1E8",lw=.6);ax.set_axisbelow(True);legend(ax,loc="lower right")
save(f,F,"Figure_05_Paired_Sensitivity","R9_7F_NESTED_ENVELOPE.csv; R9_7E_ENVIRONMENTAL_MATRIX.csv","14,580 design combinations; not a confidence interval.")
# Figure 6: conditional PKM and equal-service stress
f,axs=fig((7.2,3.6),1,2,gridspec_kw={"width_ratios":[1.55,1]});r=[get(d,case="reference",scenario=s) for s in SS]
axs[0].bar(xx-.18,nums(r,"car_partial_GWP_g_per_PKM"),.36,color=ICE,label="Private cars");axs[0].bar(xx+.18,nums(r,"bus_partial_GWP_g_per_PKM"),.36,color=BUS,edgecolor=DARK,hatch="//",lw=.4,label="Buses")
scenarios(axs[0]);axis(axs[0],"GWP (g CO₂e/PKM)");axs[0].set_title("(a) Conditional service intensity",loc="left");legend(axs[0],loc="upper right")
oc=[get(d,case=c,scenario="S3") for c in ["BEV_lower","reference","BEV_higher"]]; y=nums(oc,"equal_service_partial_GWP_tCO2e")/1000
axs[1].bar(np.arange(3),y,color=[NMC,LFP,"#4C988C"],edgecolor=DARK,lw=.5);axs[1].axhline(z,color=DARK,ls="--",lw=1,label="Paired S0");axs[1].set_xticks(range(3),["Lower","Reference","Higher"],rotation=15);axis(axs[1],"S3 GWP (kt CO₂e/year)");axs[1].set_title("(b) Equal-service stress",loc="left");legend(axs[1],loc="lower right")
save(f,F,"Figure_06_Passenger_Service","R9_7D_SERVICE_SENSITIVITY.csv","Historical occupancy and distance proxies, not observed PKM.")
# Figure 7: transfer
f,axs=fig((7.2,2.9),1,3); levels=[.8,1.,1.2]; tr=[r for r in t if r["scenario"]=="S3"]; vv=nums(tr,"reduction_vs_paired_S0_pct"); vmin,vmax=min(vv),max(vv)
for ax,b in zip(axs,levels):
    mat=np.array([[next(val(r,"reduction_vs_paired_S0_pct") for r in tr if np.allclose([val(r,k) for k in ["g_ownership","m_mileage","b_bus_supply"]],[g,mm,b])) for mm in levels] for g in levels])
    im=ax.imshow(mat,vmin=vmin,vmax=vmax,cmap="Blues",aspect="equal")
    for i,j in np.ndindex(mat.shape):ax.text(j,i,f"{mat[i,j]:.2f}",ha="center",va="center",fontsize=8,color="white" if mat[i,j]>(vmin+vmax)/2 else DARK)
    ax.set_xticks(range(3),["0.8","1.0","1.2"]);ax.set_yticks(range(3),["0.8","1.0","1.2"]);ax.set_xlabel("Mileage m");ax.set_title(f"Bus supply b = {b:.1f}")
axs[0].set_ylabel("Ownership g");f.colorbar(im,ax=axs,label="S3 reduction (%)",shrink=.8)
save(f,F,"Figure_07_Transfer_Grid","R9_7F_TRANSFER_GRID.csv","27 transfer combinations; common color scale; no Jinhua observation.")
# Figure 8: current threshold
f,ax=fig((7.2,3.25)); ll=np.linspace(100000,300000,100)
mi=val(get(prod,source_id="QIAO17_ICE"),"factor_value")*1000;mb=val(get(prod,source_id="QIAO17_BEV_NMC"),"factor_value")*1000
ue=params["car_e"];ug=params["gasoline_l100"]/100*params["gasoline_mj_l"]*params["gasoline_ef"]/1000;yy=((mi-mb)/ll+ug)/ue
ax.plot(ll/1000,yy,color=NMC,lw=2.4,label="BEV-NMC break-even");ax.axhline(params["grid_ef"],color=ICE,ls="--",lw=1.4,label="Peng Table 8 WTW");ax.axhline(params["grid_ef"]*.5,color=PHEV,ls=":",lw=1.5,label="S4 policy stress")
ax.scatter([150],[((mi-mb)/150000+ug)/ue],color=NMC,edgecolor=DARK,zorder=3);axis(ax,"Electricity factor (kg CO₂e/kWh)","Lifetime distance (thousand km)");ax.set_ylim(0,max(yy)*1.16);legend(ax,loc="lower right")
save(f,F,"Figure_08_BreakEven","R9_7B_ENERGY_INPUTS.csv; R9_7C_MANUFACTURING_FACTOR_REGISTER.csv","Current contest model; threshold derived from production + WTW, not old 0.160 kWh/km.")
# Figure 9: activity allocation (shares, separate totals)
f,axs=fig((7.2,3.0),1,2)
for ax,keys,names,colors,total,title in [(axs[0],["private_ICEV_vkt_km","private_BEV_vkt_km","private_PHEV_vkt_km"],["ICEV","BEV","PHEV"],[ICE,LFP,PHEV],"private_total_vkt_km","(a) Private cars"),(axs[1],["bus_diesel_vkt_km","bus_natural_gas_vkt_km","bus_mixed_nonBEV_vkt_km","bus_BEV_vkt_km","bus_unclassified_vkt_km"],["Diesel","Gas","Mixed non-BEV","BEV","Unknown"],[ICE,BUS,PHEV,LFP,"#B7BEC5"],"bus_total_vkt_km","(b) Buses")]:
    btm=np.zeros(6);den=nums(a,total)
    for k,lab,col in zip(keys,names,colors):
        v=nums(a,k)/den*100;ax.bar(xx,v,bottom=btm,color=col,edgecolor="white",lw=.4,label=lab);btm+=v
    assert np.allclose(btm,100);scenarios(ax);ax.set_ylim(0,100);axis(ax,"Share of mode VKT (%)");ax.set_title(title,loc="left");legend(ax,loc="upper center",bbox_to_anchor=(.5,-.12),ncol=2)
save(f,F,"Figure_09_Activity_Allocation","R9_7A_SIX_SCENARIO_VKT.csv","All shares are conditional allocations; mode VKT fixed.")
# Figure 10: energy by carrier in common unit
f,ax=fig((7.2,3.3));b=np.zeros(6)
for lab,v,col in [("Gasoline",nums(e,"gasoline_L")*params["gasoline_mj_l"]/1e9,ICE),("Diesel",nums(e,"diesel_MJ")/1e9,"#6E859B"),("Natural gas",nums(e,"natural_gas_MJ")/1e9,BUS),("Car electricity",nums(e,"private_electricity_kWh")*3.6/1e9,LFP),("Bus electricity",nums(e,"bus_electricity_kWh")*3.6/1e9,NMC)]:
    ax.bar(xx,v,bottom=b,color=col,edgecolor="white",lw=.4,label=lab);b+=v
assert np.allclose(b,nums(e,"final_energy_MJ")/1e9)
scenarios(ax);axis(ax,"Final energy (PJ/year)");legend(ax,loc="upper right",ncol=2);ax.set_ylim(0,max(b)*1.15)
save(f,F,"Figure_10_Energy_Structure","R9_7B_SIX_SCENARIO_ENERGY_WTW.csv; R9_7B_ENERGY_INPUTS.csv","Annual final energy converted to PJ; no primary-energy aggregation.")
# Figure 11: charging boundary
f,ax=fig((7.2,2.6));common(ax)
block(ax,.04,.56,.25,.25,"Grid input","Electricity WTW factor\nQgrid", "#DDEBF5");block(ax,.375,.56,.25,.25,"Charging equipment","Losses if not already\nincluded in meter", "#F1F2F4");block(ax,.71,.56,.25,.25,"Vehicle battery","Recorded energy may\nbe here or upstream", "#DDEBF5")
arrow(ax,.29,.685,.375,.685);arrow(ax,.625,.685,.71,.685)
ax.text(.5,.39,"Base: use reported charging energy as delivered; meter location unspecified",ha="center",weight="bold",fontsize=8.5)
ax.text(.5,.21,"Alternative only: Qgrid = Qreported / η,  η = 0.90, 0.92 or 0.95",ha="center",fontsize=9)
ax.text(.5,.09,"Never apply charging losses twice.",ha="center",fontsize=8,color=ICE)
save(f,F,"Figure_11_Charging_Boundary","R9_7B_ENERGY_INPUTS.csv; energy cases","Measurement boundary schematic; no measured loss factor.")

# Diagnostic appendix: historical R9.4/R9.5 results; never import into contest results.
stage=read(L,"R9_4_PHYSICAL_STAGE_SUBTOTALS.csv"); vs=["ICEV","BEV","PHEV","bus_diesel","bus_assumed_BEV"]
stages=["material_production_major_materials","parts_manufacturing","vehicle_distribution","maintenance_replacements","end_of_life_dismantling_energy","energy_supply_and_vehicle_use_WTW"]
stnames=["Materials","Parts","Distribution","Maintenance","End-of-life","Energy WTW"];stcols=["#8DB6D8","#5C8DB6","#CCD6E0","#E6A7B7","#C87892","#4E6D8A"]; hatches=["","//","..","xx","\\\\",""]
def stageval(v,k):
    rows=[r for r in stage if r["vehicle"]==v and r["stage"]==k and r["flow"]=="CO2"]
    return val(rows[0],"kg_per_vehicle_km")*1000 if rows else np.nan
f,axs=fig((7.2,4.4),1,2,gridspec_kw={"width_ratios":[1,1]});y=np.arange(len(vs))
for ax,idx,title in [(axs[0],range(6),"(a) All quantified stages"),(axs[1],range(5),"(b) Non-energy stages")]:
    left=np.zeros(len(vs))
    for j in idx:
        data=np.array([stageval(v,stages[j]) for v in vs]);known=np.isfinite(data)
        ax.barh(y[known],data[known],left=left[known],color=stcols[j],edgecolor="white",lw=.5,hatch=hatches[j],label=stnames[j])
        left[known]+=data[known]
    ax.set_yticks(y,[VLAB[v] for v in vs]);ax.invert_yaxis();ax.set_xlabel("Known CO₂ (g/vehicle-km)");ax.set_title(title,loc="left");ax.grid(axis="x",color="#D9E1E8",lw=.5);ax.set_axisbelow(True)
    for i,v in enumerate(vs):
        missing=sum(not np.isfinite(stageval(v,stages[j])) for j in idx)
        if missing: ax.text(left[i]+max(left.max(),1)*.02,i,f"{missing} NA",va="center",fontsize=7,color=DARK)
    ax.set_xlim(0,max(left.max(),1)*1.30)
axs[0].legend(loc="upper center",bbox_to_anchor=(.5,-.16),ncol=2,frameon=False)
save(f,H,"Legacy_03_Physical_CO2","R9_4_PHYSICAL_STAGE_SUBTOTALS.csv","Retrospective known-flow subtotals, not full physical inventory; NA counts shown, separate scales.")
# Legacy 5 grid comparison, difference panel
g=read(L,"R9_5_GRID_FACTOR_SENSITIVITY.csv");gr=sorted({val(r,"factor_kg_per_kWh") for r in g if r["eligible_for_strict_comparison"]=="YES"})
f,axs=fig((7.2,3.15),1,2,gridspec_kw={"width_ratios":[1.5,1]})
curves={}
for v in ["BEV_NMC","BEV_LFP"]:
    yy=np.array([next(val(r,"combined_screening_g_per_km") for r in g if r["vehicle"]==v and val(r,"factor_kg_per_kWh")==x and r["eligible_for_strict_comparison"]=="YES") for x in gr]);curves[v]=yy;series(axs[0],gr,yy,v)
axs[0].set_ylim(0,max(curves["BEV_LFP"])*1.15);axis(axs[0],"Two-stage GWP (g CO₂e/km)","Electricity WTW (kg CO₂e/kWh)");axs[0].set_title("(a) Technology comparison",loc="left");legend(axs[0],loc="lower right")
diffpanel(axs[1],np.array(gr),curves["BEV_LFP"]-curves["BEV_NMC"],"Electricity WTW (kg CO₂e/kWh)")
save(f,H,"Legacy_05_Grid_Sensitivity","R9_5_GRID_FACTOR_SENSITIVITY.csv","Historical 0.160 kWh/km model; separate LFP–NMC difference.")
# Legacy 6 lifetime
life=read(L,"R9_5_LIFETIME_SENSITIVITY.csv");ls=sorted({val(r,"lifetime_km")/1000 for r in life})
f,axs=fig((7.2,3.15),1,2,gridspec_kw={"width_ratios":[1.5,1]});curves={}
for v in ["ICEV","BEV_NMC","BEV_LFP"]:
    yy=np.array([next(val(r,"two_stage_gCO2e_per_km") for r in life if r["vehicle"]==v and val(r,"lifetime_km")/1000==x) for x in ls]);curves[v]=yy;series(axs[0],ls,yy,v)
axs[0].set_ylim(0,max(curves["ICEV"])*1.15);axis(axs[0],"Two-stage GWP (g CO₂e/km)","Lifetime distance (thousand km)");axs[0].set_title("(a) Technology comparison",loc="left");legend(axs[0],loc="upper right")
diffpanel(axs[1],np.array(ls),curves["BEV_LFP"]-curves["BEV_NMC"],"Lifetime distance (thousand km)")
save(f,H,"Legacy_06_Lifetime_Sensitivity","R9_5_LIFETIME_SENSITIVITY.csv","Retrospective energy intensity; separate chemistry difference.")
# Legacy 7 threshold range band
be=read(L,"R9_5_BREAK_EVEN_GRID_FACTOR.csv");ls=sorted({val(r,"lifetime_km")/1000 for r in be})
nc=np.array([next(val(r,"break_even_grid_EF_kgCO2e_per_kWh") for r in be if r["vehicle"]=="BEV_NMC" and val(r,"lifetime_km")/1000==x) for x in ls]);lc=np.array([next(val(r,"break_even_grid_EF_kgCO2e_per_kWh") for r in be if r["vehicle"]=="BEV_LFP" and val(r,"lifetime_km")/1000==x) for x in ls])
f,ax=fig((7.2,3.2));ax.fill_between(ls,np.minimum(nc,lc),np.maximum(nc,lc),color="#D8C5DD",label="NMC–LFP threshold band");ax.plot(ls,(nc+lc)/2,color=NMC,lw=2,label="Midpoint (display only)")
ax.axhline(val(be[0],"Peng2017_Table8_grid_EF_kgCO2e_per_kWh"),color=ICE,ls="--",label="Peng 2017 WTW");mee=next(val(r,"factor_kg_per_kWh") for r in g if r["scenario"]=="MEE2023_national_PCF");ax.axhline(mee,color=PHEV,ls=":",lw=1.8,label="MEE retrospective PCF")
ax.set_ylim(0,max(nc)*1.12);axis(ax,"Electricity factor (kg CO₂e/kWh)","Lifetime distance (thousand km)");legend(ax,loc="lower right",ncol=2)
save(f,H,"Legacy_07_BreakEven","R9_5_BREAK_EVEN_GRID_FACTOR.csv; R9_5_GRID_FACTOR_SENSITIVITY.csv","Historical threshold envelope; MEE reference is retrospective and methodologically different.")
# Legacy 8 independent battery sensitivity
bat=read(L,"R9_5_BATTERY_FACTOR_SENSITIVITY.csv");f,axs=fig((7.2,3.4),1,2)
for ax,v in zip(axs,["BEV","PHEV"]):
    r=[x for x in bat if x["vehicle"]==v and val(x,"battery_service_lifetime_km")==150000]
    groups={}
    for z in r:groups.setdefault(z["factor_boundary"],[]).append(z)
    for j,(k,z) in enumerate(groups.items()):
        ax.scatter(nums(z,"battery_factor_kgCO2e_per_kWh"),nums(z,"battery_only_gCO2e_per_vehicle_km"),c=[ICE,NMC,PHEV,BUS][j%4],marker=["o","^","s","D"][j%4],s=26,label=("Recycling net" if "recycl" in k.lower() and "no_recycl" not in k.lower() else "Production" if "production" in k.lower() else k.replace("_"," ")),edgecolor=DARK,lw=.35)
    axis(ax,"Battery-only GWP (g CO₂e/km)","Factor (kg CO₂e/kWh)");ax.set_title(v,loc="left");ax.set_ylim(bottom=0);legend(ax,loc="upper left",fontsize=7)
save(f,H,"Legacy_08_Battery_Factors","R9_5_BATTERY_FACTOR_SENSITIVITY.csv","Independent battery module, 150,000-km service life; not added to whole vehicle production.")
# Legacy 9 coverage matrix, map historical subtypes to one visibly distinct group
cov=read(L,"R9_4_STAGE_COVERAGE_MATRIX.csv");v=list(dict.fromkeys(r["vehicle"] for r in cov));st=list(dict.fromkeys(r["stage"] for r in cov))
status=lambda s: 0 if s=="MISSING" else 1 if s=="PARTIAL_PHYSICAL" else 2 if s=="SEPARATE_LCIA_ONLY" else 3 if s.startswith("NOT_APPLICABLE") else 4
mat=np.array([[status(get(cov,vehicle=x,stage=y)["coverage_status"]) for y in st] for x in v]);colors=["#E6E8EB","#82ADD0","#C56D88","#FFFFFF","#D3A16F"];f,ax=fig((7.2,4.3));ax.imshow(mat,cmap=ListedColormap(colors),norm=BoundaryNorm(np.arange(-.5,5.5),5),aspect="auto")
for i,j in np.ndindex(mat.shape):ax.text(j,i,["—","P","L","N/A","H"][mat[i,j]],ha="center",va="center",fontsize=7,color=DARK)
ax.set_xticks(range(len(st)),["Materials","Parts","Distribution","Assembly","Battery","Energy","Maintenance","Dismantling","Recycling","Non-exhaust","PKM"],rotation=45,ha="right");ax.set_yticks(range(len(v)),[VLAB[x] for x in v]);ax.set_xticks(np.arange(-.5,len(st),1),minor=True);ax.set_yticks(np.arange(-.5,len(v),1),minor=True);ax.grid(which="minor",color="white",lw=1);ax.tick_params(which="minor",bottom=False,left=False)
ax.legend(handles=[Patch(facecolor=c,edgecolor="#ADB7C2",label=l) for c,l in zip(colors,["Missing","Partial physical","Separate LCIA","Not applicable","Historical proxy"])],loc="upper center",bbox_to_anchor=(.5,-.34),ncol=3,frameon=False)
save(f,H,"Legacy_09_Coverage","R9_4_STAGE_COVERAGE_MATRIX.csv","Historical 88-cell coverage; H groups historical evidence statuses, not complete LCA.")
# Legacy 10 multi-pollutant
r=read(L,"R9_4_PHYSICAL_VEHICLE_PARTIAL_SUBTOTALS.csv");v=list(dict.fromkeys(x["vehicle"] for x in r))
f,axs=fig((7.2,7.8),3,2)
for ax,k in zip(axs.flat,["CO2","VOC","NOx","PM2.5","SO2"]):
    z=np.array([val(get(r,vehicle=x,flow=k),"kg_per_vehicle_km")*1000 for x in v]);known=np.isfinite(z);i=np.arange(len(v));ax.barh(i[known],z[known],color=[C[x] for x,ok in zip(v,known) if ok],edgecolor=DARK,lw=.35);ax.set_yticks(i,[VLAB[x] for x in v],fontsize=7);ax.invert_yaxis();ax.set_xlim(0,max(z[known])*1.16)
    for j in i[~known]:ax.text(0,j,"NA",va="center",ha="left",fontsize=7,color="#687987")
    ax.set_title(k,loc="left");ax.set_xlabel("Known mass (g/vehicle-km)");ax.grid(axis="x",color="#D9E1E8",lw=.5);ax.set_axisbelow(True)
axs.flat[5].axis("off");axs.flat[5].text(.5,.5,"Known-flow subtotals\nDifferent stage coverage\nNo full-LCA ranking",ha="center",va="center",fontsize=9,transform=axs.flat[5].transAxes)
save(f,H,"Legacy_10_Multi_Pollutant","R9_4_PHYSICAL_VEHICLE_PARTIAL_SUBTOTALS.csv","Five independent pollutant panels; NA not zero.")
# Legacy 11 grid-lifetime heatmap
gl=read(L,"R9_5_GRID_LIFETIME_FACTORIAL.csv");gx=sorted({val(r,"grid_EF_kgCO2e_per_kWh") for r in gl});lx=sorted({val(r,"lifetime_km")/1000 for r in gl});z=nums(gl,"two_stage_gCO2e_per_km")
f,axs=fig((7.2,3.0),1,3)
for ax,v in zip(axs,["ICEV","BEV_NMC","BEV_LFP"]):
    mat=np.array([[next(val(r,"two_stage_gCO2e_per_km") for r in gl if r["vehicle"]==v and val(r,"grid_EF_kgCO2e_per_kWh")==g0 and val(r,"lifetime_km")/1000==l0) for l0 in lx] for g0 in gx])
    im=ax.imshow(mat,cmap="Blues",vmin=min(z),vmax=max(z),aspect="auto")
    for i,j in np.ndindex(mat.shape):ax.text(j,i,f"{mat[i,j]:.1f}",ha="center",va="center",fontsize=8,color="white" if mat[i,j]>(min(z)+max(z))/2 else DARK)
    ax.set_xticks(range(len(lx)),[f"{x:g}" for x in lx]);ax.set_yticks(range(len(gx)),[f"{x:.4f}" for x in gx]);ax.set_xlabel("Lifetime (1000 km)");ax.set_title(VLAB[v])
axs[0].set_ylabel("Grid WTW (kg CO₂e/kWh)");f.colorbar(im,ax=axs,label="GWP (g CO₂e/km)",shrink=.8)
save(f,H,"Legacy_11_Grid_Lifetime","R9_5_GRID_LIFETIME_FACTORIAL.csv","Historical joint sensitivity; one common color scale.")
# Legacy 12 relative battery ReCiPe
rec=read(L,"R9_4_BATTERY_RECIPE_ONLY.csv");cats=list(dict.fromkeys(r["impact_category"] for r in rec));mat=[]
for k in cats:
    row=[]
    for v in ["BEV","PHEV"]:
        x=val(get(rec,vehicle=v,impact_category=k,scenario="cradle_to_gate_no_recycling_credit"),"annual_characterized_amount");y=val(get(rec,vehicle=v,impact_category=k,scenario="hypothetical_100pct_hydromet_recycling"),"annual_characterized_amount");row.append(100*(y/x-1) if x else np.nan)
    mat.append(row)
mat=np.array(mat);f,ax=fig((7.2,4.0));lim=max(np.nanmax(abs(mat)),1);im=ax.imshow(mat,cmap="RdBu_r",vmin=-lim,vmax=lim,aspect="auto")
for i,j in np.ndindex(mat.shape):ax.text(j,i,"NA" if np.isnan(mat[i,j]) else f"{mat[i,j]:+.1f}%",ha="center",va="center",fontsize=8,color="white" if np.isfinite(mat[i,j]) and abs(mat[i,j])>.6*lim else DARK)
ax.set_yticks(range(len(cats)),[x.replace("_"," ") for x in cats]);ax.set_xticks([0,1],["BEV","PHEV"]);f.colorbar(im,ax=ax,label="Change vs no recycling (%)")
save(f,H,"Legacy_12_Battery_ReCiPe","R9_4_BATTERY_RECIPE_ONLY.csv","Battery-only hypothetical 100% hydrometallurgical recycling; relative within category, never summed.")
with (P/"FINAL_FIGURE_MANIFEST.csv").open("w",encoding="utf-8",newline="") as f:
    w=csv.writer(f,lineterminator="\n");w.writerow(["svg","png","domain","source","caption"]);w.writerows(manifest)
assert len(manifest)==20
print("Generated",len(manifest),"SVG/PNG pairs from current CSV")
