import streamlit as st
import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import pickle
import os
import cv2
from streamlit_drawable_canvas import st_canvas
st.set_option('deprecation.showPyplotGlobalUse', False)



@st.cache(show_spinner=False)
def load_datasets():
    df = pd.read_csv('../MNIST/train.csv')
    y = df['label']
    df.drop('label', axis=1, inplace=True)
    df_test = pd.read_csv('../MNIST/test.csv')
    return df, y, df_test

@st.cache(allow_output_mutation=True, show_spinner=False)
def load_classifier():
    with open('RandomForestClassifier.plk', 'rb') as file:
        clf = pickle.load(file)
    return clf

def show_feature_importance(clf):
    plt.imshow(clf.feature_importances_.reshape(28,28), cmap='hot')
    st.pyplot()

def show_plt_image(df_test, index_to_predict):    
    plt.imshow(np.uint8(df_test.iloc[index_to_predict].tolist()).reshape(28,28))
    st.pyplot()

def show_image(df_test, index_to_predict):    
    st.image(np.uint8(df_test.iloc[index_to_predict].tolist()).reshape(28,28), use_column_width=True)

# Fetch data
df, y, df_test = load_datasets()

clf = load_classifier()


# Sidebar

st.sidebar.header('Parámetros de entrenamiento')

n_estimators = st.sidebar.slider('Cantidad de árboles', 1, 400, 100, 1, '%d')
min_samples_leaf = st.sidebar.slider('Cantidad mínima de muestras en una hoja', 1, 30, 1, 1, '%d')
max_samples = st.sidebar.slider('Cantidad de muestras a usar', 1, 42000, 42000, 1, '%d')

if st.sidebar.button('Entrenar'):
    clf = RandomForestClassifier(n_estimators=n_estimators, min_samples_leaf=min_samples_leaf, max_samples=max_samples)
    clf.fit(df, y)
    with open('RandomForestClassifier.plk', 'wb') as file:
        pickle.dump(clf, file)
    st.balloons()

st.sidebar.subheader('Clasificación')
index_to_predict = st.sidebar.number_input("Muestra a clasificar", min_value=0, max_value=27999, value=312)


# Main layout
st.title('Udesa-mnist streamlit app')

st.subheader('Feature importance')
st.write('Mapa de calor de la importancia de los píxeles en el clasificador actual')
show_feature_importance(clf)


st.subheader('Muestra a clasificar')
st.write('Mostrando la imagen a clasificar con matplotlib')
show_plt_image(df_test, index_to_predict)

st.write('Mostrando la imagen a clasificar con streamlit')
show_image(df_test, index_to_predict)

label_predicted = clf.predict(df_test.iloc[[index_to_predict]])[0]
st.subheader('Predicción')
st.write('La muestra elegida fue clasificada como: ' + str(label_predicted))



st.header('Reconociendo un dígito escrito a mano')

column_1, column_2 = st.beta_columns(2)

with column_1:
    SIZE = 192
    mode = st.checkbox("Draw (or Delete)?", True)
    canvas_result = st_canvas(
        fill_color='#000000',
        stroke_width=20,
        stroke_color='#FFFFFF',
        background_color='#000000',
        width=SIZE,
        height=SIZE,
        drawing_mode="freedraw" if mode else "transform",
        key='canvas')

with column_2:
    if canvas_result.image_data is not None:
        img = cv2.resize(canvas_result.image_data.astype('uint8'), (28, 28))
        rescaled = cv2.resize(img, (SIZE, SIZE), interpolation=cv2.INTER_NEAREST)
        st.write('Model Input')
        st.image(rescaled)

if st.button('Clasificar'):
    test_x = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    val = clf.predict(test_x.reshape(1, 784))[0]
    st.write(f'result: {val}')
