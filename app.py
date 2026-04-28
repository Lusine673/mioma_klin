import streamlit as st
import math

st.set_page_config(page_title="Клинический прогноз рецидива ЛМ", layout="centered")

st.title("📊 Клиническая модель прогноза рецидива лейомиомы")
st.markdown("Модель построена на основании OR из резюме диссертации")

st.divider()

# --- Ввод данных ---
vozrast = st.number_input("Возраст пациентки (лет)", 18, 50, 40)
dlit = st.radio("Длительность заболевания ≥ 7 лет", ["Нет", "Да"])
rody = st.radio("Роды в анамнезе", ["Да", "Нет"])
nzo = st.radio("Нарушение жирового обмена (ИМТ >25)", ["Нет", "Да"])

# --- Кодирование ---
X_age = 1 if vozrast <= 42 else 0
X_dlit = 1 if dlit == "Да" else 0
X_rody = 1 if rody == "Нет" else 0   # 1 = отсутствие родов
X_nzo = 1 if nzo == "Да" else 0

if st.button("Рассчитать риск"):

    Z = (
        -0.80
        + 1.16 * X_age
        + 1.18 * X_dlit
        + 1.47 * X_rody
        + 0.29 * X_nzo
    )

    P = 1 / (1 + math.exp(-Z))

    st.subheader("Результат")

    st.metric("Вероятность рецидива", f"{P*100:.1f}%")
    st.write(f"Логит (Z) = {Z:.2f}")

    if P < 0.30:
        st.success("🟢 Низкий риск")
    elif P < 0.60:
        st.warning("🟡 Умеренный риск")
    else:
        st.error("🔴 Высокий риск")

    st.progress(P)

    st.caption("Модель реконструирована на основании опубликованных OR.")
