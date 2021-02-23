import re

import tensorflow as tf
from tensorflow import keras

import pyarabic.araby as araby


def create_model(max_sentence_len, embedd_size, num_labels=10):
    sentence = keras.Input(shape=(max_sentence_len, embedd_size), name='sentence')
    label = keras.Input(shape=(num_labels,), name='label')
    forward_layer = keras.layers.LSTM(embedd_size)
    backward_layer = keras.layers.LSTM(embedd_size, go_backwards=True)
    rnn = keras.layers.Bidirectional(forward_layer, backward_layer=backward_layer)
    logits = rnn(sentence)
    logits = keras.layers.Dense(embedd_size, activation=tf.nn.sigmoid)(logits)
    logits = keras.layers.Dense(num_labels, activation=tf.nn.sigmoid)(logits)
    model = keras.Model(sentence, outputs=logits)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    
    return model


def normalize_text(text):
    text = text.strip()
    text = araby.strip_tashkeel(text)
    text = ' '.join(araby.tokenize(text))
    
    # remove extra spaces
    text = re.sub(' +', ' ', text)
    # remove html tags
    text = re.sub(re.compile('<.*?>'), ' ', text)
    # remove twitter usernames, web addresses
    text = re.sub(r"#[\w\d]*|@[.]?[\w\d]*[\'\w*]*|https?:\/\/\S+\b|"
                                              r"www\.(\w+\.)+\S*|", '', text)
    # strip repeated chars (extra vals)
    text = re.sub(r'(.)\1+', r"\1\1", text)
    # separate punctuation from words and remove not included marks
    text = " ".join(re.findall(r"[\w']+|[?!,;:]", text))
    # remove underscores
    text = text.replace('_', ' ')
    # remove double quotes
    text = text.strip('\n').replace('\"', '')
    # remove single quotes
    text = text.replace("'", '')
    # remove numbers
    text = ''.join(i for i in text if not i.isdigit())
    # remove extra spaces
    text = re.sub(' +', ' ', text)
    return text