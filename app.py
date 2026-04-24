import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# 1. Настройка страницы
st.set_page_config(page_title="Financial OS PRO", page_icon="📈", layout="wide")

# 2. Полный мультиязычный словарь
LANGS = {
    "Русский": {
        "title": "📊 Финансовый Интеллект",
        "settings": "⚙️ Настройки",
        "assets": "💼 Активы",
        "liabilities": "💸 Долги",
        "ops": "📈 Операционка",
        "simulator": "🔮 Симулятор рисков",
        "tab_main": "🎯 Главная",
        "tab_balance": "📊 Баланс",
        "tab_info": "📚 Справочник",
        "profit": "Чистая прибыль",
        "rev_change": "Изм. Выручки",
        "exp_change": "Изм. Расходов",
        "strong": "✅ Сильные стороны",
        "risks": "⚠️ Зоны внимания",
        "fixed": "Внеоборотные",
        "current": "Оборотные",
        "equity": "Капитал",
        "debt": "Всего долгов",
        "guide_roi": "**ROI:** Окупаемость затрат. Сколько прибыли приносит каждый вложенный $.",
        "guide_roe": "**ROE:** Доходность вашего личного капитала.",
        "guide_roa": "**ROA:** Насколько эффективно работают все активы компании.",
        "guide_sol2": "**Solvency 2:** Коэффициент автономии. Показывает долю активов, покрытых капиталом.",
        "guide_sol3": "**Solvency 3 (Golden Balance):** Если > 1.0, значит своих денег больше, чем долгов.",
        "guide_qr": "**Quick Ratio:** Ликвидность. Способность быстро погасить короткие долги."
    },
    "English": {
        "title": "📊 Financial Intelligence",
        "settings": "⚙️ Settings",
        "assets": "💼 Assets",
        "liabilities": "💸 Liabilities",
        "ops": "📈 Operations",
        "simulator": "🔮 Risk Simulator",
        "tab_main": "🎯 Main Panel",
        "tab_balance": "📊 Balance Sheet",
        "tab_info": "📚 Guide",
        "profit": "Net Profit",
        "rev_change": "Rev Change",
        "exp_change": "Exp Change",
        "strong": "✅ Strengths",
        "risks": "⚠️ Risks",
        "fixed": "Fixed Assets",
        "current": "Current Assets",
        "equity": "Equity",
        "debt": "Total Debt",
        "guide_roi": "**ROI:** Return on Investment. Profit per each $ invested.",
        "guide_roe": "**ROE:** Return on Equity. Efficiency of your personal capital.",
        "guide_roa": "**ROA:** Return on Assets. How well the company uses its property.",
        "guide_sol2": "**Solvency 2:** Autonomy ratio. Share of assets funded by equity.",
        "guide_sol3": "**Solvency 3 (Golden Balance):** If > 1.0, equity exceeds total debt.",
        "guide_qr": "**Quick Ratio:** Ability to pay short-term debts instantly."
    },
    "ქართული": {
        "title": "📊 ფინანსური ინტელექტი",
        "settings": "⚙️ პარამეტრები",
        "assets": "💼 აქტივები",
        "liabilities": "💸 ვალდებულებები",
        "ops": "📈 ოპერაციები",
        "simulator": "🔮 რისკების სიმულატორი",
        "tab_main": "🎯 მთავარი",
        "tab_balance": "📊 ბალანსი",
        "tab_info": "📚 ცნობარი",
        "profit": "წმინდა მოგება",
        "rev_change": "შემოსავლის ცვლ.",
        "exp_change": "ხარჯების ცვლ.",
        "strong": "✅ ძლიერი მხარეები",
        "risks": "⚠️ ყურადსაღები ზონები",
        "fixed": "გრძელვადიანი",
        "current": "მიმდინარე",
        "equity": "კაპიტალი",
        "debt": "ჯამური ვალი",
        "guide_roi": "**ROI:** ინვესტიციის უკუგება. მოგება ყოველ დახარჯულ $-ზე.",
        "guide_roe": "**ROE:** საკუთარი კაპიტალის უკუგება.",
        "guide_roa": "**ROA:** აქტივების გამოყენების ეფექტურობა.",
        "guide_sol2": "**Solvency 2:** ავტონომიის კოეფიციენტი.",
        "guide_sol3": "**Solvency 3 (ოქროს ბალანსი):** თუ > 1.0, საკუთარი ფული ვალზე მეტია.",
        "guide_qr": "**Quick Ratio:** ლიკვიდურობა. მოკლევადიანი ვალების დაფარვის უნარი."
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

    st.title(t["settings"])
    with st.expander(t["assets"], expanded=True):
        fa = st.number_input(t["fixed"], value=2100000)
        ca = st.number_input(t["current"], value=900000)
    with st.expander(t["liabilities"], expanded=True):
        ltl = st.number_input("Long-term", value=800000)
        stl = st.number_input("Short-term", value=400000)
    with st.expander(t["ops"], expanded=True):
        input_rev = st.number_input("Revenue Base", value=1500000)
        input_exp = st.number_input("Expense Base", value=1100000)

    st.markdown("---")
    st.header(t["simulator"])
    sim_rev = st.slider(t["rev_change"], -50, 50, 0)
    sim_exp = st.slider(t["exp_change"], -50, 50, 0)

# --- РАСЧЕТЫ ---
rev = input_rev * (1 + sim_rev / 100)
exp = input_exp * (1 + sim_exp / 100)
profit = rev - exp
total_assets = fa + ca
total_liabilities = ltl + stl
equity = total_assets - total_liabilities

roi = (profit / exp * 100) if exp != 0 else 0
roe = (profit / equity * 100) if equity > 0 else 0
roa = (profit / total_assets * 100) if total_assets > 0 else 0
sol2 = (total_assets / total_liabilities) if total_liabilities != 0 else 0
sol3 = (equity / total_liabilities) if total_liabilities != 0 else 0
qr = (ca / stl) if stl != 0 else 0

# --- ИНТЕРФЕЙС ---
st.title(t["title"])
tab1, tab2, tab3 = st.tabs([t["tab_main"], t["tab_balance"], t["tab_info"]])

with tab1:
    st.markdown(f'<div class="section-header">🔥 Profitability</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric(t["profit"], f"{profit:,.0f} $", delta=f"{sim_rev}%")
    c2.metric("ROI", f"{roi:.1f}%")
    c3.metric("ROE", f"{roe:.1f}%")

    st.markdown(f'<div class="section-header">🛡️ Solvency & Liquidity</div>', unsafe_allow_html=True)
    c4, c5, c6 = st.columns(3)
    c4.metric("Solvency 2", f"{sol2:.2f}")
    c5.metric("Solvency 3", f"{sol3:.2f}")
    c6.metric("Quick Ratio", f"{qr:.2f}")

    st.markdown("---")
    s1, s2 = st.columns(2)
    with s1:
        st.success(f"#### {t['strong']}")
        if sol3 >= 1.0: st