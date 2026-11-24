"""R9.7E road-exhaust screening; separate physical masses from GWP."""
import csv, math
from pathlib import Path
D=Path(__file__).resolve().parents[1]/"02_Cleaned_Data"
def read(n):
    with (D/n).open(encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))
def write(n,h,rows):
    with (D/n).open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f,lineterminator="\n");w.writerow(h.split(","));w.writerows([[f"{x:.9f}" if isinstance(x,(float,int)) else x for x in r] for r in rows])
a=read("R9_7A_SIX_SCENARIO_VKT.csv")
e={r["scenario"]:r for r in read("R9_7B_SIX_SCENARIO_ENERGY_WTW.csv") if r["case"]=="base"}
m={r["scenario"]:r for r in read("R9_7C_PARTIAL_LCA_GWP_SCENARIOS.csv")}
p={r["parameter"]:float(r["value"]) for r in read("R9_7A_CONTEST_ACTIVITY_INPUTS.csv")}
ps=["CO","VOCs","NOx","PM2_5","PM10"]
fs={(r["standard"],r["technology"]):[float(r[k]) for k in ps] for r in read("R9_7E_ROAD_FACTORS.csv")}
ud=p["bus_diesel_count"]/(p["bus_diesel_count"]+p["bus_gas_count"])
rows=[];matrix=[]
for c in read("R9_7E_ROAD_CASES.csv"):
    name,std=c["case"],c["standard"]
    uf,hm,md,mg=[float(c[k]) for k in ("phev_UF","hybrid_diesel_factor_multiplier","residual_diesel_fraction","residual_gas_fraction")]
    assert 0<=uf<=1 and 0<=md+mg<=1 and hm>=0
    f,d,g=[fs[std,k] for k in ("private_gasoline","bus_diesel","bus_natural_gas")]
    for r in a:
        s=r["scenario"]
        vi,vp,bd,bg,bh,bu=[float(r[k]) for k in ("private_ICEV_vkt_km","private_PHEV_vkt_km","bus_diesel_vkt_km","bus_natural_gas_vkt_km","bus_mixed_nonBEV_vkt_km","bus_unclassified_vkt_km")]
        dp=bd+bu*ud+bh*md;gp=bg+bu*(1-ud)+bh*mg;hp=bh*(1-md-mg)
        assert math.isclose(dp+gp+hp+float(r["bus_BEV_vkt_km"]),float(r["bus_total_vkt_km"]),abs_tol=1e-5)
        total=[]
        for j,k in enumerate(ps):
            car=(vi+vp*(1-uf))*f[j]/1e6
            bus=(dp*d[j]+gp*g[j]+hp*d[j]*hm)/1e6
            assert min(car,bus)>=0
            rows.append([name,s,k,car,bus,car+bus,"t/year","road exhaust screening"]);total.append(car+bus)
        if name=="V_reference":
            x,y=e[s],m[s]
            matrix.append([s,float(x["final_energy_MJ"])/1e9,float(x["total_WTW_tCO2e"])/1000,float(y["total_manufacturing_GWP_t_y"])/1000,float(y["partial_LCA_GWP_t_y"])/1000,*total,"NA","NA","NA"])
assert len(rows)==240 and len(matrix)==6
write("R9_7E_ROAD_POLLUTANT_SCENARIOS.csv","case,scenario,pollutant,private_t_y,bus_t_y,total_t_y,unit,boundary",rows)
write("R9_7E_ENVIRONMENTAL_MATRIX.csv","scenario,final_energy_PJ,WTW_GWP_kt_y,production_GWP_kt_y,partial_GWP_kt_y,road_CO_t_y,road_VOCs_t_y,road_NOx_t_y,road_PM2_5_t_y,road_PM10_t_y,nonexhaust_PM,full_life_cycle_GWP,full_life_cycle_pollutants",matrix)
print("PASS: 240 road pollutant rows; six matched-boundary result rows")
