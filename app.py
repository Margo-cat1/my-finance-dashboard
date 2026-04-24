import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Настройка темы
st.set_page_config(page_title="Financial Intelligence", page_icon="💎", layout="wide")

# Кастомный CSS для красоты
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #3e4253; }
    </style>
    """, unsafe_allow_
Harris = True)

st.title("💎 Financial Intelligence Suite")
st.markdown("---")

# --- SIDEBAR: ВВОД ДАННЫХ ---
with st.sidebar:
    st.header("📥 Ввод данных")
    with st.expander("💼 Активы", expanded=True):
        fa = st.number_input("Fixed Assets", value=2100000)
        ca = st.number_input("Current Assets", value=900000)
    with st.expander("💸 Обязательства", expanded=True):
        ltl = st.number_input("Long-term", value=800000)
        stl = st.number_input("Short-term", value=400000)
    with st.expander("📈 Операционка", expanded=True):
        rev = st.number_input("Выручка", value=1500000)
        exp = st.number_input("Расходы", value=1100000)

# --- РАСЧЕТЫ ---
total_assets = fa + ca
total_liabilities = ltl + stl
equity = total_assets - total_liabilities
profit = rev - exp
roi = (profit / exp * 100) if exp != 0 else 0
roe = (profit / equity * 100) if equity > 0 else 0
roa = (profit / total_assets * 100) if total_assets > 0 else 0
sol2 = (total_assets / total_liabilities) if total_liabilities != 0 else 0
sol3 = (equity / total_liabilities) if total_liabilities != 0 else 0
qr = (ca / stl) if stl != 0 else 0

# --- ГЛАВНЫЙ ЭКРАН (ВКЛАДКИ) ---
tab1, tab2, tab3 = st.tabs(["📊 Дашборд", "📑 Детализация Баланса", "🎓 Справочник"])

with tab1:
    # Ряд спидометров
    c1, c2, c3 = st.columns(3)

    with c1:
        fig_roi = go.Figure(go.Indicator(
            mode="gauge+number", value=roi, title={'text': "ROI %"},
            gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "#00d4ff"},
                   'steps': [{'range': [0, 20], 'color': "#ff4b4b"}, {'range': [20, 100], 'color': "#00ff88"}]}))
        fig_roi.update_layout(height=250, margin=dict(t=50, b=0, l=30, r=30), template="plotly_dark")
        st.plotly_chart(fig_roi, use_container_width=True)

    with c2:
        fig_roe = go.Figure(go.Indicator(
            mode="gauge+number", value=roe, title={'text': "ROE %"},
            gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "#f1c40f"},
                   'steps': [{'range': [0, 15], 'color': "#ff4b4b"}, {'range': [15, 100], 'color': "#00ff88"}]}))
        fig_roe.update_layout(height=250, margin=dict(t=50, b=0, l=30, r=30), template="plotly_dark")
        st.plotly_chart(fig_roe, use_container_width=True)

    with c3:
        fig_sol = go.Figure(go.Indicator(
            mode="gauge+number", value=sol2, title={'text': "Solvency 2"},
            gauge={'axis': {'range': [None, 5]}, 'bar': {'color': "#9b59b6"},
                   'steps': [{'range': [0, 1.5], 'color': "#ff4b4b"}, {'range': [1.5, 5], 'color': "#00ff88"}]}))
        fig_sol.update_layout(height=250, margin=dict(t=50, b=0, l=30, r=30), template="plotly_dark")
        st.plotly_chart(fig_sol, use_container_width=True)

    st.markdown("---")

    # SWOT АНАЛИЗ В КРАСИВЫХ БЛОКАХ
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("✅ Сильные стороны")
        if roi > 20: st.success(f"**Высокий ROI:** Бизнес генерирует {roi:.1f}% прибыли на затраты.")
        if sol3 > 1.0: st.success(f"**Golden Balance:** Капитал превышает долги. Вы в безопасности.")
        if roe > roa: st.info("**Рычаг работает:** Собственный капитал растет быстрее активов.")

    with col_b:
        st.subheader("🚨 Риски")
        if sol2 < 1.5: st.error(f"**Низкая устойчивость:** Активов недостаточно. Нужно снижать долг.")
        if qr < 1.0: st.error(f"**Дефицит ликвидности:** QR {qr:.2f} — риск невыплаты по текущим счетам.")
        if roa < 5: st.warning("**Слабые активы:** Низкая отдача от имущества (ROA).")

with tab2:
    st.subheader("📑 Структура Капитала и Активов")
    col_t, col_p = st.columns([1, 1])
    with col_t:
        df = pd.DataFrame({
            "Категория": ["Внеоборотные активы", "Оборотные активы", "Собственный капитал", "Долгосрочные долги",
                          "Краткосрочные долги"],
            "Значение": [fa, ca, equity, ltl, stl]
        })
        st.dataframe(df, use_container_width=True)
    with col_p:
        fig_p = go.Figure(data=[go.Pie(labels=['Свои', 'Чужие'], values=[equity, total_liabilities], hole=.4)])
        fig_p.update_layout(template="plotly_dark", title="Свой капитал vs Долг")
        st.plotly_chart(fig_p, use_container_width=True)

with tab3:
    st.info("💡 **Краткий гайд по нормам:**")
    st.write("""
    - **ROI > 20%**: Шикарно.
    - **ROE > 15%**: Инвесторы довольны.
    - **Sol2 > 1.5**: Банки дадут кредит.
    - **QR > 1.0**: Денег хватает на все текущие счета.
    """)