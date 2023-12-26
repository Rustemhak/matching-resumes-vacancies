import streamlit as st
from model import inference


# Streamlit интерфейс
st.title("Подбор подходящих вакансий и резюме")

# Создание двух форм для ввода текста
vacancy = st.text_area("Текст вакансии")
cv = st.text_area("Текст резюме")

# Кнопка для расчета сходства
if st.button("Рассчитать"):
    similarity = inference.cosine_similarity(vacancy, cv)
    st.write(f"Сходство: {similarity:.2f}")
