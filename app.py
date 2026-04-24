import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# 1. Настройка страницы
st.set_page_config(page_title="Financial OS Intelligence", page_icon="📈", layout="wide")

# 2. Полный мультиязычный словарь (RU, EN, GE)
LANGS = {
    "Русский": {
        "title": "📊 Финансовый Интеллект",
        "settings": "⚙️ Ввод данных",
        "invest_header": "💰 Капитал и Инвестиции",
        "ops_header": "📈 Операционные показатели",
        "sim_header": "🔮 Симулятор рисков",
        "own_cap": "Собственный капитал (Own Capital)",
        "init_inv": "Первоначальные инвестиции",
        "cash": "Наличные (Cash)",
        "ebitda": "EBITDA",
        "net_profit": "Чистая прибыль",
        "tab_main": "🎯 Дашборд",
        "tab_balance": "📊 Структура",
        "tab_info": "📚 Справочник",
        "strong": "✅ Сильные стороны",
        "risks": "⚠️ Зоны внимания",
        "guide": {
            "roi": "**ROI (Return on Investment):** (EBITDA / Первоначальные инвестиции) × 100. Показывает окупаемость вложенных средств.",
            "roe": "**ROE (Return on Equity):** (Чистая прибыль / Собственный капитал) × 100. Эффективность использования ваших личных денег.",
            "cash": "**Cash:** Наличные средства в распоряжении бизнеса. Важнейший показатель ликвидности.",
            "ebitda": "**EBITDA:** Прибыль до вычета процентов, налогов и амортизации. Показывает реальную мощь операционки."
        }
    },
    "English": {
        "title": "📊 Financial Intelligence",
        "settings": "⚙️ Data Input",
        "invest_header": "💰 Equity & Investment",
        "ops_header": "📈 Operations",
        "sim_header": "🔮 Risk Simulator",
        "own_cap": "Own Capital",
        "init_inv": "Initial Investment",
        "cash": "Cash",
        "ebitda": "EBITDA",
        "net_profit": "Net Profit",
        "tab_main": "🎯 Dashboard",
        "tab_balance": "📊 Structure",
        "tab_info": "📚 Guide",
        "strong": "✅ Strengths",
        "risks": "⚠️ Risks",
        "guide": {
            "roi": "**ROI:** (EBITDA / Initial Investment) × 100. Measures return on the total project cost.",
            "roe": "**ROE:** (Net Profit / Own Capital) × 100. Efficiency of your personal equity.",
            "cash": "**Cash:** Liquid funds available for immediate use.",
            "ebitda": "**EBITDA:** Earnings before interest, taxes, depreciation, and amortization."
        }
    },
    "ქართული": {
        "title": "📊 ფინანსური ინტელექტი",
        "settings": "⚙️ მონაცემები",
        "invest_header": "💰 კაპიტალი და ინვესტიცია",
        "ops_header": "📈 ოპერაციები",
        "sim_header": "🔮 რისკების სიმულატორი",
        "own_cap": "საკუთარი კაპიტალი",
        "init_inv": "საწყისი ინვესტიცია",
        "cash": "ნაღდი ფული (Cash)",
        "ebitda": "EBITDA",
        "net_profit": "წმინდა მოგება",
        "tab_main": "🎯 მთავარი",
        "tab_balance": "📊 სტრუქტურა",
        "tab_info": "📚 ცნობარი",
        "strong": "✅ ძლიერი მხარეები",
        "risks": "⚠️ რისკები",
        "guide": {
            "roi": "**ROI:** (EBITDA / საწყისი ინვესტიცია) × 100.",
            "roe": "**ROE:** (წმინდა მოგება / საკუთარი კაპიტალი) × 100.",
            "cash": "**Cash:** ბიზნესის ხელთ არსებული ნაღდი ფული.",
            "ebitda": "**EBITDA:** მოგება გადასახადებამდე და ამორტიზაციამდე."
        }
    }
}

# 3. Мощный CSS (с тенями и карточками)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    [data-testid="stMetric"] {
        background-color: #ffffff; border-radius: 15px; padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 5px solid #00d4ff;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px; background-color: #ffffff; border-radius: 10px 10px 0 0;
        padding: 10px 30px; font-weight: 600;
    }
    .stTabs [aria-selected="true"] { background-color: #1e2130 !important; color: white !important; }
    .section-header { font-size: 22px; font-weight: 700; color: #1e2130; margin: 20px 0; }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR: Ввод данных по твоей методике
with st.sidebar:
    lang_choice = st.selectbox("🌐 Language", list(LANGS.keys()))
    t = LANGS[lang_choice]

    st.header(t["settings"])
    with st.expander(t["invest_header"], expanded=True):
        own_cap = st.number_input(t["own_cap"], value=1000000)
        init_inv = st.number_input(t["init_inv"], value=1500000)
        cash_val = st.number_input(t["cash"], value=300000)

    with st.expander(t["ops_header"], expanded=True):
        ebitda_val = st.number_input(t["ebitda"], value=450000)
        np_val = st.number_input(t["net_profit"], value=320000)

    st.markdown("---")
    st.header(t["sim_header"])
    sim_ebitda_pct = st.slider("EBITDA Change %", -50, 50, 0)

# 5. ЛОГИКА РАСЧЕТОВ (по методике)
# Симулируем EBITDA
current_ebitda = ebitda_val * (1 + sim_ebitda_pct / 100)

# ROI = EBITDA / Initial Investment
roi = (current_ebitda / init_inv * 100) if init_inv != 0 else 0
# ROE = Net Profit / Own Capital
roe = (np_val / own_cap * 100) if own_cap != 0 else 0

# 6. ГЛАВНЫЙ ИНТЕРФЕЙС
st.title(t["title"])
tab1, tab2, tab3 = st.tabs([t["tab_main"], t["tab_balance"], t["tab_info"]])

with tab1:
    st.markdown(f'<div class="section-header">🚀 Key Performance Indicators</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("ROI", f"{roi:.1f}%", help="EBITDA / Initial Investment", delta=f"{sim_ebitda_pct}%")
    c2.metric("ROE", f"{roe:.1f}%", help="Net Profit / Own Capital")
    c3.metric(t["cash"], f"{cash_val:,.0f} $")

    st.markdown("---")
    # Визуальный анализ EBITDA
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=current_ebitda,
        title={'text': f"{t['ebitda']} (Simulated)"},
        gauge={'axis': {'range': [None, ebitda_val * 2]}, 'bar': {'color': "#00d4ff"}}
    ))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    s1, s2 = st.columns(2)
    with s1:
        st.success(f"#### {t['strong']}")
        if roi > 20: st.write(f"High ROI: {roi:.1f}% ✅")
        if cash_val > (init_inv * 0.1): st.write("Healthy Cash Reserve ✅")
    with s2:
        st.warning(f"#### {t['risks']}")
        if current_ebitda < (ebitda_val * 0.7): st.error("Critical EBITDA Drop 🚨")

with tab2:
    st.markdown(f'<div class="section-header">📊 {t["tab_balance"]}</div>', unsafe_allow_html=True)
    df = pd.DataFrame({
        "Parameter": [t["own_cap"], t["init_inv"], t["cash"], t["ebitda"]],
        "Value ($)": [f"{own_cap:,.0f}", f"{init_inv:,.0f}", f"{cash_val:,.0f}", f"{ebitda_val:,.0f}"]
    })
    st.table(df)

with tab3:
    st.markdown(f'<div class="section-header">📚 {t["tab_info"]}</div>', unsafe_allow_html=True)
    st.write(t["guide"]["roi"])
    st.write(t["guide"]["roe"])
    st.write(t["guide"]["cash"])
    st.write(t["guide"]["ebitda"])