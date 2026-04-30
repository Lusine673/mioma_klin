import streamlit as st
import numpy as np

# Настройка страницы
st.set_page_config(page_title="Прогноз рецидива миомы", layout="centered")

# Стилизация под образец (CSS)
st.markdown("""
    <style>
    .main {
        background-color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
    }
    .result-box {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-top: 20px;
        font-weight: bold;
    }
    .high-risk {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    .low-risk {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .recommendations {
        background-color: #f8f9fa;
        padding: 15px;
        border-left: 5px solid #dee2e6;
        margin-top: 20px;
    }
    .authors {
        font-size: 0.8em;
        color: #6c757d;
        text-align: center;
        margin-top: 50px;
        border-top: 1px solid #eee;
        padding-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Заголовок
st.markdown("<h2 style='text-align: center;'>Прогноз рецидива миомы матки после органосохраняющего лечения</h2>", unsafe_allow_html=True)
st.markdown("---")

st.subheader("Введите данные пациента")

# Используем колонки для компактности (как в образце)
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Акушерско-гинекологический анамнез**")
    f0 = st.radio("Возраст 42 года и менее", ["Нет", "Да"])
    f1 = st.radio("Длительность заболевания ≥ 7 лет", ["Нет", "Да"])
    f2 = st.radio("Отсутствие родов в анамнезе", ["Нет", "Да"])
    f3 = st.radio("Наружный генитальный эндометриоз", ["Нет", "Да"])
    f4 = st.radio("Ожирение (ИМТ > 25)", ["Нет", "Да"])

with col2:
    st.markdown("**Морфологические и ИГХ данные**")
    f5 = st.radio("Быстрый рост узла (до 6 мес)", ["Нет", "Да"])
    f6 = st.radio("Фибриноидный некроз", ["Нет", "Да"])
    f7 = st.radio("Высокая экспрессия VEGF (>80%)", ["Нет", "Да"])
    f8 = st.radio("Высокая экспрессия TGF-beta (>50%)", ["Нет", "Да"])

# Кнопка расчета
st.markdown("<br>", unsafe_allow_html=True)
if st.button("Рассчитать прогноз"):
    # Перевод "Да/Нет" в 1/0
    inputs = np.array([f0, f1, f2, f3, f4, f5, f6, f7, f8])
    x = np.where(inputs == "Да", 1, 0)
    
    # Математика модели
    weights = np.array([1.25, 0.17, 0.85, 2.13, 2.47, 0.17, 1.48, 1.81, 0.99])
    intercept = -4.5
    z = np.dot(x, weights) + intercept
    prob = 1 / (1 + np.exp(-z))

    # Вывод результата в стиле образца
    if prob >= 0.25:
        st.markdown(f"""
            <div class="result-box high-risk">
                <h2 style='margin:0;'>ВЫСОКИЙ РИСК</h2>
                <p>Вероятность рецидива: {prob:.1%}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="recommendations">
                <h4>Рекомендации:</h4>
                <ul>
                    <li>Динамическое УЗ-наблюдение 1 раз в 3-6 месяцев.</li>
                    <li>Рассмотреть назначение адъювантной гормональной терапии (аГнРГ).</li>
                    <li>Контроль метаболических показателей и коррекция массы тела.</li>
                    <li>Контроль сопутствующего эндометриоза.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="result-box low-risk">
                <h2 style='margin:0;'>НИЗКИЙ РИСК</h2>
                <p>Вероятность рецидива: {prob:.1%}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="recommendations">
                <h4>Рекомендации:</h4>
                <ul>
                    <li>Стандартное диспансерное наблюдение (УЗИ 1 раз в год).</li>
                    <li>Плановая оценка состояния миометрия в декретированные сроки.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# Подвал с авторами
st.markdown(f"""
    <div class="authors">
        © 2025 Ордиянц И.М., Карамян Р.А, Рыженков К.В.<br>
        Все права защищены.
    </div>
    """, unsafe_allow_html=True)
