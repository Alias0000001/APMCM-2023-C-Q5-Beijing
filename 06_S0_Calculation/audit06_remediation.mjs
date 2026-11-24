// Node >= 18; no third-party packages. Run from any directory.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
function parse(s){const rows=s.trim().split(/\r?\n/);const fields=l=>[...l.matchAll(/(?:^|,)(?:"((?:[^"]|"")*)"|([^,]*))/g)].map(x=>x[1]===undefined?x[2]:x[1].replace(/""/g,'"'));const h=fields(rows.shift());return rows.map(l=>Object.fromEntries(fields(l).map((v,i)=>[h[i],v])))}
function csv(rows){return rows.map(r=>r.map(v=>{const s=typeof v==="number"?v.toFixed(9):String(v??"");return /[",\n]/.test(s)?'"'+s.replace(/"/g,'""')+'"':s}).join(",")).join("\n")+"\n"}
function run(files){
const get=n=>parse(files[n]),par=n=>Object.fromEntries(get(n).map(x=>[x.parameter,+x.value])),A=par("R9_7A_CONTEST_ACTIVITY_INPUTS.csv"),E=par("R9_7B_ENERGY_INPUTS.csv"),M=get("R9_7C_MANUFACTURING_FACTOR_REGISTER.csv"),D=get("R9_7C_MANUFACTURING_DERIVATION.csv"),P=get("R9_7D_PKM_EVIDENCE.csv");
const ledger=get("../07_LCA_LCIA/R9_LCI_PARAMETER_LEDGER.csv"),cap=(id)=>+ledger.find(x=>x.parameter_id===id).value,bevCap=cap("R9_BEV_CAPACITY_PROXY"),phevCap=cap("R9_PHEV_CAPACITY_PROXY");
const mf=id=>+M.find(x=>x.source_id===id).factor_value*1000,xs=t=>D.filter(x=>x.source_id==="XIONG2019"&&x.technology===t).reduce((a,x)=>a+ +x.value,0),bf=+get("R9_7AUDIT04_BATTERY_RECIPE.csv").find(x=>x.indicator==="GWP100"&&x.recycling_case==="no_credit").factor_per_kWh;
const scale=A.target_population/A.reference_population,V=scale*A.private_small_micro_cars*A.private_daily_distance*365*A.central_city_dispatch_rate,B=scale*A.bus_vkt,d=A.bus_diesel_count/(A.bus_diesel_count+A.bus_gas_count),U=A.bus_total_count-A.bus_diesel_count-A.bus_gas_count-A.bus_mixed_count,ss=["S-1","S0","S1","S2","S3","S4"];
const mI=mf("QIAO17_ICE"),mD=mf("LIN15_BUS_CDB"),mG=mf("LIN15_BUS_NGB"),mH=mf("LIN15_BUS_DHEB"),mB=mf("LIN15_BUS_BEB");
const base={grid:E.grid_ef,etaCar:1,etaBus:1,gas:E.gasoline_l100,uf:E.uf,cd:0,eb:E.bus_e,lc:+M.find(r=>r.source_id==="QIAO17_ICE").lifetime_km,lb:+M.find(r=>r.source_id==="LIN15_BUS_CDB").lifetime_km,extra:0,res:"hy",lng:E.lng_share,ac:E.ac_share,bevM:mf("QIAO17_BEV_NMC"),phevM:mf("XIONG19_PHEV_NMC"),gasUplift:1,scope:1,privateResidual:0};
const bad={gas:6,etaCar:.9,etaBus:.9,eb:1.4,lc:100000,lb:300000,extra:1,uf:.55,cd:2,res:"di"};
const cases=[["reference",{}],["cleaner_grid",{grid:.6048}],["meter_loss",{etaCar:.9,etaBus:.9}],["low_gasoline",{gas:6}],["high_gasoline",{gas:9}],["PHEV_blended",{cd:2}],["PHEV_low_UF",{uf:.55,cd:2}],["PHEV_high_UF",{uf:.79,cd:2}],["bus_high",{eb:1.4}],["residual_diesel",{res:"di"}],["residual_gas_LNG",{res:"ga",lng:1}],["CNG",{lng:0}],["short_life",{lc:100000,lb:300000}],["long_life",{lc:200000,lb:500000}],["extra_pack",{extra:1}],["alternate_NMC",{bevM:xs("BEV_NMC")}],["LFP_proxy",{bevM:xs("BEV_LFP"),phevM:xs("PHEV_LFP")}],["adverse_joint",bad],["adverse_long_bus",{...bad,lb:500000}],["favorable_joint",{gas:9,grid:.6048,lc:200000,lb:500000,bevM:xs("BEV_NMC"),uf:.79,lng:1,res:"ga"}],["adverse_bus_delivered",{...bad,etaBus:1}],["adverse_long_bus_delivered",{...bad,etaBus:1,lb:500000}],["methane_pathway_uplift_design",{gasUplift:1.2}],["scope_exclusion_design",{scope:.9}],["private_nonBEV_residual_design",{privateResidual:.25}]];
const levels=[.8,1,1.2],structures=[],norm=a=>{const n=a.reduce((v,x)=>v+x,0);if(n<=0||a.some(x=>x<0))throw Error("shares");return a.map(x=>x/n)};
for(const s of [.05,.08,.1158])for(const t of [.6,.778,.9])for(const q of [.6,.8,1])for(const r of levels)for(const z of levels)structures.push({s,t,q,r,z,p:norm([1-s,s*t*r,s*(1-t)*r]),b:norm([A.bus_diesel_count+U*d,A.bus_gas_count+U*(1-d),A.bus_mixed_count*(1-q),A.bus_mixed_count*q*z])});
function intens(a,st){const p=st.p.slice(),b=st.b;const re=p[2]*a.privateResidual;p[0]+=re;p[2]-=re;
const wi=a.gas/100*E.gasoline_mj_l*E.gasoline_ef/1000,we=E.car_e/a.etaCar*a.grid,wh=((1-a.uf)*a.gas+a.uf*a.cd)/100*E.gasoline_mj_l*E.gasoline_ef/1000+a.uf*E.phev_cd_e/a.etaCar*a.grid,car=[wi+mI/a.lc,we+a.bevM/a.lc+a.extra*bevCap*bf/a.lc,wh+a.phevM/a.lc+a.extra*phevCap*bf/a.lc];
const wd=(E.diesel_off+(E.diesel_on-E.diesel_off)*a.ac)*E.diesel_ef/1000,wg=(E.gas_off+(E.gas_on-E.gas_off)*a.ac)*(E.cng_ef+(E.lng_ef-E.cng_ef)*a.lng)*a.gasUplift/1000,whb=(E.hybrid_off+(E.hybrid_on-E.hybrid_off)*a.ac)*E.diesel_ef/1000,wb=a.eb/a.etaBus*a.grid,bus=[wd+mD/a.lb,wg+mG/a.lb,a.res==="di"?wd+mD/a.lb:a.res==="ga"?wg+mG/a.lb:whb+mH/a.lb,wb+mB/a.lb];
return {pF:car[0],p0:p.reduce((v,x,i)=>v+x*car[i],0),pB:car[1],pClean:car[1]-we*(1-A.S4_grid_factor_multiplier),bF:d*bus[0]+(1-d)*bus[1],b0:b.reduce((v,x,i)=>v+x*bus[i],0),bB:bus[3],bClean:bus[3]-wb*(1-A.S4_grid_factor_multiplier),we,wb,p,b}}
function calc(x,p,b){return [x.pF*p+x.bF*b,x.p0*p+x.b0*b,x.p0*p+x.bB*b,x.pB*p+x.b0*b,x.pB*p+x.bB*b,x.pClean*p+x.bClean*b]}
const st0=structures.find(x=>x.s===A.private_nev_share&&x.t===A.private_bev_fraction_of_nev&&x.q===A.bus_bev_fraction_of_mixed&&x.r===1&&x.z===1),x0=intens(base,st0),r0=calc(x0,V/1e6,B/1e6),old=get("R9_7C_PARTIAL_LCA_GWP_SCENARIOS.csv");
r0.forEach((v,i)=>{if(Math.abs(v-+old.find(x=>x.scenario===ss[i]).partial_LCA_GWP_t_y/1000)>1e-6)throw Error("baseline "+ss[i])});
// Independent limiting cases at the original reference structure.
const near=(a,b,t=1e-9)=>{if(Math.abs(a-b)>t)throw Error("limit "+a+" "+b)};
calc(x0,0,0).forEach(v=>near(v,0));
const noGrid=intens({...base,grid:0},st0);
near(noGrid.pB,base.bevM/base.lc);near(noGrid.bB,mB/base.lb);near(noGrid.pClean,noGrid.pB);near(noGrid.bClean,noGrid.bB);
const long=intens({...base,lc:1e15,lb:1e15},st0);
near(long.pB,long.we,1e-9);near(long.bB,long.wb,1e-9);
const onlyPHEV={...st0,p:[0,0,1]};
near(intens({...base,uf:0},onlyPHEV).p0,base.gas/100*E.gasoline_mj_l*E.gasoline_ef/1000+base.phevM/base.lc);
near(intens({...base,uf:1,cd:0},onlyPHEV).p0,E.phev_cd_e/base.etaCar*base.grid+base.phevM/base.lc);
const allBEV=calc(intens(base,{...st0,p:[0,1,0],b:[0,0,0,1]}),V/1e6,B/1e6);
[2,3,4].forEach(i=>near(allBEV[i],allBEV[1]));
const make=()=>ss.map(()=>({lo:Infinity,hi:-Infinity,glo:Infinity,ghi:-Infinity,neg:0,w:null})),all=make(),orig=make();let n=0,n20=0,order=0,order20=0,per=[];
function add(a,y,meta){for(let i=0;i<6;i++){const v=a[i],red=100*(1-y[i]/y[1]);if(red<v.lo){v.lo=red;v.w={...meta,G0:y[1],G:y[i],red}}v.hi=Math.max(v.hi,red);v.glo=Math.min(v.glo,y[i]);v.ghi=Math.max(v.ghi,y[i]);v.neg+=+(red<0)}}
for(let j=0;j<cases.length;j++){const [name,delta]=cases[j],a={...base,...delta},one=make();let k=0;for(const st of structures){const x=intens(a,st);for(const g of levels)for(const m of levels)for(const b of levels)for(const den of [1,1/A.central_city_dispatch_rate]){const p=V*g*m*den*a.scope/1e6,w=B*b/1e6,y=calc(x,p,w),meta={case:name,s:st.s,t:st.t,q:st.q,r:st.r,z:st.z,g,m,b,den,thresholdMultiplier:A.S4_grid_factor_multiplier+(y[1]-y[5])/(x.we*p+x.wb*w)};if(y.some(v=>!Number.isFinite(v)||v<0)||Math.abs(y[4]-y[3]-y[2]+y[1])>1e-8)throw Error("invariant");const o=+(y[5]<y[4]&&y[4]<y[3]&&y[3]<y[2]&&y[2]<y[1]&&y[1]<y[0]);n++;k++;order+=o;add(all,y,meta);add(one,y,meta);if(j<20){n20++;order20+=o;add(orig,y,meta)}}}for(let i=0;i<6;i++)per.push([name,ss[i],k,one[i].lo,one[i].hi,one[i].neg,one[i].glo,one[i].ghi])}
if(n!==25*243*27*2||n20!==262440)throw Error("cardinality "+n+" "+n20);
const out={},header=["design","scenario","sets","min_reduction_pct","max_reduction_pct","negative_sets","min_GWP_kt","max_GWP_kt"],row=(id,a,n)=>a.map((v,i)=>[id,ss[i],n,v.lo,v.hi,v.neg,v.glo,v.ghi]),keys=["case","s","t","q","r","z","g","m","b","den","G0","G","red","thresholdMultiplier"];
out["R9_7FIX_SENSITIVITY_ENVELOPE.csv"]=csv([header,...row("audit06_20_packages",orig,n20),...row("remediation_25_packages",all,n)]);
out["R9_7FIX_TECH_PACKAGES.csv"]=csv([["case",...Object.keys(base),"scope_note"],...cases.map(([name,delta])=>{const a={...base,...delta};return [name,...Object.keys(base).map(k=>a[k]),name.startsWith("adverse")&&a.etaBus<1?"conditional battery-side historical bus energy; no evidence of meter position":name.includes("delivered")?"bus historical value already delivered; car losses only":"design/literature proxy; not probability"]})]);
out["R9_7FIX_PACKAGE_ENVELOPES.csv"]=csv([header.map((x,i)=>i===0?"case":x),...per]);
out["R9_7FIX_REVERSAL_WITNESSES.csv"]=csv([["design","scenario",...keys],...orig.map((v,i)=>["audit06_20_packages",ss[i],...keys.map(k=>v.w[k])]),...all.map((v,i)=>["remediation_25_packages",ss[i],...keys.map(k=>v.w[k])])]);
const occ=+P.find(r=>r.indicator==="private_occupancy").value,trip=+P.find(r=>r.indicator==="bus_trip_distance").value,pkmP=V*occ,pkmB=A.bus_boardings*scale*trip,oB=pkmB/B;
out["R9_7FIX_CALIBRATED_PKM.csv"]=csv([["case","relative_car_BEV_occupancy","relative_bus_BEV_occupancy","S0_car_PKM","S0_bus_PKM","S3_car_pax","S3_bus_pax","S3_car_VKT","S3_bus_VKT","S3_GWP_kt","paired_reduction_pct"],...[["lower",.81,.8],["reference",1,1],["higher",1.2,1.2]].map(([l,c,b])=>{const oc=occ*c/(1+x0.p[1]*(c-1)),ob=oB*b/(1+x0.b[3]*(b-1)),v=pkmP/oc,w=pkmB/ob,z=(x0.pB*v+x0.bB*w)/1e6;return [l,c,b,pkmP,pkmB,oc,ob,v,w,z,100*(1-z/r0[1])]})]);
const ep=calc(intens({...base,extra:1},st0),V/1e6,B/1e6);
out["R9_7FIX_OMITTED_MARGIN.csv"]=csv([["case","S0_GWP_kt","scenario_GWP_kt","max_additional_differential_before_reversal_kt"],["S3_reference",r0[1],r0[4],r0[1]-r0[4]],["S3_one_extra_private_pack",ep[1],ep[4],ep[1]-ep[4]],["S4_reference",r0[1],r0[5],r0[1]-r0[5]]]);
out["R9_7FIX_JINHUA_DIAGNOSTIC.csv"]=csv([["m","scenario","GWP_kt","paired_reduction_pct","scope"],...levels.flatMap(m=>{const y=calc(x0,V*1.171038*m/1e6,B*.646917/1e6);return y.map((v,i)=>[m,ss[i],v,100*(1-v/y[1]),"retrospective diagnostic only; no observed Jinhua VKT"])})]);
out["R9_7FIX_TEST_SUMMARY.csv"]=csv([["test","result","detail"],["six_baselines","PASS","within 1e-6 kt"],["limiting_cases","PASS","zero VKT; zero grid; lifetime tends to infinity; UF endpoints; identical BEV mix"],["paired_additivity_nonnegative","PASS",n],["original_20_count","PASS",n20],["strict_order_count_20","INFO",order20],["expanded_count","PASS",n],["strict_order_count_25","INFO",order],["PKM_common_baseline","PASS","same conditional S0 PKM"]]);
return {out,summary:{n,n20,order,order20,original:row("20",orig,n20),expanded:row("25",all,n),w4:all[5].w,delivered:per.filter(r=>r[0].includes("delivered")&&r[1]==="S4")}}
}
const D=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../02_Cleaned_Data');
const names=["../07_LCA_LCIA/R9_LCI_PARAMETER_LEDGER.csv","R9_7A_CONTEST_ACTIVITY_INPUTS.csv","R9_7B_ENERGY_INPUTS.csv","R9_7C_MANUFACTURING_FACTOR_REGISTER.csv","R9_7C_MANUFACTURING_DERIVATION.csv","R9_7C_PARTIAL_LCA_GWP_SCENARIOS.csv","R9_7D_PKM_EVIDENCE.csv","R9_7AUDIT04_BATTERY_RECIPE.csv"];
const files=Object.fromEntries(names.map(n=>[n,fs.readFileSync(path.join(D,n),'utf8')]));
const {out,summary}=run(files);
for(const [n,s] of Object.entries(out))fs.writeFileSync(path.join(D,n),s);
console.log(JSON.stringify(summary,null,2));
