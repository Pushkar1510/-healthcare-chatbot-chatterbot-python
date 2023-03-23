# importing the libraries
from http.client import ResponseNotReady
import json
import pickle
import random
import string

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import tensorflow as tf
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from tensorflow.keras.layers import (LSTM, Dense, Embedding, Flatten,
                                     GlobalMaxPooling1D, Input)
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

def disease_prediction(symptoms):
    df1 = pd.read_csv(
        "./Symptom-severity.csv")
    columns = ['Symptom_1', 'Symptom_2', 'Symptom_3', 'Symptom_4',
               'Symptom_5', 'Symptom_6', 'Symptom_7', 'Symptom_8', 'Symptom_9',
               'Symptom_10', 'Symptom_11', 'Symptom_12', 'Symptom_13', 'Symptom_14',
               'Symptom_15', 'Symptom_16', 'Symptom_17']
    df = pd.DataFrame(columns=columns)
    data = [0] * 17
    input_list = symptoms
    for element, i in zip(input_list, range(len(input_list))):
        data[i] = element
    df.loc[len(df)] = data
    df.isna().sum()
    df.isnull().sum()

    cols = df.columns
    data = df[cols].values.flatten()

    s = pd.Series(data)
    #s = s.str.strip()
    s = s.values.reshape(df.shape)

    df = pd.DataFrame(s, columns=df.columns)

    df = df.fillna(0)
    vals = df.values
    symptoms = df1['Symptom'].unique()

    for i in range(len(symptoms)):
        vals[vals == symptoms[i]] = df1[df1['Symptom']
                                        == symptoms[i]]['weight'].values[0]

    d = pd.DataFrame(vals, columns=cols)

    d = d.replace('dischromic _patches', 0)
    d = d.replace('spotting_ urination', 0)
    df = d.replace('foul_smell_of urine', 0)

    filename = 'disease_prediction.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    preds = loaded_model.predict(df)

    return preds

def disease_analysis(pred):
    df = pd.read_csv(
        './disease_Description.csv')
    disease_description = df[df['Disease'] == pred]['Description']
    # st.subheader('Disease description:')
    # st.write(disease_description.values[0])
    df1 = pd.read_csv(
        './disease_precaution.csv')
    disease_precaution = df1[df1['Disease'] == pred]
    disease_precaution.dropna(axis=1,inplace=True)
    disease_precaution = disease_precaution.iloc[0].to_numpy()[1:]
    # st.subheader('Disease precaution:')
    # for element in disease_precaution:
    #     st.write(element)

    # print("Disease Description:")
    # print(disease_description.values[0])
    # print("Disease Precaution")
    for element in disease_precaution:
        print(element)
    
    prec = ",".join(disease_precaution)
    respstr = "Disease: "+pred+"\n\nDisease Description: "+disease_description.values[0]+"\n\nDisease Precaution: "+prec
    return respstr

#options is list of symptoms
def symptom_extractor(options):
    pred = disease_prediction(options)
    # st.subheader('Disease predicted:', pred[0])
    # st.write(pred[0])
    respstr = disease_analysis(pred[0])
    return respstr

# ans = symptom_extractor(['skin_rash', 'itching'])
# print("#############################")
# print(ans)
# print("#############################")
