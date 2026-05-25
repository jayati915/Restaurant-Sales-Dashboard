import pandas as pd


def generate_insight(df):
    if df.empty:
        return "No data available for the selected region(s)."

    top_product = df.groupby("product")["total_sales"].sum().idxmax()
    total = df["total_sales"].sum()
    avg_order = df["total_sales"].mean()
    top_status = df.groupby("status")["total_sales"].sum().idxmax()
    num_orders = len(df)

    return (
        f"💰 Total sales: ${total:,.2f}   |   "
        f"🔥 Best-seller: {top_product}   |   "
        f"📦 Avg order value: ${avg_order:,.2f}   |   "
        f"✅ Top status: {top_status}   |   "
        f"🧾 Orders: {num_orders}"
    )


def get_kpis(df):
    if df.empty:
        return {}
    return {
        "total_sales": df["total_sales"].sum(),
        "total_orders": len(df),
        "avg_order_value": df["total_sales"].mean(),
        "top_region": df.groupby("region")["total_sales"].sum().idxmax(),
        "top_product": df.groupby("product")["total_sales"].sum().idxmax(),
        "top_status": df.groupby("status")["total_sales"].sum().idxmax(),
        "completion_rate": round(
            len(df[df["status"].str.lower() == "completed"]) / len(df) * 100, 1
        ) if "completed" in df["status"].str.lower().values else 0,
    }


def get_report_insights(df):
    """Returns a list of structured insight dicts for the Reports page."""
    if df.empty:
        return []

    insights = []

    # --- Revenue by region ---
    region_sales = df.groupby("region")["total_sales"].sum().sort_values(ascending=False)
    top_region = region_sales.index[0]
    bottom_region = region_sales.index[-1]
    total = region_sales.sum()
    top_pct = round(region_sales[top_region] / total * 100, 1)

    insights.append({
        "category": "Revenue Performance",
        "icon": "💰",
        "title": f"{top_region} leads all regions",
        "detail": f"{top_region} contributes {top_pct}% of total revenue (${region_sales[top_region]:,.2f}). "
                  f"{bottom_region} is the lowest at ${region_sales[bottom_region]:,.2f}.",
        "type": "positive"
    })

    # --- Product performance ---
    product_sales = df.groupby("product")["total_sales"].sum().sort_values(ascending=False)
    top_product = product_sales.index[0]
    top_product_pct = round(product_sales[top_product] / product_sales.sum() * 100, 1)

    insights.append({
        "category": "Product Performance",
        "icon": "📦",
        "title": f"{top_product} is the top-selling product",
        "detail": f"{top_product} accounts for {top_product_pct}% of total product revenue "
                  f"(${product_sales[top_product]:,.2f}). Consider prioritizing inventory for this product.",
        "type": "positive"
    })

    # --- Order status ---
    status_counts = df["status"].value_counts()
    status_pct = (status_counts / status_counts.sum() * 100).round(1)
    pending_pct = status_pct.get("Pending", status_pct.get("pending", 0))
    completed_pct = status_pct.get("Completed", status_pct.get("completed", 0))

    insights.append({
        "category": "Order Health",
        "icon": "✅",
        "title": f"{completed_pct}% of orders are completed",
        "detail": f"Completion rate stands at {completed_pct}%. "
                  + (f"Pending orders make up {pending_pct}% — worth monitoring for fulfillment delays."
                     if pending_pct > 0 else ""),
        "type": "positive" if completed_pct >= 70 else "warning"
    })

    # --- Avg order value by region ---
    avg_by_region = df.groupby("region")["total_sales"].mean().sort_values(ascending=False)
    high_aov_region = avg_by_region.index[0]

    insights.append({
        "category": "Strategic Opportunity",
        "icon": "🎯",
        "title": f"{high_aov_region} has the highest average order value",
        "detail": f"Customers in {high_aov_region} spend an average of ${avg_by_region[high_aov_region]:,.2f} per order — "
                  f"the highest across all regions. This is a high-value market worth investing in.",
        "type": "positive"
    })

    # --- Pending orders flag ---
    if "status" in df.columns:
        pending_by_region = df[df["status"].str.lower() == "pending"].groupby("region").size()
        if not pending_by_region.empty:
            worst_region = pending_by_region.idxmax()
            insights.append({
                "category": "Risk Flag",
                "icon": "⚠️",
                "title": f"{worst_region} has the most pending orders",
                "detail": f"{worst_region} has {pending_by_region[worst_region]} pending orders — "
                          f"highest across all regions. Investigate potential fulfillment or pipeline issues.",
                "type": "warning"
            })

    return insights