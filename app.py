import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
import plotly.express as px
from database import init_db, save_record, get_latest_record, get_all_records


# 1. Настройка страницы (строго первой командой)
st.set_page_config(page_title="FinMarge PRO", page_icon="📈", layout="wide")

# 2. Словарь переводов
LANGS = {
    "Русский": {
        "title": "📊 Финансовый Интеллект",
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
            "roi": "**ROI:** EBITDA / Инвестиции. **Цель: > 25%**.",
            "roe": "**ROE:** EBITDA / Собственный капитал. **Цель: > 20%**.",
            "roa": "**ROA:** EBITDA / Общие активы. **Цель: > 10%**.",
            "sol2": "**Solvency 2:** Активы - Долги. **Минимум: > 0**.",
            "sol3": "**Solvency 3:** Чистые активы / Общие активы. **Минимум: 50%**.",
            "qr": "**Quick Ratio:** Cash / Краткосрочные долги. **Минимум: 2.0**."
        }
    },
    "ქართული": {
        "title": "📊 ფინანსური ინტელექტი",
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
        "msg_bankrupt": "❌ **კრიტიკული რისკი:** ვალები აღემაება აქტივებს!",
        "guide": {
            "roi": "**ROI:** EBITDA / ინვესტიცია. **მიზანი: > 25%**.",
            "roe": "**ROE:** EBITDA / საკუთარი კაპიტალი. **მიზანი: > 20%**.",
            "roa": "**ROA:** EBITDA / ჯამური აქტივები. **მიზანი: > 10%**.",
            "sol2": "**Solvency 2:** აქტივები - ვალდებულებები. **მინიმუმი: > 0**.",
            "sol3": "**Solvency 3:** წმინდა აქტივები / ჯამური აქტივები. **მინიმუმი: 50%**.",
            "qr": "**Quick Ratio:** Cash / მოკლევადიანი ვალი. **მიზანი: 2.0**."
        }
    }
}

# 3. Кастомный стиль
st.markdown("""
    <style>
    [data-testid="stMetric"] { background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(10px); border-radius: 15px; padding: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
    .section-header { font-size: 1.5rem; font-weight: bold; margin-top: 20px; margin-bottom: 10px; border-bottom: 2px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

# 4. Инициализация базы и авторизация
init_db()

import yaml
from yaml.loader import SafeLoader

# 4. Инициализация базы и авторизация
init_db()

# Загружаем конфиг из файла
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

if not st.session_state["authentication_status"]:
    tab_login, tab_reg = st.tabs(["🔑 Вход", "👤 Регистрация"])
    with tab_login:
        authenticator.login()
    with tab_reg:
        try:
            # Регистрация нового пользователя
            if authenticator.register_user():
                # ВАЖНО: записываем обновленные данные обратно в файл config.yaml
                with open('config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
                st.success('Пользователь зарегистрирован! Теперь войдите во вкладке "Вход"')
        except Exception as e:
            st.error(f"Ошибка: {e}")


# 5. ОСНОВНАЯ ЧАСТЬ (выполняется только после входа)
if st.session_state["authentication_status"]:

    # Выбор языка
    lang_choice = st.sidebar.selectbox("🌐 Language", list(LANGS.keys()))
    t = LANGS[lang_choice]

    st.sidebar.write(f'👤 **{st.session_state["name"]}**')

    # Загрузка данных из базы
    last_rec = get_latest_record(st.session_state["username"])

    if last_rec:
        db_fa = float(last_rec['fixed_assets'])
        db_ca = float(last_rec['receivables'])
        db_cash = float(last_rec['cash'])
        db_ltl = float(last_rec['long_term_debt'])
        db_stl = float(last_rec['short_term_debt'])
        db_ebitda = float(last_rec['ebitda'])
        # Используем .get() или проверку ключей для новых полей
        db_own_cap = float(last_rec['own_capital']) if 'own_capital' in last_rec.keys() else 1000000.0
        db_init_inv = float(last_rec['initial_inv']) if 'initial_inv' in last_rec.keys() else 1500000.0
    else:
        db_fa, db_ca, db_cash = 2100000.0, 900000.0, 300000.0
        db_ltl, db_stl, db_ebitda = 800000.0, 400000.0, 450000.0
        db_own_cap, db_init_inv = 1000000.0, 1500000.0

    # САЙДБАР (Ввод данных)
    with st.sidebar:
        with st.expander(t["assets"], expanded=True):
            fa = st.number_input(t["fa"], value=int(db_fa), step=1, format="%d")
            ca = st.number_input(t["ca"], value=int(db_ca), step=1, format="%d")

        with st.expander(t["liabilities"], expanded=True):
            ltl = st.number_input(t["ltl"], value=int(db_ltl), step=1, format="%d")
            stl = st.number_input(t["stl"], value=int(db_stl), step=1, format="%d")

        with st.expander(t["ops"], expanded=True):
            own_cap = st.number_input(t["own_cap"], value=int(db_own_cap), step=1, format="%d")   # Теперь динамично
            init_inv = st.number_input(t["init_inv"], value=int(db_init_inv), step=1, format="%d")    # Теперь динамично
            cash_val = st.number_input(t["cash"], value=int(db_cash), step=1, format="%d")
            ebitda_val = st.number_input(t["ebitda"], value=int(db_ebitda), step=1, format="%d")

            # --- ВАЛИДАЦИЯ И ПРОФЕССИОНАЛЬНОЕ СОХРАНЕНИЕ ---
            st.markdown("---")
            if st.button("🚀 Обновить показатели", use_container_width=True):  # Кнопка на всю ширину
                if cash_val == 0 and own_cap == 0:
                    st.error("⚠️ Система: Данные для анализа отсутствуют.")
                else:
                    # Прогресс-бар вместо шариков
                    progress_bar = st.sidebar.progress(0)
                    for percent_complete in range(100):
                        import time

                        time.sleep(0.005)  # Имитация обработки
                        progress_bar.progress(percent_complete + 1)

                    data = {
                        'cash': cash_val, 'receivables': ca, 'inventory': 0,
                        'fixed_assets': fa, 'short_term_debt': stl, 'long_term_debt': ltl,
                        'revenue': 0, 'ebitda': ebitda_val,
                        'own_capital': own_cap,
                        'initial_inv': init_inv
                    }

                    save_record(st.session_state["username"], data)

                    # Стильное уведомление в углу экрана (вместо шариков)
                    st.toast('База данных успешно обновлена', icon='📈')

                    # Очищаем прогресс-бар и обновляем
                    progress_bar.empty()
                    st.rerun()

            # --- ЭКСПОРТ В EXCEL (сразу под кнопкой) ---
        st.markdown("---")
        history_df = get_all_records(st.session_state["username"])

        if not history_df.empty:
            import io

            buffer = io.BytesIO()
            # Создаем Excel файл "на лету"
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                history_df.to_excel(writer, index=False, sheet_name='Finance_Report')

            st.download_button(
                label="📥 Скачать историю в Excel",
                data=buffer,
                file_name=f"report_{st.session_state['username']}.xlsx",
                mime="application/vnd.ms-excel"
            )


        authenticator.logout('Logout', 'sidebar')

    # РАСЧЕТЫ
    total_assets = fa + ca
    total_liabilities = ltl + stl

    roi = (ebitda_val / init_inv * 100) if init_inv != 0 else 0
    roe = (ebitda_val / own_cap * 100) if own_cap != 0 else 0
    roa = (ebitda_val / total_assets * 100) if total_assets != 0 else 0
    sol2_val = total_assets - total_liabilities
    sol3_pct = (sol2_val / total_assets * 100) if total_assets != 0 else 0
    qr = (cash_val / stl) if stl != 0 else 0

    # ОСНОВНОЙ ИНТЕРФЕЙС
    st.title(t["title"])
    tab1, tab2, tab3 = st.tabs([t["tab1"], t["tab2"], t["tab3"]])

    with tab1:
        st.markdown(f'<div class="section-header">{t["sec_eff"]}</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("ROI", f"{roi:.1f}%")
        c2.metric("ROE", f"{roe:.1f}%")
        c3.metric("ROA", f"{roa:.1f}%")

        st.markdown(f'<div class="section-header">{t["sec_sol"]}</div>', unsafe_allow_html=True)
        c4, c5, c6 = st.columns(3)
        c4.metric("Net Assets (Sol 2)", f"{sol2_val:,.0f} $")
        c5.metric("Solvency 3 (%)", f"{sol3_pct:.1f}%")
        c6.metric("Quick Ratio (Ликв.)", f"{qr:.2f}")

        st.markdown(f'<div class="section-header">{t["analysis_header"]}</div>', unsafe_allow_html=True)
        col_s, col_r = st.columns(2)
        with col_s:
            st.success(f"### {t['strong']}")
            if sol3_pct >= 50: st.info(f"💎 {t['msg_autonomy']}")
            if roi >= 25: st.info(f"🚀 {t['msg_roi']} ({roi:.1f}%)")
            if qr >= 2.0: st.info(f"💧 {t['msg_liq']}")
        with col_r:
            st.warning(f"### {t['risks']}")
            if sol3_pct < 30: st.error(f"🚩 {t['msg_dep']}")
            if qr < 2.0: st.error(f"🚨 {t['msg_cash_low']} ({qr:.2f})")
            if sol2_val < 0: st.error(f"💣 {t['msg_bankrupt']}")

    import plotly.express as px  # Добавь этот импорт в самый верх файла!

    with tab2:
        st.subheader("🏦 Финансовый Дашборд")

        # --- ШАГ 1: ПОЛУЧАЕМ ДАННЫЕ (Этого не хватало на скрине!) ---
        history_df = get_all_records(st.session_state["username"])

        # 1. Основные показатели в стильных карточках
        with st.container(border=True):
            col1, col2, col3 = st.columns(3)
            col1.metric("Собственный капитал", f"{own_cap:,.0f} $")
            col2.metric("Наличные (Cash)", f"{cash_val:,.0f} $")
            col3.metric(
                "Чистые активы",
                f"{sol2_val:,.0f} $",
                delta="Норма" if sol2_val >= 0 else "Риск",
                delta_color="normal" if sol2_val >= 0 else "inverse"
            )

        st.markdown("###")

        # 2. Визуализация (только если есть история)
        if not history_df.empty:
            chart_col1, chart_col2 = st.columns(2)

            with chart_col1:
                with st.container(border=True):
                    st.write("#### 🍩 Состав активов")
                    import plotly.express as px

                    fig_pie = px.pie(
                        values=[cash_val, ca, fa],
                        names=['Наличные', 'Дебиторка', 'Внеоборотные'],
                        hole=0.5,
                        color_discrete_sequence=px.colors.qualitative.Safe
                    )
                    # Лечим обрывы: увеличиваем margin (отступы)
                    fig_pie.update_layout(
                        margin=dict(l=30, r=30, t=30, b=30),
                        height=350,
                        showlegend=False
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)

            with chart_col2:
                with st.container(border=True):
                    st.write("#### 📈 Тренд капитала")
                    fig_line = px.line(
                        history_df, x='date', y='own_capital',
                        markers=True, line_shape="spline"
                    )
                    fig_line.update_traces(line_color='#00CC96')
                    # Лечим обрывы: l=50 дает место для цифр на оси Y
                    fig_line.update_layout(
                        margin=dict(l=50, r=30, t=30, b=30),
                        height=350,
                        xaxis_title=None,
                        yaxis_title=None
                    )
                    st.plotly_chart(fig_line, use_container_width=True)

            st.markdown("###")

            # 3. Детальная история
            with st.expander("📂 Посмотреть детальную таблицу истории", expanded=False):
                st.dataframe(
                    history_df.style.background_gradient(subset=['own_capital'], cmap='Greens'),
                    use_container_width=True
                )
        else:
            st.info("История пока пуста. Нажмите 'Сохранить данные' в сайдбаре.")
    with tab3:
        st.markdown(f'<div class="section-header">📚 {t["tab3"]}</div>', unsafe_allow_html=True)
        for key in t["guide"]:
            st.info(t["guide"][key])

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')