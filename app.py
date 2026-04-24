import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Настройка страницы
st.set_page_config(page_title="Financial OS Intelligence", page_icon="📊", layout="wide")

# Дизайн (тот самый чистый стиль)
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 1.8rem; color: #00d4ff; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { 
        height: 50px; white-space: pre-wrap; background-color: #f0f2f6; 
        border-radius: 5px; color: #31333F; padding: 10px 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Financial Intelligence Dashboard")
st.markdown("---")

# --- SIDEBAR: ВВОД ДАННЫХ + СИМУЛЯТОР ---
with st.sidebar:
    st.header("📥 Ввод данных")

    with st.expander("💼 Активы (Assets)", expanded=True):
        fa = st.number_input("Fixed Assets (Внеоборотные)", value=2100000)
        ca = st.number_input("Current Assets (Оборотные)", value=900000)

    with st.expander("💸 Долги (Liabilities)", expanded=True):
        ltl = st.number_input("Long-term (Долгие)", value=800000)
        stl = st.number_input("Short-term (Короткие)", value=400000)

    with st.expander("📈 Продажи и Косты", expanded=True):
        input_rev = st.number_input("Выручка (Базовая)", value=1500000)
        input_exp = st.number_input("Расходы (Базовые)", value=1100000)

    st.markdown("---")
    st.header("🔮 Симулятор рисков")
    sim_rev_pct = st.slider("Изменение Выручки (%)", -50, 50, 0)
    sim_exp_pct = st.slider("Изменение Расходов (%)", -50, 50, 0)

# --- РАСЧЕТЫ (с учетом симуляции) ---
rev = input_rev * (1 + sim_rev_pct / 100)
exp = input_exp * (1 + sim_exp_pct / 100)
profit = rev - exp
total_assets = fa + ca
total_liabilities = ltl + stl
equity = total_assets - total_liabilities

# Коэффициенты
roi = (profit / exp * 100) if exp != 0 else 0
roe = (profit / equity * 100) if equity > 0 else 0
roa = (profit / total_assets * 100) if total_assets > 0 else 0
sol2 = (total_assets / total_liabilities) if total_liabilities != 0 else 0
sol3 = (equity / total_liabilities) if total_liabilities != 0 else 0
qr = (ca / stl) if stl != 0 else 0

# Расчет разницы для дельты в метриках
base_profit = input_rev - input_exp
profit_delta = profit - base_profit

# --- ИНТЕРФЕЙС (ВКЛАДКИ) ---
tab1, tab2, tab3 = st.tabs(["🎯 Главные показатели", "📊 Детали баланса", "📚 Обучение"])

with tab1:
    # Блок Рентабельности
    st.subheader("🔥 Рентабельность")
    c1, c2, c3 = st.columns(3)
    c1.metric("Прибыль", f"{profit:,.0f} $", delta=f"{profit_delta:,.0f} $")
    c2.metric("ROI (Окупаемость)", f"{roi:.1f}%", help="Норма > 20%")
    c3.metric("ROE (Твой капитал)", f"{roe:.1f}%", help="Доходность личных вложений")

    st.markdown("---")

    # Блок Устойчивости
    st.subheader("🛡️ Устойчивость и Ликвидность")
    c4, c5, c6 = st.columns(3)
    c4.metric("Solvency 2", f"{sol2:.2f}", help="Норма > 1.5")
    c5.metric("Solvency 3", f"{sol3:.2f}", help="Golden Balance: норма > 1.0")
    c6.metric("Quick Ratio", f"{qr:.2f}", help="Ликвидность: норма > 1.0")

    st.markdown("---")

    # Аналитический вердикт
    st.subheader("🕵️ Анализ ситуации")
    col_a, col_b = st.columns(2)
    with col_a:
        st.info("### ✅ Сильные стороны")
        if roi > 20: st.write(f"**ROI {roi:.1f}%:** Прибыль на высоком уровне.")
        if roe > roa: st.write("**Эффект рычага:** Твой капитал работает эффективнее общих активов.")
        if sol3 > 1.0: st.write("**Golden Balance:** Твои деньги полностью покрывают долги.")

    with col_b:
        st.warning("### ⚠️ Риски сценария")
        if profit < 0: st.error("**Убыток!** При таких настройках расходы выше доходов.")
        if qr < 1.0: st.write(f"**Ликвидность:** Низкий QR ({qr:.2f}) — риск невыплаты по счетам.")
        if sol2 < 1.5: st.write(f"**Автономия:** Слишком высокая зависимость от долгов.")

with tab2:
    st.subheader("📑 Структура Баланса")
    col_t, col_p = st.columns([1, 1.2])
    with col_t:
        st.write("### Таблица")
        df = pd.DataFrame({
            "Категория": ["Внеоборотные активы", "Оборотные активы", "Собственный капитал", "Долги (Всего)"],
            "Сумма ($)": [f"{fa:,.0f}", f"{ca:,.0f}", f"{equity:,.0f}", f"{total_liabilities:,.0f}"]
        })
        st.table(df)
    with col_p:
        st.write("### График: Свои vs Чужие")
        fig = go.Figure(data=[go.Pie(labels=['Свои', 'Чужие'], values=[max(0, equity), total_liabilities], hole=.4)])
        fig.update_layout(height=350, margin=dict(t=30, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown("""
    ### 🎓 Краткий справочник
    * **ROI:** Насколько эффективно тратятся деньги. Норма > 20%.
    * **ROE:** Сколько приносят ТВОИ личные деньги. Должен быть выше ROA.
    * **Solvency 2:** Общая защита. Если < 1.5, значит бизнес в опасной зоне.
    * **Solvency 3 (Golden Balance):** Если он 1.0 и выше — ты красавчик, своих денег больше чем долгов.
    * **Quick Ratio:** Твоя способность платить по счетам прямо сейчас. Норма > 1.0.
    """)