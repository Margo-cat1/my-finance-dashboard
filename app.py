import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Financial OS PRO", page_icon="📈", layout="wide")

st.title("📈 Financial Intelligence: Анализ и Симуляция")
st.markdown("---")

# --- СЕКЦИЯ 1: ВВОД ДАННЫХ И СИМУЛЯТОР (Sidebar) ---
st.sidebar.header("📥 1. Текущий Баланс")
with st.sidebar.expander("Активы и Долги", expanded=True):
    fa = st.number_input("Fixed Assets", value=2100000)
    ca = st.number_input("Current Assets", value=900000)
    ltl = st.number_input("Long-term Debt", value=800000)
    stl = st.number_input("Short-term Debt", value=400000)

st.sidebar.header("🔮 2. Симулятор Рисков")
sim_rev = st.sidebar.slider("Изменение Выручки (%)", -50, 50, 0) / 100
sim_exp = st.sidebar.slider("Изменение Расходов (%)", -50, 50, 0) / 100

# --- СЕКЦИЯ 2: РАСЧЕТЫ ---
# Базовые операционные данные
base_rev = 1500000
base_exp = 1100000

# Применяем симуляцию
rev = base_rev * (1 + sim_rev)
exp = base_exp * (1 + sim_exp)
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

# --- СЕКЦИЯ 3: ГЛАВНЫЕ МЕТРИКИ ---
st.subheader("🏁 Ключевые показатели (с учетом симуляции)")
m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("ROI", f"{roi:.1f}%")
m2.metric("ROE", f"{roe:.1f}%")
m3.metric("ROA", f"{roa:.1f}%")
m4.metric("Sol2", f"{sol2:.2f}")
m5.metric("Sol3", f"{sol3:.2f}")
m6.metric("QR", f"{qr:.2f}")

st.markdown("---")

# --- СЕКЦИЯ 4: ТАБЛИЦА БАЛАНСА И АНАЛИЗ ---
col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.write("### 📑 Таблица баланса")
    balance_data = {
        "Категория": ["Fixed Assets", "Current Assets", "TOTAL ASSETS", "Long-term Liabilities",
                      "Short-term Liabilities", "TOTAL LIABILITIES", "EQUITY (Капитал)"],
        "Сумма ($)": [f"{fa:,.0f}", f"{ca:,.0f}", f"{total_assets:,.0f}", f"{ltl:,.0f}", f"{stl:,.0f}",
                      f"{total_liabilities:,.0f}", f"{equity:,.0f}"]
    }
    st.table(pd.DataFrame(balance_data))

    st.write("### ⚖️ Golden Balance")
    fig_gb = go.Figure(data=[go.Pie(
        labels=['Equity (Свои)', 'Debt (Долги)'],
        values=[max(0, equity), total_liabilities],
        hole=.5,
        marker_colors=['#00c49f', '#ff4b4b']
    )])
    fig_gb.update_layout(height=300, template="plotly_dark", margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig_gb, use_container_width=True)

with col_right:
    st.write("### 🕵️ Анализ сильных и слабых сторон")

    # Динамические подсказки
    if roi > 20:
        st.success(f"✅ **Сильный ROI:** Даже при текущем сценарии бизнес генерирует отличную прибыль.")
    else:
        st.warning(f"⚠️ **Низкий ROI:** Прибыльность под угрозой. Нужно снижать косты или растить чек.")

    if sol3 >= 1.0:
        st.success(f"✅ **Golden Balance соблюден:** {sol3:.2f}. Ваш капитал перекрывает долги.")
    else:
        st.error(f"🚨 **Нарушение Sol3:** {sol3:.2f}. Бизнес живет в долг. Риск потери устойчивости.")

    if qr < 1.0:
        st.error(f"🚨 **Кризис ликвидности:** QR {qr:.2f}. Денег не хватит на оплату коротких долгов.")

    if roe > roa:
        st.info("💡 **Рычаг:** Вы эффективно используете заемные средства для роста доходности капитала.")

st.markdown("---")

# --- СЕКЦИЯ 5: СПРАВОЧНИК ---
with st.expander("🎓 Справочник: Что это значит?"):
    st.write("""
    - **ROI:** Окупаемость затрат. Норма > 20%.
    - **ROE:** Доходность твоих личных денег. Норма > 15%.
    - **ROA:** Насколько эффективно работают «станки и офисы».
    - **Solvency 2:** Активы / Долги. Если ниже 1.5 — банк владеет тобой.
    - **Solvency 3 (Sol3):** Капитал / Долги. Идеал > 1.0.
    - **Quick Ratio (QR):** Можешь ли ты завтра отдать короткие долги. Норма > 1.0.
    """)