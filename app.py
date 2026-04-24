import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# 1. Настройка страницы
st.set_page_config(page_title="Financial OS PRO", page_icon="📈", layout="wide")

# 2. Мультиязычный словарь
LANGS = {
    "Русский": {
        "title": "📊 Финансовый Интеллект",
        "settings": "⚙️ Настройки",
        "assets": "💼 Активы",
        "liabilities": "💸 Долги",
        "ops": "📈 Операционка",
        "simulator": "🔮 Симулятор рисков",
        "tab_main": "🎯 Главная",
        "tab_balance": "📊 Баланс",
        "tab_info": "📚 Справочник",
        "profit": "Чистая прибыль",
        "rev_change": "Изм. Выручки",
        "exp_change": "Изм. Расходов",
        "strong": "✅ Сильные стороны",
        "risks": "⚠️ Зоны внимания",
        "fixed": "Внеоборотные",
        "current": "Оборотные",
        "equity": "Капитал",
        "debt": "Всего долгов"
    },
    "English": {
        "title": "📊 Financial Intelligence",
        "settings": "⚙️ Settings",
        "assets": "💼 Assets",
        "liabilities": "💸 Liabilities",
        "ops": "📈 Operations",
        "simulator": "🔮 Risk Simulator",
        "tab_main": "🎯 Main Panel",
        "tab_balance": "📊 Balance Sheet",
        "tab_info": "📚 Guide",
        "profit": "Net Profit",
        "rev_change": "Rev Change",
        "exp_change": "Exp Change",
        "strong": "✅ Strengths",
        "risks": "⚠️ Risks",
        "fixed": "Fixed Assets",
        "current": "Current Assets",
        "equity": "Equity",
        "debt": "Total Debt"
    },
    "Español": {
        "title": "📊 Inteligencia Financiera",
        "settings": "⚙️ Ajustes",
        "assets": "💼 Activos",
        "liabilities": "💸 Pasivos",
        "ops": "📈 Operaciones",
        "simulator": "🔮 Simulador de Riesgos",
        "tab_main": "🎯 Principal",
        "tab_balance": "📊 Balance",
        "tab_info": "📚 Guía",
        "profit": "Beneficio Neto",
        "rev_change": "Cambio Ingresos",
        "exp_change": "Cambio Gastos",
        "strong": "✅ Fortalezas",
        "risks": "⚠️ Riesgos",
        "fixed": "Activos Fijos",
        "current": "Activos Corrientes",
        "equity": "Capital Propio",
        "debt": "Deuda Total"
    }
}

# 3. CSS (сохраняем твой красивый стиль)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    [data-testid="stMetric"] { background-color: #ffffff; border-radius: 15px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 5px solid #00d4ff; }
    .stTabs [aria-selected="true"] { background-color: #1e2130 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. Выбор языка в Sidebar
with st.sidebar:
    lang_choice = st.selectbox("🌐 Language / Язык", list(LANGS.keys()))
    t = LANGS[lang_choice]  # t - сокращение от translations

    st.title(t["settings"])
    with st.expander(t["assets"], expanded=True):
        fa = st.number_input(t["fixed"], value=2100000)
        ca = st.number_input(t["current"], value=900000)
    with st.expander(t["liabilities"], expanded=True):
        ltl = st.number_input("Long-term", value=800000)
        stl = st.number_input("Short-term", value=400000)

    st.markdown("---")
    st.header(t["simulator"])
    sim_rev = st.slider(t["rev_change"], -50, 50, 0)
    sim_exp = st.slider(t["exp_change"], -50, 50, 0)

# --- ЛОГИКА (без изменений) ---
input_rev, input_exp = 1500000, 1100000
rev = input_rev * (1 + sim_rev / 100)
exp = input_exp * (1 + sim_exp / 100)
profit = rev - exp
total_assets = fa + ca
total_liabilities = ltl + stl
equity = total_assets - total_liabilities

roi = (profit / exp * 100) if exp != 0 else 0
roe = (profit / equity * 100) if equity > 0 else 0
sol3 = (equity / total_liabilities) if total_liabilities != 0 else 0

# --- ИНТЕРФЕЙС ---
st.title(t["title"])
tab1, tab2, tab3 = st.tabs([t["tab_main"], t["tab_balance"], t["tab_info"]])

with tab1:
    c1, c2, c3 = st.columns(3)
    c1.metric(t["profit"], f"{profit:,.0f} $", delta=f"{sim_rev}%")
    c2.metric("ROI", f"{roi:.1f}%")
    c3.metric("ROE", f"{roe:.1f}%")

    st.markdown("---")
    s1, s2 = st.columns(2)
    with s1:
        st.success(f"#### {t['strong']}")
        if sol3 >= 1.0: st.write("Golden Balance ✅")
    with s2:
        st.warning(f"#### {t['risks']}")
        if profit < 0: st.error("Negative Profit 🚨")

with tab2:
    st.write(f"#### {t['tab_balance']}")
    df = pd.DataFrame({
        "Item": [t["fixed"], t["current"], t["equity"], t["debt"]],
        "Value": [fa, ca, equity, total_liabilities]
    })
    st.table(df)

with tab3:
    st.info("💡 Business Intelligence Guide")
    st.write("ROI - Return on Investment / Окупаемость")