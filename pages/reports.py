# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from datetime import datetime
# from utils.insights import get_kpis, get_report_insights

# st.set_page_config(
#     page_title="Sales Report",
#     page_icon="📋",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # ── Custom CSS ────────────────────────────────────────────────────────────────
# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono&display=swap');

#     html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
#     .main { background-color: #f8f9fc; }

#     .report-header {
#         background: linear-gradient(135deg, #1e3a5f 0%, #2d5986 100%);
#         border-radius: 16px;
#         padding: 40px 48px;
#         color: white;
#         margin-bottom: 32px;
#     }
#     .report-title {
#         font-size: 32px;
#         font-weight: 700;
#         letter-spacing: -0.02em;
#         margin-bottom: 6px;
#     }
#     .report-subtitle {
#         font-size: 15px;
#         opacity: 0.75;
#         font-weight: 300;
#     }
#     .report-date {
#         font-size: 12px;
#         opacity: 0.6;
#         margin-top: 12px;
#         font-family: 'DM Mono', monospace;
#     }

#     .kpi-card {
#         background: white;
#         border-radius: 12px;
#         padding: 22px 26px;
#         box-shadow: 0 1px 4px rgba(0,0,0,0.07);
#         border-top: 4px solid #2d5986;
#         text-align: center;
#     }
#     .kpi-label {
#         font-size: 11px;
#         font-weight: 600;
#         color: #6b7280;
#         text-transform: uppercase;
#         letter-spacing: 0.08em;
#         margin-bottom: 8px;
#     }
#     .kpi-value {
#         font-size: 28px;
#         font-weight: 700;
#         color: #111827;
#         font-family: 'DM Mono', monospace;
#     }
#     .kpi-sub {
#         font-size: 12px;
#         color: #9ca3af;
#         margin-top: 5px;
#     }

#     .section-title {
#         font-size: 18px;
#         font-weight: 600;
#         color: #1f2937;
#         margin: 32px 0 16px 0;
#         padding-bottom: 10px;
#         border-bottom: 2px solid #e5e7eb;
#     }

#     .insight-card {
#         background: white;
#         border-radius: 12px;
#         padding: 20px 24px;
#         margin-bottom: 14px;
#         box-shadow: 0 1px 3px rgba(0,0,0,0.06);
#         border-left: 5px solid #2d5986;
#     }
#     .insight-card.warning {
#         border-left-color: #f59e0b;
#     }
#     .insight-category {
#         font-size: 10px;
#         font-weight: 600;
#         text-transform: uppercase;
#         letter-spacing: 0.1em;
#         color: #6b7280;
#         margin-bottom: 6px;
#     }
#     .insight-title {
#         font-size: 15px;
#         font-weight: 600;
#         color: #111827;
#         margin-bottom: 6px;
#     }
#     .insight-detail {
#         font-size: 13px;
#         color: #4b5563;
#         line-height: 1.6;
#     }

#     .summary-box {
#         background: #f0f4ff;
#         border-radius: 12px;
#         padding: 24px 28px;
#         border: 1px solid #c7d7f9;
#         margin-bottom: 24px;
#     }
#     .summary-title {
#         font-size: 14px;
#         font-weight: 600;
#         color: #1e3a5f;
#         margin-bottom: 10px;
#     }
#     .summary-text {
#         font-size: 13px;
#         color: #374151;
#         line-height: 1.7;
#     }

#     .footer {
#         text-align: center;
#         color: #9ca3af;
#         font-size: 11px;
#         padding: 24px 0 8px;
#         border-top: 1px solid #e5e7eb;
#         margin-top: 40px;
#     }

#     div[data-testid="stButton"] > button {
#         background: white;
#         color: #2d5986;
#         border: 1.5px solid #2d5986;
#         border-radius: 8px;
#         padding: 8px 20px;
#         font-weight: 500;
#         font-size: 13px;
#     }
#     div[data-testid="stButton"] > button:hover {
#         background: #2d5986;
#         color: white;
#     }
# </style>
# """, unsafe_allow_html=True)

# # ── Load Data ─────────────────────────────────────────────────────────────────
# try:
#     df = pd.read_csv("data/sales_data.csv")
# except Exception as e:
#     st.error(f"❌ Could not load data: {e}")
#     st.stop()

# kpis = get_kpis(df)
# insights = get_report_insights(df)

# # ── Back Button ───────────────────────────────────────────────────────────────
# col_back, _ = st.columns([1, 7])
# with col_back:
#     st.page_link("app.py", label="← Back to Dashboard")

# # ── Report Header ─────────────────────────────────────────────────────────────
# st.markdown(f"""
# <div class="report-header">
#     <div class="report-title">📋 Sales Performance Report</div>
#     <div class="report-subtitle">Executive summary across all regions and products</div>
#     <div class="report-date">Generated on {datetime.now().strftime("%B %d, %Y at %H:%M")}</div>
# </div>
# """, unsafe_allow_html=True)

# # ── KPI Summary ───────────────────────────────────────────────────────────────
# st.markdown('<div class="section-title">Key Performance Indicators</div>', unsafe_allow_html=True)

# k1, k2, k3, k4, k5 = st.columns(5)

# metrics = [
#     (k1, "Total Revenue", f"${kpis['total_sales']:,.0f}", "all regions combined", "#2d5986"),
#     (k2, "Total Orders", f"{kpis['total_orders']:,}", f"{kpis['completion_rate']}% completed", "#10b981"),
#     (k3, "Avg Order Value", f"${kpis['avg_order_value']:,.0f}", "per transaction", "#f59e0b"),
#     (k4, "Top Region", kpis['top_region'], "highest revenue", "#8b5cf6"),
#     (k5, "Top Product", kpis['top_product'], "best-selling item", "#ef4444"),
# ]

# for col, label, value, sub, color in metrics:
#     with col:
#         st.markdown(f"""<div class="kpi-card" style="border-top-color:{color}">
#             <div class="kpi-label">{label}</div>
#             <div class="kpi-value" style="font-size:{'22px' if len(str(value)) > 8 else '28px'}">{value}</div>
#             <div class="kpi-sub">{sub}</div>
#         </div>""", unsafe_allow_html=True)

# # ── Executive Summary ─────────────────────────────────────────────────────────
# st.markdown('<div class="section-title">Executive Summary</div>', unsafe_allow_html=True)

# region_sales = df.groupby("region")["total_sales"].sum().sort_values(ascending=False)
# top_r = region_sales.index[0]
# top_r_pct = round(region_sales[top_r] / region_sales.sum() * 100, 1)
# product_sales = df.groupby("product")["total_sales"].sum()
# top_p = product_sales.idxmax()

# st.markdown(f"""
# <div class="summary-box">
#     <div class="summary-title">Summary for Management</div>
#     <div class="summary-text">
#         Total revenue across all regions reached <strong>${kpis['total_sales']:,.2f}</strong> from
#         <strong>{kpis['total_orders']:,} orders</strong>, with an average order value of
#         <strong>${kpis['avg_order_value']:,.2f}</strong>. <strong>{top_r}</strong> is the
#         highest-performing region, contributing <strong>{top_r_pct}%</strong> of overall revenue.
#         <strong>{top_p}</strong> remains the best-selling product. The overall completion rate
#         stands at <strong>{kpis['completion_rate']}%</strong>, reflecting operational health
#         across the sales pipeline.
#     </div>
# </div>
# """, unsafe_allow_html=True)

# # ── Key Insights ──────────────────────────────────────────────────────────────
# st.markdown('<div class="section-title">Key Insights</div>', unsafe_allow_html=True)

# for insight in insights:
#     card_class = "insight-card warning" if insight["type"] == "warning" else "insight-card"
#     st.markdown(f"""
#     <div class="{card_class}">
#         <div class="insight-category">{insight['icon']} {insight['category']}</div>
#         <div class="insight-title">{insight['title']}</div>
#         <div class="insight-detail">{insight['detail']}</div>
#     </div>
#     """, unsafe_allow_html=True)

# # ── Charts ────────────────────────────────────────────────────────────────────
# st.markdown('<div class="section-title">Visual Breakdown</div>', unsafe_allow_html=True)

# c1, c2 = st.columns(2)

# with c1:
#     region_df = df.groupby("region")["total_sales"].sum().reset_index().sort_values("total_sales", ascending=True)
#     fig1 = px.bar(
#         region_df, x="total_sales", y="region", orientation="h",
#         template="plotly_white",
#         color_discrete_sequence=["#2d5986"]
#     )
#     fig1.update_layout(
#         title="Revenue by Region",
#         plot_bgcolor="white", paper_bgcolor="white",
#         margin=dict(t=40, b=10, l=0, r=0),
#         xaxis_title="Total Sales ($)", yaxis_title="",
#         font=dict(family="DM Sans", size=12)
#     )
#     st.plotly_chart(fig1, use_container_width=True)

# with c2:
#     product_df = df.groupby("product")["total_sales"].sum().reset_index().sort_values("total_sales", ascending=True)
#     fig2 = px.bar(
#         product_df, x="total_sales", y="product", orientation="h",
#         template="plotly_white",
#         color_discrete_sequence=["#10b981"]
#     )
#     fig2.update_layout(
#         title="Revenue by Product",
#         plot_bgcolor="white", paper_bgcolor="white",
#         margin=dict(t=40, b=10, l=0, r=0),
#         xaxis_title="Total Sales ($)", yaxis_title="",
#         font=dict(family="DM Sans", size=12)
#     )
#     st.plotly_chart(fig2, use_container_width=True)

# c3, c4 = st.columns(2)

# with c3:
#     status_df = df.groupby("status")["total_sales"].sum().reset_index()
#     fig3 = px.pie(
#         status_df, values="total_sales", names="status",
#         hole=0.5, template="plotly_white",
#         color_discrete_sequence=["#2d5986", "#10b981", "#f59e0b", "#ef4444"]
#     )
#     fig3.update_layout(
#         title="Sales by Order Status",
#         margin=dict(t=40, b=10, l=0, r=0),
#         font=dict(family="DM Sans", size=12),
#         legend=dict(orientation="h", y=-0.2)
#     )
#     st.plotly_chart(fig3, use_container_width=True)

# with c4:
#     heatmap_df = df.pivot_table(index="region", columns="product", values="total_sales", aggfunc="sum").fillna(0)
#     fig4 = px.imshow(
#         heatmap_df, text_auto=".0f", aspect="auto",
#         color_continuous_scale="Blues", template="plotly_white"
#     )
#     fig4.update_layout(
#         title="Region × Product Heatmap",
#         margin=dict(t=40, b=10, l=0, r=0),
#         font=dict(family="DM Sans", size=12),
#         xaxis_title="", yaxis_title=""
#     )
#     st.plotly_chart(fig4, use_container_width=True)

# # ── Footer ────────────────────────────────────────────────────────────────────
# st.markdown(f'<div class="footer">Confidential · Sales Performance Report · {datetime.now().strftime("%B %Y")}</div>', unsafe_allow_html=True)


import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from utils.insights import get_kpis, get_report_insights

st.set_page_config(
    page_title="Sales Report",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Hide default page nav + theme-adaptive CSS ────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono&display=swap');

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

    /* Hide auto-generated sidebar page links */
    [data-testid="stSidebarNav"] { display: none !important; }

    /* Report header — always dark blue bg so text is always white */
    .report-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d5986 100%);
        border-radius: 16px;
        padding: 40px 48px;
        color: #ffffff;
        margin-bottom: 32px;
    }
    .report-title   { font-size: 32px; font-weight: 700; letter-spacing: -0.02em; margin-bottom: 6px; }
    .report-subtitle { font-size: 15px; opacity: 0.75; font-weight: 300; }
    .report-date    { font-size: 12px; opacity: 0.55; margin-top: 12px; font-family: 'DM Mono', monospace; }

    /* KPI cards */
    .kpi-card {
        background-color: var(--secondary-background-color);
        border-radius: 12px;
        padding: 22px 26px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        border-top: 4px solid #2d5986;
        text-align: center;
    }
    .kpi-label {
        font-size: 11px; font-weight: 600;
        color: var(--text-color); opacity: 0.55;
        text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 28px; font-weight: 700;
        color: var(--text-color);
        font-family: 'DM Mono', monospace;
    }
    .kpi-sub { font-size: 12px; color: var(--text-color); opacity: 0.4; margin-top: 5px; }

    /* Section titles */
    .section-title {
        font-size: 18px; font-weight: 600;
        color: var(--text-color);
        margin: 32px 0 16px 0;
        padding-bottom: 10px;
        border-bottom: 1.5px solid rgba(128,128,128,0.2);
    }

    /* Insight cards */
    .insight-card {
        background-color: var(--secondary-background-color);
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 14px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.07);
        border-left: 5px solid #2d5986;
    }
    .insight-card.warning { border-left-color: #f59e0b; }
    .insight-category {
        font-size: 10px; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.1em;
        color: var(--text-color); opacity: 0.5; margin-bottom: 6px;
    }
    .insight-title  { font-size: 15px; font-weight: 600; color: var(--text-color); margin-bottom: 6px; }
    .insight-detail { font-size: 13px; color: var(--text-color); opacity: 0.75; line-height: 1.6; }

    /* Summary box */
    .summary-box {
        background-color: var(--secondary-background-color);
        border-radius: 12px;
        padding: 24px 28px;
        border: 1px solid rgba(128,128,128,0.2);
        margin-bottom: 24px;
    }
    .summary-title { font-size: 14px; font-weight: 600; color: var(--text-color); margin-bottom: 10px; }
    .summary-text  { font-size: 13px; color: var(--text-color); opacity: 0.8; line-height: 1.7; }

    /* Footer */
    .footer {
        text-align: center;
        color: var(--text-color); opacity: 0.35;
        font-size: 11px;
        padding: 24px 0 8px;
        border-top: 1px solid rgba(128,128,128,0.2);
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────────────────────────
try:
    df = pd.read_csv("data/sales_data.csv")
except Exception as e:
    st.error(f"❌ Could not load data: {e}")
    st.stop()

kpis = get_kpis(df)
insights = get_report_insights(df)

# ── Back link ─────────────────────────────────────────────────────────────────
st.page_link("app.py", label="← Back to Dashboard")

# ── Report Header ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="report-header">
    <div class="report-title">📋 Sales Performance Report</div>
    <div class="report-subtitle">Executive summary across all regions and products</div>
    <div class="report-date">Generated on {datetime.now().strftime("%B %d, %Y at %H:%M")}</div>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ─────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Key Performance Indicators</div>', unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)
metrics = [
    (k1, "Total Revenue",   f"${kpis['total_sales']:,.0f}",       "all regions combined",  "#2d5986"),
    (k2, "Total Orders",    f"{kpis['total_orders']:,}",           f"{kpis['completion_rate']}% completed", "#10b981"),
    (k3, "Avg Order Value", f"${kpis['avg_order_value']:,.0f}",    "per transaction",       "#f59e0b"),
    (k4, "Top Region",      kpis['top_region'],                    "highest revenue",       "#8b5cf6"),
    (k5, "Top Product",     kpis['top_product'],                   "best-selling item",     "#ef4444"),
]
for col, label, value, sub, color in metrics:
    with col:
        st.markdown(f"""<div class="kpi-card" style="border-top-color:{color}">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value" style="font-size:{'20px' if len(str(value)) > 8 else '28px'}">{value}</div>
            <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

# ── Executive Summary ─────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Executive Summary</div>', unsafe_allow_html=True)

region_sales  = df.groupby("region")["total_sales"].sum().sort_values(ascending=False)
top_r         = region_sales.index[0]
top_r_pct     = round(region_sales[top_r] / region_sales.sum() * 100, 1)
top_p         = df.groupby("product")["total_sales"].sum().idxmax()

st.markdown(f"""
<div class="summary-box">
    <div class="summary-title">Summary for Management</div>
    <div class="summary-text">
        Total revenue across all regions reached <strong>${kpis['total_sales']:,.2f}</strong> from
        <strong>{kpis['total_orders']:,} orders</strong>, with an average order value of
        <strong>${kpis['avg_order_value']:,.2f}</strong>. <strong>{top_r}</strong> is the
        highest-performing region, contributing <strong>{top_r_pct}%</strong> of overall revenue.
        <strong>{top_p}</strong> remains the best-selling product. The overall completion rate
        stands at <strong>{kpis['completion_rate']}%</strong>, reflecting operational health
        across the sales pipeline.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Key Insights ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Key Insights</div>', unsafe_allow_html=True)

for insight in insights:
    card_class = "insight-card warning" if insight["type"] == "warning" else "insight-card"
    st.markdown(f"""
    <div class="{card_class}">
        <div class="insight-category">{insight['icon']} {insight['category']}</div>
        <div class="insight-title">{insight['title']}</div>
        <div class="insight-detail">{insight['detail']}</div>
    </div>""", unsafe_allow_html=True)

# ── Charts ────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Visual Breakdown</div>', unsafe_allow_html=True)

def chart_layout(fig, **kwargs):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", size=12),
        margin=dict(t=40, b=10, l=0, r=0),
        **kwargs
    )
    fig.update_xaxes(gridcolor="rgba(128,128,128,0.15)", zerolinecolor="rgba(128,128,128,0.15)")
    fig.update_yaxes(gridcolor="rgba(128,128,128,0.15)", zerolinecolor="rgba(128,128,128,0.15)")
    return fig

COLORS = ["#2d5986", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"]

c1, c2 = st.columns(2)

with c1:
    region_df = df.groupby("region")["total_sales"].sum().reset_index().sort_values("total_sales")
    fig1 = px.bar(region_df, x="total_sales", y="region", orientation="h", color_discrete_sequence=COLORS)
    chart_layout(fig1, title="Revenue by Region", xaxis_title="Total Sales ($)", yaxis_title="")
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    product_df = df.groupby("product")["total_sales"].sum().reset_index().sort_values("total_sales")
    fig2 = px.bar(product_df, x="total_sales", y="product", orientation="h", color_discrete_sequence=["#10b981"])
    chart_layout(fig2, title="Revenue by Product", xaxis_title="Total Sales ($)", yaxis_title="")
    st.plotly_chart(fig2, use_container_width=True)

c3, c4 = st.columns(2)

with c3:
    status_df = df.groupby("status")["total_sales"].sum().reset_index()
    fig3 = px.pie(status_df, values="total_sales", names="status", hole=0.5, color_discrete_sequence=COLORS)
    chart_layout(fig3, title="Sales by Order Status", legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    heatmap_df = df.pivot_table(index="region", columns="product", values="total_sales", aggfunc="sum").fillna(0)
    fig4 = px.imshow(heatmap_df, text_auto=".0f", aspect="auto", color_continuous_scale="Blues")
    chart_layout(fig4, title="Region × Product Heatmap", xaxis_title="", yaxis_title="")
    st.plotly_chart(fig4, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(f'<div class="footer">Confidential · Sales Performance Report · {datetime.now().strftime("%B %Y")}</div>', unsafe_allow_html=True)