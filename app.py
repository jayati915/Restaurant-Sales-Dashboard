import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from utils.insights import generate_insight, get_kpis

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Hide default Streamlit page nav + theme-adaptive CSS ──────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono&display=swap');

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

    /* Hide auto-generated sidebar page links */
    [data-testid="stSidebarNav"] { display: none !important; }

    /* KPI Cards — inherit theme background */
    .kpi-card {
        background-color: var(--secondary-background-color);
        border-radius: 12px;
        padding: 20px 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        border-left: 4px solid #4f8ef7;
    }
    .kpi-label {
        font-size: 12px;
        font-weight: 500;
        color: var(--text-color);
        opacity: 0.6;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 26px;
        font-weight: 600;
        color: var(--text-color);
        font-family: 'DM Mono', monospace;
    }
    .kpi-sub {
        font-size: 12px;
        color: var(--text-color);
        opacity: 0.45;
        margin-top: 4px;
    }

    /* Section headers */
    .section-header {
        font-size: 15px;
        font-weight: 600;
        color: var(--text-color);
        padding-bottom: 8px;
        border-bottom: 1.5px solid rgba(128,128,128,0.2);
        margin-bottom: 16px;
    }

    /* Insight bar — always has its own bg so always readable */
    .insight-bar {
        background: linear-gradient(135deg, #3b5bdb 0%, #4f8ef7 100%);
        border-radius: 10px;
        padding: 14px 20px;
        color: #ffffff;
        font-size: 13px;
        font-weight: 400;
        letter-spacing: 0.01em;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: var(--text-color);
        opacity: 0.35;
        font-size: 11px;
        padding-top: 24px;
        border-top: 1px solid rgba(128,128,128,0.2);
        margin-top: 32px;
    }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 Sales Dashboard")
    st.markdown("---")
    st.markdown("### Filter Options")

    try:
        df = pd.read_csv("data/sales_data.csv")

        all_regions = sorted(df["region"].unique().tolist())
        all_statuses = sorted(df["status"].unique().tolist())

        # Region filter
        select_all = st.checkbox("Select All Regions", value=True)
        if select_all:
            selected_regions = all_regions
            st.multiselect("Choose Region(s)", options=all_regions, default=all_regions, disabled=True)
        else:
            selected_regions = st.multiselect("Choose Region(s)", options=all_regions, default=[])

        st.markdown(" ")

        # Status filter
        selected_statuses = st.multiselect(
            "Filter by Status",
            options=all_statuses,
            default=all_statuses
        )
        ### Reports button
        st.markdown("### Reports")
        st.page_link("pages/reports.py", label="📋 View Full Report", icon=None)


        st.markdown("---")
        st.caption(f"Last refreshed: {datetime.now().strftime('%b %d, %Y %H:%M')}")

    except Exception as e:
        st.error(f"❌ Failed to load data: {e}")
        st.stop()


# ── Main Content ──────────────────────────────────────────────────────────────
st.markdown("## 📊 Sales Dashboard")
region_label = "All Regions" if select_all else (", ".join(selected_regions) if selected_regions else "No Region")
st.caption(f"Showing data for **{region_label}**")

# Filter data
if not selected_regions or not selected_statuses:
    filtered_df = pd.DataFrame(columns=df.columns)
else:
    filtered_df = df[
        df["region"].isin(selected_regions) &
        df["status"].isin(selected_statuses)
    ]

if filtered_df.empty:
    st.warning("⚠️ No data to display. Adjust your filters.")
    st.stop()

# ── KPI Cards ─────────────────────────────────────────────────────────────────
kpis = get_kpis(filtered_df)
k1, k2, k3, k4 = st.columns(4)

cards = [
    (k1, "Total Revenue",    f"${kpis['total_sales']:,.0f}",        "across all selected regions", "#4f8ef7"),
    (k2, "Total Orders",     f"{kpis['total_orders']:,}",            f"completion rate: {kpis['completion_rate']}%", "#10b981"),
    (k3, "Avg Order Value",  f"${kpis['avg_order_value']:,.0f}",     "per transaction", "#f59e0b"),
    (k4, "Top Region",       kpis['top_region'],                     f"best-seller: {kpis['top_product']}", "#8b5cf6"),
]

for col, label, value, sub, color in cards:
    with col:
        st.markdown(f"""<div class="kpi-card" style="border-left-color:{color}">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value" style="font-size:{'20px' if len(str(value)) > 10 else '26px'}">{value}</div>
            <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Plotly theme helper — transparent bg, respects Streamlit theme ────────────
def chart_layout(fig, **kwargs):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans"),
        margin=dict(t=10, b=10, l=0, r=0),
        **kwargs
    )
    fig.update_xaxes(gridcolor="rgba(128,128,128,0.15)", zerolinecolor="rgba(128,128,128,0.15)")
    fig.update_yaxes(gridcolor="rgba(128,128,128,0.15)", zerolinecolor="rgba(128,128,128,0.15)")
    return fig

COLORS = ["#4f8ef7", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"]

# ── Charts Row 1 ──────────────────────────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    st.markdown('<div class="section-header">📦 Sales by Product</div>', unsafe_allow_html=True)
    fig1 = px.bar(
        filtered_df.groupby(["product", "status"])["total_sales"].sum().reset_index(),
        x="product", y="total_sales", color="status",
        color_discrete_sequence=COLORS
    )
    chart_layout(fig1,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_title="", yaxis_title="Total Sales ($)"
    )
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.markdown('<div class="section-header">🌍 Revenue by Region</div>', unsafe_allow_html=True)
    region_totals = filtered_df.groupby("region")["total_sales"].sum().reset_index()
    fig2 = px.pie(
        region_totals, values="total_sales", names="region",
        hole=0.45, color_discrete_sequence=COLORS
    )
    chart_layout(fig2, legend=dict(orientation="h", yanchor="bottom", y=-0.2))
    st.plotly_chart(fig2, use_container_width=True)

# ── Charts Row 2 ──────────────────────────────────────────────────────────────
c3, c4 = st.columns(2)

with c3:
    st.markdown('<div class="section-header">🗺️ Region vs Product Heatmap</div>', unsafe_allow_html=True)
    heatmap_df = filtered_df.pivot_table(
        index="region", columns="product", values="total_sales", aggfunc="sum"
    ).fillna(0)
    fig3 = px.imshow(heatmap_df, text_auto=".0f", aspect="auto", color_continuous_scale="Blues")
    chart_layout(fig3, xaxis_title="", yaxis_title="")
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    st.markdown('<div class="section-header">📋 Order Status Breakdown</div>', unsafe_allow_html=True)
    status_df = filtered_df.groupby("status")["total_sales"].sum().reset_index()
    fig4 = px.bar(
        status_df, x="status", y="total_sales",
        color="status", color_discrete_sequence=COLORS
    )
    chart_layout(fig4, showlegend=False, xaxis_title="", yaxis_title="Total Sales ($)")
    st.plotly_chart(fig4, use_container_width=True)

# ── Data Table ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🗃️ Filtered Data Table</div>', unsafe_allow_html=True)
st.dataframe(filtered_df, use_container_width=True, hide_index=True)

# ── AI Insight Bar ────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-header">🔍 AI Insight</div>', unsafe_allow_html=True)
st.markdown(f'<div class="insight-bar">{generate_insight(filtered_df)}</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(f'<div class="footer">Sales Dashboard · Generated {datetime.now().strftime("%B %d, %Y")}</div>', unsafe_allow_html=True)