import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Financial OS Premium", page_icon="⚖️", layout="wide")

st.title("⚖️ Financial OS: Глубокая аналитика")
st.markdown("---")

# --- СЕКЦИЯ 1: УПРАВЛЕНИЕ (Sidebar) ---
st.sidebar.header("🕹️ Настройка сценария")
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
current_assets = base["current_assets"] * (1 + d_assets)
debt = base["liabilities"] * (1 + d_debt)
equity = total_assets - debt
profit = rev - exp

# 1. ROE / ROA / ROI
roe = (profit / equity * 100) if equity > 0 else 0
roa = (profit / total_assets * 100) if total_assets > 0 else 0
roi = (profit / exp * 100) if exp != 0 else 0

# 2. Solvency 2 (Assets / Debt) - Коэффициент автономии
sol2 = (total_assets / debt) if debt != 0 else 10
# 3. Solvency 3 (Equity / Debt) - Финансовый леверидж
sol3 = (equity / debt) if debt != 0 else 10
# 4. Quick Ratio (Current Assets / Debt) - Быстрая ликвидность
qr = (current_assets / debt) if debt != 0 else 0
# 5. Gearing Ratio (Debt / Equity * 100) - Зависимость от займов
gearing = (debt / equity * 100) if equity > 0 else 0

# --- СЕКЦИЯ 4: ТАБЛО ПОКАЗАТЕЛЕЙ ---
st.subheader("🏁 Ключевые коэффициенты")
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Solvency 2", f"{sol2:.2f}", help="Цель: > 1.5")
col2.metric("Solvency 3", f"{sol3:.2f}", help="Цель: > 1.0")
col3.metric("Quick Ratio", f"{qr:.2f}", help="Цель: > 1.0")
col4.metric("Gearing", f"{gearing:.1f}%", help="Цель: < 50%")
col5.metric("ROE", f"{roe:.1f}%")

st.markdown("---")

# --- СЕКЦИЯ 5: ВИЗУАЛИЗАЦИЯ ---
c1, c2 = st.columns(2)

with c1:
    # Радар устойчивости (сравнение с нормой)
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=[sol2, sol3, qr, min(gearing/10, 5)],
        theta=['Sol 2', 'Sol 3', 'QR', 'Gearing (scaled)'],
        fill='toself',
        name='Текущее состояние',
        line_color='#00d4ff'
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 3])),
        showlegend=False,
        title="Радар финансовой устойчивости",
        template="plotly_dark"
    )
    st.plotly_chart(fig_radar, use_container_width=True)

with c2:
    # Индикатор прибыли
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = profit,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Чистая прибыль ($)"},
        gauge = {'axis': {'range': [None, 1000000]},
                 'bar': {'color': "#00ff88"},
                 'steps' : [
                     {'range': [0, 200000], 'color': "#333"},
                     {'range': [200000, 500000], 'color': "#444"}]}))
    fig_gauge.update_layout(template="plotly_dark")
    st.plotly_chart(fig_gauge, use_container_width=True)

# --- СЕКЦИЯ 6: ПОДРОБНЫЙ ВЕРДИКТ ---
st.subheader("📢 Аналитический отчет")
if gearing > 100:
    st.error(f"🚨 КРИТИЧЕСКИЙ ГЕРИНГ: Долги превышают капитал ({gearing:.1f}%). Срочно рассмотрите возможность докапитализации.")
elif qr < 1.0:
    st.warning(f"⚠️ ПРОБЛЕМА ЛИКВИДНОСТИ: Quick Ratio ({qr:.2f}) ниже нормы. Денег может не хватить на срочные выплаты.")
else:
    st.success("✅ ФИНАНСОВОЕ ЗДОРОВЬЕ: Все показатели устойчивости и ликвидности находятся в зеленой зоне.")

expander = st.expander("Посмотреть расшифровку формул")
expander.write("""
- **Solvency 2 (Автономия):** Способность покрыть все долги общими активами.
- **Solvency 3 (Плечо):** Соотношение собственных денег к заемным.
- **Quick Ratio:** Моментальная готовность платить по счетам текущими активами.
- **Gearing Ratio:** Степень финансового риска и зависимости от кредиторов.
""")