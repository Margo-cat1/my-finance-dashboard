import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# 1. Настройка страницы
st.set_page_config(page_title="Financial Intelligence Dashboard", page_icon="📈", layout="wide")

# 2. Полный мультиязычный словарь с исправленными пояснениями
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
        "ebitda": "EBITDA",
        "tab1": "🎯 Дашборд", "tab2": "📊 Структура", "tab3": "📚 Справочник",
        "strong": "✅ Сильные стороны",
        "risks": "⚠️ Зоны внимания",
        "analysis_header": "🔍 Автоматический анализ",
        "guide": {
            "roi": "**ROI (Return on Investment):** EBITDA / Первоначальные инвестиции * 100%. Показывает общую доходность проекта на вложенный капитал.",
            "roe": "**ROE (Return on Equity):** EBITDA / Собственный капитал * 100%. Показывает эффективность использования именно ваших средств.",
            "roa": "**ROA (Return on Assets):** EBITDA / Общие активы (Total Assets) * 100%. Отражает отдачу от каждого доллара, вложенного в имущество компании.",
            "sol2": "**Solvency 2 (Чистые активы):** Общие активы минус Общие долги (LTL + STL). Это реальная стоимость вашего участия в бизнесе в денежном эквиваленте.",
            "sol3": "**Solvency 3 (%):** (Чистые активы / Общие активы) * 100%. Коэффициент автономии, показывающий долю собственности в общем балансе.",
            "qr": "**Quick Ratio (Мгновенная ликвидность):** Наличные (Cash) / Краткосрочные долги (STL). Сможете ли вы заплатить по счетам прямо сейчас."
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
        "cash": "Cash", "ebitda": "EBITDA",
        "tab1": "🎯 Dashboard", "tab2": "📊 Structure", "tab3": "📚 Guide",
        "strong": "✅ Strengths",
        "risks": "⚠️ Risks",
        "analysis_header": "🔍 Automated Analysis",
        "guide": {
            "roi": "**ROI:** EBITDA / Initial Investment * 100%. Measures total project profitability.",
            "roe": "**ROE:** EBITDA / Own Capital * 100%. Efficiency of personal equity.",
            "roa": "**ROA:** EBITDA / Total Assets * 100%. Efficiency of total asset usage.",
            "sol2": "**Solvency 2 (Net Assets):** Total Assets - Total Liabilities. The real value of your business stake.",
            "sol3": "**Solvency 3 (%):** (Net Assets / Total Assets) * 100%. Self-sufficiency ratio.",
            "qr": "**Quick Ratio:** Cash / Short-term Liabilities. Immediate payment ability."
        }
    },
    "ქართული": {
        "title": "📊 ფინანსური ინტელექტი",
        "settings": "⚙️ მონაცემები",
        "assets": "💼 აქტივები", "liabilities": "💸 ვალდებულებები",
        "ops": "📈 ოპერაციები",
        "own_cap": "საკუთარი კაპიტალი", "init_inv": "საწყისი ინვესტიცია",
        "cash": "Cash", "ebitda": "EBITDA",
        "tab1": "🎯 მთავარი", "tab2": "📊 ბალანსი", "tab3": "📚 ცნობარი",
        "strong": "✅ ძლიერი მხარეები",
        "risks": "⚠️ რისკები",
        "analysis_header": "🔍 ავტომატური ანალიზი",
        "guide": {
            "roi": "**ROI:** EBITDA / საწყისი ინვესტიცია * 100%.",
            "roe": "**ROE:** EBITDA / საკუთარი კაპიტალი * 100%.",
            "roa": "**ROA:** EBITDA / ჯამური აქტივები * 100%.",
            "sol2": "**Solvency 2 (წმინდა აქტივები):** ჯამური აქტივები - ჯამური ვალდებულებები.",
            "sol3": "**Solvency 3 (%):** (წმინდა აქტივები / ჯამური აქტივები) * 100%.",
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

    sim_ebitda = st.slider("EBITDA Change %", -50, 50, 0)

# 5. ЛОГИКА РАСЧЕТОВ
total_assets = fa + ca
total_liabilities = ltl + stl
current_ebitda = ebitda_val * (1 + sim_ebitda / 100)

roi = (current_ebitda / init_inv * 100) if init_inv != 0 else 0
roe = (current_ebitda / own_cap * 100) if own_cap != 0 else 0
roa = (current_ebitda / total_assets * 100) if total_assets != 0 else 0
sol2_val = total_assets - total_liabilities
sol3_pct = (sol2_val / total_assets * 100) if total_assets != 0 else 0
qr = (cash_val / stl) if stl != 0 else 0

# 6. ГЛАВНЫЙ ИНТЕРФЕЙС
st.title(t["title"])
tab1, tab2, tab3 = st.tabs([t["tab1"], t["tab2"], t["tab3"]])

with tab1:
    st.markdown('<div class="section-header">🚀 Эффективность (EBITDA)</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("ROI", f"{roi:.1f}%", delta=f"{sim_ebitda}%")
    c2.metric("ROE", f"{roe:.1f}%")
    c3.metric("ROA", f"{roa:.1f}%")

    st.markdown('<div class="section-header">🛡️ Устойчивость и Ликвидность</div>', unsafe_allow_html=True)
    c4, c5, c6 = st.columns(3)
    c4.metric("Solvency 2 (Net Assets)", f"{sol2_val:,.0f} $")
    c5.metric("Solvency 3 (%)", f"{sol3_pct:.1f}%")
    c6.metric("Quick Ratio (Cash/STL)", f"{qr:.2f}")

    # Блок Анализа
    st.markdown(f'<div class="section-header">{t["analysis_header"]}</div>', unsafe_allow_html=True)
    col_s, col_r = st.columns(2)
    with col_s:
        st.success(f"### {t['strong']}")
        if sol3_pct > 50: st.write("🌟 **Высокая независимость:** Более половины активов принадлежат вам.")
        if roi > 25: st.write(f"📈 **ROI ({roi:.1f}%):** Проект очень быстро окупает инвестиции.")
        if qr >= 0.5: st.write("💧 **Ликвидность:** Достаточно наличных для покрытия срочных долгов.")

    with col_r:
        st.warning(f"### {t['risks']}")
        if sol3_pct < 30: st.write("🚩 **Низкая автономия:** Бизнес сильно зависит от заемных средств.")
        if qr < 0.2: st.write("💸 **Дефицит Cash:** Наличных критически мало для текущих обязательств.")
        if sol2_val < 0: st.error("❌ **Отрицательный капитал:** Долги превышают активы!")

with tab2:
    st.markdown(f"#### {t['tab2']}")
    st.table(pd.DataFrame({
        "Parameter": ["Total Assets", "Total Liabilities", "Own Capital", "Net Assets (Sol2)", "Cash", "EBITDA"],
        "Value ($)": [f"{total_assets:,.0f}", f"{total_liabilities:,.0f}", f"{own_cap:,.0f}", f"{sol2_val:,.0f}",
                      f"{cash_val:,.0f}", f"{current_ebitda:,.0f}"]
    }))

with tab3:
    st.markdown(f'<div class="section-header">📚 {t["tab3"]}</div>', unsafe_allow_html=True)
    # Выводим исправленные пояснения из словаря
    for key in t["guide"]:
        st.info(t["guide"][key])