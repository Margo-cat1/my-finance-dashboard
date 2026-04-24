import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# 1. Настройка страницы
st.set_page_config(page_title="Financial Intelligence Dashboard", page_icon="📈", layout="wide")

# 2. Словарь переводов
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
            "roi": "**ROI:** EBITDA / Первоначальные инвестиции * 100%.",
            "roe": "**ROE:** EBITDA / Собственный капитал * 100%.",
            "roa": "**ROA:** EBITDA / Всего долгов (Total Liabilities) * 100%.",
            "sol2": "**Solvency 2:** Активы - Долги (Чистые активы).",
            "sol3": "**Solvency 3 (%):** (Чистые активы / Общие активы) * 100%.",
            "qr": "**Quick Ratio:** Cash / Short-term Liabilities."
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
            "roi": "**ROI:** EBITDA / Initial Investment * 100%.",
            "roe": "**ROE:** EBITDA / Own Capital * 100%.",
            "roa": "**ROA:** EBITDA / Total Liabilities * 100%.",
            "sol2": "**Solvency 2:** Total Assets - Total Liabilities.",
            "sol3": "**Solvency 3 (%):** (Net Assets / Total Assets) * 100%.",
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
            "roi": "**ROI:** EBITDA / საწყისი ინვესტიცია * 100%.",
            "roe": "**ROE:** EBITDA / საკუთარი კაპიტალი * 100%.",
            "roa": "**ROA:** EBITDA / ჯამური ვალდებულებები * 100%.",
            "sol2": "**Solvency 2:** აქტივები - ვალდებულებები.",
            "sol3": "**Solvency 3 (%):** (წმინდა აქტივები / ჯამური აქტივები) * 100%.",
            "qr": "**Quick Ratio:** Cash / მოკლევადიანი ვალი."
        }
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

    sim_ebitda = st.slider("EBITDA Change %", -50, 50, 0)

# 5. ИСПРАВЛЕННЫЕ ФОРМУЛЫ (Строго по твоему запросу)
total_assets = fa + ca
total_liabilities = ltl + stl
current_ebitda = ebitda_val * (1 + sim_ebitda / 100)

# ROI = EBITDA / Initial Investment
roi = (current_ebitda / init_inv * 100) if init_inv != 0 else 0

# ROE = EBITDA / Own Capital
roe = (current_ebitda / own_cap * 100) if own_cap != 0 else 0

# ROA = EBITDA / Total Liabilities
roa = (current_ebitda / total_liabilities * 100) if total_liabilities != 0 else 0

# Solvency 2 (Net Assets)
sol2_val = total_assets - total_liabilities

# Solvency 3 (%)
sol3_pct = (sol2_val / total_assets * 100) if total_assets != 0 else 0

# Quick Ratio (Cash / STL)
qr = (cash_val / stl) if stl != 0 else 0

# 6. ИНТЕРФЕЙС
st.title(t["title"])
tab1, tab2, tab3 = st.tabs([t["tab1"], t["tab2"], t["tab3"]])

with tab1:
    st.markdown('<div class="section-header">🚀 Эффективность (на базе EBITDA)</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("ROI", f"{roi:.1f}%", delta=f"{sim_ebitda}%")
    c2.metric("ROE", f"{roe:.1f}%")
    c3.metric("ROA", f"{roa:.1f}%")

    st.markdown('<div class="section-header">🛡️ Устойчивость и Ликвидность</div>', unsafe_allow_html=True)
    c4, c5, c6 = st.columns(3)
    c4.metric("Solvency 2 (Net Assets)", f"{sol2_val:,.0f} $")
    c5.metric("Solvency 3 (%)", f"{sol3_pct:.1f}%")
    c6.metric("Quick Ratio (Cash/STL)", f"{qr:.2f}")

with tab2:
    st.markdown(f"#### {t['tab2']}")
    st.table(pd.DataFrame({
        "Parameter": ["Total Assets", "Total Liabilities", "Own Capital", "Net Assets (Sol2)", "Cash", "EBITDA"],
        "Value ($)": [f"{total_assets:,.0f}", f"{total_liabilities:,.0f}", f"{own_cap:,.0f}", f"{sol2_val:,.0f}",
                      f"{cash_val:,.0f}", f"{current_ebitda:,.0f}"]
    }))

with tab3:
    st.markdown(f'<div class="section-header">📚 {t["tab3"]}</div>', unsafe_allow_html=True)
    st.write(t["guide"]["roi"])
    st.write(t["guide"]["roe"])
    st.write(t["guide"]["roa"])
    st.write(t["guide"]["sol2"])
    st.write(t["guide"]["sol3"])
    st.write(t["guide"]["qr"])