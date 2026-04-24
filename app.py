import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Financial OS Intelligence", page_icon="📊", layout="wide")

st.title("📊 Financial OS: Детальный баланс и аудит")
st.markdown("---")

# --- СЕКЦИЯ 1: ВВОД ДАННЫХ (Sidebar) ---
st.sidebar.header("📥 Ввод данных баланса")

st.sidebar.subheader("Активы (Assets)")
fa = st.sidebar.number_input("Fixed Assets (Внеоборотные)", value=2100000, step=10000)
ca = st.sidebar.number_input("Current Assets (Оборотные)", value=900000, step=10000)

st.sidebar.subheader("Обязательства (Liabilities)")
ltl = st.sidebar.number_input("Long-term (Долгосрочные)", value=800000, step=10000)
stl = st.sidebar.number_input("Short-term (Краткосрочные)", value=400000, step=10000)

st.sidebar.subheader("Доходы и расходы")
rev = st.sidebar.number_input("Выручка (Revenue)", value=1500000, step=10000)
exp = st.sidebar.number_input("Расходы (Expenses)", value=1100000, step=10000)

# --- СЕКЦИЯ 2: РАСЧЕТЫ ПОКАЗАТЕЛЕЙ ---
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
qr = (ca / stl) if stl != 0 else 0  # Ликвидность: оборотные к коротким долгам

# --- СЕКЦИЯ 3: ТАБЛИЦА БАЛАНСА ---
st.subheader("📑 Структура баланса (Balance Sheet)")
col_table, col_metrics = st.columns([1.5, 1])

with col_table:
    balance_data = {
        "Категория": ["Fixed Assets", "Current Assets", "TOTAL ASSETS", "Long-term Liabilities",
                      "Short-term Liabilities", "TOTAL LIABILITIES", "EQUITY (Капитал)"],
        "Сумма ($)": [f"{fa:,.0f}", f"{ca:,.0f}", f"{total_assets:,.0f}", f"{ltl:,.0f}", f"{stl:,.0f}",
                      f"{total_liabilities:,.0f}", f"{equity:,.0f}"]
    }
    st.table(pd.DataFrame(balance_data))

with col_metrics:
    st.write("### 🏁 Итоги")
    st.metric("Чистая прибыль", f"{profit:,.0f} $")
    st.metric("ROI (Окупаемость)", f"{roi:.1f}%")
    st.metric("ROE (Рентабельность)", f"{roe:.1f}%")

st.markdown("---")

# --- СЕКЦИЯ 4: ВИЗУАЛИЗАЦИЯ И SWOT ---
c1, c2 = st.columns(2)

with c1:
    st.write("### ⚖️ Golden Balance")
    fig_gb = go.Figure(data=[go.Pie(
        labels=['Собственный капитал (Equity)', 'Весь долг (Liabilities)'],
        values=[max(0, equity), total_liabilities],
        hole=.5,
        marker_colors=['#00c49f', '#ff4b4b']
    )])
    fig_gb.update_layout(template="plotly_dark", showlegend=True)
    st.plotly_chart(fig_gb, use_container_width=True)

with c2:
    st.write("### 🕵️ Сильные и слабые стороны")
    # Анализ ликвидности и устойчивости
    if qr >= 1.0:
        st.success(f"✅ **Ликвидность в норме:** Quick Ratio = {qr:.2f}. Ты можешь быстро закрыть краткосрочные долги.")
    else:
        st.error(f"❌ **Риск ликвидности:** QR = {qr:.2f}. Оборотных активов не хватает для покрытия текущих долгов!")

    if sol3 >= 1.0:
        st.success(f"✅ **Sol3 в норме:** {sol3:.2f}. Капитал полностью перекрывает обязательства.")
    else:
        st.warning(f"⚠️ **Sol3 низкий:** {sol3:.2f}. Бизнес сильно зависит от внешних займов.")

# --- СЕКЦИЯ 5: СПРАВОЧНИК ---
with st.expander("🎓 Справочник показателей"):
    st.write("""
    - **Fixed Assets:** Здания, оборудование, софт — то, что сложно быстро продать.
    - **Current Assets:** Деньги на счету, товары, дебиторка — то, что быстро превращается в кэш.
    - **Short-term Liabilities:** Долги, которые нужно отдать в течение года.
    - **Long-term Liabilities:** Кредиты на долгий срок.
    - **Golden Balance:** Идеально, когда Equity (зеленое) занимает больше половины круга.
    """)