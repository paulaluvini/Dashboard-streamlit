#!/usr/bin/env python
# coding: utf-8
import streamlit as st
import pandas as pd
import requests

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
select = st.sidebar.selectbox('Seleccione', ['Longitud de emails', 'Nube de Palabras'], key='1')

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
largo = emails_df["length"]


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
                comment_words = '' 
                stopwords = set(STOPWORDS)
                #stopwords = set(stopwords.words('english')) 
                for val in emails_df['emails']: 
                    # typecaste each val to string 
                    val = str(val) 
                    # split the value 
                    tokens = val.split() 
                    # Converts each token into lowercase 
                    for i in range(len(tokens)):
                        tokens[i] = tokens[i].lower() 
                    comment_words += " ".join(tokens)+" "
                wordcloud = WordCloud(width = 1000, height = 800, background_color ='black', colormap = "Pastel1",
                        stopwords = stopwords, min_font_size = 20).generate(comment_words) 
                plt.figure(figsize = (8, 8), facecolor = None) 
                plt.title("Palabras más importantes", size = 24)
                plt.imshow(wordcloud) 
                plt.axis("off") 
                plt.tight_layout(pad = 0) 
                st.pyplot()

