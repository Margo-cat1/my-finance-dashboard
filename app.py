import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Настройка страницы
st.set_page_config(page_title="Financial OS Intelligence", page_icon="📈", layout="wide")

# Исправленный CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #00d4ff;
    }
    .section-header {
        font-size: 24px; font-weight: 700; color: #1e2130;
        margin-bottom: 20px; padding-top: 10px;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; background-color: #ffffff;
        border-radius: 10px 10px 0 0; border: 1px solid #e0e0e0;
        padding: 10px 30px; font-weight: 600;
    }
    .stTabs [aria-selected="true"] { background-color: #1e2130 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Настройки")
    with st.expander("💼 Баланс (Assets)", expanded=True):
        fa = st.number_input("Fixed Assets", value=2100000)
        ca = st.number_input("Current Assets", value=900000)
    with st.expander("💸 Долги (Liabilities)", expanded=True):
        ltl = st.number_input("Long-term Debt", value=800000)
        stl = st.number_input("Short-term Debt", value=400000)
    with st.expander("📊 Операционка", expanded=True):
        input_rev = st.number_input("Выручка (Base)", value=1500000)
        input_exp = st.number_input("Расходы (Base)", value=1100000)

    st.markdown("---")
    st.header("🔮 Симулятор")
    sim_rev_pct = st.slider("Изменение Выручки (%)", -50, 50, 0)
    sim_exp_pct = st.slider("Изменение Расходов (%)", -50, 50, 0)

# --- РАСЧЕТЫ ---
rev = input_rev * (1 + sim_rev_pct / 100)
exp = input_exp * (1 + sim_exp_pct / 100)
profit = rev - exp
total_assets = fa + ca
total_liabilities = ltl + stl
equity = total_assets - total_liabilities

roi = (profit / exp * 100) if exp != 0 else 0
roe = (profit / equity * 100) if equity > 0 else 0
roa = (profit / total_assets * 100) if total_assets > 0 else 0
sol2 = (total_assets / total_liabilities) if total_liabilities != 0 else 0
sol3 = (equity / total_liabilities) if total_liabilities != 0 else 0
qr = (ca / stl) if stl != 0 else 0

# --- ИНТЕРФЕЙС ---
st.title("🚀 Financial OS Intelligence")

tab1, tab2, tab3 = st.tabs(["🎯 Главная Панель", "📊 Анализ Баланса", "📚 Справочник"])

with tab1:
    st.markdown('<div class="section-header">🔥 Эффективность и Прибыль</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Чистая прибыль", f"{profit:,.0f} $", delta=f"{sim_rev_pct}%")
    c2.metric("ROI (Окупаемость)", f"{roi:.1f}%")
    c3.metric("ROE (На капитал)", f"{roe:.1f}%")

    st.markdown('<div class="section-header" style="border-top: 1px solid #ddd; padding-top:20px;">🛡️ Устойчивость и Риски</div>', unsafe_allow_html=True)
    c4, c5, c6 = st.columns(3)
    c4.metric("Solvency 2", f"{sol2:.2f}")
    c5.metric("Solvency 3 (GB)", f"{sol3:.2f}")
    c6.metric("Quick Ratio", f"{qr:.2f}")

    st.markdown("---")
    sw1, sw2 = st.columns(2)
    with sw1:
        st.success("#### ✅ СИЛЬНЫЕ СТОРОНЫ")
        if roi > 20: st.markdown(f"**ROI {roi:.1f}%:** Прибыль в норме.")
        if sol3 >= 1.0: st.markdown("**Golden Balance:** Своих денег больше чем долгов.")
    with sw2:
        st.warning("#### ⚠️ ЗОНЫ ВНИМАНИЯ")
        if qr < 1.0: st.markdown(f"**Ликвидность:** QR {qr:.2f} — мало кэша.")
        if profit < 0: st.error("**УБЫТОК!** Проверьте настройки симулятора.")

with tab2:
    st.markdown('<div class="section-header">📊 Глубокий разбор баланса</div>', unsafe_allow_html=True)
    tl, tr = st.columns([1, 1.2])
    with tl:
        st.table(pd.DataFrame({
            "Параметр": ["Assets", "Equity", "Debt"],
            "Сумма ($)": [f"{total_assets:,.0f}", f"{equity:,.0f}", f"{total_liabilities:,.0f}"]
        }))
    with tr:
        fig = go.Figure(data=[go.Pie(labels=['Equity', 'Debt'], values=[max(0, equity), total_liabilities], hole=.5)])
        fig.update_layout(height=350, margin=dict(t=20, b=20, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown('<div class="section-header">📚 База знаний</div>', unsafe_allow_html=True)
    with st.expander("Что такое ROI?"):
        st.write("Это окупаемость ваших затрат. Сколько прибыли приносит каждый вложенный доллар.")
    with st.expander("Что такое Golden Balance?"):
        st.write("Состояние (Sol3 > 1.0), когда ваш капитал превышает общую сумму долгов.")