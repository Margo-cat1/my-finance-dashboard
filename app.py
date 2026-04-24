import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Financial OS PRO", page_icon="📈", layout="wide")

st.title("📈 Financial Intelligence: Полный анализ и аудит")
st.markdown("---")

# --- СЕКЦИЯ 1: УПРАВЛЕНИЕ (Sidebar) ---
st.sidebar.header("🕹️ Симулятор сценариев")
d_rev = st.sidebar.slider("Выручка (%)", -50, 100, 0) / 100
d_exp = st.sidebar.slider("Расходы (%)", -50, 50, 0) / 100
d_assets = st.sidebar.slider("Активы (%)", -20, 50, 0) / 100
d_debt = st.sidebar.slider("Долги (%)", -50, 100, 0) / 100

# --- СЕКЦИЯ 2: БАЗОВЫЕ ДАННЫЕ (Твой фундамент) ---
base = {
    "rev": 1500000,
    "exp": 1100000,
    "total_assets": 3000000,
    "current_assets": 900000,
    "liabilities": 1200000
}

# --- СЕКЦИЯ 3: РАСЧЕТЫ ---
rev = base["rev"] * (1 + d_rev)
exp = base["exp"] * (1 + d_exp)
total_assets = base["total_assets"] * (1 + d_assets)
debt = base["liabilities"] * (1 + d_debt)
equity = total_assets - debt
profit = rev - exp

# Коэффициенты
roi = (profit / exp * 100) if exp != 0 else 0
roe = (profit / equity * 100) if equity > 0 else 0
roa = (profit / total_assets * 100) if total_assets > 0 else 0
sol2 = (total_assets / debt) if debt != 0 else 0
sol3 = (equity / debt) if debt != 0 else 0
qr = (base["current_assets"] * (1 + d_assets) / debt) if debt != 0 else 0

# --- СЕКЦИЯ 4: ТАБЛО ПОКАЗАТЕЛЕЙ ---
st.subheader("🚀 Рентабельность и Устойчивость")
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("ROI", f"{roi:.1f}%")
m2.metric("ROE", f"{roe:.1f}%")
m3.metric("ROA", f"{roa:.1f}%")
m4.metric("Sol2", f"{sol2:.2f}")
m5.metric("Quick Ratio", f"{qr:.2f}")

st.markdown("---")

# --- СЕКЦИЯ 5: ВИЗУАЛИЗАЦИЯ (Активы vs Долги) ---
col_left, col_right = st.columns(2)

with col_left:
    # График структуры баланса
    fig_balance = go.Figure(data=[
        go.Bar(name='Активы (Assets)', x=['Баланс'], y=[total_assets], marker_color='#00b4d8'),
        go.Bar(name='Долги (Liabilities)', x=['Баланс'], y=[debt], marker_color='#ef476f'),
        go.Bar(name='Капитал (Equity)', x=['Баланс'], y=[equity], marker_color='#06d6a0')
    ])
    fig_balance.update_layout(title="Структура: Где активы и где долги", barmode='group', template="plotly_dark")
    st.plotly_chart(fig_balance, use_container_width=True)

with col_right:
    # Сравнение ROE / ROA
    fig_rent = go.Figure(data=[
        go.Bar(name='ROE', x=['Рентабельность %'], y=[roe], marker_color='#ffd166'),
        go.Bar(name='ROA', x=['Рентабельность %'], y=[roa], marker_color='#118ab2')
    ])
    fig_rent.update_layout(title="ROE vs ROA", template="plotly_dark", yaxis_ticksuffix="%")
    st.plotly_chart(fig_rent, use_container_width=True)

# --- СЕКЦИЯ 6: SWOT-АНАЛИЗ (Сильные и слабые стороны) ---
st.subheader("🕵️ Анализ сильных и слабых сторон")
swot_1, swot_2 = st.columns(2)

with swot_1:
    st.write("### ✅ Сильные стороны")
    if roi > 20: st.write("- **Высокая маржинальность:** Твой ROI выше 20%, это отличный показатель.")
    if sol2 > 1.5: st.write("- **Устойчивость:** Активов значительно больше, чем долгов.")
    if roe > roa: st.write("- **Финансовый рычаг:** Ты эффективно используешь заемный капитал для роста прибыли.")

with swot_2:
    st.write("### ⚠️ Слабые стороны / Риски")
    if debt > total_assets * 0.6: st.write("- **Задолженность:** Долги составляют более 60% активов. Опасно!")
    if qr < 1.0: st.write("- **Ликвидность:** Денег «здесь и сейчас» может не хватить на покрытие долгов.")
    if profit < 0: st.error("- **Убыточность:** В данной модели расходы превышают доходы!")

st.markdown("---")

# --- СЕКЦИЯ 7: ОБУЧЕНИЕ (Справочник) ---
with st.expander("🎓 Что значат эти буквы? (Справочник и нормы)"):
    st.write("""
    ### 1. ROI (Return on Investment)
    * **Что это:** Окупаемость затрат. Сколько прибыли приносит каждый вложенный доллар в производство.
    * **Норма:** > 15-20%.

    ### 2. ROE (Return on Equity)
    * **Что это:** Рентабельность собственного капитала. Самый важный показатель для владельца.
    * **Норма:** Должен быть выше ROA и выше банковского депозита (обычно > 15%).

    ### 3. ROA (Return on Assets)
    * **Что это:** Насколько эффективно компания использует всё, чем владеет (здания, технику, деньги).
    * **Норма:** Зависит от отрасли, но в среднем > 5-10%.

    ### 4. Solvency 2 (Устойчивость)
    * **Что это:** Соотношение активов к долгам.
    * **Норма:** > 1.5. Если меньше — компания живет "в долг".

    ### 5. Quick Ratio (Ликвидность)
    * **Что это:** Сможешь ли ты завтра отдать долги, если бизнес внезапно закроется.
    * **Норма:** > 1.0.
    """)