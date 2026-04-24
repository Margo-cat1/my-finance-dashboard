import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# 1. Настройка страницы
st.set_page_config(page_title="Financial Intelligence PRO", page_icon="📈", layout="wide")

# 2. Словарь (RU, EN, GE)
LANGS = {
    "Русский": {
        "title": "📊 Финансовый Интеллект",
        "settings": "⚙️ Ввод данных",
        "assets": "💼 Активы (Assets)",
        "liabilities": "💸 Долги (Liabilities)",
        "ops": "📈 Операционка & Капитал",
        "fa": "Fixed Assets", "ca": "Current Assets",
        "ltl": "Long-term Debt", "stl": "Short-term Debt",
        "own_cap": "Собственный капитал",
        "init_inv": "Первоначальные инвестиции",
        "cash": "Наличные (Cash)",
        "ebitda": "EBITDA", "np": "Чистая прибыль",
        "tab1": "🎯 Дашборд", "tab2": "📊 Структура", "tab3": "📚 Справочник",
        "guide": {
            "roi": "**ROI:** EBITDA / Первоначальные инвестиции. Окупаемость проекта.",
            "roe": "**ROE:** Чистая прибыль / Собственный капитал. Эффективность ваших денег.",
            "sol2": "**Solvency 2 (Net Assets):** Total Assets - Total Liabilities. Ваш чистый капитал.",
            "sol3": "**Solvency 3 (%):** (Чистый капитал / Total Assets) × 100. Доля собственности в активах.",
            "qr": "**Quick Ratio:** Cash / Short-term Liabilities. Мгновенная ликвидность."
        }
    },
    "English": {
        "title": "📊 Financial Intelligence",
        "settings": "⚙️ Data Input",
        "assets": "💼 Assets", "liabilities": "💸 Liabilities",
        "ops": "📈 Ops & Equity",
        "fa": "Fixed Assets", "ca": "Current Assets",
        "ltl": "Long-term Debt", "stl": "Short-term Debt",
        "own_cap": "Own Capital", "init_inv": "Initial Investment",
        "cash": "Cash", "ebitda": "EBITDA", "np": "Net Profit",
        "tab1": "🎯 Dashboard", "tab2": "📊 Structure", "tab3": "📚 Guide",
        "guide": {
            "roi": "**ROI:** EBITDA / Initial Investment.",
            "roe": "**ROE:** Net Profit / Own Capital.",
            "sol2": "**Solvency 2:** Total Assets - Total Liabilities.",
            "sol3": "**Solvency 3 (%):** (Net Assets / Total Assets) × 100.",
            "qr": "**Quick Ratio:** Cash / Short-term Liabilities."
        }
    },
    "ქართული": {
        "title": "📊 ფინანსური ინტელექტი",
        "settings": "⚙️ მონაცემები",
        "assets": "💼 აქტივები", "liabilities": "💸 ვალდებულებები",
        "ops": "📈 ოპერაციები",
        "own_cap": "საკუთარი კაპიტალი", "init_inv": "საწყისი ინვესტიცია",
        "cash": "Cash", "ebitda": "EBITDA", "np": "წმინდა მოგება",
        "tab1": "🎯 მთავარი", "tab2": "📊 ბალანსი", "tab3": "📚 ცნობარი",
        "guide": {
            "roi": "**ROI:** EBITDA / საწყისი ინვესტიცია.",
            "roe": "**ROE:** წმინდა მოგება / საკუთარი კაპიტალი.",
            "sol2": "**Solvency 2:** ჯამური აქტივები - ჯამური ვალდებულებები.",
            "sol3": "**Solvency 3 (%):** (წმინდა აქტივები / ჯამური აქტივები) × 100.",
            "qr": "**Quick Ratio:** Cash / მოკლევადიანი ვალი."
        }
    }
}

# 3. CSS
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

# 4. SIDEBAR
with st.sidebar:
    lang_choice = st.selectbox("🌐 Language", list(LANGS.keys()))
    t = LANGS[lang_choice]

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

    sim_ebitda = st.slider("EBITDA Change %", -50, 50, 0)

# 5. ИСПРАВЛЕННЫЕ ФОРМУЛЫ
total_assets = fa + ca
total_liabilities = ltl + stl
current_ebitda = ebitda_val * (1 + sim_ebitda / 100)

roi = (current_ebitda / init_inv * 100) if init_inv != 0 else 0
roe = (np_val / own_cap * 100) if own_cap != 0 else 0

# Solvency 2 (Чистые активы / Капитал в деньгах)
sol2_val = total_assets - total_liabilities

# Solvency 3 (Коэффициент автономии в %)
sol3_pct = (sol2_val / total_assets * 100) if total_assets != 0 else 0

# Quick Ratio (По твоей просьбе: только Cash)
qr = (cash_val / stl) if stl != 0 else 0

# 6. ИНТЕРФЕЙС
st.title(t["title"])
tab1, tab2, tab3 = st.tabs([t["tab1"], t["tab2"], t["tab3"]])

with tab1:
    st.markdown('<div class="section-header">🚀 Эффективность</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("ROI", f"{roi:.1f}%", delta=f"{sim_ebitda}%")
    c2.metric("ROE", f"{roe:.1f}%")
    c3.metric(t["ebitda"], f"{current_ebitda:,.0f} $")

    st.markdown('<div class="section-header">🛡️ Устойчивость и Ликвидность</div>', unsafe_allow_html=True)
    c4, c5, c6 = st.columns(3)
    c4.metric("Solvency 2 (Net Assets)", f"{sol2_val:,.0f} $")
    c5.metric("Solvency 3 (%)", f"{sol3_pct:.1f}%")
    c6.metric("Quick Ratio (Cash/STL)", f"{qr:.2f}")

with tab2:
    st.table(pd.DataFrame({
        "Parameter": ["Total Assets", "Total Liabilities", "Own Capital", "Net Assets (Sol2)", "Cash"],
        "Value ($)": [f"{total_assets:,.0f}", f"{total_liabilities:,.0f}", f"{own_cap:,.0f}", f"{sol2_val:,.0f}",
                      f"{cash_val:,.0f}"]
    }))

with tab3:
    st.markdown(f'<div class="section-header">📚 {t["tab3"]}</div>', unsafe_allow_html=True)
    st.write(t["guide"]["roi"])
    st.write(t["guide"]["roe"])
    st.write(t["guide"]["sol2"])
    st.write(t["guide"]["sol3"])
    st.write(t["guide"]["qr"])