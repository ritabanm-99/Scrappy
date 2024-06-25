import streamlit as st
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Function to scrape headings and content from a URL
def scrape_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        return None, None
    
    try:
        soup = BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        st.error(f"Failed to parse content: {e}")
        return None, None
    
    headings = soup.find_all(['h1', 'h2', 'h3'])
    content = soup.find_all('p')
    
    heading_texts = [heading.text.strip() for heading in headings]
    content_texts = [paragraph.text.strip() for paragraph in content]
    
    return heading_texts, content_texts

# Function to generate a word cloud from text
def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    return wordcloud

# Streamlit app
st.title('Webpage Content Scraper and Word Cloud Generator')

# Input URL
url = st.text_input('Enter the URL of the webpage:')

if st.button('Scrape Content'):
    if url:
        headings, content = scrape_content(url)
        if headings and content:
            st.subheader('Headings')
            st.write(headings)
            
            full_text = ' '.join(headings + content)
            
            # Generate and display the word cloud
            st.subheader('Word Cloud of Content')
            wordcloud = generate_wordcloud(full_text)
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            st.pyplot(plt)
    else:
        st.error("Please enter a URL.")
