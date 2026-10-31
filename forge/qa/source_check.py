import csv,sys,statistics as st
rows=list(csv.DictReader(open(sys.argv[1],encoding='utf-8-sig')))
cols=['진동(mm/s)','온도(℃)','압력(bar)']
for eq in ['설비A','설비B']:
    r=[x for x in rows if x['설비'].startswith(eq)]
    for c in cols:
        v=[float(x[c]) for x in r]; t=[x['시간'][11:] for x in r]
        m,s=st.mean(v),st.stdev(v); hi=m+2*s; lo=m-2*s
        out=[(t[i],v[i]) for i in range(len(v)) if v[i]>hi or v[i]<lo]
        b=v[:12]; bh=st.mean(b)+3*st.stdev(b)
        over=[v[i]>bh for i in range(len(v))]
        start=None
        for i in range(len(v)-2):
            if all(over[i:i+3]): start=t[i];break
        print(eq,c,f"2σ=[{lo:.3f},{hi:.3f}] out={out} base_hi={bh:.3f} over={[t[i] for i in range(len(v)) if over[i]]} trend_start={start}")
