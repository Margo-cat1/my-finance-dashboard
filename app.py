import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
from database import init_db, save_record, get_latest_record

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
        "msg_bankrupt": "❌ **კრიტიკული რისკი:** ვალები აღემაება აქტივებს!",
        "guide": {
            "roi": "**ROI:** EBITDA / ინვესტიცია. **მიზანი: > 25%**.",
            "roe": "**ROE:** EBITDA / საკუთარი კაპიტალი. **მიზანი: > 20%**.",
            "roa": "**ROA:** EBITDA / ჯამური აქტივები. **მიზანი: > 10%**.",
            "sol2": "**Solvency 2:** აქტივები - ვალდებულებები. **მინიმუმი: > 0**.",
            "sol3": "**Solvency 3:** წმინდა აქტივები / ჯამური აქტივები. **მინიმუმი: 50%**.",
            "qr": "**Quick Ratio:** Cash / მოკლევადიანი ვალი. **მინიმუმი: 2.0**."
        }
    }
}








# 3. Теперь в сайдбаре (где st.sidebar) подставляем эти переменные в value
with st.sidebar:
    with st.expander(t["assets"], expanded=True):
        fa = st.number_input(t["fa"], value=db_fa)  # Вместо actual_balance ставим db_fa
        ca = st.number_input(t["ca"], value=db_ca)

    with st.expander(t["ops"], expanded=True):
        cash_val = st.number_input(t["cash"], value=db_cash)
        ebitda_val = st.number_input(t["ebitda"], value=db_ebitda)


# Позволяет телефону распознать сайт как приложение
st.markdown(f'<link rel="manifest" href="manifest.json">', unsafe_allow_html=True)
# 1. Настройка страницы
st.set_page_config(page_title="FinMarge PRO", page_icon="📈", layout="wide")

# --- СТИЛИЗАЦИЯ ФОРМЫ ЛОГИНА ---
st.markdown("""
    <style>
    /* Центрируем блок логина */
    [data-testid="stForm"] {
        border: none;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        background-color: #ffffff;
        max-width: 450px;
        margin: 50px auto;
    }
    /* Заголовок формы */
    .login-header {
        text-align: center;
        font-family: 'Inter', sans-serif;
        color: #1e2130;
        margin-bottom: 30px;
    }
    /* Кнопка входа */
    button[kind="primaryFormSubmit"] {
        width: 100%;
        background: linear-gradient(90deg, #00d4ff 0%, #090979 100%);
        border: none;
        color: white;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- БЛОК АВТОРИЗАЦИИ ---
credentials = {
    'usernames': {
        'admin': {'name': 'Admin User', 'password': '123'},
        'margo': {'name': 'Margo', 'password': '456'}
    }
}

authenticator = stauth.Authenticate(
    credentials,
    'finance_cookie',
    'auth_key',
    cookie_expiry_days=30
)

# Красивый заголовок над формой
if not st.session_state.get("authentication_status"):
    st.markdown("<h1 class='login-header'>🔐 Financial Intelligence</h1>", unsafe_allow_html=True)

# Вызываем логин
# 1. Сначала инициализируем базу
init_db()

# 2. Показываем форму логина
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:

    # --- ТОЛЬКО ТУТ, КОГДА ВХОД ВЫПОЛНЕН, ЗАГРУЖАЕМ ДАННЫЕ ---

    lang_choice = st.selectbox("🌐 Language", list(LANGS.keys()))
    t = LANGS[lang_choice]
    st.write(f'👤 *{st.session_state["name"]}*')
    last_rec = get_latest_record(st.session_state["username"])

    if last_rec:
                db_fa = float(last_rec['fixed_assets'])
                db_ca = float(last_rec['receivables'])
                db_cash = float(last_rec['cash'])
                db_ltl = float(last_rec['long_term_debt'])
                db_stl = float(last_rec['short_term_debt'])
                db_ebitda = float(last_rec['ebitda'])
    else:
                db_fa, db_ca, db_cash = 2100000.0, 900000.0, 300000.0
                db_ltl, db_stl, db_ebitda = 800000.0, 400000.0, 450000.0

        # 3. основной интерфейс (с отступом!)
        with st.sidebar:
            with st.expander(t["assets"], expanded=True):
                fa = st.number_input(t["fa"], value=db_fa)  # Используем db_fa





    # 3. Дальше идет отрисовка твоего интерфейса (st.sidebar и т.д.)
    st.sidebar.title(f"Welcome {name}")
    # ...

    # ОСНОВНОЙ КОД


    st.markdown("""
        <style>
        /* 1. ОБЩИЕ НАСТРОЙКИ ШРИФТА И ФОНА */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

        html, body, [data-testid="stAppViewContainer"] {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
        }

        /* 2. ВОЗВРАЩАЕМ КНОПКУ МЕНЮ И НАСТРАИВАЕМ САЙДБАР */
        header {
            visibility: visible !important; /* Кнопка меню должна быть видна! */
            background: transparent !important;
        }

        [data-testid="stSidebar"] {
            background-color: white !important;
            border-right: 1px solid rgba(0,0,0,0.05);
        }

        /* 3. ФИКС ДЛЯ МОБИЛОК (Чтобы не было каши) */
        @media (max-width: 640px) {
            [data-testid="stSidebar"] {
                width: 80vw !important; /* Меню занимает 80% экрана */
                z-index: 1000001 !important;
            }

            /* Добавляем отступ сверху в меню, чтобы элементы не вылазили под кнопку закрытия */
            [data-testid="stSidebar"] .block-container {
                padding-top: 3rem !important;
            }

            /* Метрики чуть мельче на мобилке, чтобы не наезжали друг на друга */
            [data-testid="stMetricValue"] {
                font-size: 1.4rem !important;
            }
        }

        /* 4. КАРТОЧКИ (Glassmorphism) */
        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.7) !important;
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.4);
            border-radius: 20px !important;
            padding: 15px !important;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.05) !important;
        }

        /* 5. ПОЛЯ ВВОДА */
        input {
            -webkit-user-select: text !important;
            user-select: text !important;
        }

        /* 6. КРАСИВЫЕ ТАБЫ */
        .stTabs [aria-selected="true"] {
            background: linear-gradient(90deg, #00d4ff 0%, #090979 100%) !important;
            color: white !important;
            border-radius: 12px !important;
        }

        /* Скрываем только футер (сделано в Streamlit) */
        footer {visibility: hidden;}
        </style>
        """, unsafe_allow_html=True)












    with st.expander(t["assets"], expanded=True):
        fa = st.number_input(t["fa"], value=float(actual_balance))
        ca = st.number_input(t["ca"], value=float(actual_balance))
    with st.expander(t["liabilities"], expanded=True):
        ltl = st.number_input(t["ltl"], value=800000)
        stl = st.number_input(t["stl"], value=400000)
    with st.expander(t["ops"], expanded=True):
        own_cap = st.number_input(t["own_cap"], value=1000000)
        init_inv = st.number_input(t["init_inv"], value=1500000)
        cash_val = st.number_input(t["cash"], value=300000)
        ebitda_val = st.number_input(t["ebitda"], value=450000)

        sim_ebitda = st.slider("EBITDA Change %", -50, 50, 0)
        authenticator.logout('Logout', 'sidebar')
        # --- КНОПКА СОХРАНЕНИЯ  ---
        if st.button("🚀 Сохранить данные в базу"):
            # Собираем данные
            data_to_save = {
                'cash': cash_val,  # из строки 214
                'receivables': ca,  # твои Current Assets (ca)
                'inventory': 0,  # если нет отдельного поля, ставим 0
                'fixed_assets': fa,  # из строки 206
                'short_term_debt': stl,  # из строки 210
                'long_term_debt': ltl,  # из строки 209
                'revenue': 0,  # если выручки нет в инпутах, ставим 0
                'ebitda': ebitda_val  # из строки 215
            }

            # Берем имя пользователя из сессии (которое на скрине в строке 201)
            current_user = st.session_state["username"]

            # Сохраняем (функция из database.py)
            save_record(current_user, data_to_save)
            st.sidebar.success(f"Данные для {current_user} сохранены!")
    # Расчеты
    total_assets = fa + ca
    total_liabilities = ltl + stl
    current_ebitda = ebitda_val * (1 + sim_ebitda / 100)
    roi = (current_ebitda / init_inv * 100) if init_inv != 0 else 0
    roe = (current_ebitda / own_cap * 100) if own_cap != 0 else 0
    roa = (current_ebitda / total_assets * 100) if total_assets != 0 else 0
    sol2_val = total_assets - total_liabilities
    sol3_pct = (sol2_val / total_assets * 100) if total_assets != 0 else 0
    qr = (cash_val / stl) if stl != 0 else 0

    st.title(t["title"])
    tab1, tab2, tab3 = st.tabs([t["tab1"], t["tab2"], t["tab3"]])

    with tab1:
        # --- СЕКЦИЯ 1: ЭФФЕКТИВНОСТЬ (ROI, ROE, ROA) ---
        st.markdown(f'<div class="section-header">{t["sec_eff"]}</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)

        # Расчеты (убедись, что переменные определены выше в коде)
        # roi = (current_ebitda / init_inv * 100)
        # roe = (current_ebitda / own_cap * 100)
        # roa = (current_ebitda / total_assets * 100)

        c1.metric("ROI (Окупаемость)", f"{roi:.1f}%", delta=f"{sim_ebitda}%")
        c2.metric("ROE (Капитал)", f"{roe:.1f}%")
        c3.metric("ROA (Активы)", f"{roa:.1f}%")

        # --- СЕКЦИЯ 2: УСТОЙЧИВОСТЬ ---
        st.markdown(f'<div class="section-header">{t["sec_sol"]}</div>', unsafe_allow_html=True)
        c4, c5, c6 = st.columns(3)
        c4.metric("Solvency 2 (Net Assets)", f"{sol2_val:,.0f} $")
        c5.metric("Solvency 3 (%)", f"{sol3_pct:.1f}%")
        c6.metric("Quick Ratio (Ликвидность)", f"{qr:.2f}")

        # --- СЕКЦИЯ 3: АВТОМАТИЧЕСКИЙ АНАЛИЗ (Как на твоем фото) ---
        st.markdown(f'<div class="section-header">{t["analysis_header"]}</div>', unsafe_allow_html=True)

        col_s, col_r = st.columns(2)

        with col_s:
            st.success(f"### {t['strong']}")
            if sol3_pct >= 50:
                st.info(f"💎 {t['msg_autonomy']}")
            if roi >= 25:
                st.info(f"🚀 {t['msg_roi']} ({roi:.1f}%)")
            if qr >= 2.0:
                st.info(f"💧 {t['msg_liq']}")

        with col_r:
            st.warning(f"### {t['risks']}")
            if sol3_pct < 30:
                st.error(f"🚩 {t['msg_dep']}")
            if qr < 2.0:
                st.error(f"🚨 {t['msg_cash_low']} (Current: {qr:.2f})")
            if sol2_val < 0:
                st.error(f"💣 {t['msg_bankrupt']}")


    with tab2:
        st.table(pd.DataFrame({
            "Parameter": ["Assets", "Liabilities", "Equity", "Net Assets", "EBITDA"],
            "Value ($)": [f"{total_assets:,.0f}", f"{total_liabilities:,.0f}", f"{own_cap:,.0f}", f"{sol2_val:,.0f}",
                          f"{current_ebitda:,.0f}"]
        }))

    with tab3:
        st.markdown(f'<div class="section-header">📚 {t["tab3"]}</div>', unsafe_allow_html=True)
        for key in t["guide"]:
            st.info(t["guide"][key])


