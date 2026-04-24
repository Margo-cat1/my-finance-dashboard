import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth

st.set_page_config(page_title="Finance PRO", layout="wide")

# 1. НОВЫЙ ФОРМАТ ДАННЫХ (без старых хешей, которые вызывают ValueError)
credentials = {
    'usernames': {
        'admin': {'name': 'Admin', 'password': '123'},
        'margo': {'name': 'Margo', 'password': '456'}
    }
}

# 2. ИСПРАВЛЕННЫЙ ОБЪЕКТ (убираем конфликты версий)
authenticator = stauth.Authenticate(
    credentials,
    'finance_cookie',
    'auth_key',
    cookie_expiry_days=30
)

# 3. ИСПРАВЛЕННЫЙ ВЫЗОВ (решаем ошибку Location must be one of 'main'...)
# Теперь вызываем БЕЗ аргументов 'main' или 'sidebar'
authenticator.login()

if st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
elif st.session_state["authentication_status"]:

    with st.sidebar:
        st.write(f'Welcome, *{st.session_state["name"]}*')
        authenticator.logout('Logout', 'sidebar')

    # Твой основной интерфейс и расчет QR 2.0
    st.title("📊 Финансовый Интеллект")
    cash = st.number_input("Наличные", value=300000)
    stl = st.number_input("Краткоср. долги", value=100000)

    qr = cash / stl if stl != 0 else 0
    st.metric("Quick Ratio", f"{qr:.2f}")

    if qr < 2.0:
        st.error("⚠️ Ниже твоего норматива 2.0!")
    else:
        st.success("✅ Ликвидность в порядке")