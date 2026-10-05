import numpy as np
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Cybersecurity Awareness & Threat Intelligence Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
        :root {
            --bg-1: #081420;
            --bg-2: #0d1b2a;
            --panel-1: rgba(12, 20, 30, 0.75);
            --panel-2: rgba(17, 27, 42, 0.9);
            --panel-3: rgba(27, 42, 60, 0.9);
            --border: rgba(140, 170, 207, 0.18);
            --text-1: #edf4ff;
            --text-2: #a9bfdc;
            --teal: #4ecdc4;
            --teal-2: #7ee7d9;
            --cyan: #56ccf2;
            --green: #55d483;
            --yellow: #ffd166;
            --orange: #ff9f43;
            --red: #ff5d73;
            --purple: #a78bfa;
        }

        .stApp {
            background: linear-gradient(180deg, var(--bg-1) 0%, var(--bg-2) 100%);
        }
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1500px;
        }
        h1 {
            letter-spacing: -0.04em;
            margin-bottom: 0.2rem;
            color: var(--text-1);
            font-size: clamp(1.9rem, 3vw, 2.4rem);
            line-height: 1.12;
        }
        h2, h3, h4, h5, h6 {
            color: var(--text-1);
        }
        .section-tag {
            display: inline-block;
            padding: 0.35rem 0.8rem;
            border-radius: 999px;
            background: rgba(78, 205, 196, 0.12);
            border: 1px solid rgba(78, 205, 196, 0.35);
            color: var(--teal-2);
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 0.9rem;
        }
        .brand-strip {
            background: linear-gradient(90deg, rgba(18, 34, 51, 0.95), rgba(10, 23, 35, 0.9));
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 1rem 1.2rem;
            margin-bottom: 1.2rem;
            box-shadow: 0 12px 28px rgba(2, 8, 17, 0.22);
        }
        .brand-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
        }
        .brand-left {
            display: flex;
            align-items: center;
            gap: 0.9rem;
        }
        .brand-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 44px;
            height: 44px;
            border-radius: 12px;
            background: linear-gradient(135deg, var(--teal), var(--cyan));
            box-shadow: 0 8px 22px rgba(78, 205, 196, 0.26);
            font-size: 1.5rem;
        }
        .brand-meta {
            display: flex;
            flex-direction: column;
            line-height: 1.2;
        }
        .brand-meta strong {
            font-size: 0.88rem;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            color: var(--teal-2);
        }
        .brand-meta span {
            font-size: 1.15rem;
            color: var(--text-1);
            font-weight: 700;
        }
        .brand-status {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.4rem 0.75rem;
            border-radius: 999px;
            background: rgba(85, 212, 131, 0.12);
            border: 1px solid rgba(85, 212, 131, 0.35);
            color: var(--green);
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }
        .brand-status::before {
            content: "";
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--green);
            display: inline-block;
            box-shadow: 0 0 10px rgba(85, 212, 131, 0.9);
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0b1723 0%, #0d1a2c 100%);
            border-right: 1px solid rgba(155, 176, 199, 0.16);
        }
        [data-testid="stSidebar"] .block-container {
            padding-top: 1.2rem;
        }
        [data-testid="stMetric"] {
            background: rgba(15, 26, 39, 0.9);
            border: 1px solid rgba(142, 160, 182, 0.18);
            border-radius: 18px;
            padding: 0.8rem 1rem;
            box-shadow: 0 10px 24px rgba(4, 10, 18, 0.18);
        }
        [data-testid="stMetricLabel"] {
            color: #d9e7f7;
            font-weight: 600;
        }
        [data-testid="stMetricValue"] {
            color: #f2f6fb;
            font-weight: 700;
        }
        [data-testid="stMetricDelta"] {
            color: #a8bedf;
            font-size: 0.75rem;
        }
        .stDataFrame {
            border: 1px solid rgba(142, 160, 182, 0.18);
            border-radius: 14px;
            overflow: hidden;
        }
        .stDataFrame > div {
            background: rgba(11, 19, 31, 0.5);
        }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border: 1px solid rgba(142, 160, 182, 0.18);
            border-radius: 16px;
            padding: 0.25rem 0.45rem 0.5rem;
            background: rgba(12, 20, 30, 0.65);
        }
        .stAlert, .stMarkdownContainer {
            color: #eaf2ff;
        }
        .stSidebar > div:first-child {
            padding-top: 1.2rem;
        }
        .sidebar-card {
            background: rgba(18, 29, 44, 0.78);
            border: 1px solid rgba(142, 160, 182, 0.18);
            border-radius: 16px;
            padding: 0.8rem 0.9rem;
            margin-bottom: 1rem;
        }
        .status-chip {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 999px;
            padding: 0.28rem 0.7rem;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            margin-bottom: 0.4rem;
        }
        .status-critical { background: rgba(255, 93, 115, 0.12); border: 1px solid rgba(255, 93, 115, 0.38); color: #ff8ea1; }
        .status-high { background: rgba(255, 159, 67, 0.12); border: 1px solid rgba(255, 159, 67, 0.38); color: #ffba79; }
        .status-medium { background: rgba(255, 209, 102, 0.12); border: 1px solid rgba(255, 209, 102, 0.38); color: #ffd874; }
        .status-low { background: rgba(86, 204, 242, 0.12); border: 1px solid rgba(86, 204, 242, 0.38); color: #8fe7ff; }
        .status-open { background: rgba(86, 204, 242, 0.12); border: 1px solid rgba(86, 204, 242, 0.38); color: #8fe7ff; }
        .status-investigating { background: rgba(167, 139, 250, 0.12); border: 1px solid rgba(167, 139, 250, 0.38); color: #c6b3ff; }
        .status-contained { background: rgba(85, 212, 131, 0.12); border: 1px solid rgba(85, 212, 131, 0.38); color: #97f1b0; }
        .status-mitigated { background: rgba(136, 146, 170, 0.12); border: 1px solid rgba(136, 146, 170, 0.38); color: #d0d9e9; }
        .nav-bar {
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
            margin: 0.2rem 0 1.3rem;
        }
        .nav-pill {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0.45rem 0.8rem;
            border-radius: 999px;
            border: 1px solid rgba(140, 170, 207, 0.2);
            background: rgba(12, 20, 30, 0.55);
            color: var(--text-2);
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }
        .nav-pill.active {
            color: var(--teal-2);
            border-color: rgba(78, 205, 196, 0.45);
            background: rgba(78, 205, 196, 0.12);
        }
        .region-tile {
            background: linear-gradient(180deg, rgba(18, 31, 48, 0.96), rgba(11, 19, 31, 0.92));
            border: 1px solid rgba(140, 170, 207, 0.2);
            border-radius: 18px;
            padding: 1rem 0.9rem 0.8rem;
            min-height: 150px;
            box-shadow: 0 8px 18px rgba(4, 10, 18, 0.18);
        }
        .region-label {
            font-size: 0.73rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--text-2);
            margin-bottom: 0.55rem;
        }
        .region-score {
            font-size: 2rem;
            font-weight: 800;
            color: var(--text-1);
            line-height: 1;
            margin-bottom: 0.5rem;
        }
        .region-sub {
            color: var(--text-2);
            font-size: 0.8rem;
            margin-bottom: 0.55rem;
        }
        .mini-bar {
            width: 100%;
            height: 8px;
            border-radius: 999px;
            background: rgba(255,255,255,0.08);
            overflow: hidden;
            margin-top: 0.45rem;
        }
        .mini-fill {
            height: 100%;
            border-radius: inherit;
            background: linear-gradient(90deg, #4ecdc4, #56ccf2);
        }
        .timeline {
            position: relative;
            margin-top: 0.5rem;
            padding-left: 1rem;
            border-left: 1px solid rgba(140, 170, 207, 0.25);
        }
        .timeline-item {
            position: relative;
            margin: 0 0 1rem 0;
            padding-left: 1rem;
        }
        .timeline-item:before {
            content: "";
            position: absolute;
            left: -1.12rem;
            top: 0.3rem;
            width: 10px;
            height: 10px;
            background: var(--teal);
            border-radius: 50%;
            box-shadow: 0 0 12px rgba(78,205,196,0.8);
        }
        .timeline-head {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.2rem;
        }
        .timeline-title {
            color: var(--text-1);
            font-weight: 700;
            font-size: 0.9rem;
        }
        .timeline-time {
            color: var(--text-2);
            font-size: 0.74rem;
        }
        .feed-card {
            background: linear-gradient(180deg, rgba(18, 31, 48, 0.96), rgba(11, 19, 31, 0.92));
            border: 1px solid rgba(140, 170, 207, 0.2);
            border-radius: 16px;
            padding: 0.8rem 0.9rem;
            margin-bottom: 0.8rem;
        }
        .feed-head {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.35rem;
        }
        .feed-title {
            color: var(--text-1);
            font-weight: 700;
            font-size: 0.9rem;
        }
        .feed-meta {
            color: var(--text-2);
            font-size: 0.78rem;
        }
        .main .block-container {
            max-width: 1700px;
            padding: 1.4rem clamp(1rem, 2vw, 2rem) 2.5rem;
        }
        [data-testid="stSidebar"] {
            min-width: 17rem;
            max-width: 17rem;
        }
        [data-testid="stMetric"] {
            min-height: 112px;
            padding: 0.8rem 0.85rem;
            background: linear-gradient(145deg, rgba(19, 34, 49, 0.96), rgba(12, 22, 34, 0.96));
            border-color: rgba(140, 170, 207, 0.22);
        }
        [data-testid="stMetricLabel"] {
            font-size: 0.78rem;
            letter-spacing: 0.04em;
        }
        [data-testid="stMetricValue"] {
            font-size: clamp(1.15rem, 2vw, 1.65rem);
        }
        [data-testid="stMetricValue"] > div {
            overflow-wrap: anywhere;
        }
        [data-testid="stVerticalBlockBorderWrapper"] {
            background: linear-gradient(145deg, rgba(17, 30, 45, 0.9), rgba(10, 19, 30, 0.86));
            border-color: rgba(140, 170, 207, 0.2);
            box-shadow: 0 12px 26px rgba(2, 8, 17, 0.14);
        }
        .brand-strip {
            padding: 0.9rem 1rem;
            background:
                radial-gradient(ellipse at 88% 15%, rgba(78, 205, 196, 0.15), transparent 35%),
                linear-gradient(115deg, #122336 0%, #0c1928 72%);
        }
        .brand-meta span {
            font-size: 1.05rem;
        }
        .brand-meta strong {
            font-size: 0.72rem;
        }
        .brand-status {
            white-space: nowrap;
        }
        .nav-bar {
            flex-wrap: nowrap;
            overflow-x: auto;
            scrollbar-width: none;
            border-bottom: 1px solid rgba(140, 170, 207, 0.15);
            padding-bottom: 0.8rem;
        }
        .nav-bar::-webkit-scrollbar {
            display: none;
        }
        .nav-pill {
            flex: 0 0 auto;
            padding: 0.36rem 0.5rem;
            font-size: 0.61rem;
        }
        .region-tile {
            min-height: 132px;
            padding: 0.9rem 0.85rem 0.75rem;
            transition: transform 160ms ease, border-color 160ms ease;
        }
        .region-tile:hover, .feed-card:hover {
            transform: translateY(-2px);
            border-color: rgba(78, 205, 196, 0.45);
        }
        .feed-card {
            transition: transform 160ms ease, border-color 160ms ease;
        }
        .stDataFrame {
            border-color: rgba(140, 170, 207, 0.24);
        }
        @media (max-width: 760px) {
            [data-testid="stSidebar"] {
                min-width: 0;
                max-width: none;
            }
            .brand-row {
                align-items: flex-start;
            }
            .brand-meta span {
                font-size: 0.92rem;
            }
            .brand-status {
                font-size: 0.62rem;
                padding: 0.35rem 0.55rem;
            }
            .region-score {
                font-size: 1.55rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    np.random.seed(42)

    dates = pd.date_range(start="2024-01-01", periods=180, freq="D")
    regions = ["North America", "Europe", "APAC", "LATAM", "Middle East"]
    threat_types = [
        "Phishing",
        "Credential Stuffing",
        "Ransomware",
        "Malware",
        "DDoS",
        "Insider Threat",
        "Supply Chain",
    ]
    severities = ["Critical", "High", "Medium", "Low"]
    business_units = ["Finance", "Engineering", "Identity", "Operations", "HR", "Support"]
    assets = [
        "VPN Gateway",
        "Finance ERP",
        "Customer Portal",
        "Email Security",
        "Production Cluster",
        "IAM Platform",
        "Endpoint Fleet",
        "Ticketing System",
    ]

    rows = []
    for idx, date in enumerate(dates):
        for _ in range(np.random.randint(1, 4)):
            row = {
                "date": date,
                "region": np.random.choice(regions),
                "threat_type": np.random.choice(threat_types),
                "severity": np.random.choice(severities, p=[0.12, 0.28, 0.42, 0.18]),
                "business_unit": np.random.choice(business_units),
                "asset": np.random.choice(assets),
                "status": np.random.choice(["Open", "Investigating", "Contained", "Mitigated"]),
                "response_time_h": np.random.randint(1, 72),
                "confidence": np.random.randint(60, 98),
                "risk_score": np.random.randint(35, 95),
                "is_active": bool(np.random.randint(0, 2)),
            }
            rows.append(row)

    incidents = pd.DataFrame(rows)
    incidents["date"] = pd.to_datetime(incidents["date"])

    awareness = pd.DataFrame(
        {
            "department": ["Engineering", "Finance", "Support", "Operations", "HR", "Executive"],
            "training_completion": [96, 88, 94, 91, 85, 79],
            "phishing_score": [92, 78, 90, 87, 83, 72],
            "policy_ack": [98, 93, 95, 90, 86, 81],
            "simulation_pass": [94, 81, 88, 86, 80, 73],
        }
    )

    recommendations = [
        {
            "title": "Tighten identity controls",
            "detail": "Prioritize MFA fatigue and session hijacking protections for remote access users.",
            "priority": "Critical",
        },
        {
            "title": "Patch exposed services",
            "detail": "Accelerate remediation for internet-facing assets with pending vendor updates.",
            "priority": "High",
        },
        {
            "title": "Refresh phishing drills",
            "detail": "Increase high-risk teams’ awareness exercises using role-based attacker simulations.",
            "priority": "Medium",
        },
        {
            "title": "Improve threat intel enrichment",
            "detail": "Correlate external IOC feeds with internal telemetry to reduce detection latency.",
            "priority": "High",
        },
    ]

    return incidents, awareness, recommendations


incidents, awareness, recommendations = load_data()

with st.sidebar:
    st.markdown(
        "<div style='text-align:left; font-size:34px; padding:0.2rem 0 0.4rem;'>🛡️</div>",
        unsafe_allow_html=True,
    )
    st.markdown("### Dashboard filters")
    with st.container(border=True):
        start_date = st.date_input("Start date", value=incidents["date"].min().date())
        end_date = st.date_input("End date", value=incidents["date"].max().date())

        selected_regions = st.multiselect(
            "Regions",
            options=sorted(incidents["region"].unique()),
            default=sorted(incidents["region"].unique()),
        )

        selected_types = st.multiselect(
            "Threat types",
            options=sorted(incidents["threat_type"].unique()),
            default=sorted(incidents["threat_type"].unique()),
        )

        risk_threshold = st.slider("Minimum risk score", 0, 100, 50, step=5)

    with st.container(border=True):
        st.markdown("**Analyst brief**")
        st.caption(
            "Demo dataset: identity and phishing exposures remain key focus areas. "
            "Prioritize rapid containment and credential hygiene."
        )

filtered = incidents[
    (incidents["date"] >= pd.Timestamp(start_date))
    & (incidents["date"] <= pd.Timestamp(end_date))
    & (incidents["region"].isin(selected_regions))
    & (incidents["threat_type"].isin(selected_types))
    & (incidents["risk_score"] >= risk_threshold)
].copy()

if filtered.empty:
    filtered = incidents.copy()

st.markdown(
    """
    <div class="brand-strip">
      <div class="brand-row">
        <div class="brand-left">
          <div class="brand-icon">🛡️</div>
          <div class="brand-meta">
            <strong>SOC platform</strong>
            <span>Threat intelligence &amp; awareness</span>
          </div>
        </div>
        <div class="brand-status">Demo environment</div>
      </div>
    </div>
    <div class="nav-bar">
      <span class="nav-pill active">Overview</span>
      <span class="nav-pill">Threat intelligence</span>
      <span class="nav-pill">Awareness</span>
      <span class="nav-pill">Assets</span>
      <span class="nav-pill">Reports</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='section-tag'>Security operations · Executive overview</div>", unsafe_allow_html=True)
st.title("Security posture overview")
st.caption("A clear view of incident activity, regional exposure, and team readiness.")

col1, col2, col3, col4 = st.columns(4)

critical_events = int((filtered["severity"] == "Critical").sum())
high_events = int((filtered["severity"] == "High").sum())
mean_mttr = round(float(filtered["response_time_h"].mean()), 1)
training_completion = round(float(awareness["training_completion"].mean()), 1)

col1.metric("Incidents", f"{len(filtered):,}", f"{critical_events} crit", delta_color="normal")
col2.metric("High risk", f"{high_events:,}", "+8.4%", delta_color="inverse")
col3.metric("MTTR", f"{mean_mttr}h", "hours", delta_color="off")
col4.metric("Training", f"{training_completion}%", "+3.1%", delta_color="normal")

st.markdown("---")

st.subheader("Regional exposure")
region_summary = (
    filtered.groupby("region", as_index=False)
    .agg(
        incidents=("region", "size"),
        critical=("severity", lambda s: int((s == "Critical").sum())),
        avg_risk=("risk_score", "mean"),
    )
    .sort_values("avg_risk", ascending=False)
    .reset_index(drop=True)
)
region_summary["risk_level"] = pd.cut(
    region_summary["avg_risk"],
    bins=[0, 45, 60, 75, 100],
    labels=["Low", "Moderate", "Elevated", "Critical"],
    include_lowest=True,
)
region_summary["risk_color"] = region_summary["risk_level"].map(
    {"Low": "#56ccf2", "Moderate": "#ffd166", "Elevated": "#ff9f43", "Critical": "#ff5d73"}
)

region_cols = st.columns(len(region_summary))
for idx, row in region_summary.iterrows():
    with region_cols[idx]:
        fill_pct = max(15, min(100, int(row["avg_risk"])))
        st.markdown(
            f"""
            <div class="region-tile">
                <div class="region-label">{row['region']}</div>
                <div class="region-score">{int(row['avg_risk'])}</div>
                <div class="region-sub">{row['incidents']} incidents · {row['critical']} critical</div>
                <div class="mini-bar"><div class="mini-fill" style="width: {fill_pct}%; background: linear-gradient(90deg, {row['risk_color']}, #7ee7d9);"></div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("---")

left, right = st.columns([2, 1])

with left:
    st.subheader("Threat trend")
    weekly_activity = (
        filtered.assign(week=filtered["date"].dt.to_period("W").astype(str))
        .groupby("week")
        .size()
        .reset_index(name="events")
    )
    st.line_chart(
        weekly_activity.set_index("week"),
        height=260,
        use_container_width=True,
        color="#4ecdc4",
    )

with right:
    st.subheader("Severity mix")
    severity_breakdown = filtered["severity"].value_counts().reindex(["Critical", "High", "Medium", "Low"], fill_value=0)
    st.bar_chart(
        severity_breakdown.rename("incidents").to_frame(),
        height=260,
        use_container_width=True,
        color="#ff9f43",
    )

mid_left, mid_right = st.columns(2)

with mid_left:
    st.subheader("Attack vectors")
    vector_totals = filtered["threat_type"].value_counts().reset_index()
    vector_totals.columns = ["threat_type", "events"]
    st.bar_chart(
        vector_totals.set_index("threat_type"),
        height=280,
        use_container_width=True,
        color="#7ee7d9",
    )

with mid_right:
    st.subheader("High-risk business units")
    risk_areas = (
        filtered.groupby("business_unit")["risk_score"].mean().sort_values(ascending=False).head(6).reset_index()
    )
    risk_areas.columns = ["business_unit", "avg_risk"]
    st.bar_chart(
        risk_areas.set_index("business_unit"),
        height=280,
        use_container_width=True,
        color="#a78bfa",
    )

st.markdown("---")

timeline_col, feed_col = st.columns([1.4, 1.0])

with timeline_col:
    st.subheader("Incident timeline")
    timeline_df = filtered.sort_values("date").tail(6).copy()
    timeline_df["date_label"] = timeline_df["date"].dt.strftime("%b %d, %Y")
    timeline_items = []
    for _, row in timeline_df.iterrows():
        severity_class = row["severity"].lower()
        timeline_items.append(
            f"<div class='timeline-item'>"
            f"<div class='timeline-head'>"
            f"<span class='timeline-title'>{row['threat_type']}</span>"
            f"<span class='status-chip status-{severity_class}'>{row['severity']}</span>"
            f"</div>"
            f"<div class='timeline-time'>{row['date_label']} · {row['region']} · {row['asset']}</div>"
            f"</div>"
        )
    timeline_html = "<div class='timeline'>" + "".join(timeline_items) + "</div>"
    st.markdown(timeline_html, unsafe_allow_html=True)

with feed_col:
    st.subheader("Live threat feed")
    feed_df = filtered.sort_values("date", ascending=False).head(5).copy()
    for _, row in feed_df.iterrows():
        st.markdown(
            f"""
            <div class="feed-card">
                <div class="feed-head">
                    <span class="feed-title">{row['threat_type']}</span>
                    <span class="status-chip status-{str(row['severity']).lower()}">{row['severity']}</span>
                </div>
                <div class="feed-meta">{row['region']} · {row['business_unit']} · Risk {int(row['risk_score'])}</div>
                <div class="feed-meta">{row['status']} · {row['date'].strftime('%b %d, %Y')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("---")

st.subheader("Recent incident activity")
latest_activity = (
    filtered[
        ["date", "region", "threat_type", "severity", "business_unit", "asset", "status", "risk_score"]
    ]
    .sort_values("date", ascending=False)
    .head(12)
    .rename(
        columns={
            "date": "Date",
            "region": "Region",
            "threat_type": "Threat",
            "severity": "Severity",
            "business_unit": "Business unit",
            "asset": "Asset",
            "status": "Status",
            "risk_score": "Risk",
        }
    )
)
latest_activity["Date"] = latest_activity["Date"].dt.strftime("%Y-%m-%d")
st.dataframe(
    latest_activity,
    hide_index=True,
    use_container_width=True,
    column_config={
        "Date": st.column_config.TextColumn(width="small"),
        "Region": st.column_config.TextColumn(width="medium"),
        "Threat": st.column_config.TextColumn(width="medium"),
        "Severity": st.column_config.TextColumn(width="small"),
        "Business unit": st.column_config.TextColumn(width="medium"),
        "Asset": st.column_config.TextColumn(width="medium"),
        "Status": st.column_config.TextColumn(width="small"),
        "Risk": st.column_config.NumberColumn(format="%d", width="small"),
    },
)

st.subheader("Priority actions")
action_columns = st.columns(len(recommendations))
for column, item in zip(action_columns, recommendations):
    with column:
        priority = item["priority"]
        with st.container(border=True):
            st.markdown(
                f"<span class='status-chip status-{priority.lower()}'>{priority}</span>",
                unsafe_allow_html=True,
            )
            st.markdown(f"**{item['title']}**")
            st.caption(item["detail"])

st.markdown("---")

st.subheader("Department security awareness readiness")
awareness_chart = awareness.set_index("department")
st.bar_chart(
    awareness_chart[["training_completion", "phishing_score", "policy_ack"]],
    height=260,
    use_container_width=True,
    color=["#4ecdc4", "#56ccf2", "#a78bfa"],
)

st.caption("Operational note: security training remains strong overall, but executive and finance cohorts still require targeted phishing simulations and policy reinforcement.")

st.markdown("---")

st.subheader("Risk register")
risk_register = (
    filtered.groupby("asset", as_index=False)
    .agg(
        active_incidents=("is_active", "sum"),
        avg_risk=("risk_score", "mean"),
        highest_severity=("severity", lambda s: s.mode().iloc[0] if not s.empty else "N/A"),
    )
    .sort_values("avg_risk", ascending=False)
    .head(8)
)

risk_register["risk_band"] = pd.cut(
    risk_register["avg_risk"],
    bins=[0, 40, 60, 80, 100],
    labels=["Low", "Moderate", "Elevated", "Critical"],
    include_lowest=True,
)

risk_register["risk_heat"] = risk_register["risk_band"].map(
    {"Low": "#56ccf2", "Moderate": "#ffd166", "Elevated": "#ff9f43", "Critical": "#ff5d73"}
)

display_risk_register = risk_register[
    ["asset", "active_incidents", "avg_risk", "highest_severity", "risk_band"]
].rename(
    columns={
        "asset": "Asset",
        "active_incidents": "Active incidents",
        "avg_risk": "Average risk",
        "highest_severity": "Highest severity",
        "risk_band": "Risk band",
    }
)

st.dataframe(
    display_risk_register,
    hide_index=True,
    use_container_width=True,
    column_config={
        "Asset": st.column_config.TextColumn(width="medium"),
        "Active incidents": st.column_config.NumberColumn(format="%d", width="small"),
        "Average risk": st.column_config.ProgressColumn(
            format="%.1f",
            min_value=0,
            max_value=100,
            width="medium",
        ),
        "Highest severity": st.column_config.TextColumn(width="medium"),
        "Risk band": st.column_config.TextColumn(width="small"),
    },
)

st.caption("Average risk is shown on a 0–100 scale; higher scores indicate greater remediation urgency.")
