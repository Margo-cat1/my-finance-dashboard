import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth

st.set_page_config(page_title="Financial Intelligence PRO", page_icon="📈", layout="wide")

# Авторизация (margo / 456)
credentials = {
    'usernames': {'admin': {'name': 'Admin', 'password': '123'}, 'margo': {'name': 'Margo', 'password': '456'}}}
authenticator = stauth.Authenticate(credentials, 'finance_cookie', 'auth_key', cookie_expiry_days=30)
authenticator.login()

if st.session_state["authentication_status"]:
    LANGS = {
        "Русский": {
            "title": "📊 Финансовый Интеллект",
            "eff_head": "🚀 Эффективность и Окупаемость",
            "sol_head": "🛡️ Устойчивость и Ликвидность",
            "analys_head": "🔍 Автоматический финансовый анализ",
            "guide_head": "📚 Справочник эксперта",
            "assets": "💼 Активы", "liabs": "💸 Обязательства", "ops": "📈 Операционные показатели",
            "qr_label": "Quick Ratio (Ликвидность)",
            "qr_desc": "Показывает способность компании погасить краткосрочные долги за счет кэша.",
            "qr_norm": "Норматив: > 2.0",
            "roi_desc": "ROI (Return on Investment) — окупаемость вложений.",
            "roe_desc": "ROE (Return on Equity) — рентабельность собственного капитала.",
            "status_ok": "✅ Показатель в норме",
            "status_warn": "⚠️ Требует внимания",
            "qr_warn_msg": "Критическая нехватка кэша! QR ниже 2.0",
            "qr_ok_msg": "Ликвидность отличная, кэша достаточно."
        },
        "ქართული": {
            "title": "📊 ფინანსური ინტელექტი",
            "eff_head": "🚀 ეფექტურობა და უკუგება",
            "sol_head": "🛡️ მდგრადობა და ლიკვიდურობა",
            "analys_head": "🔍 ავტომატური ფინანსური ანალიზი",
            "guide_head": "📚 ექსპერტის ცნობარი",
            "assets": "💼 აქტივები", "liabs": "💸 ვალდებულებები", "ops": "📈 ოპერაციული მაჩვენებლები",
            "qr_label": "Quick Ratio (ლიკვიდობა)",
            "qr_desc": "აჩვენებს კომპანიის უნარს დაფაროს მოკლევადიანი ვალები ნაღდი ფულით.",
            "qr_norm": "ნორმატივი: > 2.0",
            "roi_desc": "ROI — ინვესტიციის უკუგება.",
            "roe_desc": "ROE — საკუთარი კაპიტალის რენტაბელობა.",
            "status_ok": "✅ მაჩვენებელი ნორმაშია",
            "status_warn": "⚠️ საჭიროებს ყურადღებას",
            "qr_warn_msg": "ნაღდი ფულის კრიტიკული ნაკლებობა! QR < 2.0",
            "qr_ok_msg": "ლიკვიდობა შესანიშნავია, ნაღდი ფული საკმარისია."
        }
    }

    with st.sidebar:
        lang = st.selectbox("🌐 Language / ენა", list(LANGS.keys()))
        t = LANGS[lang]

        with st.expander(t["assets"]):
            fa = st.number_input("Fixed Assets", value=2100000)
            ca = st.number_input("Current Assets", value=900000)
        with st.expander(t["liabs"]):
            stl = st.number_input("Short-term Debt", value=400000)
            ltl = st.number_input("Long-term Debt", value=1100000)
        with st.expander(t["ops"]):
            cash = st.number_input("Cash", value=300000)
            ebitda = st.number_input("EBITDA", value=450000)
            revenue = st.number_input("Revenue", value=2000000)
            own_cap = st.number_input("Equity", value=1000000)

        authenticator.logout('Logout', 'sidebar')

    # --- МАТЕМАТИЧЕСКИЕ ФОРМУЛЫ ---
    qr = cash / stl if stl != 0 else 0
    roi = (ebitda / (fa + ca) * 100) if (fa + ca) != 0 else 0
    roe = (ebitda / own_cap * 100) if own_cap != 0 else 0
    ros = (ebitda / revenue * 100) if revenue != 0 else 0

    st.title(t["title"])
    tab1, tab2, tab3 = st.tabs(["🎯 Dashboard", "🔍 Analysis", "📚 Guide"])

    with tab1:
        st.subheader(t["eff_head"])
        c1, c2, c3 = st.columns(3)
        c1.metric("ROI", f"{roi:.1f}%")
        c2.metric("ROE", f"{roe:.1f}%")
        c3.metric("ROS", f"{ros:.1f}%")

        st.subheader(t["sol_head"])
        st.metric(t["qr_label"], f"{qr:.2f}", delta=round(qr - 2.0, 2))
        if qr < 2.0:
            st.error(t["qr_warn_msg"])
        else:
            st.success(t["qr_ok_msg"])

    with tab2:
        st.header(t["analys_head"])
        # Автоматический анализ QR по твоему нормативу 2.0
        if qr < 2.0:
            st.error(f"❌ **Quick Ratio ({qr:.2f})**: {t['status_warn']}. {t['qr_norm']}.")
        else:
            st.success(f"💎 **Quick Ratio ({qr:.2f})**: {t['status_ok']}.")

        # Анализ рентабельности
        if roe > 20:
            st.success(f"🔥 **ROE ({roe:.1f}%)**: Высокая эффективность капитала.")
        else:
            st.warning(f"📉 **ROE ({roe:.1f}%)**: Ниже целевых 20%.")

    with tab3:
        st.header(t["guide_head"])
        st.markdown(f"### {t['qr_label']}")
        st.write(t["qr_desc"])
        st.code("Formula: Cash / Short-term Debt")
        st.info(f"**{t['qr_norm']}**")

        st.markdown("---")
        st.markdown(f"### ROI & ROE")
        st.write(t["roi_desc"])
        st.write(t["roe_desc"])
        st.info("**Цель для ROE: > 20%**")

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')