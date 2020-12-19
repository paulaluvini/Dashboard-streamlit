#!/usr/bin/env python
# coding: utf-8
import streamlit as st
import pandas as pd
import requests

st.markdown(
            """
            <style>
            .css-1aumxhk.e1fqkh3o1 {
                    background-image: linear-gradient(#00B7BD,#00B7BD);
                            color: white
                            }
                    </style>
                    """,
                        unsafe_allow_html=True,
                        )

URL_LOGIN = 'http://miweb-dev22.us-east-1.elasticbeanstalk.com/api-token-auth/'
data = {'username':'facundoprueba','password':'Palmera01'}
res_request_login = requests.post(URL_LOGIN, data)

import json
token = json.loads(res_request_login.content.decode('utf-8'))['token']
headers = { 'Authorization': f'JWT {token}' }

res_request_email = requests.get('http://miweb-dev22.us-east-1.elasticbeanstalk.com/query/',headers=headers)
query = json.loads(res_request_email.text)

emails = []
n = len(query)-1

for i in range(0,n):
    emails.append(query[i]['text'])
    
emails_df = pd.DataFrame(emails)
emails_df.columns = ["emails"]
emails_df['length'] = emails_df['emails'].apply(len)

# Sidebar
st.sidebar.title("Dashboard con Métricas de API:")
st.sidebar.title("Métricas")
select = st.sidebar.selectbox('Seleccione', ['Longitud de emails', 'Nube de Palabras', 'Palabras más frecuentes'],
        key='1')

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from collections import Counter  
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize  

largo = emails_df["length"]
comment_words = ''
stopwords = set(STOPWORDS)
stopwords.add('subject')
stopwords.add('Subject')
stopwords.add('re')
for val in emails_df['emails']:
    val = str(val)
    # split the value
    tokens = val.split()
    # Converts each token into lowercase
    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()
    comment_words += " ".join(tokens)+" "
wordcloud = WordCloud(width = 1000, height = 800,background_color ='black',colormap = "Pastel1",\
        stopwords = stopwords, min_font_size = 20).generate(comment_words) 

punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
# remove punctuation from the string
no_punct = ""
for char in comment_words:
    if char not in punctuations:
        no_punct = no_punct + char
        # display the unpunctuated string
comment_words = no_punct
word_tokens = word_tokenize(comment_words)
filtered_sentence = [w for w in word_tokens if not w in stopwords]
filtered_sentence = []
for w in word_tokens:
    if w not in stopwords:
        filtered_sentence.append(w)
comment_words = filtered_sentence
# Pass the split_it list to instance of Counter class.
Counter = Counter(comment_words)
most_occur = Counter.most_common(10)
palabra = []
cantidad= []
for i in range(10):
    palabra.append(most_occur[i][0])
    cantidad.append(most_occur[i][1])
mas_frecuentes = pd.DataFrame()
mas_frecuentes['palabra'] = palabra
mas_frecuentes['cantidad'] = cantidad


st.title("Clasificación de emails en Spam y Ham")
if select == 'Longitud de emails':
                fig, ax = plt.subplots(figsize = (6,4))
                # Plots ## Plot histogram
                largo.plot(kind = "hist", density = True, bins = 15) # change density to true, because KDE uses density
                # Plot KDE
                largo.plot(kind = "kde")
                # X #
                ax.set_xlabel("Cantidad de palabras")
                # Remove y ticks
                ax.set_yticks([])
                # Relabel the axis as "Frequency"
                ax.set_ylabel("Frequency")
                # Overall #
                ax.set_title("Longitud de emails consultados")
                # Remove ticks and spines
                ax.tick_params(left = False, bottom = False)
                for ax, spine in ax.spines.items():
                    spine.set_visible(False)
                st.set_option('deprecation.showPyplotGlobalUse', False)
                st.pyplot()
if select == 'Nube de Palabras':
                plt.figure(figsize = (8, 8), facecolor = None) 
                plt.title("Palabras más importantes", size = 24)
                plt.imshow(wordcloud) 
                plt.axis("off") 
                plt.tight_layout(pad = 0) 
                st.pyplot()
if select == 'Palabras más frecuentes':
    st.header("Las 10 palabras más frecuentes")
    st.table(mas_frecuentes.assign(hack='').set_index('hack'))
