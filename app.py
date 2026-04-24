import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth

# 1. Настройка страницы
st.set_page_config(page_title="Financial Intelligence PRO", page_icon="📈", layout="wide")

# --- БЛОК АВТОРИЗАЦИИ ---
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

# Вызов окна логина
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
            "eff": "🚀 Эффективность (EBITDA)",
            "sol": "🛡️ Устойчивость и Ликвидность",
            "fa": "Внеоборотные активы", "ca": "Оборотные активы",
            "stl": "Краткосрочные долги", "cash": "Наличные",
            "guide_title": "📚 Справочник нормативов",
            "qr_text": "**Quick Ratio:** Минимум: **2.0**. Показывает, хватит ли кэша закрыть долги дважды.",
            "roi_text": "**ROI:** Цель: **> 25%**. Окупаемость инвестиций.",
            "roe_text": "**ROE:** Цель: **> 20%**. Эффективность ваших личных денег."
        },
        "English": {
            "title": "📊 Financial Intelligence",
            "eff": "🚀 Efficiency (EBITDA)",
            "sol": "🛡️ Solvency & Liquidity",
            "fa": "Fixed Assets", "ca": "Current Assets",
            "stl": "Short-term Debt", "cash": "Cash",
            "guide_title": "📚 Benchmarks Guide",
            "qr_text": "**Quick Ratio:** Minimum: **2.0**. Cash should cover urgent debts twice.",
            "roi_text": "**ROI:** Target: **> 25%**. Return on Investment.",
            "roe_text": "**ROE:** Target: **> 20%**. Return on Equity."
        },
        "ქართული": {
            "title": "📊 ფინანსური ინტელექტი",
            "eff": "🚀 ეფექტურობა (EBITDA)",
            "sol": "🛡️ მდგრადობა და ლიკვიდურობა",
            "fa": "ძირითადი აქტივები", "ca": "მიმდინარე აქტივები",
            "stl": "მოკლევადიანი ვალი", "cash": "ნაღდი ფული",
            "guide_title": "📚 ცნობარი",
            "qr_text": "**Quick Ratio:** მინიმუმი: **2.0**.",
            "roi_text": "**ROI:** მიზანი: **> 25%**.",
            "roe_text": "**ROE:** მიზანი: **> 20%**."
        }
    }

    # Интерфейс
    with st.sidebar:
        lang = st.selectbox("🌐 Language", list(LANGS.keys()))
        t = LANGS[lang]
        fa_val = st.number_input(t["fa"], value=2100000)
        ca_val = st.number_input(t["ca"], value=900000)
        stl_val = st.number_input(t["stl"], value=400000)
        cash_v = st.number_input(t["cash"], value=300000)
        ebitda = st.number_input("EBITDA", value=450000)
        init_inv = st.number_input("Initial Investment", value=1500000)
        own_cap = st.number_input("Own Capital", value=1000000)

    # Расчеты
    qr = cash_v / stl_val if stl_val != 0 else 0
    roi = (ebitda / init_inv * 100) if init_inv != 0 else 0
    roe = (ebitda / own_cap * 100) if own_cap != 0 else 0

    st.title(t["title"])
    tab1, tab3 = st.tabs(["🎯 Dashboard", "📚 Guide"])

    with tab1:
        st.subheader(t["eff"])
        c1, c2 = st.columns(2)
        c1.metric("ROI", f"{roi:.1f}%")
        c2.metric("ROE", f"{roe:.1f}%")

        st.subheader(t["sol"])
        st.metric("Quick Ratio", f"{qr:.2f}")
        if qr < 2.0:
            st.warning(f"⚠️ QR ниже нормы 2.0! Текущий: {qr:.2f}")
        else:
            st.success(f"✅ Ликвидность в норме (QR > 2.0)")

    with tab3:
        st.header(t["guide_title"])
        st.info(t["qr_text"])
        st.info(t["roi_text"])
        st.info(t["roe_text"])