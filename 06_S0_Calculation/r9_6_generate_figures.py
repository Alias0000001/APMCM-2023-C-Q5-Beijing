#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R9.6 reproducible SVG figure generator. Standard library only.

Run from any directory:
    python 06_S0_Calculation/r9_6_generate_figures.py

Every quantitative figure reads its values from the repository CSV ledgers.
No manually copied result arrays are used.
"""
from __future__ import annotations
import csv
import html
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "07_LCA_LCIA"
FIG = ROOT / "09_Paper_Draft" / "figures"
NAVY = "#172B3A"
INK = "#243B4A"
MUTED = "#647783"
GRID = "#DCE3E8"
PANEL = "#F6F8FA"
ICE = "#496783"
NMC = "#C56D88"
LFP = "#82ADD0"
PHEV = "#9B8AB8"
BUS = "#D3A16F"
BUS_E = "#4F968D"
STAGE_COLORS = {
    "material_production_major_materials": "#8DB6D8",
    "parts_manufacturing": "#5C8DB6",
    "vehicle_distribution": "#CCD6E0",
    "maintenance_replacements": "#E6A7B7",
    "end_of_life_dismantling_energy": "#C87892",
    "energy_supply_and_vehicle_use_WTW": "#4E6D8A",
}
VEHICLE_COLORS = {
    "ICEV": ICE, "BEV": NMC, "PHEV": PHEV,
    "BEV_NMC": NMC, "BEV_LFP": LFP,
    "bus_diesel": BUS, "bus_assumed_BEV": BUS_E,
    "bus_natural_gas": "#B68A56", "bus_unassigned_nonBEV": "#9AA8AE",
    "bus_unclassified": "#C6CDD2",
}
VEHICLE_LABELS = {
    "ICEV": "Private ICEV", "BEV": "Private BEV", "PHEV": "Private PHEV",
    "BEV_NMC": "BEV-NMC", "BEV_LFP": "BEV-LFP",
    "bus_diesel": "Diesel bus", "bus_assumed_BEV": "Assumed BEV bus",
    "bus_natural_gas": "Natural-gas bus",
    "bus_unassigned_nonBEV": "Unassigned mixed bus",
    "bus_unclassified": "Unclassified bus",
}

def read_csv(name):
    with (D / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def number(value):
    try:
        n = float(value)
    except (TypeError, ValueError):
        return None
    return n if math.isfinite(n) else None

def esc(value):
    return html.escape(str(value), quote=True)

def tx(x, y, value, size=16, fill=INK, anchor="start", weight=400, rotate=None):
    transform = f' transform="rotate({rotate} {x} {y})"' if rotate is not None else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial,Helvetica,sans-serif" '
            f'font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}"{transform}>{esc(value)}</text>')

def rect(x, y, w, h, fill, stroke="none", sw=1, rx=0, opacity=1):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" rx="{rx}" '
            f'opacity="{opacity}"/>')

def ln(x1, y1, x2, y2, stroke=GRID, sw=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="{sw}"{d}/>')

def circ(x, y, r, fill, stroke="white", sw=1.5):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'

def poly(points, fill="none", stroke=INK, sw=2, opacity=1, dash=None):
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{opacity}"{d}/>'

def polygon(points, fill, stroke="none", sw=1, opacity=1):
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return f'<polygon points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{opacity}"/>'

def start_svg(title, subtitle, width=1200, height=760):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}">',
        f'<title>{esc(title)}</title><desc>{esc(subtitle)}</desc>',
        rect(0, 0, width, height, "#FFFFFF"),
        tx(58, 58, title, 29, NAVY, weight=700),
        tx(60, 91, subtitle, 14, MUTED),
        ln(58, 112, width-58, 112, GRID, 1.2),
    ]

def finish_svg(parts, name):
    parts.append("</svg>")
    FIG.mkdir(parents=True, exist_ok=True)
    (FIG / name).write_text("\n".join(parts), encoding="utf-8")

def axis_y(parts, x0, x1, y0, y1, ymin, ymax, ticks, suffix="", fmt="{:.0f}"):
    for v in ticks:
        y = y0 - (v-ymin)/(ymax-ymin)*(y0-y1)
        parts.append(ln(x0, y, x1, y, GRID, 1))
        parts.append(tx(x0-12, y+5, fmt.format(v)+suffix, 12, MUTED, "end"))
    parts.append(ln(x0, y0, x1, y0, MUTED, 1.2))
    parts.append(ln(x0, y0, x0, y1, MUTED, 1.2))

def legend_item(parts, x, y, color, label, shape="rect"):
    if shape == "circle":
        parts.append(circ(x+7, y-5, 6, color))
    elif shape == "line":
        parts.append(ln(x, y-5, x+20, y-5, color, 3))
    else:
        parts.append(rect(x, y-12, 14, 14, color, rx=2))
    parts.append(tx(x+25, y, label, 13, MUTED))

def figure3():
    rows = read_csv("R9_4_PHYSICAL_STAGE_SUBTOTALS.csv")
    vehicles = ["ICEV", "BEV", "PHEV"]
    stages = list(STAGE_COLORS)
    values = {v: {s: 0.0 for s in stages} for v in vehicles}
    for r in rows:
        if r["flow"] == "CO2" and r["vehicle"] in values and r["stage"] in values[r["vehicle"]]:
            values[r["vehicle"]][r["stage"]] = (number(r["annual_known_kg"]) or 0) / 1000
    nonenergy = [s for s in stages if s != "energy_supply_and_vehicle_use_WTW"]
    totals_a = [sum(values[v].values()) for v in vehicles]
    totals_b = [sum(values[v][s] for s in nonenergy) for v in vehicles]
    max_a = max(totals_a) * 1.12
    max_b = max(totals_b) * 1.18
    p = start_svg("Figure 3. Partial physical CO₂ inventory by lifecycle stage",
                  "Two scales are shown deliberately: full known-flow inventory and a separate non-energy-stage zoom.")
    p += [tx(90, 150, "A. All known stages", 18, NAVY, weight=700),
          tx(690, 150, "B. Non-energy stages — enlarged", 18, NAVY, weight=700)]
    y0, y1 = 560, 205
    axis_y(p, 115, 585, y0, y1, 0, max_a, [0, max_a/4, max_a/2, 3*max_a/4, max_a], " t", "{:.0f}")
    axis_y(p, 710, 1170, y0, y1, 0, max_b, [0, max_b/4, max_b/2, 3*max_b/4, max_b], " t", "{:.0f}")
    for i, v in enumerate(vehicles):
        x = 180 + i*145
        y = y0
        for stage in stages:
            val = values[v][stage]
            h = val/max_a*(y0-y1)
            if h > 0.25:
                p.append(rect(x, y-h, 66, h, STAGE_COLORS[stage], stroke="white", sw=0.8))
            y -= h
        p.append(tx(x+33, y-9, f"{totals_a[i]:,.0f}", 13, NAVY, "middle", 700))
        p.append(tx(x+33, y0+26, VEHICLE_LABELS[v], 13, MUTED, "middle"))
        x2 = 775 + i*135
        y = y0
        for stage in nonenergy:
            val = values[v][stage]
            h = val/max_b*(y0-y1)
            if h > 0.25:
                p.append(rect(x2, y-h, 62, h, STAGE_COLORS[stage], stroke="white", sw=0.8))
            y -= h
        p.append(tx(x2+31, y-9, f"{totals_b[i]:,.0f}", 13, NAVY, "middle", 700))
        p.append(tx(x2+31, y0+26, VEHICLE_LABELS[v], 13, MUTED, "middle"))
    legend_x = 95
    for stage in stages:
        label = {
            "material_production_major_materials":"Materials",
            "parts_manufacturing":"Parts",
            "vehicle_distribution":"Distribution",
            "maintenance_replacements":"Maintenance",
            "end_of_life_dismantling_energy":"Dismantling",
            "energy_supply_and_vehicle_use_WTW":"Energy WTW",
        }[stage]
        legend_item(p, legend_x, 640, STAGE_COLORS[stage], label)
        legend_x += 175
    p.append(tx(60, 710, "Known-flow subtotals only; missing stages remain NA. These bars are not complete lifecycle totals.", 13, MUTED))
    finish_svg(p, "Fig_R9_4_Physical_Inventory_Stage.svg")

def figure5():
    rows = read_csv("R9_5_GRID_FACTOR_SENSITIVITY.csv")
    p = start_svg("Figure 5. Electricity-factor sensitivity",
                  "Two-stage GWP100 screening; historical China WTW factors are separated from retrospective 2023 references.")
    x0, x1, y0, y1 = 135, 1125, 425, 175
    xmin, xmax, ymin, ymax = 0.58, 0.76, 155, 200
    axis_y(p, x0, x1, y0, y1, ymin, ymax, [160,170,180,190,200], " g/km", "{:.0f}")
    for vehicle, color, shape in [("BEV_NMC", NMC, "circle"), ("BEV_LFP", LFP, "square")]:
        pts = []
        selected = sorted([r for r in rows if r["vehicle"] == vehicle], key=lambda r: float(r["factor_kg_per_kWh"]))
        for r in selected:
            ef = float(r["factor_kg_per_kWh"])
            val = float(r["combined_screening_g_per_km"])
            x = x0 + (ef-xmin)/(xmax-xmin)*(x1-x0)
            y = y0 - (val-ymin)/(ymax-ymin)*(y0-y1)
            pts.append((x,y))
        p.append(poly(pts, stroke=color, sw=3))
        for (x,y), r in zip(pts, selected):
            if r["scenario"] == "Peng2017_Table8_WTW":
                fill = "#496783"
            elif r["scenario"] == "Peng2017_text_WTW":
                fill = "#9B8AB8"
            else:
                fill = "#D3A16F"
            if shape == "circle":
                p.append(circ(x,y,7,fill,stroke=color,sw=2))
            else:
                p.append(rect(x-7,y-7,14,14,fill,stroke=color,sw=2,rx=2))
    for ef in [0.6048,0.6205,0.73224]:
        x = x0 + (ef-xmin)/(xmax-xmin)*(x1-x0)
        p.append(ln(x,y0,x,y0+5,MUTED,1))
        p.append(tx(x,y0+23,f"{ef:.4f}",12,MUTED,"middle"))
    p.append(tx((x0+x1)/2,470,"Electricity lifecycle factor (kg CO₂e/kWh)",14,MUTED,"middle"))
    p.append(tx(80,154,"Local difference between NMC and LFP",17,NAVY,weight=700))
    d0,d1=0.7,1.0
    yy0,yy1=625,505
    axis_y(p,135,1125,yy0,yy1,d0,d1,[0.7,0.8,0.9,1.0]," g/km","{:.1f}")
    diffs=[]
    for r in rows:
        if r["vehicle"]=="BEV_NMC": continue
        n=next(x for x in rows if x["vehicle"]=="BEV_NMC" and x["scenario"]==r["scenario"])
        ef=float(r["factor_kg_per_kWh"])
        diff=float(r["combined_screening_g_per_km"])-float(n["combined_screening_g_per_km"])
        x=x0+(ef-xmin)/(xmax-xmin)*(x1-x0)
        y=yy0-(diff-d0)/(d1-d0)*(yy0-yy1)
        diffs.append((x,y))
    p.append(poly(diffs,stroke=LFP,sw=3))
    for x,y in diffs:p.append(circ(x,y,6,LFP))
    p.append(tx(60,700,"MEE2023 is a post-competition national PCF reference; it is not a Beijing-specific 2023 operational grid factor.",12,MUTED))
    legend_item(p,820,145,NMC,"BEV-NMC","line")
    legend_item(p,960,145,LFP,"BEV-LFP","line")
    finish_svg(p,"Fig_R9_5_Grid_Sensitivity.svg")

def figure6():
    rows=read_csv("R9_5_LIFETIME_SENSITIVITY.csv")
    p=start_svg("Figure 6. Vehicle-lifetime sensitivity",
                "Two-stage GWP100 screening; manufacturing is amortized over the selected lifetime mileage.")
    x0,x1,y0,y1=140,1120,420,175
    xmin,xmax=100000,300000
    ymin,ymax=140,330
    axis_y(p,x0,x1,y0,y1,ymin,ymax,[150,200,250,300]," g/km","{:.0f}")
    for vehicle,color in [("ICEV",ICE),("BEV_NMC",NMC),("BEV_LFP",LFP)]:
        selected=sorted([r for r in rows if r["vehicle"]==vehicle],key=lambda r:int(r["lifetime_km"]))
        pts=[]
        for r in selected:
            life=float(r["lifetime_km"]);val=float(r["two_stage_gCO2e_per_km"])
            x=x0+(life-xmin)/(xmax-xmin)*(x1-x0)
            y=y0-(val-ymin)/(ymax-ymin)*(y0-y1)
            pts.append((x,y))
        p.append(poly(pts,stroke=color,sw=3))
        for x,y in pts:p.append(circ(x,y,6,color))
    p.append(tx((x0+x1)/2,462,"Lifetime vehicle-kilometres (km)",14,MUTED,"middle"))
    p.append(tx(80,505,"NMC–LFP difference (g CO₂e/km)",16,NAVY,weight=700))
    ylo,yhi=1.0,1.8
    axis_y(p,140,1120,640,535,ylo,yhi,[1.0,1.2,1.4,1.6,1.8],"","{:.1f}")
    nmc=[r for r in rows if r["vehicle"]=="BEV_NMC"]
    lfp=[r for r in rows if r["vehicle"]=="BEV_LFP"]
    diffs=[]
    for n in sorted(nmc,key=lambda r:int(r["lifetime_km"])):
        l=next(r for r in lfp if r["lifetime_km"]==n["lifetime_km"])
        life=float(n["lifetime_km"])
        d=float(l["two_stage_gCO2e_per_km"])-float(n["two_stage_gCO2e_per_km"])
        x=140+(life-xmin)/(xmax-xmin)*(1120-140)
        y=640-(d-ylo)/(yhi-ylo)*(640-535)
        diffs.append((x,y))
    p.append(poly(diffs,stroke="#647783",sw=3))
    for x,y in diffs:p.append(circ(x,y,5,"#647783"))
    p.append(tx(60,710,"This is a two-stage screening result, not a complete cradle-to-grave vehicle LCA.",12,MUTED))
    legend_item(p,760,145,ICE,"ICEV","line")
    legend_item(p,870,145,NMC,"BEV-NMC","line")
    legend_item(p,1000,145,LFP,"BEV-LFP","line")
    finish_svg(p,"Fig_R9_5_Lifetime_Sensitivity.svg")

def figure7():
    rows=read_csv("R9_5_BREAK_EVEN_GRID_FACTOR.csv")
    lifetimes=sorted(set(int(r["lifetime_km"]) for r in rows))
    nmc=[];lfp=[]
    for life in lifetimes:
        nmc.append(float(next(r for r in rows if int(r["lifetime_km"])==life and r["vehicle"]=="BEV_NMC")["break_even_grid_EF_kgCO2e_per_kWh"]))
        lfp.append(float(next(r for r in rows if int(r["lifetime_km"])==life and r["vehicle"]=="BEV_LFP")["break_even_grid_EF_kgCO2e_per_kWh"]))
    p=start_svg("Figure 7. Break-even electricity-factor threshold",
                "The shaded band spans BEV-NMC and BEV-LFP thresholds; reference factors have different evidence scopes.")
    x0,x1,y0,y1=150,1120,600,180
    xmin,xmax=min(lifetimes),max(lifetimes)
    ymin,ymax=0.5,1.5
    axis_y(p,x0,x1,y0,y1,ymin,ymax,[0.5,0.7,0.9,1.1,1.3,1.5]," kg CO₂e/kWh","{:.1f}")
    xs=[x0+(v-xmin)/(xmax-xmin)*(x1-x0) for v in lifetimes]
    upper=[y0-(v-ymin)/(ymax-ymin)*(y0-y1) for v in nmc]
    lower=[y0-(v-ymin)/(ymax-ymin)*(y0-y1) for v in lfp]
    p.append(polygon(list(zip(xs,upper))+list(zip(xs[::-1],lower[::-1])),"#DDEAF2",opacity=0.95))
    center=[(a+b)/2 for a,b in zip(nmc,lfp)]
    pts=[(x,y0-(v-ymin)/(ymax-ymin)*(y0-y1)) for x,v in zip(xs,center)]
    p.append(poly(pts,stroke=ICE,sw=3))
    for x,y in pts:p.append(circ(x,y,6,ICE))
    refs=[(0.73224,"Peng2017 Table 8",ICE,"5 5"),(0.6048,"Peng2017 text",PHEV,"3 5"),(0.6205,"MEE2023 national PCF",BUS,"2 5")]
    for value,label,color,dash in refs:
        y=y0-(value-ymin)/(ymax-ymin)*(y0-y1)
        p.append(ln(x0,y,x1,y,color,2,dash))
        p.append(tx(x1-4,y-7,f"{label}: {value:.4f}",12,color,"end",700))
    p.append(tx((x0+x1)/2,650,"Vehicle lifetime (km)",14,MUTED,"middle"))
    p.append(tx(60,710,"MEE2023 is retrospective and has a broader PCF boundary; use only as a separate reference.",12,MUTED))
    finish_svg(p,"Fig_R9_5_BreakEven.svg")

def figure8():
    rows=read_csv("R9_5_BATTERY_FACTOR_SENSITIVITY.csv")
    rows=[r for r in rows if r["vehicle"]=="BEV" and int(float(r["battery_service_lifetime_km"]))==150000]
    rows=sorted(rows,key=lambda r:float(r["annual_battery_only_GWP_tCO2e"]))
    p=start_svg("Figure 8. Battery-factor sensitivity",
                "Battery-only cradle-to-gate GWP for the BEV reference pack; never add these values to Qiao whole-vehicle manufacturing.")
    x0,x1=400,1110
    top=155
    bar_h=31
    maxv=max(float(r["annual_battery_only_GWP_tCO2e"]) for r in rows)*1.12
    for i,r in enumerate(rows):
        y=top+i*43
        val=float(r["annual_battery_only_GWP_tCO2e"])
        color=LFP if "LFP" in r["source_id"] else NMC if "NMC" in r["source_id"] or "NCM" in r["source_id"] else ICE
        p.append(tx(380,y+21,r["source_id"],12,MUTED,"end"))
        p.append(rect(x0,y,x1-x0,bar_h,"#EEF2F5",rx=4))
        p.append(rect(x0,y,val/maxv*(x1-x0),bar_h,color,rx=4))
        p.append(tx(x0+val/maxv*(x1-x0)+9,y+21,f"{val:,.0f} t",12,NAVY,weight=700))
    p.append(tx(60,700,"Battery-only values are kept in a separate LCIA domain; no double counting with whole-vehicle production.",12,MUTED))
    finish_svg(p,"Fig_R9_5_Battery_Factor_Sensitivity.svg")

def figure9():
    rows=read_csv("R9_4_STAGE_COVERAGE_MATRIX.csv")
    vehicles=["ICEV","BEV","PHEV","bus_diesel","bus_assumed_BEV","bus_natural_gas","bus_unassigned_nonBEV","bus_unclassified"]
    stages=["vehicle_materials","parts_manufacturing","vehicle_distribution","vehicle_assembly","battery_manufacturing","energy_WTW","maintenance","end_of_life_dismantling","end_of_life_recycling","non_exhaust","passenger_km"]
    labels=["Materials","Parts","Distribution","Assembly","Battery","Energy WTW","Maintenance","EOL dismantle","EOL recycle","Non-exhaust","Passenger-km"]
    colors={
        "PARTIAL_PHYSICAL":"#5C9B8F",
        "SEPARATE_LCIA_ONLY":"#9B8AB8",
        "NOT_APPLICABLE_TRACTION_BATTERY":"#E5E9ED",
        "MISSING":"#F0C5C7",
        "HISTORICAL_GWP_PROXY_ONLY":"#D3A16F",
        "HISTORICAL_PROXY_NOT_SEPARABLE":"#E7C89D",
        "HISTORICAL_INCLUDED_IN_MATERIALS_NOT_SEPARATE":"#B6A1C8",
        "HISTORICAL_REFERENCE_ONLY":"#A8BAC3",
    }
    lookup={(r["vehicle"],r["stage"]):r["coverage_status"] for r in rows}
    p=start_svg("Figure 9. Lifecycle-stage evidence coverage matrix",
                "Coverage is not completeness: historical proxies are distinguished from 2023 direct observations.")
    x0=250;y0=205;cw=78;ch=48
    for j,label in enumerate(labels):
        x=x0+j*cw+cw/2
        p.append(tx(x,y0-16,label,11,MUTED,"middle",rotate=-35))
    for i,v in enumerate(vehicles):
        y=y0+i*ch
        p.append(tx(x0-18,y+30,VEHICLE_LABELS.get(v,v),13,INK,"end"))
        for j,st in enumerate(stages):
            status=lookup.get((v,st),"MISSING")
            color=colors.get(status,"#F0C5C7")
            p.append(rect(x0+j*cw,y,cw-4,ch-4,color,stroke="white",sw=1,rx=4))
            code={"PARTIAL_PHYSICAL":"P","SEPARATE_LCIA_ONLY":"L","NOT_APPLICABLE_TRACTION_BATTERY":"—","MISSING":"NA","HISTORICAL_GWP_PROXY_ONLY":"H","HISTORICAL_PROXY_NOT_SEPARABLE":"H*","HISTORICAL_INCLUDED_IN_MATERIALS_NOT_SEPARATE":"B","HISTORICAL_REFERENCE_ONLY":"R"}.get(status,"NA")
            p.append(tx(x0+j*cw+(cw-4)/2,y+27,code,12,NAVY,"middle",700))
    legend=[
        ("P","Partial physical","#5C9B8F"),("L","Separate battery LCIA","#9B8AB8"),
        ("H","Historical GWP proxy","#D3A16F"),("H*","Combined / not separable","#E7C89D"),
        ("R","Historical reference only","#A8BAC3"),("NA","Missing","#F0C5C7"),("—","Not applicable","#E5E9ED")
    ]
    lx=70;ly=645
    for code,label,color in legend:
        p.append(rect(lx,ly-17,28,22,color,rx=3))
        p.append(tx(lx+14,ly-1,code,10,NAVY,"middle",700))
        p.append(tx(lx+35,ly,label,11,MUTED))
        lx+=160
    p.append(tx(60,710,"No vehicle class is fully modelled cradle-to-grave. Historical proxy cells are not 2023 observations.",12,MUTED))
    finish_svg(p,"Fig_R9_6_Coverage_Matrix.svg")

def figure10():
    rows=read_csv("R9_4_PHYSICAL_VEHICLE_PARTIAL_SUBTOTALS.csv")
    pollutants=["CO2","VOC","NOx","PM2.5","SO2"]
    vehicles=["ICEV","BEV","PHEV","bus_diesel","bus_assumed_BEV"]
    p=start_svg("Figure 10. Partial physical inventory across five pollutants",
                "Each pollutant has its own scale; known-flow subtotals are not complete lifecycle emissions.")
    panel_w=345;panel_h=245
    for k,poll in enumerate(pollutants):
        col=k%3;row=k//3
        x0=65+col*375;y0=180+row*265
        vals=[]
        for v in vehicles:
            r=next((r for r in rows if r["flow"]==poll and r["vehicle"]==v),None)
            val=number(r["annual_known_kg"]) if r else None
            vals.append(val/1000 if val is not None else None)
        finite=[v for v in vals if v is not None]
        ymax=max(finite)*1.2 if finite else 1
        p.append(rect(x0,y0,panel_w,panel_h,PANEL,rx=10))
        p.append(tx(x0+16,y0+28,poll+" (t/year)",16,NAVY,weight=700))
        chart_top=y0+55;chart_bottom=y0+190
        for tick in [0,0.5,1.0]:
            yy=chart_bottom-tick*(chart_bottom-chart_top)
            p.append(ln(x0+38,yy,x0+panel_w-12,yy,GRID,1))
        for j,(v,val) in enumerate(zip(vehicles,vals)):
            bx=x0+55+j*55
            bh=(val or 0)/ymax*(chart_bottom-chart_top)
            color=VEHICLE_COLORS[v]
            p.append(rect(bx,chart_bottom-bh,32,bh,color,rx=3))
            if val is not None:
                p.append(tx(bx+16,chart_bottom-bh-6,f"{val:.1f}",10,NAVY,"middle"))
            else:
                p.append(tx(bx+16,chart_bottom-8,"NA",10,MUTED,"middle"))
            short={"ICEV":"ICE","BEV":"BEV","PHEV":"PHEV","bus_diesel":"D-bus","bus_assumed_BEV":"E-bus"}[v]
            p.append(tx(bx+16,chart_bottom+18,short,10,MUTED,"middle"))
    p.append(tx(60,710,"Physical pollutant masses are not CO₂e or ReCiPe characterization factors; missing bus flows remain NA.",12,MUTED))
    finish_svg(p,"Fig_R9_6_Multi_Pollutant_Inventory.svg")

def figure11():
    rows=read_csv("R9_5_GRID_LIFETIME_FACTORIAL.csv")
    vehicles=["ICEV","BEV_NMC","BEV_LFP"]
    life=sorted(set(int(r["lifetime_km"]) for r in rows))
    scenarios=sorted(set(r["grid_scenario"] for r in rows))
    vals=[float(r["two_stage_gCO2e_per_km"]) for r in rows]
    vmin,vmax=min(vals),max(vals)
    p=start_svg("Figure 11. Joint electricity-factor × lifetime sensitivity",
                "Two-stage GWP100 screening in g CO₂e/vehicle-km; the same color scale is used across vehicle panels.")
    for k,v in enumerate(vehicles):
        x0=70+k*380;y0=220;cw=92;ch=100
        p.append(tx(x0+150,170,VEHICLE_LABELS[v],18,NAVY,"middle",700))
        for j,life_km in enumerate(life):
            p.append(tx(x0+cw*(j+1),y0-18,f"{life_km//1000}k",12,MUTED,"middle"))
        for i,sc in enumerate(scenarios):
            p.append(tx(x0+cw-10,y0+i*ch+52,sc.replace("Peng2017_","").replace("_WTW",""),10,MUTED,"end"))
            for j,life_km in enumerate(life):
                r=next(r for r in rows if r["vehicle"]==v and int(r["lifetime_km"])==life_km and r["grid_scenario"]==sc)
                val=float(r["two_stage_gCO2e_per_km"])
                z=(val-vmin)/(vmax-vmin) if vmax>vmin else 0
                # Pale-to-deep blue interpolation.
                a=(246,248,250);b=(52,83,111)
                rgb=tuple(round(a[t]*(1-z)+b[t]*z) for t in range(3))
                color="#%02X%02X%02X"%rgb
                xx=x0+cw*(j+1);yy=y0+i*ch
                p.append(rect(xx,yy,cw-5,ch-5,color,stroke="white",sw=1,rx=4))
                p.append(tx(xx+(cw-5)/2,yy+55,f"{val:.1f}",14,"#FFFFFF" if z>0.55 else NAVY,"middle",700))
    p.append(tx(60,650,f"Shared color range: {vmin:.1f}–{vmax:.1f} g CO₂e/km. MEE2023 retrospective electricity factors are not included in this strict two-scenario factorial.",12,MUTED))
    finish_svg(p,"Fig_R9_6_Grid_Lifetime_Heatmap.svg")

def figure12():
    rows=read_csv("R9_4_BATTERY_RECIPE_ONLY.csv")
    cats=[]
    for r in rows:
        if r["impact_category"] not in cats: cats.append(r["impact_category"])
    cats=cats[:11]
    vehicles=["BEV","PHEV"]
    short={
        "GWP100":"GWP","terrestrial_acidification":"Acidification",
        "photochemical_oxidant_formation":"Photochemical",
        "freshwater_eutrophication":"Freshwater\neutro.","marine_eutrophication":"Marine\neutro.",
        "human_toxicity":"Human\ntoxicity","terrestrial_ecotoxicity":"Terrestrial\necotox.",
        "freshwater_ecotoxicity":"Freshwater\necotox.","particulate_matter_formation":"PM formation",
        "metal_depletion":"Metal depletion","fossil_depletion":"Fossil depletion"
    }
    p=start_svg("Figure 12. Battery-only ReCiPe profile under hypothetical recycling",
                "Cell values show percentage reduction versus no-recycling-credit baseline; categories remain separate and unit-specific.")
    x0=250;y0=240;cw=78;ch=125
    for j,c in enumerate(cats):
        label=short.get(c,c)
        for q,line in enumerate(label.split("\\n")):
            p.append(tx(x0+j*cw+cw/2,y0-34+q*14,line,10,MUTED,"middle"))
    for i,v in enumerate(vehicles):
        p.append(tx(x0-20,y0+i*ch+70,v,16,NAVY,"end",700))
        for j,c in enumerate(cats):
            base=next((number(r["annual_characterized_amount"]) for r in rows if r["vehicle"]==v and r["scenario"]=="cradle_to_gate_no_recycling_credit" and r["impact_category"]==c),None)
            rec=next((number(r["annual_characterized_amount"]) for r in rows if r["vehicle"]==v and r["scenario"]=="hypothetical_100pct_hydromet_recycling" and r["impact_category"]==c),None)
            change=((base-rec)/base*100) if base not in (None,0) and rec is not None else None
            if change is None: color="#E5E9ED";label="NA"
            else:
                mag=min(abs(change)/100,1)
                if change>=0:
                    color="#%02X%02X%02X"%(round(239-130*mag),round(247-65*mag),round(245-52*mag))
                else:
                    color="#%02X%02X%02X"%(round(249-15*mag),round(237-125*mag),round(239-95*mag))
                label=f"{change:.0f}%"
            xx=x0+j*cw;yy=y0+i*ch
            p.append(rect(xx,yy,cw-4,ch-4,color,stroke="white",sw=1,rx=4))
            p.append(tx(xx+(cw-4)/2,yy+72,label,13,NAVY,"middle",700))
    p.append(tx(60,610,"Positive values indicate reduced characterized impact. The 100% hydrometallurgical recycling case is hypothetical.",12,MUTED))
    p.append(tx(60,640,"Battery-only LCIA; do not add these values to physical pollutant mass or Qiao whole-vehicle GWP.",12,MUTED))
    finish_svg(p,"Fig_R9_6_Battery_ReCiPe_Profile.svg")

def figure13():
    rows=read_csv("R9_6_BUS_MANUFACTURING_FACTOR_EVIDENCE.csv")
    labels={"CDB_diesel":"Diesel","NGB_natural_gas":"Natural gas","DHEB_diesel_hybrid":"Diesel hybrid","BEB_battery_electric":"Battery electric"}
    p=start_svg("Figure 13. Historical Beijing bus manufacturing GWP proxies",
                "Derived from Lin et al. (2015) Figure 2 and Table 5; 2011–2014 technology, not 2023 observed bus factors.")
    x0,x1=390,1080;top=190;barh=58;maxv=55
    for i,r in enumerate(rows):
        y=top+i*105
        val=float(r["manufacturing_tCO2e_per_bus"])
        color=BUS_E if "BEB" in r["bus_type"] else BUS
        p.append(tx(x0-20,y+34,labels[r["bus_type"]],16,NAVY,"end",700))
        p.append(rect(x0,y,x1-x0,barh,"#EEF2F5",rx=5))
        p.append(rect(x0,y,val/maxv*(x1-x0),barh,color,rx=5))
        p.append(tx(x0+val/maxv*(x1-x0)+12,y+36,f"{val:.2f} t CO₂e/bus",16,NAVY,weight=700))
    p.append(tx(60,680,"Manufacturing = raw-material production + assembly/distribution proxy. Vehicle scrapping is excluded and remains a separate stage.",12,MUTED))
    p.append(tx(60,710,"Not a 2023 local purchase-factor observation; use only as historical literature sensitivity.",12,MUTED))
    finish_svg(p,"Fig_R9_6_Bus_Manufacturing_Evidence.svg")

def figure14():
    rows=read_csv("R9_6_R7_ENERGY_BOUNDARY_AUDIT.csv")
    car=next(r for r in rows if r["vehicle_class"]=="private_BEV")
    bus=next(r for r in rows if r["vehicle_class"]=="electric_bus")
    p=start_svg("Figure 14. R7 charging-energy measurement boundary",
                "Reported charging energy per distance is verified; the physical meter location is not identified by the source.")
    boxes=[("Grid supply",80),("Charging equipment",315),("Battery pack",550),("Traction motor",785),("Wheels",1020)]
    for label,x in boxes:
        p.append(rect(x,285,150,100,"#EEF3F7",stroke="#A8BAC3",sw=1.5,rx=10))
        p.append(tx(x+75,342,label,15,NAVY,"middle",700))
    for i in range(len(boxes)-1):
        x=boxes[i][1]+150
        p.append(ln(x,335,x+82,335,ICE,3))
        p.append(polygon([(x+82,335),(x+70,328),(x+70,342)],ICE))
    p.append(rect(285,165,475,75,"#FFF3E7",stroke=BUS,sw=1.5,rx=8))
    p.append(tx(522,195,"R5_CHARGE Table 4-1",16,NAVY,"middle",700))
    p.append(tx(522,220,"Monthly charging energy ÷ monthly vehicle distance",13,MUTED,"middle"))
    p.append(ln(522,240,522,275,BUS,2,"6 4"))
    p.append(tx(75,465,f"Private BEV: {float(car['reported_kWh_per_100km']):.1f} kWh/100 km",16,NMC,weight=700))
    p.append(tx(75,495,f"Bus: {float(bus['reported_kWh_per_100km']):.1f} kWh/100 km",16,BUS_E,weight=700))
    p.append(rect(690,440,440,105,"#F8F4EE",stroke="#C29A6B",sw=1.3,rx=8))
    p.append(tx(910,474,"Meter point unresolved",17,NAVY,"middle",700))
    p.append(tx(910,500,"Grid input / charger output / battery discharge",12,MUTED,"middle"))
    p.append(tx(60,630,"Base case uses the reported charging-energy intensity without an extra loss multiplier.",13,MUTED))
    p.append(tx(60,660,"If the value is battery-side, apply a separate grid-input sensitivity: reported kWh ÷ charging efficiency.",13,MUTED))
    finish_svg(p,"Fig_R9_6_Energy_Meter_Boundary.svg")

def figure15():
    rows=read_csv("R9_6_PKM_EVIDENCE_REGISTER.csv")
    get=lambda rid: next(r for r in rows if r["record_id"]==rid)
    vkt=float(get("PKM01")["value"]);board=float(get("PKM02")["value"]);ratio=float(get("PKM03")["value"])
    hist=float(get("PKM06")["value"]);pkm=get("PKM08")["value"]
    p=start_svg("Figure 15. Evidence status of 2023 bus passenger-kilometres",
                "Published bus boardings and vehicle-kilometres do not identify passenger-kilometres.")
    p.append(rect(75,185,470,245,"#F4F7F9",stroke=GRID,sw=1,rx=12))
    p.append(tx(105,225,"2023 direct operator statistics",18,NAVY,weight=700))
    p.append(tx(105,285,f"{vkt/1e9:.3f} billion vehicle-km",22,ICE,weight=700))
    p.append(tx(105,335,f"{board/1e9:.5f} billion passenger boardings",20,NMC,weight=700))
    p.append(tx(105,385,f"{ratio:.3f} boardings per vehicle-km",15,MUTED))
    p.append(rect(625,185,500,245,"#FBF6F3",stroke="#E7C7B9",sw=1,rx=12))
    p.append(tx(875,225,"2023 city-bus PKM",18,NAVY,"middle",700))
    p.append(tx(875,300,str(pkm),34,NMC,"middle",700))
    p.append(tx(875,350,"No public bus-only annual total located",15,MUTED,"middle"))
    p.append(tx(875,390,"Do not infer from boardings × arbitrary trip length",13,MUTED,"middle"))
    p.append(rect(75,490,1050,120,"#F4F7F9",stroke=GRID,sw=1,rx=10))
    p.append(tx(105,530,f"Historical reference only: approximately {hist/1e9:.2f} billion passenger-km around 2017",18,ICE,weight=700))
    p.append(tx(105,570,"Lin et al. (2015) cite this earlier Beijing conventional-bus estimate; it is not a 2023 observation.",13,MUTED))
    p.append(tx(60,690,"Preferred next source: 2023 AFC boarding/alighting OD, route-level passenger turnover, or bus-operator passenger-km records.",12,MUTED))
    finish_svg(p,"Fig_R9_6_PKM_Evidence_Status.svg")

def main():
    FIG.mkdir(parents=True,exist_ok=True)
    figure3();figure5();figure6();figure7();figure8()
    figure9();figure10();figure11();figure12();figure13();figure14();figure15()
    manifest=[
        ("3","Physical CO2 inventory","R9_4_PHYSICAL_STAGE_SUBTOTALS.csv","partial known-flow only"),
        ("5","Grid-factor sensitivity","R9_5_GRID_FACTOR_SENSITIVITY.csv","two-stage GWP screening"),
        ("6","Lifetime sensitivity","R9_5_LIFETIME_SENSITIVITY.csv","two-stage GWP screening"),
        ("7","Break-even grid factor","R9_5_BREAK_EVEN_GRID_FACTOR.csv","two-stage GWP screening"),
        ("8","Battery-factor sensitivity","R9_5_BATTERY_FACTOR_SENSITIVITY.csv","battery-only GWP"),
        ("9","Lifecycle coverage matrix","R9_4_STAGE_COVERAGE_MATRIX.csv","evidence completeness"),
        ("10","Multi-pollutant physical inventory","R9_4_PHYSICAL_VEHICLE_PARTIAL_SUBTOTALS.csv","partial physical masses"),
        ("11","Grid x lifetime factorial","R9_5_GRID_LIFETIME_FACTORIAL.csv","two-stage GWP screening"),
        ("12","Battery ReCiPe profile","R9_4_BATTERY_RECIPE_ONLY.csv","battery-only LCIA"),
        ("13","Bus manufacturing evidence","R9_6_BUS_MANUFACTURING_FACTOR_EVIDENCE.csv","historical 2015 proxy"),
        ("14","R7 energy meter boundary","R9_6_R7_ENERGY_BOUNDARY_AUDIT.csv","measurement-point audit"),
        ("15","Bus PKM evidence status","R9_6_PKM_EVIDENCE_REGISTER.csv","2023 PKM remains NA"),
    ]
    with (FIG/"R9_6_FIGURE_MANIFEST.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.writer(f);w.writerow(["figure","title","source_csv","scope_note"]);w.writerows(manifest)
    print("Generated 12 SVG figures plus manifest in",FIG)

if __name__=="__main__":
    main()
