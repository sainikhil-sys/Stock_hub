import streamlit as st
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

def chat_with_ai():
    st.subheader("💬 Ask the AI Assistant")

    user_input = st.text_input("Type your market-related question here...")

    if user_input:
        with st.spinner("Thinking..."):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a financial assistant that provides clear, reliable stock market insights."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response['choices'][0]['message']['content'])
