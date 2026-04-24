import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Настройка страницы
st.set_page_config(page_title="Financial OS Intelligence", page_icon="📈", layout="wide")

# Исправленный CSS для красоты
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 1.8rem; color: #00d4ff; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { 
        height: 50px; white-space: pre-wrap; background-color: #1e2130; 
        border-radius: 5px; color: white; padding: 10px 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📈 Financial Intelligence Dashboard")
st.markdown("---")

# --- SIDEBAR: УДОБНЫЙ ВВОД ---
with st.sidebar:
    st.header("📥 Ввод данных")
    with st.expander("💼 Активы (Assets)", expanded=True):
        fa = st.number_input("Fixed Assets (Внеоборотные)", value=2100000)
        ca = st.number_input("Current Assets (Оборотные)", value=900000)
    with st.expander("💸 Долги (Liabilities)", expanded=True):
        ltl = st.number_input("Long-term (Долгие)", value=800000)
        stl = st.number_input("Short-term (Короткие)", value=400000)
    with st.expander("📈 Продажи и Косты", expanded=True):
        rev = st.number_input("Выручка", value=1500000)
        exp = st.number_input("Расходы", value=1100000)

# --- РАСЧЕТЫ ---
total_assets = fa + ca
total_liabilities = ltl + stl
equity = total_assets - total_liabilities
profit = rev - exp

# Коэффициенты
roi = (profit / exp * 100) if exp != 0 else 0
roe = (profit / equity * 100) if equity > 0 else 0
roa = (profit / total_assets * 100) if total_assets > 0 else 0
sol2 = (total_assets / total_liabilities) if total_liabilities != 0 else 0
sol3 = (equity / total_liabilities) if total_liabilities != 0 else 0
qr = (ca / stl) if stl != 0 else 0

# --- ГЛАВНЫЙ ИНТЕРФЕЙС ---
tab1, tab2, tab3 = st.tabs(["🎯 Главные показатели", "📊 Детали баланса", "📚 Обучение"])

with tab1:
    # Блок Рентабельности (ROI, ROE, ROA)
    st.subheader("🔥 Рентабельность")
    col1, col2, col3 = st.columns(3)
    col1.metric("ROI (Окупаемость)", f"{roi:.1f}%", help="Норма > 20%")
    col2.metric("ROE (Твой капитал)", f"{roe:.1f}%", help="Должен быть > ROA")
    col3.metric("ROA (Все активы)", f"{roa:.1f}%", help="Эффективность имущества")

    st.markdown("---")

    # Блок Устойчивости (Sol2, Sol3, QR)
    st.subheader("🛡️ Устойчивость и Ликвидность")
    col4, col5, col6 = st.columns(3)
    col4.metric("Solvency 2", f"{sol2:.2f}", delta_color="normal", help="Норма > 1.5")
    col5.metric("Solvency 3", f"{sol3:.2f}", help="Golden Balance: норма > 1.0")
    col6.metric("Quick Ratio", f"{qr:.2f}", help="Ликвидность: норма > 1.0")

    st.markdown("---")

    # Визуальный SWOT
    c_left, c_right = st.columns(2)
    with c_left:
        st.info("### ✅ Почему бизнес молодец:")
        if roi > 20: st.write(f"**ROI {roi:.1f}%:** Прибыль на высоком уровне.")
        if roe > roa: st.write("**Эффект рычага:** Ты зарабатываешь на чужих деньгах больше, чем они стоят.")
        if sol3 > 1.0: st.write("**Golden Balance:** Твой капитал перекрывает все долги.")

    with c_right:
        st.warning("### ⚠️ Где нужно поднажать:")
        if qr < 1.0: st.write(f"**Ликвидность:** QR {qr:.2f} — маловато оборотных средств.")
        if sol2 < 1.5: st.write(f"**Риск:** Sol2 ниже 1.5 — активы слишком зависят от долгов.")

with tab2:
    # График баланса
    st.subheader("📊 Баланс: Активы vs Обязательства")
    fig_b = go.Figure(data=[
        go.Bar(name='Активы', x=['Assets'], y=[total_assets], marker_color='#00d4ff'),
        go.Bar(name='Долги', x=['Liabilities'], y=[total_liabilities], marker_color='#ff4b4b'),
        go.Bar(name='Капитал', x=['Equity'], y=[equity], marker_color='#00ff88')
    ])
    fig_b.update_layout(barmode='group', template="plotly_dark", height=400)
    st.plotly_chart(fig_b, use_container_width=True)

    # Таблица
    st.write("### 📑 Подробная структура")
    st.table(pd.DataFrame({
        "Категория": ["Fixed Assets", "Current Assets", "Long-term Debt", "Short-term Debt", "EQUITY"],
        "Сумма ($)": [fa, ca, ltl, stl, equity]
    }))

with tab3:
    st.markdown("""
    ### 🎓 Мини-справочник
    * **ROI:** Если он 25%, значит на каждый потраченный $1 ты получил $0.25 чистой прибыли.
    * **ROE:** Твоя личная доходность как владельца. Сравнивай её со ставкой в банке.
    * **Sol2:** Коэффициент автономии. Если он < 1.5, значит банк владеет твоим бизнесом больше, чем ты.
    * **Golden Balance (Sol3):** Когда своих денег больше, чем долгов. Это база спокойного сна.
    """)