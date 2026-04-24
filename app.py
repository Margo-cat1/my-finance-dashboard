import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# 1. Настройка страницы
st.set_page_config(page_title="Financial OS PRO", page_icon="📈", layout="wide")

# 2. Мультиязычный словарь (RU, EN, GE)
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
        "guide_text": "ROI — окупаемость затрат. Sol3 — золотой баланс."
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
        "guide_text": "ROI - Return on Investment. Sol3 - Golden Balance."
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
        "guide_text": "ROI — უკუგება ინვესტიციაზე. Sol3 — ოქროს ბალანსი."
    }
}

# 3. Улучшенный CSS (для поддержки разных шрифтов)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #00d4ff;
    }
    .stTabs [aria-selected="true"] { 
        background-color: #1e2130 !important; 
        color: white !important; 
    }
    .section-header {
        font-size: 24px; font-weight: 700; color: #1e2130;
        margin-bottom: 20px; padding-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. Выбор языка в Sidebar
with st.sidebar:
    lang_choice = st.selectbox("🌐 Choose Language", list(LANGS.keys()))
    t = LANGS[lang_choice]

    st.title(t["settings"])
    with st.expander(t["assets"], expanded=True):
        fa = st.number_input(t["fixed"], value=2100000)
        ca = st.number_input(t["current"], value=900000)
    with st.expander(t["liabilities"], expanded=True):
        ltl = st.number_input("Long-term", value=800000)
        stl = st.number_input("Short-term", value=400000)

    st.markdown("---")
    st.header(t["simulator"])
    sim_rev = st.slider(t["rev_change"], -50, 50, 0)
    sim_exp = st.slider(t["exp_change"], -50, 50, 0)

# --- ЛОГИКА РАСЧЕТОВ ---
input_rev, input_exp = 1500000, 1100000
rev = input_rev * (1 + sim_rev / 100)
exp = input_exp * (1 + sim_exp / 100)
profit = rev - exp
total_assets = fa + ca
total_liabilities = ltl + stl
equity = total_assets - total_liabilities

roi = (profit / exp * 100) if exp != 0 else 0
roe = (profit / equity * 100) if equity > 0 else 0
sol3 = (equity / total_liabilities) if total_liabilities != 0 else 0

# --- ГЛАВНЫЙ ИНТЕРФЕЙС ---
st.title(t["title"])
tab1, tab2, tab3 = st.tabs([t["tab_main"], t["tab_balance"], t["tab_info"]])

with tab1:
    st.markdown(f'<div class="section-header">🔥 {t["profit"]} & ROI</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric(t["profit"], f"{profit:,.0f} $", delta=f"{sim_rev}%")
    c2.metric("ROI", f"{roi:.1f}%")
    c3.metric("ROE", f"{roe:.1f}%")

    st.markdown("---")
    s1, s2 = st.columns(2)
    with s1:
        st.success(f"#### {t['strong']}")
        if sol3 >= 1.0: st.write(f"Golden Balance ✅ (Sol3: {sol3:.2f})")
    with s2:
        st.warning(f"#### {t['risks']}")
        if profit < 0: st.error("🚨 Scenario Loss / მოგება უარყოფითია")

with tab2:
    st.markdown(f'<div class="section-header">📊 {t["tab_balance"]}</div>', unsafe_allow_html=True)
    col_l, col_r = st.columns([1, 1.2])
    with col_l:
        df = pd.DataFrame({
            "Category": [t["fixed"], t["current"], t["equity"], t["debt"]],
            "Value ($)": [f"{fa:,.0f}", f"{ca:,.0f}", f"{equity:,.0f}", f"{total_liabilities:,.0f}"]
        })
        st.table(df)
    with col_r:
        fig = go.Figure(data=[go.Pie(labels=['Equity', 'Debt'], values=[max(0, equity), total_liabilities], hole=.4)])
        fig.update_layout(height=350, margin=dict(t=20, b=20, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown(f'<div class="section-header">📚 {t["tab_info"]}</div>', unsafe_allow_html=True)
    st.info(t["guide_text"])