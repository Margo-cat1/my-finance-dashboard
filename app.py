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
        "msg_autonomy": "🌟 **Автономия:** Большая часть активов — ваши. Это дает высокую устойчивость.",
        "msg_roi": "📈 **Окупаемость:** У вас отличный возврат на инвестиции (ROI).",
        "msg_liq": "💧 **Ликвидность:** Запас наличности позволяет мгновенно гасить срочные долги.",
        "msg_dep": "🚩 **Зависимость:** Высокая доля заемного капитала. Риск потери контроля.",
        "msg_cash_low": "💸 **Дефицит Cash:** Наличных денег недостаточно для покрытия текущих обязательств.",
        "msg_bankrupt": "❌ **Критический риск:** Отрицательный капитал! Долги превышают стоимость активов.",
        "chart_pie": "🍩 Состав активов", "chart_line": "📈 Тренд капитала",
        "forecast_title": "🔮 Прогноз окупаемости",
        "payback_msg": "Инвестиции окупятся через **{:.1f}** лет.",
        "never_payback": "⚠️ При текущем доходе окупаемость невозможна.",
        "projected_chart": "📈 Прогноз роста капитала (12 мес.)",
        "months_label": "Месяцы",
        "capital_label": "Капитал",
        "payback_line": "Точка окупаемости",
        "targets": {"roi": 25.0, "sol": 50.0, "qr": 1.5},
        "hints": {
            "roi": "ROI = EBITDA / Инвестиции. Сколько прибыли приносит каждый вложенный доллар.",
            "roe": "ROE = EBITDA / Капитал. Эффективность работы ваших собственных средств.",
            "roa": "ROA = EBITDA / Активы. Насколько эффективно работают все ресурсы бизнеса.",
            "net_assets": "Чистые активы = Активы - Долги. Реальная стоимость вашего бизнеса сегодня.",
            "solv": "Автономия = Чистые активы / Активы. Показывает долю собственности в бизнесе.",
            "qr": "Quick Ratio = Наличные / Краткоср. долги. Способность платить по счетам прямо сейчас."
        },
        "guide": {
            "roi": "📊 **ROI (Return on Investment):** Цель > 25%. Если ниже — бизнес приносит меньше, чем надежные фин. инструменты.",
            "roe": "💰 **ROE (Return on Equity):** Эффективность капитала. Важно, чтобы ROE был выше ROA — это признак работы 'рычага'.",
            "roa": "🏗️ **ROA (Return on Assets):** Показывает отдачу от всего имущества. Помогает понять, не слишком ли много у вас 'мертвых' активов.",
            "sol": "🛡️ **Solvency (Автономия):** Золотой стандарт — 50%. Если ниже 30%, бизнес становится заложником кредиторов.",
            "liq": "🌊 **Liquidity (Ликвидность):** Коэффициент выше 2.0 означает, что вы в безопасности. Ниже 1.0 — риск кассового разрыва.",
            "na": "💎 **Чистые активы:** Самый главный показатель. Если он растет от месяца к месяцу — вы богатеете."
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
        "msg_autonomy": "🌟 **Autonomy:** Most assets are yours, providing high stability.",
        "msg_roi": "📈 **Profitability:** Excellent return on investment level.",
        "msg_liq": "💧 **Liquidity:** Cash reserves allow instant coverage of short-term debts.",
        "msg_dep": "🚩 **Dependency:** High debt ratio. Risk of losing management control.",
        "msg_cash_low": "💸 **Cash Deficit:** Not enough cash to cover immediate liabilities.",
        "msg_bankrupt": "❌ **Critical Risk:** Negative equity! Debt exceeds total asset value.",
        "chart_pie": "🍩 Asset Structure", "chart_line": "📈 Equity Trend",
        "forecast_title": "🔮 Payback Forecast",
        "payback_msg": "Investment will break even in **{:.1f}** years.",
        "never_payback": "⚠️ Payback impossible at current EBITDA.",
        "projected_chart": "📈 Equity Growth Forecast (12 mo.)",
        "months_label": "Months",
        "capital_label": "Equity",
        "payback_line": "Break-even Point",
        "targets": {"roi": 25.0, "sol": 50.0, "qr": 1.5},
        "hints": {
            "roi": "ROI = EBITDA / Initial Investment. Total return on capital invested.",
            "roe": "ROE = EBITDA / Equity. Efficiency of your personal capital management.",
            "roa": "ROA = EBITDA / Total Assets. Efficiency of all business resources used.",
            "net_assets": "Net Assets = Assets - Debt. The real current value of your business.",
            "solv": "Solvency = Net Assets / Assets. Shows the ownership share in the business.",
            "qr": "Quick Ratio = Cash / S-term Debt. Ability to pay bills instantly."
        },
        "guide": {
            "roi": "📊 **ROI:** Target > 25%. If lower, consider alternative investment options.",
            "roe": "💰 **ROE:** Equity efficiency. Ideally, ROE should exceed ROA (leverage effect).",
            "roa": "🏗️ **ROA:** Return on all assets. Helps identify 'dead' or unproductive assets.",
            "sol": "🛡️ **Solvency:** 50% is the gold standard. Below 30% is high risk.",
            "liq": "🌊 **Liquidity:** Ratio > 2.0 is safe. Below 1.0 indicates potential cash flow issues.",
            "na": "💎 **Net Assets:** The ultimate metric. Growth means you are building wealth."
        }
    },
    "GE": {
        "name": "ქართული", "title": "📈 ფინანსური ინტელექტი",
        "tab1": "📥 შეტანა", "tab2": "📊 ანალიზი", "tab3": "📜 ისტორია", "tab4": "📚 ცნობარი",
        "save": "🚀 განახლება", "download": "📥 ჩამოტვირთვა",
        "sec_eff": "🚀 ეფექტურობა", "sec_sol": "🛡️ მდგრადობა და ლიკვიდურობა",
        "card_cap": "საკუთარი კაპიტალი", "card_cash": "ნაღდი ფული", "card_net": "წმინდა აქტივები",
        "assets": "💼 აქტივები", "liabilities": "💸 ვალდებულებები", "ops": "⚙️ ოპერაციები",
        "fa": "ძირითადი აქტივები", "ca": "მიმდინარე აქტივები", "ltl": "გრძელვადიანი ვალი", "stl": "მოკლევადიანი ვალი",
        "own_cap": "კაპიტალი", "init_inv": "ინვესტიცია", "cash": "ნაღდი ფული", "ebitda": "EBITDA",
        "analysis_header": "🔍 ავტომატური ანალიზი", "strong": "✅ ძლიერი მხარეები", "risks": "⚠️ რისკები",
        "msg_autonomy": "🌟 **ავტონომია:** აქტივების უმეტესი ნაწილი თქვენია. ეს იძლევა მაღალ მდგრადობას.",
        "msg_roi": "📈 **უკუგება:** თქვენ გაქვთ საუკეთესო ROI.",
        "msg_liq": "💧 **ლიკვიდობა:** ნაღდი ფულის მარაგი იძლევა ვალების დაფარვის საშუალებას.",
        "msg_dep": "🚩 **დამოკიდებულება:** ვალების მაღალი წილი. კონტროლის დაკარგვის რისკი.",
        "msg_cash_low": "💸 **Cash-ის დეფიციტი:** ნაღდი ფული არ არის საკმარისი ვალდებულებებისთვის.",
        "msg_bankrupt": "❌ **კრიტიკული რისკი:** ვალები აღემატება აქტივების ღირებულებას!",
        "chart_pie": "🍩 აქტივების შემადგენლობა", "chart_line": "📈 კაპიტალის ტრენდი",
        "forecast_title": "🔮 ანაზღაურების პროგნოზი",
        "payback_msg": "ინვესტიცია ამოღებული იქნება **{:.1f}** წელიწადში.",
        "never_payback": "⚠️ ამ მოგებით ინვესტიციის ამოღება შეუძლებელია.",
        "projected_chart": "📈 კაპიტალის ზრდის პროგნოზი (12 თვე)",
        "months_label": "თვეები",
        "capital_label": "კაპიტალი",
        "payback_line": "ანაზღაურების წერტილი",
        "targets": {"roi": 25.0, "sol": 50.0, "qr": 1.5},
        "hints": {
            "roi": "ROI = EBITDA / ინვესტიცია. გვიჩვენებს ყოველი ჩადებული ლარის უკუგებას.",
            "roe": "ROE = EBITDA / კაპიტალი. საკუთარი სახსრების მართვის ეფექტურობა.",
            "roa": "ROA = EBITDA / აქტივები. ბიზნეს რესურსების გამოყენების ეფექტურობა.",
            "net_assets": "წმინდა აქტივები = აქტივები - ვალები. თქვენი ბიზნესის რეალური ფასი.",
            "solv": "ავტონომია = წმინდა აქტივები / აქტივები. გვიჩვენებს საკუთრების წილს ბიზნესში.",
            "qr": "Quick Ratio = ნაღდი ფული / მოკლევადიანი ვალი. გადახდისუნარიანობა."
        },
        "guide": {
            "roi": "📊 **ROI:** მიზანი > 25%. თუ ნაკლებია — ბიზნესს მოაქვს იმაზე ნაკლები, ვიდრე ანაბარს.",
            "roe": "💰 **ROE:** კაპიტალის ეფექტურობა. მნიშვნელოვანია ROE იყოს მეტი ვიდრე ROA.",
            "roa": "🏗️ **ROA:** გვიჩვენებს მთელი ქონების უკუგებას. გვეხმარება 'მკვდარი' აქტივების პოვნაში.",
            "sol": "🛡️ **Solvency:** 50% არის ოქროს სტანდარტი. 30%-ზე დაბლა მაღალი რისკია.",
            "liq": "🌊 **Liquidity:** კოეფიციენტი > 2.0 ნიშნავს უსაფრთხოებას. 1.0-ზე დაბლა კრიზისია.",
            "na": "💎 **წმინდა აქტივები:** მთავარი მაჩვენებელი. მისი ზრდა ნიშნავს, რომ მდიდრდებით."
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

auth = stauth.Authenticate(config['credentials'],
                           config['cookie']['name'],
                           config['cookie']['key'],
                           config['cookie']['expiry_days'])

if not st.session_state.get("authentication_status"):
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        st.markdown("<h1 style='text-align: center;'>🏦 FinMarge PRO</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>Ваш персональный финансовый аналитик</p>",
                    unsafe_allow_html=True)


        auth_tab1, auth_tab2 = st.tabs(["🔐 Вход в систему", "👤 Регистрация"])
        with auth_tab1:
            auth.login(location='main')
            if st.session_state["authentication_status"] is False:
                st.error("Неверное имя пользователя или пароль")
            elif st.session_state["authentication_status"] is None:
                st.warning("Пожалуйста, введите данные")

        with auth_tab2:
            st.markdown("### Создать аккаунт")
            try:
                # Включаем регистрацию
                if auth.register_user(location='main'):
                    with open('config.yaml', 'w') as f:
                        yaml.dump(config, f, default_flow_style=False)
                    st.success('Аккаунт создан! Теперь перейдите во вкладку Вход.')
            except Exception as e:
                st.error(f"Ошибка при регистрации: {e}")


# --- 4. MAIN APP ---
if st.session_state.get("authentication_status"):
    user = st.session_state["username"]

    # --- ОБНОВЛЕННЫЙ CSS ---
    st.markdown("""
            <style>
                .block-container {
                    padding-top: 1rem !important;
                }
                /* Создаем обертку для навигации */
                .nav-wrapper {
                    background-color: #f8f9fb;
                    padding: 15px 25px;
                    border-radius: 12px;
                    border: 1px solid #e6e9ef;
                    margin-bottom: 30px;
                }
                /* Скрываем заголовки селекторов */
                div[data-testid="stSelectbox"] label {
                    display: none;
                }
                /* Убираем лишние отступы у колонок */
                [data-testid="column"] {
                    display: flex;
                    align-items: center;
                }
            </style>
        """, unsafe_allow_html=True)

    # --- ВЕРХНЯЯ ПАНЕЛЬ ---
    # Мы создаем одну общую плашку через Markdown,
    # а затем используем колонки прямо под ней
    st.markdown('<div class="nav-wrapper">', unsafe_allow_html=True)

    # Важно: колонки должны быть ВНУТРИ контейнера, чтобы попасть на фон
    nav_container = st.container()
    with nav_container:
        c_nav1, c_nav2, c_nav3 = st.columns([4, 1.2, 1])

        with c_nav1:
            st.markdown("<h2 style='margin:0; color:#1f77b4; font-size:24px;'>🏦 FinMarge PRO</h2>",
                        unsafe_allow_html=True)

        with c_nav2:
            lang = st.selectbox("", options=list(UI_TEXTS.keys()), index=2,
                                format_func=lambda x: UI_TEXTS[x]['name'], key="nav_lang")
            t = UI_TEXTS[lang]

        with c_nav3:
            target_currency = st.selectbox("", options=["GEL", "USD", "EUR"], key="nav_curr")
            curr_symbol = {"USD": "$", "EUR": "€", "GEL": "₾"}[target_currency]

    st.markdown('</div>', unsafe_allow_html=True)



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
        # --- СЕКЦИЯ: ЭФФЕКТИВНОСТЬ ---
        st.write(f"### {t['sec_eff']}")
        c_a, c_b, c_c = st.columns(3)

        # ROI
        roi_target = t["targets"]["roi"]
        roi_delta = m['roi'] - roi_target
        # Если ROI выше цели -> красим дельту в зеленый (normal)
        # Если ROI ниже цели -> красим дельту в красный (normal + отрицательное число даст красный)
        c_a.metric(
            label="ROI",
            value=f"{m['roi']:.1f}%",
            delta=f"{roi_delta:+.1f}% vs target",
            delta_color="normal",
            help=t['hints']['roi']
        )

        c_b.metric("ROE", f"{m['roe']:.1f}%", help=t['hints']['roe'])
        c_c.metric("ROA", f"{m['roa']:.1f}%", help=t['hints']['roa'])

        # --- СЕКЦИЯ: УСТОЙЧИВОСТЬ ---
        st.write(f"### {t['sec_sol']}")
        c_d, c_e, c_f = st.columns(3)
        c_d.metric(t["card_net"], f"{m['sol2']:,.0f} {curr_symbol}", help=t['hints']['net_assets'])

        # Solvency Ratio
        sol_target = t["targets"]["sol"]
        sol_delta = m['sol3'] - sol_target
        c_e.metric(
            label="Solvency Ratio",
            value=f"{m['sol3']:.1f}%",
            delta=f"{sol_delta:+.1f}% vs target",
            delta_color="normal",
            help=t['hints']['solv']
        )

        # Quick Ratio
        qr_target = t["targets"]["qr"]
        qr_delta = m['qr'] - qr_target
        c_f.metric(
            label="Quick Ratio",
            value=f"{m['qr']:.2f}",
            delta=f"{qr_delta:+.2f} vs target",
            delta_color="normal",
            help=t['hints']['qr']
        )

        # --- АВТОМАТИЧЕСКИЙ АНАЛИЗ (Твой старый блок) ---
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

        # --- Секция прогноза (добавляем ПОСЛЕ твоих графиков) ---
        st.markdown("---")
        st.write(f"### {t['forecast_title']}")

        if ebitda_v > 0:
            payback_years = init_inv / ebitda_v
            st.success(t["payback_msg"].format(payback_years))

            # Строим прогноз на 12 месяцев
            future_months = list(range(13))
            # Твой текущий капитал + (прибыль/12 * месяц)
            equity_projection = [own_cap + (ebitda_v / 12 * m) for m in future_months]

            df_forecast = pd.DataFrame({
                "Month": future_months,
                "Equity": equity_projection
            })

            # Новый график прогноза
            fig_f = px.line(df_forecast, x="Month", y="Equity",
                            title=t["projected_chart"], markers=True)

            # Зеленая пунктирная линия — когда мы выходим "в ноль"
            fig_f.add_hline(y=init_inv, line_dash="dot", line_color="green",
                            annotation_text=t["payback_line"])

            st.plotly_chart(fig_f, use_container_width=True)
        else:
            st.error(t["never_payback"])

    with tab3:
        st.write(f"### {t['tab3']}")
        history_df = get_all_records(user)

        if not history_df.empty:
            st.dataframe(history_df, use_container_width=True)

            st.markdown("---")
            st.write("📥 **Выгрузить отчет:**")
            col_ex, col_csv = st.columns(2)

            # --- ПОДГОТОВКА EXCEL ---
            # Используем io.BytesIO(), чтобы файл создавался в памяти, а не на диске
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                history_df.to_excel(writer, index=False, sheet_name='Financial_Report')

            # Вытаскиваем данные из буфера ПЕРЕД тем как кнопка их запросит
            excel_data = buffer.getvalue()

            with col_ex:
                st.download_button(
                    label="💾 Скачать в Excel (.xlsx)",
                    data=excel_data,
                    file_name=f"fin_report_{user}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

            # --- ПОДГОТОВКА CSV ---
            csv_data = history_df.to_csv(index=False).encode('utf-8-sig')
            with col_csv:
                st.download_button(
                    label="📄 Скачать в CSV (.csv)",
                    data=csv_data,
                    file_name=f"fin_report_{user}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        else:
            # Если данных нет, мы хотя бы объясняем пользователю, почему кнопок нет
            st.info("Чтобы скачать отчет, сначала добавьте данные через боковое меню и нажмите 'Обновить показатели'.")

    with tab4:
        st.write(f"### {t['tab4']}")
        for k, v in t["guide"].items():
            st.info(v)