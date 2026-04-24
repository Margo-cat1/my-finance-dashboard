import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Financial OS Ultimate", page_icon="🏆", layout="wide")

st.title("🏆 Financial OS: Full Analytics Suite")
st.markdown("---")

# --- СЕКЦИЯ 1: SIDEBAR ---
st.sidebar.header("🕹️ Настройка сценария")
d_rev = st.sidebar.slider("Изменение Выручки (%)", -50, 100, 0) / 100
d_exp = st.sidebar.slider("Изменение Расходов (%)", -50, 50, 0) / 100
d_assets = st.sidebar.slider("Изменение Активов (%)", -20, 50, 0) / 100
d_debt = st.sidebar.slider("Изменение Долгов (%)", -50, 100, 0) / 100

# --- СЕКЦИЯ 2: БАЗА ---
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
current_assets = base["current_assets"] * (1 + d_assets)
debt = base["liabilities"] * (1 + d_debt)
equity = total_assets - debt
profit = rev - exp

# ГРУППА 1: Рентабельность
roi = (profit / exp * 100) if exp != 0 else 0
roe = (profit / equity * 100) if equity > 0 else 0
roa = (profit / total_assets * 100) if total_assets > 0 else 0

# ГРУППА 2: Устойчивость
sol2 = (total_assets / debt) if debt != 0 else 0
sol3 = (equity / debt) if debt != 0 else 0

# ГРУППА 3: Ликвидность и Долг
qr = (current_assets / debt) if debt != 0 else 0
gearing = (debt / equity * 100) if equity > 0 else 0

# --- СЕКЦИЯ 4: ТАБЛО МЕТРИК ---
st.subheader("📊 Ключевые показатели")
# Ряд 1: Рентабельность
row1_1, row1_2, row1_3 = st.columns(3)
row1_1.metric("ROI (Инвестиции)", f"{roi:.1f}%")
row1_2.metric("ROE (Капитал)", f"{roe:.1f}%")
row1_3.metric("ROA (Активы)", f"{roa:.1f}%")

# Ряд 2: Устойчивость и Риски
row2_1, row2_2, row2_3, row2_4 = st.columns(4)
row2_1.metric("Solvency 2", f"{sol2:.2f}")
row2_2.metric("Solvency 3", f"{sol3:.2f}")
row2_3.metric("Quick Ratio", f"{qr:.2f}")
row2_4.metric("Gearing", f"{gearing:.1f}%")

st.markdown("---")

# --- СЕКЦИЯ 5: ВИЗУАЛИЗАЦИЯ ---
c1, c2 = st.columns(2)

with c1:
    # Сравнение всех % рентабельности
    fig_rent = go.Figure(data=[
        go.Bar(name='ROI', x=['Показатели %'], y=[roi], marker_color='#2ecc71'),
        go.Bar(name='ROE', x=['Показатели %'], y=[roe], marker_color='#f1c40f'),
        go.Bar(name='ROA', x=['Показатели %'], y=[roa], marker_color='#3498db')
    ])
    fig_rent.update_layout(title="Сравнение рентабельности", template="plotly_dark", yaxis_ticksuffix="%")
    st.plotly_chart(fig_rent, use_container_width=True)

with c2:
    # Структура Капитал/Долг
    fig_pie = go.Figure(data=[go.Pie(labels=['Свой капитал', 'Долги'], values=[max(0, equity), debt], hole=.4)])
    fig_pie.update_layout(title="Баланс: Свои vs Заемные", template="plotly_dark")
    st.plotly_chart(fig_pie, use_container_width=True)

# --- СЕКЦИЯ 6: ВЕРДИКТ ---
st.subheader("📢 Аналитика")
if roe > roa:
    st.success(f"Эффект финансового рычага работает: ROE ({roe:.1f}%) выше ROA. Вы эффективно используете долг.")
else:
    st.warning("Внимание: Низкая отдача на капитал относительно активов.")