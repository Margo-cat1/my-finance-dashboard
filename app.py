import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth

st.set_page_config(page_title="Financial Intelligence PRO", page_icon="📈", layout="wide")

# Данные для входа (теперь они точно работают)
credentials = {
    'usernames': {
        'admin': {'name': 'Admin', 'password': '123'},
        'margo': {'name': 'Margo', 'password': '456'}
    }
}

authenticator = stauth.Authenticate(credentials, 'finance_cookie', 'auth_key', cookie_expiry_days=30)

# Чистый вызов логина
authenticator.login()

if st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
elif st.session_state["authentication_status"]:

    # --- СЛОВАРЬ ПЕРЕВОДОВ (Здесь всё, что было на русском) ---
    LANGS = {
        "Русский": {
            "title": "📊 Финансовый Интеллект",
            "eff": "🚀 Эффективность (EBITDA)",
            "sol": "🛡️ Устойчивость и Ликвидность",
            "guide": "📚 Справочник нормативов",
            "assets": "💼 Активы", "liabs": "💸 Долги", "ops": "📈 Операционка",
            "qr_label": "Quick Ratio (Ликвидность)",
            "qr_guide": "**Quick Ratio:** Минимум: **2.0**. У вас должно быть в 2 раза больше кэша, чем срочных долгов.",
            "warn_qr": "⚠️ QR ниже нормы 2.0!",
            "ok_qr": "✅ Ликвидность в норме"
        },
        "ქართული": {
            "title": "📊 ფინანსური ინტელექტი",
            "eff": "🚀 ეფექტურობა (EBITDA)",
            "sol": "🛡️ მდგრადობა და ლიკვიდურობა",
            "guide": "📚 ცნობარი",
            "assets": "💼 აქტივები", "liabs": "💸 ვალდებულებები", "ops": "📈 ოპერაციები",
            "qr_label": "Quick Ratio (ლიკვიდობა)",
            "qr_guide": "**Quick Ratio:** მინიმუმი: **2.0**. ნაღდი ფული უნდა ფარავდეს ვალებს ორმაგად.",
            "warn_qr": "⚠️ QR ნორმაზე (2.0) დაბალია!",
            "ok_qr": "✅ ლიკვიდობა ნორმაშია"
        }
    }

    with st.sidebar:
        st.write(f'Welcome, *{st.session_state["name"]}*')
        lang = st.selectbox("🌐 Language", list(LANGS.keys()))
        t = LANGS[lang]

        # Поля ввода (чтобы дашборд не был пустым)
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

        authenticator.logout('Logout', 'sidebar')

    # Расчеты
    qr = cash / stl if stl != 0 else 0
    roi = (ebitda / init_inv * 100) if init_inv != 0 else 0
    roe = (ebitda / own_cap * 100) if own_cap != 0 else 0

    st.title(t["title"])
    tab1, tab2 = st.tabs(["🎯 Dashboard", t["guide"]])

    with tab1:
        st.subheader(t["eff"])
        c1, c2 = st.columns(2)
        c1.metric("ROI", f"{roi:.1f}%")
        c2.metric("ROE", f"{roe:.1f}%")

        st.subheader(t["sol"])
        st.metric(t["qr_label"], f"{qr:.2f}")
        if qr < 2.0:
            st.warning(f"{t['warn_qr']} (Current: {qr:.2f})")
        else:
            st.success(t["ok_qr"])

    with tab2:
        st.header(t["guide"])
        st.info(t["qr_guide"])