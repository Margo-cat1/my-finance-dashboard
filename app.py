import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Financial OS PRO", page_icon="📈", layout="wide")

st.title("📊 Financial OS: Полный анализ показателей")
st.markdown("---")

# --- СЕКЦИЯ 1: УПРАВЛЕНИЕ (Sidebar) ---
st.sidebar.header("🕹️ Глобальные рычаги")

st.sidebar.subheader("Доходы и Расходы")
d_rev = st.sidebar.slider("Изменение Выручки (%)", -50, 100, 0) / 100
d_exp = st.sidebar.slider("Изменение Расходов (%)", -50, 50, 0) / 100

st.sidebar.subheader("Баланс")
d_assets = st.sidebar.slider("Изменение Активов (%)", -20, 50, 0) / 100
d_debt = st.sidebar.slider("Изменение Долгов (%)", -50, 100, 0) / 100

# --- СЕКЦИЯ 2: БАЗОВЫЕ ЦИФРЫ ---
# Эти данные — фундамент. Позже мы привяжем их к Excel.
base = {
    "rev": 1500000,
    "exp": 1100000,
    "current_assets": 900000,
    "total_assets": 3000000,
    "liabilities": 1200000
}

# --- СЕКЦИЯ 3: РАСЧЕТ ВСЕХ ФОРМУЛ ---
rev = base["rev"] * (1 + d_rev)
exp = base["exp"] * (1 + d_exp)
assets = base["total_assets"] * (1 + d_assets)
current_assets = base["current_assets"] * (1 + d_assets)
debt = base["liabilities"] * (1 + d_debt)

# 1. ROI (Return on Investment)
profit = rev - exp
roi = (profit / exp * 100) if exp != 0 else 0

# 2. Solvency 2 (Автономия: насколько мы зависим от долгов)
sol2 = (assets / debt) if debt != 0 else 10

# 3. Solvency 3 (Покрытие долга капиталом)
equity = assets - debt
sol3 = (equity / debt) if debt != 0 else 10

# 4. Quick Ratio (Ликвидность: сможем ли быстро раздать долги)
qr = (current_assets / debt) if debt != 0 else 0

# --- СЕКЦИЯ 4: ТАБЛО ПОКАЗАТЕЛЕЙ (Metrics) ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("ROI", f"{roi:.1f}%", delta=f"{d_rev*100:.0f}%")
c2.metric("Sol2 (Устойчивость)", f"{sol2:.2f}", help="Цель: > 1.5")
c3.metric("Sol3 (Капитал/Долг)", f"{sol3:.2f}")
c4.metric("QR (Ликвидность)", f"{qr:.2f}", help="Цель: > 1.0")

st.markdown("---")

# --- СЕКЦИЯ 5: ВИЗУАЛЬНЫЙ АНАЛИЗ (Графики) ---
col_left, col_right = st.columns(2)

with col_left:
    # График прибыли
    fig_profit = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = profit,
        title = {'text': "Прогнозная Прибыль ($)"},
        gauge = {'axis': {'range': [None, 1000000]},
                 'bar': {'color': "#2ecc71"}}
    ))
    st.plotly_chart(fig_profit, use_container_width=True)

with col_right:
    # Сравнение коэффициентов
    fig_comp = go.Figure(data=[
        go.Bar(name='Текущий', x=['Sol2', 'Sol3', 'QR'], y=[1.5, 1.0, 1.0], marker_color='#95a5a6'),
        go.Bar(name='Прогноз', x=['Sol2', 'Sol3', 'QR'], y=[sol2, sol3, qr], marker_color='#3498db')
    ])
    fig_comp.update_layout(title="Сравнение с нормативами", barmode='group', template="plotly_dark")
    st.plotly_chart(fig_comp, use_container_width=True)

# --- СЕКЦИЯ 6: АВТО-ВЕРДИКТ ---
st.subheader("🤖 Аналитическое заключение")
if sol2 < 1.2 or qr < 0.8:
    st.error("⚠️ РИСК: Низкая ликвидность или высокая долговая нагрузка. Рекомендуется сократить расходы.")
elif roi > 25:
    st.success("✅ РОСТ: Модель показывает высокую эффективность. Можно рассмотреть инвестиции.")
else:
    st.info("ℹ️ СТАБИЛЬНО: Показатели находятся в пределах допустимых значений.")