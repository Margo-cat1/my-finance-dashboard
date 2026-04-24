import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth

# 1. Настройка страницы
st.set_page_config(page_title="Financial Intelligence PRO", page_icon="📈", layout="wide")

# --- БЛОК АВТОРИЗАЦИИ (admin123 / margo456) ---
credentials = {
    'usernames': {
        'admin': {
            'name': 'Admin User',
            'password': 'pbkdf2:sha256:600000$p6U7W7Wv$8f8a379c65697d81747864f19b26618451733675f922759e691238626f212234'
        },
        'margo': {
            'name': 'Margo',
            'password': 'pbkdf2:sha256:600000$TjYp9z1a$c4921b71478225e30528e6789f2122341733675f922759e691238626f212234'
        }
    }
}

authenticator = stauth.Authenticate(credentials, 'finance_cookie', 'auth_key', cookie_expiry_days=30)
authenticator.login()

if st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
elif st.session_state["authentication_status"]:

    # --- ПРИЛОЖЕНИЕ ПОСЛЕ ВХОДА ---
    with st.sidebar:
        st.write(f'Welcome, *{st.session_state["name"]}*')
        authenticator.logout('Logout', 'sidebar')

    LANGS = {
        "Русский": {
            "title": "📊 Финансовый Интеллект",
            "eff_head": "🚀 Эффективность (EBITDA)",
            "sol_head": "🛡️ Устойчивость и Ликвидность",
            "analys_head": "🔍 Автоматический анализ",
            "guide_head": "📚 Справочник нормативов",
            "assets": "💼 Активы", "liabs": "💸 Долги", "ops": "📈 Операционка",
            "qr_label": "Quick Ratio (Ликвидность)",
            "qr_guide": "**Quick Ratio:** Минимум: **2.0**. У вас должно быть в 2 раза больше кэша, чем срочных долгов.",
            "roi_guide": "**ROI:** Цель: **> 25%**. Показывает окупаемость вложений.",
            "roe_guide": "**ROE:** Цель: **> 20%**. Эффективность использования капитала.",
            "warn_qr": "⚠️ QR ниже нормы 2.0!",
            "success_qr": "✅ Ликвидность в норме (QR > 2.0)"
        },
        "English": {
            "title": "📊 Financial Intelligence",
            "eff_head": "🚀 Efficiency (EBITDA)",
            "sol_head": "🛡️ Solvency & Liquidity",
            "analys_head": "🔍 Automated Analysis",
            "guide_head": "📚 Benchmarks Guide",
            "assets": "💼 Assets", "liabs": "💸 Liabilities", "ops": "📈 Operations",
            "qr_label": "Quick Ratio",
            "qr_guide": "**Quick Ratio:** Minimum: **2.0**. Cash should cover urgent debts twice.",
            "roi_guide": "**ROI:** Target: **> 25%**. Measures investment return.",
            "roe_guide": "**ROE:** Target: **> 20%**. Measures equity efficiency.",
            "warn_qr": "⚠️ QR below 2.0 benchmark!",
            "success_qr": "✅ Liquidity is healthy (QR > 2.0)"
        },
        "ქართული": {
            "title": "📊 ფინანსური ინტელექტი",
            "eff_head": "🚀 ეფექტურობა (EBITDA)",
            "sol_head": "🛡️ მდგრადობა და ლიკვიდურობა",
            "analys_head": "🔍 ავტომატური ანალიზი",
            "guide_head": "📚 ცნობარი",
            "assets": "💼 აქტივები", "liabs": "💸 ვალდებულებები", "ops": "📈 ოპერაციები",
            "qr_label": "Quick Ratio (ლიკვიდობა)",
            "qr_guide": "**Quick Ratio:** მინიმუმი: **2.0**. ნაღდი ფული უნდა ფარავდეს ვალებს ორმაგად.",
            "roi_guide": "**ROI:** მიზანი: **> 25%**.",
            "roe_guide": "**ROE:** მიზანი: **> 20%**.",
            "warn_qr": "⚠️ QR ნორმაზე (2.0) დაბალია!",
            "success_qr": "✅ ლიკვიდობა ნორმაშია (QR > 2.0)"
        }
    }

    with st.sidebar:
        lang = st.selectbox("🌐 Language", list(LANGS.keys()))
        t = LANGS[lang]

        with st.expander(t["assets"]):
            fa = st.number_input("Fixed Assets", value=2100000)
            ca = st.number_input("Current Assets", value=900000)
        with st.expander(t["liabs"]):
            stl = st.number_input("Short-term Debt", value=400000)
        with st.expander(t["ops"]):
            cash = st.number_input("Cash", value=300000)
            ebitda = st.number_input("EBITDA", value=450000)
            init_inv = st.number_input("Investment", value=1500000)
            own_cap = st.number_input("Equity", value=1000000)

    # Расчеты
    qr = cash / stl if stl != 0 else 0
    roi = (ebitda / init_inv * 100) if init_inv != 0 else 0
    roe = (ebitda / own_cap * 100) if own_cap != 0 else 0

    st.title(t["title"])
    tab1, tab3 = st.tabs(["🎯 Dashboard", "📚 Guide"])

    with tab1:
        st.subheader(t["eff_head"])
        c1, c2 = st.columns(2)
        c1.metric("ROI", f"{roi:.1f}%")
        c2.metric("ROE", f"{roe:.1f}%")

        st.subheader(t["sol_head"])
        st.metric(t["qr_label"], f"{qr:.2f}")
        if qr < 2.0:
            st.warning(f"{t['warn_qr']} (Current: {qr:.2f})")
        else:
            st.success(t["success_qr"])

    with tab3:
        st.header(t["guide_head"])
        st.info(t["qr_guide"])
        st.info(t["roi_guide"])
        st.info(t["roe_guide"])