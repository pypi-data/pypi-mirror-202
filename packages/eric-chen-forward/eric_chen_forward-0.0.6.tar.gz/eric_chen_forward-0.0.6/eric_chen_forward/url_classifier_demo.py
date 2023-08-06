from eric_chen_forward import util
import streamlit as st
import pickle
import requests
from bs4 import BeautifulSoup
import pandas as pd
from trafilatura import fetch_url, extract
from trafilatura.settings import use_config
from transformers import AutoTokenizer, BartForConditionalGeneration

def Demo(model_file_path, max_summary_length=100):
    
    with open(model_file_path, 'rb') as f:
        model = pickle.load(f)

    def extract_paragraphs(url):
        config = use_config()
        config.set("DEFAULT", "EXTRACTION_TIMEOUT", "0")
        downloaded = fetch_url(url)
        result = extract(downloaded, config=config, output_format='xml', include_links=True, include_formatting=True)

        soup = BeautifulSoup(result, 'lxml')
        paragraphs = []
        for p in soup.find_all('p'):
            text = p.get_text(strip=True, separator='\n')
            if '.' in text:
                paragraphs.append(text)
        return paragraphs



    title = st.text_input(label="Enter url", placeholder='url')

    tab1, tab2, tab3 = st.tabs(['Paragraph form', 'Passage form', 'Passage form + summarization'])

    bart_model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
    tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")

    if title:
        paragraphs = extract_paragraphs(title)
        passage = ' '.join(paragraphs)
        with tab1:
            for paragraph in paragraphs:
                cleaned_text = util.clean_document(paragraph)
                if len(cleaned_text) == 0:
                    continue
                temp = pd.DataFrame()
                temp['cleaned_text'] = [cleaned_text]
                temp['num_years'] = [util.num_years(paragraph)]
                pred = model.predict(temp[['cleaned_text', 'num_years']])
                
                st.write("Predicted Category: " + pred[0])
                st.write(paragraph)
                st.markdown('''---''')
        with tab2:
            cleaned_text = util.clean_document(passage)
            temp = pd.DataFrame()
            temp['cleaned_text'] = [cleaned_text]
            temp['num_years'] = [util.num_years(passage)]
            pred = model.predict(temp[['cleaned_text', 'num_years']])
            
            st.write("Predicted Category: " + pred[0])
            st.write(passage)
            st.markdown('''---''')
        with tab3:
            inputs = tokenizer([passage], max_length=1024, return_tensors="pt")
            summary_ids = bart_model.generate(inputs["input_ids"], num_beams=2, min_length=0, max_length=max_summary_length)
            summary = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False, truncation=True)[0]
            cleaned_text = util.clean_document(summary)
            temp = pd.DataFrame()
            temp['cleaned_text'] = [cleaned_text]
            temp['num_years'] = [util.num_years(summary)]
            pred = model.predict(temp[['cleaned_text', 'num_years']])
            
            st.write("Predicted Category: " + pred[0])
            st.write(summary)
            st.markdown('''---''')