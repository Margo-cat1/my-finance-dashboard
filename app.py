import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# 1. Настройка страницы
st.set_page_config(page_title="Financial OS Intelligence", page_icon="📈", layout="wide")

# 2. Мощный CSS для крутого интерфейса
st.markdown("""
    <style>
    /* Общий фон и шрифт */
    .main { background-color: #f8f9fa; }

    /* Стилизация карточек метрик */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #00d4ff;
    }

    /* Кастомные заголовки разделов */
    .section-header {
        font-size: 24px;
        font-weight: 700;
        color: #1e2130;
        margin-bottom: 20px;
        padding-top: 10px;
    }

    /* Стилизация вкладок */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #ffffff;
        border-radius: 10px 10px 0 0;
        border: 1px solid #e0e0e0;
        padding: 10px 30px;
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab"]:hover { color: #00d4ff; }
    .stTabs [aria-selected="true"] { background-color: #1e2130 !important; color: white !important; }

    /* Инфо-блоки */
    .stAlert { border-radius: 12px; border: none; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (Твоя логика ввода) ---
with st.sidebar:
    st.title("⚙️ Настройки")
    with st.expander("💼 Баланс (Assets)", expanded=True):
        fa = st.number_input("Fixed Assets", value=2100000)
        ca = st.number_input("Current Assets", value=900000)
    with st.expander("💸 Долги (Liabilities)", expanded=True):
        ltl = st.number_input("Long-term Debt", value=800000)
        stl = st.number_input("Short-term Debt", value=400000)
    with st.expander("📊 Операционка", expanded=True):
        input_rev = st.number_input("Выручка (Base)", value=1500000)
        input_exp = st.number_input("Расходы (Base)", value=1100000)

    st.markdown("---")
    st.header("🔮 Симулятор")
    sim_rev_pct = st.slider("Изменение Выручки (%)", -50, 50, 0)
    sim_exp_pct = st.slider("Изменение Расходов (%)", -50, 50, 0)

# --- ЛОГИКА РАСЧЕТОВ ---
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

# --- ИНТЕРФЕЙС ---
st.title("🚀 Financial OS Intelligence")

tab1, tab2, tab3 = st.tabs(["🎯 Главная Панель", "📊 Анализ Баланса", "📚 Справочник"])

with tab1:
    # Блок рентабельности
    st.markdown('<div class="section-header">🔥 Эффективность и Прибыль</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Чистая прибыль", f"{profit:,.0f} $", delta=f"{sim_rev_pct}%")
    with c2:
        st.metric("ROI (Окупаемость)", f"{roi:.1f}%")
    with c3:
        st.metric("ROE (На капитал)", f"{roe:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # Блок устойчивости
    st.markdown(
        '<div class="section-header" style="border-top: 1px solid #ddd; padding-top:20px;">🛡️ Устойчивость и Риски</div>',
        unsafe_allow_html=True)
    c4, c5, c6 = st.columns(3)
    with c4:
        st.metric("Solvency 2 (Автономия)", f"{sol2:.2f}")
    with c5:
        st.metric("Solvency 3 (GB)", f"{sol3:.2f}")
    with c6:
        st.metric("Quick Ratio (Ликвидность)", f"{qr:.2f}")

    st.markdown("---")

    # Визуальный SWOT
    swot_col1, swot_col2 = st.columns(2)
    with swot_col1:
        st.success("#### ✅ СИЛЬНЫЕ СТОРОНЫ")
        if roi > 20: st.markdown(f"**Высокая маржа:** ROI {roi:.1f}% — производство эффективно.")
        if sol3 >= 1.0: st.markdown(f"**Golden Balance:** Собственный капитал ({equity:,.0f} $) перекрывает долги.")
        if roe > roa: st.markdown("**Рычаг:** Вы зарабатываете на заемных средствах.")

    with swot_col2:
        st.warning("#### ⚠️ ЗОНЫ ВНИМАНИЯ")
        if qr < 1.0: st.markdown(f"**Риск ликвидности:** QR {qr:.2f} — может не хватить кэша на счета.")
        if sol2 < 1.5: st.markdown("**Зависимость:** Слишком много долгов относительно активов.")
        if profit < 0: st.markdown("**🚨 УБЫТОК:** Срочно сокращайте переменные расходы!")

with tab2:
    st.markdown('<div class="section-header">📊 Глубокий разбор баланса</div>', unsafe_allow_html=True)
    t_left, t_right = st.columns([1, 1.2])

    with t_left:
        st.write("#### 📑 Текущие цифры")
        df_display = pd.DataFrame({
            "Параметр": ["Внеоборотные активы", "Оборотные активы", "Ваш Капитал", "Общий Долг"],
            "Сумма ($)": [f"{fa:,.0f}", f"{ca:,.0f}", f"{equity:,.0f}", f"{total_liabilities:,.0f}"]
        })
        st.table(df_display)

    with t_right:
        st.write("#### ⚖️ Распределение Капитал / Долг")
        fig = go.Figure(data=[
            go.Pie(labels=['Equity (Свои)', 'Debt (Долги)'], values=[max(0, equity), total_liabilities], hole=.5)])
        fig.update_layout(height=350, margin=dict(t=20, b=20, l=0, r=0), showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown('<div class="section-header">📚 База знаний</div>', unsafe_allow_html=True)
    with st.expander("Что такое ROI?"):