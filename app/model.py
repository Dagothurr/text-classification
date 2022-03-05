from tensorflow.keras.models import Sequential
from tensorflow.keras import models
from tensorflow.keras.layers import Dense, Embedding, MaxPooling1D, Dropout, LSTM, Bidirectional, SpatialDropout1D
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.metrics import AUC

import nltk
from nltk.corpus import stopwords
from spacy.lang.ru import Russian

import requests
import json
import random
import string
import time
import numpy as np
import pickle
import re

model_lstm_path = 'model_lstm.h5'
tokenizer_pickle_path = 'tokenizer.pickle'

num_words = 10000
max_comment_len = 20

classes = ["normal", "insult", "threat", "obscenity"]

model_lstm = models.load_model(model_lstm_path)

with open(tokenizer_pickle_path, 'rb') as handle:
    tokenizer = pickle.load(handle)

def delete_emoji(text):
    regrex_pattern = re.compile(pattern="["
        u"\U0001F600-\U0001F64F"                    # emoticons
        u"\U0001F300-\U0001F5FF"                    # symbols & pictographs
        u"\U0001F680-\U0001F6FF"                    # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"                    # flags (iOS)
                        "]+", flags=re.UNICODE)
    return regrex_pattern.sub(r' ', text)

nlp = Russian()

def lemmatization(text):                               
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc]
    return " ".join(tokens)
w_tokenizer = nltk.tokenize.WhitespaceTokenizer()

def tokenize_and_lemmatize_text(text):                  
    return [lemmatization(w) for w in w_tokenizer.tokenize(text)]

def remove_punctuation(text):
    punctuationfree = "".join([i for i in text if i not in string.punctuation])
    return punctuationfree

def remove_stopwords(text):
    filtered_text = []
    for w in text:
        if w not in stopwords:
            filtered_text.append(w)
    return filtered_text

def predict(text):
    message = delete_emoji(text.replace(',', '')).split(" ")
    lower_message = ' '.join(message).lower()
    removed_punctuation = remove_punctuation(lower_message)

    lemmatized_message = tokenize_and_lemmatize_text(removed_punctuation)
    sequence = tokenizer.texts_to_sequences([lemmatized_message])
    data = pad_sequences(sequence, maxlen=max_comment_len)

    result = model_lstm.predict(data)
    predictions = np.argwhere(result[0] > 0.25).tolist()
    count_of_pred_classes = len(predictions)
    output_classes = ""
    i = 0
    while (count_of_pred_classes > 0):
        output_classes = output_classes + classes[predictions[i][0]] + " "
        i += 1
        count_of_pred_classes -= 1

    #output = "Текст: " + text + "\nКласс: " + str(output_classes) + "\nЛеммы: " + str(lemmatized_message) + "\nСкоры: " + str(result)

    appDict = {
       'text': text,
       'class': "Классы: " + str(output_classes),
       'lemmas': "Леммы: " + str(lemmatized_message),
       'scores_normal': "normal: " + str(result[0][0]),
       'scores_insult': "insult: " + str(result[0][1]),
       'scores_threat': "threat: " + str(result[0][2]),
       'scores_obscenity': "obscenity: " + str(result[0][3])
    }
    #output = json.dumps(appDict, ensure_ascii=False)
    output = appDict
    return output