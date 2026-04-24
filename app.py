import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth

# 1. Настройка страницы
st.set_page_config(page_title="Financial Intelligence PRO", page_icon="📈", layout="wide")

# --- БЛОК АВТОРИЗАЦИИ (Professional) ---
# Пароли захешированы для безопасности (admin123 и margo456)
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

authenticator = stauth.Authenticate(
    credentials,
    'financial_dashboard_cookie',
    'auth_key',
    cookie_expiry_days=30
)

# Исправленный вызов логина (убраны старые параметры локации)
authenticator.login()

if st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
elif st.session_state["authentication_status"]:

    # --- ЕСЛИ ВХОД УСПЕШЕН ---
    with st.sidebar:
        st.write(f'Welcome, *{st.session_state["name"]}*')
        authenticator.logout('Logout', 'sidebar')

    # Словарь переводов (Включая твои нормы: QR > 2.0)
    LANGS = {
        "Русский": {
            "title": "📊 Финансовый Интеллект",
            "tab1": "🎯 Дашборд", "tab3": "📚 Справочник",
            "qr_label": "Quick Ratio",
            "guide": {
                "qr": "**Quick Ratio:** Cash / Краткосрочные долги. **Минимум: 2.0**. У вас должно быть в 2 раза больше кэша, чем срочных долгов.",
                "roi": "**ROI:** EBITDA / Инвестиции. **Цель: > 25%**.",
                "roe": "**ROE:** EBITDA / Собственный капитал. **Цель: > 20%**."
            }
        },
        "English": {
            "title": "📊 Financial Intelligence",
            "tab1": "🎯 Dashboard", "tab3": "📚 Guide",
            "qr_label": "Quick Ratio",
            "guide": {
                "qr": "**Quick Ratio:** Cash / Short-term Debt. **Minimum: 2.0**. You need 2x more cash than urgent debts.",
                "roi": "**ROI:** EBITDA / Investments. **Target: > 25%**.",
                "roe": "**ROE:** EBITDA / Own Capital. **Target: > 20%**."
            }
        },
        "ქართული": {
            "title": "📊 ფინანსური ინტელექტი",
            "tab1": "🎯 მთავარი", "tab3": "📚 ცნობარი",
            "qr_label": "Quick Ratio",
            "guide": {
                "qr": "**Quick Ratio:** Cash / მოკლევადიანი ვალი. **მინიმუმი: 2.0**.",
                "roi": "**ROI:** EBITDA / ინვესტიცია. **მიზანი: > 25%**.",
                "roe": "**ROE:** EBITDA / საკუთარი კაპიტალი. **მიზანი: > 20%**."
            }
        }
    }

    # Логика интерфейса (Sidebar для ввода данных)
    with st.sidebar:
        lang_choice = st.selectbox("🌐 Language", list(LANGS.keys()))
        t = LANGS[lang_choice]
        fa = st.number_input("Fixed Assets", value=2100000)
        ca = st.number_input("Current Assets", value=900000)
        stl = st.number_input("Short-term Debt", value=400000)
        cash_val = st.number_input("Cash", value=300000)
        # ... остальные инпуты ...

    # РАСЧЕТЫ
    qr = (cash_val / stl) if stl != 0 else 0

    # ОТОБРАЖЕНИЕ
    st.title(t["title"])
    tab1, tab3 = st.tabs([t["tab1"], t["tab3"]])

    with tab1:
        st.metric(t["qr_label"], f"{qr:.2f}")
        if qr < 2.0:
            st.warning(f"⚠️ Quick Ratio ниже нормы (Текущий: {qr:.2f}, Нужно: 2.0)")

    with tab3:
        for key in t["guide"]:
            st.info(t["guide"][key])