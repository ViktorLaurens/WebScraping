import streamlit as st
from scrape import (scrape_website, 
                    extract_body_content, 
                    clean_body_content, 
                    split_dom_content)

st.title('AI Web Scraper')
url = st.text_input('Enter a website URL: ')

if st.button('Scrape Site'):
    st.write('Scraping...')
    result = scrape_website(url)
    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)
    st.session_state.dom_content = cleaned_content
    with st.expander('View DOM content'):
        st.text_area('DOM content', value=cleaned_content, height=300)
    st.write('Scraping complete!')

if "dom_content" in st.session_state:
    parse_description = st.text_area('Describe what you want to parse:', height=100)
    if st.button('Parse Content'):
        if parse_description: 
            st.write('Parsing...')
            dom_chunks = split_dom_content(st.session_state.dom_content)
            st.write('Parsing complete!')
            