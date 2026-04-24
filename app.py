import streamlit as st
import pd as pd
import pandas as pd

# 1. Настройка страницы
st.set_page_config(page_title="Financial Intelligence PRO", page_icon="📈", layout="wide")

# 2. Словарь переводов (Обновлен блок Guide с нормативами)
LANGS = {
    "Русский": {
        "title": "📊 Финансовый Интеллект",
        "settings": "⚙️ Ввод данных",
        "assets": "💼 Активы", "liabilities": "💸 Долги", "ops": "📈 Операционка",
        "fa": "Fixed Assets", "ca": "Current Assets",
        "ltl": "Long-term Debt", "stl": "Short-term Debt",
        "own_cap": "Собственный капитал", "init_inv": "Первоначальные инвестиции",
        "cash": "Наличные (Cash)", "ebitda": "EBITDA",
        "tab1": "🎯 Дашборд", "tab2": "📊 Структура", "tab3": "📚 Справочник",
        "sec_eff": "🚀 Эффективность (EBITDA)",
        "sec_sol": "🛡️ Устойчивость и Ликвидность",
        "analysis_header": "🔍 Автоматический анализ",
        "strong": "✅ Сильные стороны", "risks": "⚠️ Зоны внимания",
        "msg_autonomy": "🌟 **Автономия:** Большая часть активов — ваши.",
        "msg_roi": "📈 **Окупаемость:** Высокий уровень ROI",
        "msg_liq": "💧 **Ликвидность:** Хороший запас наличности.",
        "msg_dep": "🚩 **Зависимость:** Высокая доля долгов.",
        "msg_cash_low": "💸 **Дефицит Cash:** Мало денег для платежей.",
        "msg_bankrupt": "❌ **Критический риск:** Долги больше активов!",
        "guide": {
            "roi": "**ROI (Return on Investment):** EBITDA / Инвестиции. Норма: >20%. Показывает, как быстро окупаются вложения.",
            "roe": "**ROE (Return on Equity):** EBITDA / Собственный капитал. Норма: >15-20%. Эффективность ваших личных денег.",
            "roa": "**ROA (Return on Assets):** EBITDA / Общие активы. Норма: >5-10%. Насколько эффективно работает всё имущество.",
            "sol2": "**Solvency 2 (Чистые активы):** Активы - Долги. Должно быть > 0. Если значение отрицательное — бизнес в зоне банкротства.",
            "sol3": "**Solvency 3 (Автономия):** Чистые активы / Общие активы. Норма: >50%. Показывает вашу независимость от кредиторов.",
            "qr": "**Quick Ratio:** Cash / Краткосрочные долги. Норма: >0.5 - 1.0. Способность погасить долги немедленно."
        }
    },
    "English": {
        "title": "📊 Financial Intelligence",
        "settings": "⚙️ Data Input",
        "assets": "💼 Assets", "liabilities": "💸 Liabilities", "ops": "📈 Operations",
        "fa": "Fixed Assets", "ca": "Current Assets",
        "ltl": "Long-term Debt", "stl": "Short-term Debt",
        "own_cap": "Own Capital", "init_inv": "Initial Investment",
        "cash": "Cash", "ebitda": "EBITDA",
        "tab1": "🎯 Dashboard", "tab2": "📊 Structure", "tab3": "📚 Guide",
        "sec_eff": "🚀 Efficiency (EBITDA)",
        "sec_sol": "🛡️ Solvency & Liquidity",
        "analysis_header": "🔍 Automated Analysis",
        "strong": "✅ Strengths", "risks": "⚠️ Risks",
        "msg_autonomy": "🌟 **Autonomy:** Most assets belong to you.",
        "msg_roi": "📈 **Profitability:** High ROI level",
        "msg_liq": "💧 **Liquidity:** Good cash reserve.",
        "msg_dep": "🚩 **Dependency:** High debt ratio.",
        "msg_cash_low": "💸 **Cash Deficit:** Low cash for quick payments.",
        "msg_bankrupt": "❌ **Critical Risk:** Liabilities exceed assets!",
        "guide": {
            "roi": "**ROI:** EBITDA / Investments. Target: >20%. Shows how fast the project pays back.",
            "roe": "**ROE:** EBITDA / Own Capital. Target: >15-20%. Efficiency of your own funds.",
            "roa": "**ROA:** EBITDA / Total Assets. Target: >5-10%. How well all company assets perform.",
            "sol2": "**Solvency 2 (Net Assets):** Assets - Liabilities. Must be > 0. Negative means technical bankruptcy.",
            "sol3": "**Solvency 3 (Autonomy):** Net Assets / Total Assets. Target: >50%. Shows independence from creditors.",
            "qr": "**Quick Ratio:** Cash / Short-term Debt. Target: >0.5 - 1.0. Ability to pay bills instantly."
        }
    },
    "ქართული": {
        "title": "📊 ფინანსური ინტელექტი",
        "settings": "⚙️ მონაცემები",
        "assets": "💼 აქტივები", "liabilities": "💸 ვალდებულებები", "ops": "📈 ოპერაციები",
        "fa": "ძირითადი აქტივები", "ca": "მიმდინარე აქტივები",
        "ltl": "გრძელვადიანი ვალი", "stl": "მოკლევადიანი ვალი",
        "own_cap": "საკუთარი კაპიტალი", "init_inv": "საწყისი ინვესტიცია",
        "cash": "Cash", "ebitda": "EBITDA",
        "tab1": "🎯 მთავარი", "tab2": "📊 ბალანსი", "tab3": "📚 ცნობარი",
        "sec_eff": "🚀 ეფექტურობა (EBITDA)",
        "sec_sol": "🛡️ მდგრადობა და ლიკვიდურობა",
        "analysis_header": "🔍 ავტომატური ანალიზი",
        "strong": "✅ ძლიერი მხარეები", "risks": "⚠️ რისკები",
        "msg_autonomy": "🌟 **ავტონომია:** აქტივების უმეტესი ნაწილი თქვენია.",
        "msg_roi": "📈 **უკუგება:** ROI-ს მაღალი დონე",
        "msg_liq": "💧 **ლიკვიდურობა:** ნაღდი ფულის კარგი მარაგი.",
        "msg_dep": "🚩 **დამოკიდებულება:** ვალების მაღალი წილი.",
        "msg_cash_low": "💸 **Cash-ის დეფიციტი:** ცოტა ფული გადახდებისთვის.",
        "msg_bankrupt": "❌ **კრიტიკული რისკი:** ვალები აღემატება აქტივებს!",
        "guide": {
            "roi": "**ROI:** EBITDA / ინვესტიცია. ნორმა: >20%.",
            "roe": "**ROE:** EBITDA / საკუთარი კაპიტალი. ნორმა: >15-20%.",
            "roa": "**ROA:** EBITDA / ჯამური აქტივები. ნორმა: >5-10%.",
            "sol2": "**Solvency 2:** აქტივები - ვალდებულებები. უნდა იყოს > 0.",
            "sol3": "**Solvency 3:** წმინდა აქტივები / ჯამური აქტივები. ნორმა: >50%.",
            "qr": "**Quick Ratio:** Cash / მოკლევადიანი ვალი. ნორმა: >0.5 - 1.0."
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

# 5. РАСЧЕТЫ (Твоя логика EBITDA / Total Assets * 100)
total_assets = fa + ca
total_liabilities = ltl + stl
current_ebitda = ebitda_val * (1 + sim_ebitda / 100)
roi = (current_ebitda / init_inv * 100) if init_inv != 0 else 0
roe = (current_ebitda / own_cap * 100) if own_cap != 0 else 0
roa = (current_ebitda / total_assets * 100) if total_assets != 0 else 0
sol2_val = total_assets - total_liabilities
sol3_pct = (sol2_val / total_assets * 100) if total_assets != 0 else 0
qr = (cash_val / stl) if stl != 0 else 0

# 6. ИНТЕРФЕЙС
st.title(t["title"])
tab1, tab2, tab3 = st.tabs([t["tab1"], t["tab2"], t["tab3"]])

with tab1:
    st.markdown(f'<div class="section-header">{t["sec_eff"]}</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("ROI", f"{roi:.1f}%", delta=f"{sim_ebitda}%")
    c2.metric("ROE", f"{roe:.1f}%")
    c3.metric("ROA", f"{roa:.1f}%")

    st.markdown(f'<div class="section-header">{t["sec_sol"]}</div>', unsafe_allow_html=True)
    c4, c5, c6 = st.columns(3)
    c4.metric("Solvency 2 (Net Assets)", f"{sol2_val:,.0f} $")
    c5.metric("Solvency 3 (%)", f"{sol3_pct:.1f}%")
    c6.metric("Quick Ratio (Cash/STL)", f"{qr:.2f}")

    # Блок Анализа
    st.markdown(f'<div class="section-header">{t["analysis_header"]}</div>', unsafe_allow_html=True)
    col_s, col_r = st.columns(2)
    with col_s:
        st.success(f"### {t['strong']}")
        if sol3_pct > 50: st.write(t["msg_autonomy"])
        if roi > 20: st.write(f"{t['msg_roi']} ({roi:.1f}%)")
        if qr >= 0.5: st.write(t["msg_liq"])
    with col_r:
        st.warning(f"### {t['risks']}")
        if sol3_pct < 30: st.write(t["msg_dep"])
        if qr < 0.2: st.write(t["msg_cash_low"])
        if sol2_val < 0: st.error(t["msg_bankrupt"])

with tab2:
    st.markdown(f"#### {t['tab2']}")
    st.table(pd.DataFrame({
        "Parameter": ["Total Assets", "Total Liabilities", "Own Capital", "Net Assets (Sol2)", "Cash", "EBITDA"],
        "Value ($)": [f"{total_assets:,.0f}", f"{total_liabilities:,.0f}", f"{own_cap:,.0f}", f"{sol2_val:,.0f}",
                      f"{cash_val:,.0f}", f"{current_ebitda:,.0f}"]
    }))

with tab3:
    st.markdown(f'<div class="section-header">📚 {t["tab3"]}</div>', unsafe_allow_html=True)
    for key in t["guide"]:
        st.info(t["guide"][key])