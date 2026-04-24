import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Financial Intelligence OS", page_icon="📈", layout="wide")

# Дизайн метрик
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 1.6rem; font-weight: 700; }
    .stAlert { border-radius: 10px; border: none; }
    </style>
    """, unsafe_allow_html=True)

st.title("📈 Financial Intelligence: Advanced Analytics")

# --- SIDEBAR: ВВОД ДАННЫХ И СИМУЛЯТОР ---
with st.sidebar:
    st.header("📥 Ввод текущих данных")
    with st.expander("💼 Баланс (Активы и Долги)", expanded=True):
        fa = st.number_input("Fixed Assets", value=2100000)
        ca = st.number_input("Current Assets", value=900000)
        ltl = st.number_input("Long-term Debt", value=800000)
        stl = st.number_input("Short-term Debt", value=400000)

    st.header("🔮 Симулятор рисков")
    sim_rev = st.slider("Изменение выручки (%)", -50, 50, 0) / 100
    sim_exp = st.slider("Изменение расходов (%)", -50, 50, 0) / 100

# --- БАЗОВЫЕ РАСЧЕТЫ ---
base_rev = 1500000
base_exp = 1100000
# Прогнозные значения
rev = base_rev * (1 + sim_rev)
exp = base_exp * (1 + sim_exp)

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

# --- ИНТЕРФЕЙС ---
t1, t2 = st.tabs(["🚀 Аналитический Дашборд", "⚖️ Глубокий Аудит"])

with t1:
    # Главный статус
    status_score = 0
    if roi > 20: status_score += 1
    if sol2 > 1.5: status_score += 1
    if qr > 1.0: status_score += 1

    if status_score == 3:
        st.success("🌟 **Статус: БИЗНЕС В ОТЛИЧНОЙ ФОРМЕ.** Все ключевые показатели в зеленой зоне.")
    elif status_score == 2:
        st.warning("⚠️ **Статус: ЕСТЬ ЗОНЫ ДЛЯ РОСТА.** Один из критических показателей требует внимания.")
    else:
        st.error("🚨 **Статус: КРИТИЧЕСКАЯ СИТУАЦИЯ.** Требуется немедленная оптимизация структуры долга или костов.")

    # Метрики
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Прибыль (Прогноз)", f"{profit:,.0f} $", delta=f"{sim_rev * 100:.1f}%")
    col2.metric("ROI", f"{roi:.1f}%", delta="Норма >20%", delta_color="off")
    col3.metric("Solvency 2", f"{sol2:.2f}", delta="Норма >1.5", delta_color="off")
    col4.metric("Golden Balance", f"{sol3:.2f}", delta="Норма >1.0", delta_color="off")

    st.markdown("---")

    # График: Прогноз рентабельности
    fig = go.Figure()
    metrics_names = ['ROI', 'ROE', 'ROA']
    metrics_values = [roi, roe, roa]
    norms = [20, 15, 8]  # Условные нормы

    fig.add_trace(go.Bar(x=metrics_names, y=metrics_values, marker_color=['#00d4ff', '#00ff88', '#9b59b6'],
                         name="Текущий прогноз"))
    fig.add_trace(
        go.Scatter(x=metrics_names, y=norms, mode='markers', marker=dict(size=15, color='red', symbol='line-ew'),
                   name="Минимальная норма"))

    fig.update_layout(title="Рентабельность vs Рыночные нормы (%)", template="plotly_dark", height=400)
    st.plotly_chart(fig, use_container_width=True)

with t2:
    col_l, col_r = st.columns(2)
    with col_l:
        st.write("### 🏛️ Структура Баланса")
        fig_pie = go.Figure(data=[go.Pie(labels=['Fixed Assets', 'Current Assets'], values=[fa, ca], hole=.3)])
        fig_pie.update_layout(template="plotly_dark")
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_r:
        st.write("### 🕵️ Рекомендации")
        if qr < 1.0:
            st.error(
                f"**Ликвидность:** У вас всего {qr:.2f} оборотных активов на 1$ краткосрочного долга. Постарайтесь перевести часть коротких кредитов в длинные.")
        if roe < 10:
            st.warning(
                "**Эффективность:** ROE слишком низкий. Ваши личные деньги работают неэффективно. Проверьте маржинальность.")
        if sol3 > 2.0:
            st.info(
                "**Заметка:** У вас очень много лишнего капитала. Возможно, стоит инвестировать его в расширение, а не просто держать на балансе.")

    st.markdown("---")
    st.write("### 📖 Пояснения к 'Золотому балансу'")
    st.markdown("""

    Золотой баланс (Solvency 3) — это когда ваш собственный капитал равен или больше всех ваших долгов. 
    Если стрелка вашего прогресса выше **1.0**, это значит, что даже если вы закроете бизнес сегодня, вы раздадите все долги и у вас еще останутся деньги.
    """)