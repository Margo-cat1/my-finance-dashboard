import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
import plotly.express as px
import yaml
import io
import time
from yaml.loader import SafeLoader
from database import init_db, save_record, get_latest_record, get_all_records

# --- 1. CONFIGURATION & DICTIONARIES ---
st.set_page_config(page_title="FinMarge PRO", page_icon="📈", layout="wide")

UI_TEXTS = {
    "RU": {
        "name": "Русский", "title": "📈 Финансовый Интеллект",
        "tab_input": "📥 Ввод", "tab_analysis": "📊 Анализ", "tab_history": "📜 История", "tab_guide": "📚 Справочник",
        "sec_eff": "🚀 Эффективность", "sec_sol": "🛡️ Устойчивость и Ликвидность",
        "save": "🚀 Обновить показатели", "download": "📥 Скачать Excel",
        "card_cap": "Собственный капитал", "card_cash": "Наличные", "card_net": "Чистые активы",
        "assets": "💼 Активы", "liabilities": "💸 Долги", "ops": "📈 Операционка",
        "fa": "Внеоборотные", "ca": "Оборотные", "ltl": "Долгоср. долги", "stl": "Краткоср. долги",
        "own_cap": "Капитал", "init_inv": "Инвест.", "cash": "Наличные", "ebitda": "EBITDA",
        "chart_pie": "🍩 Состав активов", "chart_line": "📈 Тренд капитала",
        "strong": "✅ Сильные стороны", "risks": "⚠️ Зоны внимания",
        "msg_autonomy": "Автономия: активы ваши.", "msg_roi": "Окупаемость: высокий ROI.",
        "msg_liq": "Ликвидность: запас в норме.", "msg_dep": "Зависимость от долгов.",
        "msg_cash_low": "Дефицит наличности.", "msg_bankrupt": "Критический риск!",
        "guide": {
            "roi": "**ROI:** EBITDA / Инвестиции. Цель: > 25%.",
            "solvency": "**Solvency:** Чистые активы / Общие активы. Минимум: 50%."
        }
    },
    "EN": {
        "name": "English", "title": "📈 Financial Intelligence",
        "tab_input": "📥 Input", "tab_analysis": "📊 Analysis", "tab_history": "📜 History", "tab_guide": "📚 Guide",
        "sec_eff": "🚀 Efficiency", "sec_sol": "🛡️ Solvency & Liquidity",
        "save": "🚀 Update Stats", "download": "📥 Download Excel",
        "card_cap": "Equity", "card_cash": "Cash", "card_net": "Net Assets",
        "assets": "💼 Assets", "liabilities": "💸 Liabilities", "ops": "📈 Operations",
        "fa": "Fixed Assets", "ca": "Current Assets", "ltl": "L-term Debt", "stl": "S-term Debt",
        "own_cap": "Equity", "init_inv": "Initial Inv.", "cash": "Cash", "ebitda": "EBITDA",
        "chart_pie": "🍩 Asset Structure", "chart_line": "📈 Equity Trend",
        "strong": "✅ Strengths", "risks": "⚠️ Areas of Focus",
        "msg_autonomy": "Autonomy: most assets are yours.", "msg_roi": "Profitability: high ROI level.",
        "msg_liq": "Liquidity: cash reserves are good.", "msg_dep": "Dependence: high debt ratio.",
        "msg_cash_low": "Cash deficit: risky liquidity.", "msg_bankrupt": "Critical risk: debt > assets!",
        "guide": {
            "roi": "**ROI:** EBITDA / Investments. Target: > 25%.",
            "solvency": "**Solvency:** Net Assets / Total Assets. Min: 50%."
        }
    },
    "GE": {
        "name": "ქართული", "title": "📈 ფინანსური ინტელექტი",
        "tab_input": "📥 შეტანა", "tab_analysis": "📊 ანალიზი", "tab_history": "📜 ისტორია", "tab_guide": "📚 ცნობარი",
        "sec_eff": "🚀 ეფექტურობა", "sec_sol": "🛡️ მდგრადობა და ლიკვიდურობა",
        "save": "🚀 განახლება", "download": "📥 ჩამოტვირთვა Excel",
        "card_cap": "საკუთარი კაპიტალი", "card_cash": "ნაღდი ფული", "card_net": "წმინდა აქტივები",
        "assets": "💼 აქტივები", "liabilities": "💸 ვალდებულებები", "ops": "⚙️ ოპერაციები",
        "fa": "ძირითადი აქტივები", "ca": "მიმდინარე აქტივები", "ltl": "გრძელვადიანი ვალი", "stl": "მოკლევადიანი ვალი",
        "own_cap": "კაპიტალი", "init_inv": "საწყისი ინვესტიცია", "cash": "Cash", "ebitda": "EBITDA",
        "chart_pie": "🍩 აქტივების შემადგენლობა", "chart_line": "📈 კაპიტალის ტრენდი",
        "strong": "✅ ძლიერი მხარეები", "risks": "⚠️ რისკები",
        "msg_autonomy": "ავტონომია: აქტივები თქვენია.", "msg_roi": "უკუგება: მაღალი ROI.",
        "msg_liq": "ლიკვიდობა: მარაგი ნორმაშია.", "msg_dep": "დამოკიდებულება ვალებზე.",
        "msg_cash_low": "ნაღდი ფულის დეფიციტი.", "msg_bankrupt": "კრიტიკული რისკი!",
        "guide": {
            "roi": "**ROI:** EBITDA / ინვესტიცია. მიზანი: > 25%.",
            "solvency": "**Solvency:** წმინდა აქტივები / ჯამური აქტივები. მინიმუმი: 50%."
        }
    }
}


# --- 2. HELPERS & LOGIC ---
def apply_custom_styles():
    st.markdown("""
        <style>
        [data-testid="stMetric"] { background: rgba(255, 255, 255, 0.8); border-radius: 12px; padding: 15px; border: 1px solid #eee; }
        .section-header { font-size: 1.4rem; font-weight: bold; margin: 20px 0 10px 0; color: #1f77b4; }
        </style>
    """, unsafe_allow_html=True)


def calculate_metrics(fa, ca, ltl, stl, own_cap, init_inv, cash, ebitda):
    total_assets = fa + ca
    total_liabilities = ltl + stl
    net_assets = total_assets - total_liabilities

    metrics = {
        "roi": (ebitda / init_inv * 100) if init_inv > 0 else 0,
        "roe": (ebitda / own_cap * 100) if own_cap > 0 else 0,
        "roa": (ebitda / total_assets * 100) if total_assets > 0 else 0,
        "solvency_ratio": (net_assets / total_assets * 100) if total_assets > 0 else 0,
        "quick_ratio": (cash / stl) if stl > 0 else 0,
        "net_assets": net_assets
    }
    return metrics


# --- 3. AUTHENTICATION ---
init_db()
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'], config['cookie']['name'], config['cookie']['key'], config['cookie']['expiry_days']
)

if not st.session_state.get("authentication_status"):
    t_login, t_reg = st.tabs(["🔑 Вход", "👤 Регистрация"])
    with t_login:
        authenticator.login()
    with t_reg:
        if authenticator.register_user():
            with open('config.yaml', 'w') as f: yaml.dump(config, f)
            st.success('Регистрация успешна! Войдите.')

# --- 4. MAIN APPLICATION ---
if st.session_state.get("authentication_status"):
    apply_custom_styles()
    user = st.session_state["username"]

    # Header with Selectors
    head_left, head_mid, head_right = st.columns([3, 1, 1])
    with head_mid:
        lang = st.selectbox("", options=list(UI_TEXTS.keys()), index=1, format_func=lambda x: UI_TEXTS[x]['name'])
        t = UI_TEXTS[lang]
    with head_right:
        curr_map = {"GEL": "₾", "USD": "$", "EUR": "€"}
        curr_symbol = curr_map[st.selectbox("", options=list(curr_map.keys()))]
    with head_left:
        st.subheader(t["title"])

    # Load Data
    last_rec = get_latest_record(user)
    defaults = last_rec if last_rec else {
        'fixed_assets': 2000000, 'receivables': 500000, 'cash': 300000,
        'long_term_debt': 800000, 'short_term_debt': 200000, 'ebitda': 400000,
        'own_capital': 1000000, 'initial_inv': 1500000
    }

    # Sidebar UI
    with st.sidebar:
        st.write(f"👤 {user}")
        with st.expander(t["assets"], expanded=True):
            fa = st.number_input(t["fa"], value=int(defaults['fixed_assets']))
            ca = st.number_input(t["ca"], value=int(defaults['receivables']))
        with st.expander(t["liabilities"], expanded=True):
            ltl = st.number_input(t["ltl"], value=int(defaults['long_term_debt']))
            stl = st.number_input(t["stl"], value=int(defaults['short_term_debt']))
        with st.expander(t["ops"], expanded=True):
            own_cap = st.number_input(t["own_cap"], value=int(defaults.get('own_capital', 1000000)))
            init_inv = st.number_input(t["init_inv"], value=int(defaults.get('initial_inv', 1500000)))
            cash_val = st.number_input(t["cash"], value=int(defaults['cash']))
            ebitda_val = st.number_input(t["ebitda"], value=int(defaults['ebitda']))

        if st.button(t["save"], use_container_width=True):
            save_record(user, {
                'fixed_assets': fa, 'receivables': ca, 'cash': cash_val,
                'long_term_debt': ltl, 'short_term_debt': stl, 'ebitda': ebitda_val,
                'own_capital': own_cap, 'initial_inv': init_inv, 'inventory': 0, 'revenue': 0
            })
            st.toast("Данные сохранены!", icon="✅")
            time.sleep(1)
            st.rerun()

        authenticator.logout('Logout', 'sidebar')

    # Calculations
    m = calculate_metrics(fa, ca, ltl, stl, own_cap, init_inv, cash_val, ebitda_val)

    # Main Tabs
    tab1, tab2, tab3, tab4 = st.tabs([t["tab_input"], t["tab_analysis"], t["tab_history"], t["tab_guide"]])

    with tab1:
        st.markdown(f'<div class="section-header">{t["sec_eff"]}</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("ROI", f"{m['roi']:.1f}%")
        c2.metric("ROE", f"{m['roe']:.1f}%")
        c3.metric("ROA", f"{m['roa']:.1f}%")

        st.markdown(f'<div class="section-header">{t["sec_sol"]}</div>', unsafe_allow_html=True)
        c4, c5, c6 = st.columns(3)
        c4.metric(t["card_net"], f"{m['net_assets']:,.0f} {curr_symbol}")
        c5.metric("Solvency Ratio", f"{m['solvency_ratio']:.1f}%")
        c6.metric("Quick Ratio", f"{m['quick_ratio']:.2f}")

    with tab2:
        col_s, col_r = st.columns(2)
        with col_s:
            st.success(f"### {t['strong']}")
            if m['solvency_ratio'] >= 50: st.info(t['msg_autonomy'])
            if m['roi'] >= 25: st.info(t['msg_roi'])
        with col_r:
            st.warning(f"### {t['risks']}")
            if m['quick_ratio'] < 1.0: st.error(t['msg_cash_low'])
            if m['net_assets'] < 0: st.error(t['msg_bankrupt'])

    with tab3:
        history_df = get_all_records(user)
        if not history_df.empty:
            chart1, chart2 = st.columns(2)
            with chart1:
                st.write(f"**{t['chart_pie']}**")
                fig_pie = px.pie(values=[cash_val, ca, fa], names=[t['cash'], t['ca'], t['fa']], hole=0.4)
                st.plotly_chart(fig_pie, use_container_width=True)
            with chart2:
                st.write(f"**{t['chart_line']}**")
                fig_line = px.line(history_df, x='date', y='own_capital', markers=True)
                st.plotly_chart(fig_line, use_container_width=True)

            st.dataframe(history_df, use_container_width=True)

            # EXCEL EXPORT (Безопасный метод)
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                history_df.to_excel(writer, index=False)
            st.download_button(label=t["download"], data=buffer.getvalue(), file_name="report.xlsx")

    with tab4:
        for k, v in t["guide"].items(): st.info(v)