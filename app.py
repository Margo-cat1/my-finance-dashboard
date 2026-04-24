import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Financial OS Intelligence", page_icon="💎", layout="wide")

st.title("💎 Financial Intelligence & Audit System")
st.markdown("---")

# --- СЕКЦИЯ 1: ВВОД ДАННЫХ (Sidebar) ---
st.sidebar.header("📥 Ввод данных")

with st.sidebar.expander("💼 Активы (Assets)", expanded=True):
    fa = st.sidebar.number_input("Fixed Assets (Внеоборотные)", value=2100000,
                                 help="Здания, оборудование, долгосрочные вложения")
    ca = st.sidebar.number_input("Current Assets (Оборотные)", value=900000, help="Кэш, дебиторка, запасы на складе")

with st.sidebar.expander("💸 Обязательства (Liabilities)", expanded=True):
    ltl = st.sidebar.number_input("Long-term (Долгосрочные)", value=800000, help="Кредиты более года")
    stl = st.sidebar.number_input("Short-term (Краткосрочные)", value=400000,
                                  help="Задолженность перед поставщиками, налоги, короткие займы")

with st.sidebar.expander("📈 Операционка", expanded=True):
    rev = st.sidebar.number_input("Выручка (Revenue)", value=1500000)
    exp = st.sidebar.number_input("Расходы (Expenses)", value=1100000)

# --- СЕКЦИЯ 2: РАСЧЕТЫ ---
total_assets = fa + ca
total_liabilities = ltl + stl
equity = total_assets - total_liabilities
profit = rev - exp

# Рентабельность
roi = (profit / exp * 100) if exp != 0 else 0
roe = (profit / equity * 100) if equity > 0 else 0
roa = (profit / total_assets * 100) if total_assets > 0 else 0

# Устойчивость
sol2 = (total_assets / total_liabilities) if total_liabilities != 0 else 0
sol3 = (equity / total_liabilities) if total_liabilities != 0 else 0
qr = (ca / stl) if stl != 0 else 0

# --- СЕКЦИЯ 3: ТАБЛО МЕТРИК ---
st.subheader("🚀 Ключевые показатели эффективности")
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("ROI", f"{roi:.1f}%")
c2.metric("ROE", f"{roe:.1f}%")
c3.metric("ROA", f"{roa:.1f}%")
c4.metric("Sol2", f"{sol2:.2f}")
c5.metric("Sol3", f"{sol3:.2f}")
c6.metric("QR", f"{qr:.2f}")

st.markdown("---")

# --- СЕКЦИЯ 4: ТАБЛИЦА БАЛАНСА И SWOT ---
col_table, col_swot = st.columns([1, 1.2])

with col_table:
    st.write("### 📑 Детализация баланса")
    df_balance = pd.DataFrame({
        "Показатель": ["Внеоборотные активы", "Оборотные активы", "ДОЛГИ (Всего)", "Собственный капитал"],
        "Сумма ($)": [f"{fa:,.0f}", f"{ca:,.0f}", f"{total_liabilities:,.0f}", f"{equity:,.0f}"]
    })
    st.table(df_balance)

    # Визуал Golden Balance
    fig_pie = go.Figure(data=[go.Pie(labels=['Equity', 'Debt'], values=[max(0, equity), total_liabilities], hole=.4)])
    fig_pie.update_layout(height=300, margin=dict(t=0, b=0, l=0, r=0), template="plotly_dark")
    st.plotly_chart(fig_pie, use_container_width=True)

with col_swot:
    st.write("### 🕵️ Глубокий анализ (SWOT)")

    # Логика ROI
    if roi > 20:
        st.success(
            f"✅ **ROI {roi:.1f}%:** Отлично! Каждый доллар затрат приносит {roi / 100:.2f} прибыли. Эффективное производство.")
    else:
        st.warning(f"⚠️ **ROI {roi:.1f}%:** Ниже нормы (20%). Проверь себестоимость или наценку.")

    # Логика ROE vs ROA
    if roe > roa: st.info(
        f"✅ **ROE > ROA:** Твои деньги работают эффективнее общих активов. Кредитное плечо помогает расти.")

    # Логика Sol2
    if sol2 > 1.5:
        st.success(f"✅ **Sol2 {sol2:.2f}:** Бизнес очень устойчив. Активы перекрывают долги с запасом.")
    else:
        st.error(f"🚨 **Sol2 {sol2:.2f}:** Риск! У тебя слишком мало активов на такой объем долга. Норма > 1.5.")

    # Логика Sol3 (Golden Balance)
    if 1.0 <= sol3 <= 2.0:
        st.success(f"✅ **Sol3 {sol3:.2f}:** Идеальный Golden Balance. Своих денег больше, чем чужих.")
    elif sol3 < 1.0:
        st.error(f"🚨 **Sol3 {sol3:.2f}:** Ты работаешь в основном на чужих деньгах. Это опасно при падении выручки.")

st.markdown("---")

# --- СЕКЦИЯ 5: БАЗА ЗНАНИЙ (Обучение) ---
with st.expander("🎓 Справочник: Как читать эти данные?"):
    st.write("""
    ### Рентабельность (Profitability)
    * **ROI (Return on Investment):** Показывает «выхлоп» от вложенных денег в проект. Если ROI 30%, значит на 1$ затрат ты получил 1.3$ выручки. **Норма: > 20%**.
    * **ROE (Return on Equity):** Рентабельность ТВОИХ денег. Если ROE 40%, значит твои личные вложения приносят 40% годовых. **Должен быть выше ROA**.
    * **ROA (Return on Assets):** Эффективность всех «станков и офисов». Если он низкий, значит активы «простаивают».

    ### Устойчивость и Ликвидность (Stability)
    * **Solvency 2 (Автономия):** Можешь ли ты продать всё имущество и закрыть долги. **Норма: 1.5 - 2.0**.
    * **Solvency 3 (Golden Balance):** Соотношение Свое / Чужое. Если 1.0 — у тебя поровну своих и заемных денег. **Норма: > 1.0**.
    * **Quick Ratio (Ликвидность):** Хватит ли тебе денег на счету и товаров, чтобы отдать долги, которые придут завтра. **Норма: > 1.0**.
    """)