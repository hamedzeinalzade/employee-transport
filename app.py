# app.py

import streamlit as st
import pandas as pd
from core.service import compute_optimized_routes

st.set_page_config(
    page_title="سیستم هوشمند مسیر‌یابی سرویس کارکنان",
    layout="wide"
)

st.title("🚍 سیستم هوشمند بهینه‌سازی مسیر سرویس کارکنان")

addresses = st.text_area(
    "📍 آدرس کارکنان را وارد کنید (هر آدرس در یک خط):",
    height=200,
    placeholder="تهران، سعادت‌آباد، خیابان ..."
)

if st.button("🚦 محاسبه مسیرهای بهینه"):
    addr_list = [a.strip() for a in addresses.split("\n") if a.strip()]

    with st.spinner("⏳ در حال محاسبه مسیرها..."):
        routes = compute_optimized_routes(addr_list)

    if not routes:
        st.warning("⚠️ هیچ آدرس معتبری شناسایی نشد.")
    else:
        st.subheader("🛣️ نتیجه مسیرهای پیشنهادی")

        for r in routes:
            st.write(f"🚌 **سرویس شماره {r['bus_id']}**")
            st.write(f"مسیر (اندیس نقاط): {r['route_indices']}")
            st.divider()

        st.success("✅ محاسبه مسیرها با موفقیت انجام شد.")
