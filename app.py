import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# 1. Настройка страницы
st.set_page_config(page_title="Financial Intelligence Dashboard", page_icon="📈", layout="wide")

# 2. Полный мультиязычный словарь
LANGS = {
    "Русский": {
        "title": "📊 Финансовый Интеллект",
        "settings": "⚙️ Ввод данных",
        "assets": "💼 Активы (Assets)",
        "liabilities": "💸 Долги (Liabilities)",
        "ops": "📈 Операционка & Капитал",
        "sim": "🔮 Симулятор",
        "fa": "Fixed Assets (Внеоборотные)",
        "ca": "Current Assets (Оборотные)",
        "ltl": "Long-term (Долгосрочные)",
        "stl": "Short-term (Краткосрочные)",
        "own_cap": "Собственный капитал (Own Capital)",
        "init_inv": "Первоначальные инвестиции",
        "cash": "Наличные (Cash)",
        "ebitda": "EBITDA",
        "np": "Чистая прибыль (Net Profit)",
        "tab1": "🎯 Дашборд",
        "tab2": "📊 Детали баланса",
        "tab3": "📚 Справочник",
        "strong": "✅ Сильные стороны",
        "risks": "⚠️ Зоны внимания",
        "guide": [
            "**ROI:** (EBITDA / Первоначальные инвестиции) × 100. Окупаемость проекта.",
            "**ROE:** (Net Profit / Собственный капитал) × 100. Эффективность ваших денег.",
            "**ROA:** Чистая прибыль / Всего активов.",
            "**Solvency 3:** Собственный капитал / Общие долги. Если > 1.0 — это Золотой Баланс.",
            "**Quick Ratio:** Оборотные активы / Краткосрочные долги. Способность платить по счетам."
        ]
    },
    "English": {
        "title": "📊 Financial Intelligence",
        "settings": "⚙️ Data Input",
        "assets": "💼 Assets",
        "liabilities": "💸 Liabilities",
        "ops": "📈 Ops & Equity",
        "sim": "🔮 Simulator",
        "fa": "Fixed Assets",
        "ca": "Current Assets",
        "ltl": "Long-term Debt",
        "stl": "Short-term Debt",
        "own_cap": "Own Capital",
        "init_inv": "Initial Investment",
        "cash": "Cash",
        "ebitda": "EBITDA",
        "np": "Net Profit",
        "tab1": "🎯 Dashboard",
        "tab2": "📊 Balance Details",
        "tab3": "📚 Guide",
        "strong": "✅ Strengths",
        "risks": "⚠️ Risks",
        "guide": [
            "**ROI:** (EBITDA / Initial Investment) × 100.",
            "**ROE:** (Net Profit / Own Capital) × 100.",
            "**ROA:** Net Profit / Total Assets.",
            "**Solvency 3:** Own Capital / Total Liabilities.",
            "**Quick Ratio:** Current Assets / Short-term Debt."
        ]
    },
    "ქართული": {
        "title": "📊 ფინანსური ინტელექტი",
        "settings": "⚙️ მონაცემები",
        "assets": "💼 აქტივები",
        "liabilities": "💸 ვალდებულებები",
        "ops": "📈 ოპერაციები და კაპიტალი",
        "sim": "🔮 სიმულატორი",
        "fa": "გრძელვადიანი აქტივები",
        "ca": "მიმდინარე აქტივები",
        "ltl": "გრძელვადიანი ვალი",
        "stl": "მოკლევადიანი ვალი",
        "own_cap": "საკუთარი კაპიტალი",
        "init_inv": "საწყისი ინვესტიცია",
        "cash": "ნაღდი ფული (Cash)",
        "ebitda": "EBITDA",
        "np": "წმინდა მოგება",
        "tab1": "🎯 მთავარი",
        "tab2": "📊 ბალანსი",
        "tab3": "📚 ცნობარი",
        "strong": "✅ ძლიერი მხარეები",
        "risks": "⚠️ რისკები",
        "guide": [
            "**ROI:** (EBITDA / საწყისი ინვესტიცია) × 100.",
            "**ROE:** (წმინდა მოგება / საკუთარი კაპიტალი) × 100.",
            "**ROA:** წმინდა მოგება / ჯამური აქტივები.",
            "**Solvency 3:** საკუთარი კაპიტალი / ჯამური ვალდებულებები.",
            "**Quick Ratio:** მიმდინარე აქტივები / მოკლევადიანი ვალი."
        ]
    }
}

# 3. Стильный CSS
st.markdown("""
    <style>
    [data-testid="stMetric"] {
        background-color: #ffffff; border-radius: 15px; padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 5px solid #00d4ff;
    }
    .stTabs [aria-selected="true"] { background-color: #1e2130 !important; color: white !important; }
    .section-header { font-size: 22px; font-weight: 700; color: #1e2130; margin: 20px 0; }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR: Полный набор данных
with st.sidebar:
    lang_choice = st.selectbox("🌐 Choose Language", list(LANGS.keys()))
    t = LANGS[lang_choice]
    st.header(t["settings"])

    with st.expander(t["assets"], expanded=True):
        fa = st.number_input(t["fa"], value=2100000)
        ca = st.number_input(t["ca"], value=900000)

    with st.expander(t["liabilities"], expanded=True):
        ltl = st.number_input(t["ltl"], value=800000)
        stl = st.number_input(t["stl"], value=400000)

    with st.expander(t["ops"], expanded=True):
        own_cap = st.number_input(t["own_cap"], value=1000000)
        init_inv = st.number_input(t["init_inv"], value=1500000)
        cash_val = st.number_input(t["cash"], value=300000)
        ebitda_val = st.number_input(t["ebitda"], value=450000)
        np_val = st.number_input(t["np"], value=320000)

    st.markdown("---")
    st.header(t["sim"])
    sim_ebitda = st.slider("EBITDA Change %", -50, 50, 0)

# 5. РАСЧЕТЫ (Классическая школа)
current_ebitda = ebitda_val * (1 + sim_ebitda / 100)
total_assets = fa + ca
total_liabilities = ltl + stl

roi = (current_ebitda / init_inv * 100) if init_inv != 0 else 0
roe = (np_val / own_cap * 100) if own_cap != 0 else 0
roa = (np_val / total_assets * 100) if total_assets != 0 else 0
sol3 = (own_cap / total_liabilities) if total_liabilities != 0 else 0
qr = (ca / stl) if stl != 0 else 0

# 6. ГЛАВНЫЙ ИНТЕРФЕЙС
st.title(t["title"])
tab1, tab2, tab3 = st.tabs([t["tab1"], t["tab2"], t["tab3"]])

with tab1:
    st.markdown('<div class="section-header">🔥 Рентабельность и Эффективность</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("ROI (Project)", f"{roi:.1f}%", delta=f"{sim_ebitda}%")
    c2.metric("ROE (Equity)", f"{roe:.1f}%")
    c3.metric("ROA (Assets)", f"{roa:.1f}%")

    st.markdown('<div class="section-header">🛡️ Устойчивость и Ликвидность</div>', unsafe_allow_html=True)
    c4, c5, c6 = st.columns(3)
    c4.metric("Solvency 3", f"{sol3:.2f}")
    c5.metric("Quick Ratio", f"{qr:.2f}")
    c6.metric(t["cash"], f"{cash_val:,.0f} $")

    st.markdown("---")
    s1, s2 = st.columns(2)
    with s1:
        st.success(f"#### {t['strong']}")
        if sol3 >= 1.0: st.write("Golden Balance ✅")
        if roi > 25: st.write("Excellent Project ROI ✅")
    with s2:
        st.warning(f"#### {t['risks']}")
        if qr < 1.0: st.error("Liquidity Risk 🚨")
        if cash_val < (stl * 0.5): st.error("Low Cash Buffer 🚨")

with tab2:
    st.markdown(f"#### {t['tab2']}")
    col_t, col_p = st.columns([1, 1.2])
    with col_t:
        st.table(pd.DataFrame({
            "Category": ["Fixed Assets", "Current Assets", "Own Capital", "Total Liabilities"],
            "Value ($)": [f"{fa:,.0f}", f"{ca:,.0f}", f"{own_cap:,.0f}", f"{total_liabilities:,.0f}"]
        }))
    with col_p:
        fig = go.Figure(data=[go.Pie(labels=['Own Capital', 'Total Debt'],
                                     values=[max(0, own_cap), total_liabilities], hole=.4)])
        fig.update_layout(height=350, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown(f'<div class="section-header">📚 {t["tab3"]}</div>', unsafe_allow_html=True)
    for item in t["guide"]:
        st.write(item)