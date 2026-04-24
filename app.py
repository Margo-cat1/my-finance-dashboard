import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Financial OS Ultimate", page_icon="💎", layout="wide")

st.title("💎 Financial Intelligence Dashboard")
st.markdown("---")

# --- СЕКЦИЯ 1: УПРАВЛЕНИЕ (Sidebar) ---
st.sidebar.header("🕹️ Управление сценариями")
d_rev = st.sidebar.slider("Изменение Выручки (%)", -50, 100, 0) / 100
d_exp = st.sidebar.slider("Изменение Расходов (%)", -50, 50, 0) / 100
d_assets = st.sidebar.slider("Изменение Активов (%)", -20, 50, 0) / 100
d_debt = st.sidebar.slider("Изменение Долгов (%)", -50, 100, 0) / 100

# --- СЕКЦИЯ 2: БАЗОВЫЕ ДАННЫЕ ---
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

# Новые формулы:
# ROE = Чистая прибыль / Собственный капитал
roe = (profit / equity * 100) if equity > 0 else 0

# ROA = Чистая прибыль / Общие активы
roa = (profit / total_assets * 100) if total_assets > 0 else 0

# Старые формулы для полноты картины:
roi = (profit / exp * 100) if exp != 0 else 0
sol2 = (total_assets / debt) if debt != 0 else 0

# --- СЕКЦИЯ 4: ГЛАВНЫЕ МЕТРИКИ (ROE, ROA, ROI) ---
st.subheader("📈 Показатели рентабельности")
m1, m2, m3 = st.columns(3)
m1.metric("ROE (Капитал)", f"{roe:.1f}%", help="Насколько эффективно работают деньги собственников")
m2.metric("ROA (Активы)", f"{roa:.1f}%", help="Эффективность использования всех ресурсов компании")
m3.metric("ROI (Инвестиции)", f"{roi:.1f}%", help="Окупаемость затрат")

st.markdown("---")

# --- СЕКЦИЯ 5: ВИЗУАЛИЗАЦИЯ ---
c1, c2 = st.columns(2)

with c1:
    # График структуры (Капитал vs Долг)
    fig_structure = go.Figure(data=[go.Pie(
        labels=['Собственный капитал', 'Долги'],
        values=[max(0, equity), debt],
        hole=.4,
        marker_colors=['#2ecc71', '#e74c3c']
    )])
    fig_structure.update_layout(title="Структура финансирования", template="plotly_dark")
    st.plotly_chart(fig_structure, use_container_width=True)

with c2:
    # Сравнение ROE и ROA
    fig_compare = go.Figure(data=[
        go.Bar(name='ROE', x=['Рентабельность'], y=[roe], marker_color='#f1c40f'),
        go.Bar(name='ROA', x=['Рентабельность'], y=[roa], marker_color='#3498db')
    ])
    fig_compare.update_layout(title="ROE vs ROA", template="plotly_dark", yaxis_suffix="%")
    st.plotly_chart(fig_compare, use_container_width=True)

# --- СЕКЦИЯ 6: АВТО-АНАЛИЗ ---
st.subheader("🔍 Что это значит?")
col_text1, col_text2 = st.columns(2)

with col_text1:
    if roe > roa:
        st.info(f"ROE ({roe:.1f}%) выше ROA ({roa:.1f}%). Это значит, что компания успешно использует 'эффект рычага' — заемные средства помогают зарабатывать больше для собственников.")
    else:
        st.warning("ROE ниже или равен ROA. Вероятно, долги обходятся компании слишком дорого или капитал используется неэффективно.")

with col_text2:
    if sol2 < 1.5:
        st.error(f"Внимание! Коэффициент устойчивости Sol2 ({sol2:.2f}) ниже нормы. Риск слишком высокой долговой нагрузки.")
    else:
        st.success(f"Финансовая устойчивость в норме (Sol2: {sol2:.2f}).")