import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
import plotly.express as px
import yaml
import io
import time
from yaml.loader import SafeLoader
from database import init_db, save_record, get_latest_record, get_all_records

# --- 1. CONFIGURATION & FULL DICTIONARY ---
st.set_page_config(page_title="FinMarge PRO", page_icon="📈", layout="wide")

UI_TEXTS = {
    "RU": {
        "name": "Русский", "title": "📈 Финансовый Интеллект",
        "tab1": "📥 Ввод", "tab2": "📊 Анализ", "tab3": "📜 История", "tab4": "📚 Справочник",
        "save": "🚀 Обновить показатели", "download": "📥 Скачать Excel",
        "sec_eff": "🚀 Эффективность", "sec_sol": "🛡️ Устойчивость и Ликвидность",
        "card_cap": "Собственный капитал", "card_cash": "Наличные", "card_net": "Чистые активы",
        "assets": "🏠 Активы", "liabilities": "📉 Долги", "ops": "⚙️ Операционка",
        "fa": "Внеоборотные", "ca": "Оборотные", "ltl": "Долгоср. долги", "stl": "Краткоср. долги",
        "own_cap": "Капитал", "init_inv": "Инвест.", "cash": "Наличные", "ebitda": "EBITDA",
        "analysis_header": "🔍 Автоматический анализ", "strong": "✅ Сильные стороны", "risks": "⚠️ Зоны внимания",
        "msg_autonomy": "🌟 **Автономия:** Большая часть активов — ваши.",
        "msg_roi": "📈 **Окупаемость:** Высокий уровень ROI.",
        "msg_liq": "💧 **Ликвидность:** Хороший запас наличности.",
        "msg_dep": "🚩 **Зависимость:** Высокая доля долгов.",
        "msg_cash_low": "💸 **Дефицит Cash:** Мало денег для платежей.",
        "msg_bankrupt": "❌ **Критический риск:** Долги больше активов!",
        "chart_pie": "🍩 Состав активов", "chart_line": "📈 Тренд капитала",
        "guide": {
            "roi": "**ROI:** EBITDA / Инвестиции. Цель: > 25%.",
            "roe": "**ROE:** EBITDA / Собственный капитал. Цель: > 20%.",
            "roa": "**ROA:** EBITDA / Общие активы. Цель: > 10%.",
            "sol2": "**Solvency 2:** Активы - Долги. Минимум: > 0.",
            "sol3": "**Solvency 3:** Чистые активы / Общие активы. Минимум: 50%.",
            "qr": "**Quick Ratio:** Cash / Краткосрочные долги. Минимум: 2.0."
        }
    },
    "EN": {
        "name": "English", "title": "📈 Financial Intelligence",
        "tab1": "📥 Input", "tab2": "📊 Analysis", "tab3": "📜 History", "tab4": "📚 Guide",
        "save": "🚀 Update Stats", "download": "📥 Download Excel",
        "sec_eff": "🚀 Efficiency", "sec_sol": "🛡️ Solvency & Liquidity",
        "card_cap": "Equity", "card_cash": "Cash", "card_net": "Net Assets",
        "assets": "💼 Assets", "liabilities": "💸 Liabilities", "ops": "📈 Operations",
        "fa": "Fixed Assets", "ca": "Current Assets", "ltl": "L-term Debt", "stl": "S-term Debt",
        "own_cap": "Equity", "init_inv": "Initial Inv.", "cash": "Cash", "ebitda": "EBITDA",
        "analysis_header": "🔍 Automated Analysis", "strong": "✅ Strengths", "risks": "⚠️ Risks",
        "msg_autonomy": "🌟 **Autonomy:** Most assets are yours.",
        "msg_roi": "📈 **Profitability:** High ROI level.",
        "msg_liq": "💧 **Liquidity:** Solid cash reserves.",
        "msg_dep": "🚩 **Dependency:** High debt ratio.",
        "msg_cash_low": "💸 **Cash Deficit:** Low liquidity for payments.",
        "msg_bankrupt": "❌ **Critical Risk:** Liabilities exceed assets!",
        "chart_pie": "🍩 Asset Structure", "chart_line": "📈 Equity Trend",
        "guide": {
            "roi": "**ROI:** EBITDA / Investments. Target: > 25%.",
            "roe": "**ROE:** EBITDA / Equity. Target: > 20%.",
            "roa": "**ROA:** EBITDA / Total Assets. Target: > 10%.",
            "sol2": "**Solvency 2:** Assets - Debts. Min: > 0.",
            "sol3": "**Solvency 3:** Net Assets / Total Assets. Min: 50%.",
            "qr": "**Quick Ratio:** Cash / Short-term Debt. Target: 2.0."
        }
    },
    "GE": {
        "name": "ქართული", "title": "📈 ფინანსური ინტელექტი",
        "tab1": "📥 შეტანა", "tab2": "📊 ანალიზი", "tab3": "📜 ისტორია", "tab4": "📚 ცნობარი",
        "save": "🚀 განახლება", "download": "📥 ჩამოტვირთვა Excel",
        "sec_eff": "🚀 ეფექტურობა", "sec_sol": "🛡️ მდგრადობა და ლიკვიდურობა",
        "card_cap": "საკუთარი კაპიტალი", "card_cash": "ნაღდი ფული", "card_net": "წმინდა აქტივები",
        "assets": "💼 აქტივები", "liabilities": "💸 ვალდებულებები", "ops": "⚙️ ოპერაციები",
        "fa": "ძირითადი აქტივები", "ca": "მიმდინარე აქტივები", "ltl": "გრძელვადიანი ვალი", "stl": "მოკლევადიანი ვალი",
        "own_cap": "კაპიტალი", "init_inv": "საწყისი ინვესტიცია", "cash": "ნაღდი ფული", "ebitda": "EBITDA",
        "analysis_header": "🔍 ავტომატური ანალიზი", "strong": "✅ ძლიერი მხარეები", "risks": "⚠️ რისკები",
        "msg_autonomy": "🌟 **ავტონომია:** აქტივების უმეტესი ნაწილი თქვენია.",
        "msg_roi": "📈 **უკუგება:** ROI-ს მაღალი დონე.",
        "msg_liq": "💧 **ლიკვიდობა:** ნაღდი ფულის კარგი მარაგი.",
        "msg_dep": "🚩 **დამოკიდებულება:** ვალების მაღალი წილი.",
        "msg_cash_low": "💸 **Cash-ის დეფიციტი:** ცოტა ფული გადახდებისთვის.",
        "msg_bankrupt": "❌ **კრიტიკული რისკი:** ვალები აღემატება აქტივებს!",
        "chart_pie": "🍩 აქტივების შემადგენლობა", "chart_line": "📈 კაპიტალის ტრენდი",
        "guide": {
            "roi": "**ROI:** EBITDA / ინვესტიცია. მიზანი: > 25%.",
            "roe": "**ROE:** EBITDA / საკუთარი კაპიტალი. მიზანი: > 20%.",
            "roa": "**ROA:** EBITDA / ჯამური აქტივები. მიზანი: > 10%.",
            "sol2": "**Solvency 2:** აქტივები - ვალდებულებები. მინიმუმი: > 0.",
            "sol3": "**Solvency 3:** წმინდა აქტივები / ჯამური აქტივები. მინიმუმი: 50%.",
            "qr": "**Quick Ratio:** Cash / მოკლევადიანი ვალი. მიზანი: 2.0."
        }
    }
}


# --- 2. LOGIC FUNCTIONS ---
def get_analysis(m, t):
    strong, risks = [], []
    if m['sol3'] >= 50: strong.append(t['msg_autonomy'])
    if m['roi'] >= 25: strong.append(t['msg_roi'])
    if m['qr'] >= 2.0: strong.append(t['msg_liq'])

    if m['sol3'] < 30: risks.append(t['msg_dep'])
    if m['qr'] < 1.0: risks.append(t['msg_cash_low'])
    if m['sol2'] < 0: risks.append(t['msg_bankrupt'])
    return strong, risks


# --- 3. AUTHENTICATION & DB ---
init_db()
with open('config.yaml') as f:
    config = yaml.load(f, Loader=SafeLoader)

auth = stauth.Authenticate(config['credentials'], config['cookie']['name'], config['cookie']['key'],
                           config['cookie']['expiry_days'])

if not st.session_state.get("authentication_status"):
    t1, t2 = st.tabs(["🔑 Вход", "👤 Регистрация"])
    with t1:
        auth.login()
    with t2:
        if auth.register_user():
            with open('config.yaml', 'w') as f: yaml.dump(config, f)
            st.success('Успешно! Войдите во вкладке Вход.')

# --- 4. MAIN APP ---
if st.session_state.get("authentication_status"):
    user = st.session_state["username"]

    # Header & Multilingual
    c1, c2, c3 = st.columns([3, 1, 1])
    with c2:
        lang = st.selectbox("", options=list(UI_TEXTS.keys()), index=2, format_func=lambda x: UI_TEXTS[x]['name'])
        t = UI_TEXTS[lang]
    with c3:
        curr_symbol = {"USD": "$", "EUR": "€", "GEL": "₾"}[st.selectbox("", options=["GEL", "USD", "EUR"])]
    with c1:
        st.subheader(t["title"])
    st.markdown("---")

    # DB Defaults (FIX for sqlite3.Row error)
    raw_rec = get_latest_record(user)
    d = dict(raw_rec) if raw_rec else {
        'fixed_assets': 2000000, 'receivables': 500000, 'cash': 300000,
        'long_term_debt': 800000, 'short_term_debt': 200000, 'ebitda': 450000,
        'own_capital': 1000000, 'initial_inv': 1500000
    }

    # Sidebar with Progress Bar Logic
    with st.sidebar:
        st.write(f"👤 {user}")
        with st.expander(t["assets"], expanded=True):
            fa = st.number_input(t["fa"], value=int(d.get('fixed_assets', 0)))
            ca = st.number_input(t["ca"], value=int(d.get('receivables', 0)))
        with st.expander(t["liabilities"], expanded=True):
            ltl = st.number_input(t["ltl"], value=int(d.get('long_term_debt', 0)))
            stl = st.number_input(t["stl"], value=int(d.get('short_term_debt', 0)))
        with st.expander(t["ops"], expanded=True):
            own_cap = st.number_input(t["own_cap"], value=int(d.get('own_capital', 1000000)))
            init_inv = st.number_input(t["init_inv"], value=int(d.get('initial_inv', 1500000)))
            cash_v = st.number_input(t["cash"], value=int(d.get('cash', 0)))
            ebitda_v = st.number_input(t["ebitda"], value=int(d.get('ebitda', 0)))

        st.markdown("---")
        if st.button(t["save"], use_container_width=True):
            progress_bar = st.sidebar.progress(0)
            for percent in range(100):
                time.sleep(0.005)
                progress_bar.progress(percent + 1)

            save_record(user, {
                'fixed_assets': fa, 'receivables': ca, 'cash': cash_v,
                'long_term_debt': ltl, 'short_term_debt': stl,
                'ebitda': ebitda_v, 'own_capital': own_cap, 'initial_inv': init_inv,
                'inventory': 0, 'revenue': 0
            })
            st.toast("Updated!", icon="✅")
            time.sleep(0.5)
            st.rerun()

        auth.logout('Logout', 'sidebar')

    # Math
    total_a = fa + ca
    total_l = ltl + stl
    m = {
        'roi': (ebitda_v / init_inv * 100) if init_inv > 0 else 0,
        'roe': (ebitda_v / own_cap * 100) if own_cap > 0 else 0,
        'roa': (ebitda_v / total_a * 100) if total_a > 0 else 0,
        'sol2': total_a - total_l,
        'sol3': ((total_a - total_l) / total_a * 100) if total_a > 0 else 0,
        'qr': (cash_v / stl) if stl > 0 else 0
    }

    # Main Tabs
    tab1, tab2, tab3, tab4 = st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"]])

    with tab1:
        st.write(f"### {t['sec_eff']}")
        c_a, c_b, c_c = st.columns(3)
        c_a.metric("ROI", f"{m['roi']:.1f}%")
        c_b.metric("ROE", f"{m['roe']:.1f}%")
        c_c.metric("ROA", f"{m['roa']:.1f}%")

        st.write(f"### {t['sec_sol']}")
        c_d, c_e, c_f = st.columns(3)
        c_d.metric(t["card_net"], f"{m['sol2']:,.0f} {curr_symbol}")
        c_e.metric("Solvency Ratio", f"{m['sol3']:.1f}%")
        c_f.metric("Quick Ratio", f"{m['qr']:.2f}")

        st.write(f"### {t['analysis_header']}")
        s_list, r_list = get_analysis(m, t)
        col_s, col_r = st.columns(2)
        with col_s:
            st.success(f"**{t['strong']}**")
            for s in s_list: st.info(s)
        with col_r:
            st.warning(f"**{t['risks']}**")
            for r in r_list: st.error(r)

    with tab2:
        st.write(f"### {t['tab2']}")
        col_p, col_l = st.columns(2)
        with col_p:
            st.write(f"**{t['chart_pie']}**")
            st.plotly_chart(px.pie(values=[cash_v, ca, fa], names=[t['cash'], t['ca'], t['fa']], hole=0.4),
                            use_container_width=True)
        with col_l:
            hist_data = get_all_records(user)
            if not hist_data.empty:
                st.write(f"**{t['chart_line']}**")
                st.plotly_chart(px.line(hist_data, x='date', y='own_capital', markers=True), use_container_width=True)

    with tab3:
        st.write(f"### {t['tab3']}")
        history_df = get_all_records(user)
        if not history_df.empty:
            st.dataframe(history_df, use_container_width=True)

            # EXCEL EXPORT FIX
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                history_df.to_excel(writer, index=False, sheet_name='Finance_Report')

            st.download_button(
                label=t["download"],
                data=buffer.getvalue(),
                file_name=f"report_{user}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.info("No data found.")

    with tab4:
        st.write(f"### {t['tab4']}")
        for k, v in t["guide"].items():
            st.info(v)