import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Financial OS", page_icon="🏦", layout="wide")

st.title("🏦 Корпоративный финансовый симулятор")
st.markdown("---")

# --- СЕКЦИЯ 1: ГЛОБАЛЬНЫЙ КОНТРОЛЛЕР (Боковая панель) ---
st.sidebar.header("🕹️ Управление сценариями")
st.sidebar.subheader("Рычаги роста")
d_rev = st.sidebar.slider("Δ Выручка (%)", -50, 100, 0) / 100
d_exp = st.sidebar.slider("Δ Расходы (%)", -50, 50, 0) / 100

st.sidebar.subheader("Рычаги долга")
d_debt = st.sidebar.slider("Δ Долги (%)", -100, 100, 0) / 100

# --- СЕКЦИЯ 2: БАЗОВЫЕ ДАННЫЕ (Твои Числители и Знаменатели) ---
# В будущем мы сделаем загрузку этих цифр из Excel
base_data = {
    "Revenue": 1200000,
    "Expenses": 950000,
    "Current_Assets": 800000,  # Оборотные активы (для QR)
    "Total_Assets": 2500000,   # Все активы (для Sol)
    "Liabilities": 1100000     # Долги
}

# --- СЕКЦИЯ 3: РАСЧЕТ ПРОГНОЗА ---
prog_rev = base_data["Revenue"] * (1 + d_rev)
prog_exp = base_data["Expenses"] * (1 + d_exp)
prog_debt = base_data["Liabilities"] * (1 + d_debt)

# Считаем показатели по твоим формулам
roi = ((prog_rev - prog_exp) / prog_exp) * 100
sol2 = (base_data["Total_Assets"] / prog_debt) if prog_debt != 0 else 0
qr = (base_data["Current_Assets"] / prog_debt) if prog_debt != 0 else 0

# --- СЕКЦИЯ 4: ВИЗУАЛИЗАЦИЯ (Метрики) ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("ROI (Рентабельность)", f"{roi:.1f}%", delta=f"{d_rev*100:.1f}% Rev")
with col2:
    color = "normal" if sol2 > 1.5 else "inverse"
    st.metric("Sol2 (Устойчивость)", f"{sol2:.2f}", delta=f"{d_debt*100:.1f}% Debt", delta_color=color)
with col3:
    st.metric("QR (Ликвидность)", f"{qr:.2f}")
with col4:
    st.metric("Прогноз Долга", f"{prog_debt:,.0f} $")

st.markdown("---")

# --- СЕКЦИЯ 5: ГРАФИК (Сравнение показателей) ---
# Создаем полоски как в Notion, но круче
fig = go.Figure()

# Полоска ROI
fig.add_trace(go.Bar(
    name='ROI %',
    x=['Показатели'], y=[roi],
    marker_color='green' if roi > 20 else 'orange'
))

# Полоска Sol2 (делим на 10 для масштаба, чтобы графики были сопоставимы)
fig.add_trace(go.Bar(
    name='Sol2 (Масштаб 1:10)',
    x=['Показатели'], y=[sol2 * 10],
    marker_color='blue'
))

fig.update_layout(
    barmode='group',
    template="plotly_dark",
    title="Визуальный анализ сценария",
    yaxis_range=[0, 100] # Тот самый "ограничитель", чтобы проценты не улетали
)

st.plotly_chart(fig, use_container_width=True)

# СЕКЦИЯ 6: ТЕКСТОВЫЙ ВЕРДИКТ (Авто-аналитика)
st.subheader("📝 Аналитический отчет")
if sol2 < 1.0:
    st.error("ВНИМАНИЕ: Критический уровень долга! Предприятие неустойчиво.")
elif roi > 30:
    st.success("ОТЛИЧНО: Высокая эффективность операций при текущем сценарии.")
else:
    st.info("Стабильно: Показатели в пределах нормы.")