import streamlit as st
import requests

def show_financial_news():
    st.subheader("🗞️ Latest Financial News")

    api_key = st.secrets["NEWS_API_KEY"]
    url = f"https://newsapi.org/v2/top-headlines?category=business&language=en&apiKey={api_key}"

    response = requests.get(url)
    if response.status_code != 200:
        st.error("Failed to fetch news.")
        return

    articles = response.json().get("articles", [])

    for article in articles[:5]:
        st.markdown(f"### [{article['title']}]({article['url']})")
        st.write(article['description'])
