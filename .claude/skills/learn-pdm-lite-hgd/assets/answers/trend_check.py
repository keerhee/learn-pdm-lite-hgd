"""예지보전 실습판 정답 — 노이즈 vs 추세 판정과 그래프 한 장 대시보드.

사용: 센서 csv(sensor_50_virtual.csv)가 있는 폴더에서 python3 -I trend_check.py
산출: outputs/trend_judgement.csv, index.html, expected.json
판정 규칙은 원본 「예지보전 따라하기 II」 프롬프트 3, 평상 범위는 원본 덱 ③ 전처리를 그대로 따른다.
"""
import csv, json, statistics as st
from pathlib import Path

SRC = Path("sensor_50_virtual.csv")
if not SRC.exists():
    SRC = Path("data/sensor_50_virtual.csv")
SENSORS = ["진동(mm/s)", "온도(℃)", "압력(bar)"]

rows = list(csv.DictReader(SRC.open(encoding="utf-8-sig")))
equips = sorted({r["설비"] for r in rows})  # 설비A(...), 설비B(...)


def series(eq, col):
    r = [x for x in rows if x["설비"] == eq]
    return [x["시간"][11:16] for x in r], [float(x[col]) for x in r]


def minutes(t):
    h, m = t.split(":")
    return int(h) * 60 + int(m)


judge = []          # 판정표 행
first_2sigma = {}   # 설비별 평상 범위로 처음 잡힌 시각
info = {}           # 그래프에 쓸 값
for eq in equips:
    short = eq[:3]  # '설비A' / '설비B'
    for col in SENSORS:
        t, v = series(eq, col)
        # 1) 평상 범위 = 평균 ± 2 × 표준편차 (하루 전체 25점, 표본 표준편차)
        m, s = st.mean(v), st.stdev(v)
        lo, hi = m - 2 * s, m + 2 * s
        cand = [(t[i], v[i]) for i in range(len(v)) if v[i] < lo or v[i] > hi]
        if cand:
            first = min(cand, key=lambda x: minutes(x[0]))[0]
            if short not in first_2sigma or minutes(first) < minutes(first_2sigma[short]):
                first_2sigma[short] = first
        # 2) 기준선 = 처음 12점(08:00~11:40), 상한 = 평균 + 3 × 표준편차
        base = v[:12]
        upper = st.mean(base) + 3 * st.stdev(base)
        over = [x > upper for x in v]
        start = next((t[i] for i in range(len(v) - 2) if all(over[i:i + 3])), None)
        if start:
            verdict = "추세"
        elif any(over):
            verdict = "노이즈"
        else:
            verdict = "정상"
        over_times = [t[i] for i in range(len(v)) if over[i]]
        judge.append({
            "설비": eq, "센서": col,
            "평상범위_하한": round(lo, 3), "평상범위_상한": round(hi, 3),
            "이상후보": " ".join(f"{a}({b})" for a, b in cand),
            "기준선_상한": round(upper, 3),
            "상한초과_시각": " ".join(over_times),
            "판정": verdict, "추세시작": start or "",
        })
        info[(short, col)] = {"t": t, "v": v, "start": start, "over": over_times,
                              "upper": upper, "verdict": verdict}

# 판정표 저장
Path("outputs").mkdir(exist_ok=True)
with open("outputs/trend_judgement.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(judge[0].keys()))
    w.writeheader()
    w.writerows(judge)

a_vib = info[("설비A", "진동(mm/s)")]
b_vib = info[("설비B", "진동(mm/s)")]
b_tmp = info[("설비B", "온도(℃)")]
a_noise_time = a_vib["over"][0]
a_noise_value = a_vib["v"][a_vib["t"].index(a_noise_time)]
starts = [x["start"] for x in info.values() if x["start"]]
earliest = min(starts, key=minutes)
lead = minutes(first_2sigma["설비B"]) - minutes(earliest)

# 3) 그래프 한 장 대시보드
labels = a_vib["t"]
mark = lambda times, base_r=2: [7 if x in times else base_r for x in labels]
html = f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>노이즈 vs 추세</title>
<style>
 body{{margin:0;font-family:system-ui,-apple-system,'Malgun Gothic',sans-serif;background:#f7f8fa;color:#1d2433}}
 main{{max-width:960px;margin:0 auto;padding:20px 16px}}
 h1{{font-size:1.3rem;margin:0 0 6px}}
 .sum{{background:#fff;border-left:4px solid #c2410c;padding:10px 14px;margin:10px 0 16px;line-height:1.5}}
 .box{{background:#fff;border-radius:8px;padding:12px;position:relative;height:380px}}
 footer{{font-size:.8rem;color:#5b6475;margin-top:12px;line-height:1.5}}
 @media (max-width:600px){{.box{{height:300px}}}}
</style></head><body><main>
<h1>노이즈 vs 추세 — 설비센서 판정</h1>
<div class="sum">설비B 온도 추세 시작 <b>{b_tmp['start']}</b> · 진동 <b>{b_vib['start']}</b> — 평상 범위(±2σ)로 처음 잡힌 {first_2sigma['설비B']}보다 <b>{lead}분</b> 빠름.
설비A 진동 {a_noise_time} {a_noise_value}은 한 번 튄 <b>노이즈</b>.</div>
<div class="box"><canvas id="c"></canvas></div>
<footer>판정 규칙: 처음 12점(08:00~11:40) 기준선의 평균 + 3σ를 3번 연속 넘으면 추세, 연속이 아니면 노이즈. 큰 점 = 노이즈 시각·추세 시작.<br>
데이터: keerhee/kma-auto-genai-3-1 · data/Day5/Day5_설비센서_50건_가상.csv — <b>센서 값은 실습용 가상 데이터</b>입니다.</footer>
</main>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<script>
new Chart(document.getElementById('c'), {{
  type: 'line',
  data: {{ labels: {json.dumps(labels)}, datasets: [
    {{ label: '설비A 진동 (mm/s)', data: {json.dumps(a_vib['v'])}, borderColor: '#2563eb', backgroundColor: '#2563eb',
       pointRadius: {json.dumps(mark([a_noise_time]))}, yAxisID: 'y' }},
    {{ label: '설비B 진동 (mm/s)', data: {json.dumps(b_vib['v'])}, borderColor: '#c2410c', backgroundColor: '#c2410c',
       pointRadius: {json.dumps(mark([b_vib['start']]))}, yAxisID: 'y' }},
    {{ label: '설비B 온도 (℃, 오른쪽)', data: {json.dumps(b_tmp['v'])}, borderColor: '#9333ea', backgroundColor: '#9333ea',
       borderDash: [5, 4], pointRadius: {json.dumps(mark([b_tmp['start']]))}, yAxisID: 'y2' }}
  ]}},
  options: {{ responsive: true, maintainAspectRatio: false, interaction: {{ mode: 'index', intersect: false }},
    plugins: {{ legend: {{ position: 'bottom' }} }},
    scales: {{ y: {{ title: {{ display: true, text: '진동 mm/s' }} }},
              y2: {{ position: 'right', grid: {{ drawOnChartArea: false }}, title: {{ display: true, text: '온도 ℃' }} }},
              x: {{ ticks: {{ maxTicksLimit: 9 }} }} }} }}
}});
</script></body></html>
"""
Path("index.html").write_text(html, encoding="utf-8")

# 4) 확인값
expected = {"values": {
    "a_noise_time": {"value": a_noise_time, "decimals": None, "block": 1},
    "a_noise_value": {"value": a_noise_value, "decimals": 1, "block": 1},
    "b_temp_trend_start": {"value": b_tmp["start"], "decimals": None, "block": 1},
    "b_vib_trend_start": {"value": b_vib["start"], "decimals": None, "block": 1},
    "b_first_2sigma": {"value": first_2sigma["설비B"], "decimals": None, "block": 1},
    "lead_minutes": {"value": lead, "decimals": 0, "block": 1},
}}
Path("expected.json").write_text(json.dumps(expected, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({k: v["value"] for k, v in expected["values"].items()}, ensure_ascii=False))
