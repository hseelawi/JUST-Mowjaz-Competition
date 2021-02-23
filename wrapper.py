"""
wrapper class for the classification model
"""
import joblib
from embed_classer import embed
import tensorflow as tf
from tensorflow import keras
from utils import normalize_text
import os
MAX_SENTENCE_LENGTH = 170
EMBEDDING_SIZE = 300


def create_dl_model(max_sentence_len, embedd_size, num_labels=10):
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


class Classifier:
    def __init__(self, vectorizer_path, model_path, dl_vectorizer, dl_model_path):
        """
        initialize the class of the classifier by loading the model.
        Args:
            vectorizer_path(str): represents the path of the vectorizer.
            model_path(str): represents the path of the model, the model should be with extension .pkl.
            dl_vectorizer(str): represents the path of the vectorizer for the deep learning model.
            dl_model_path(str): represents the path of the deep learning model, the model should be with extension
            .hdf5.
        """
        self.vectroizer = joblib.load(vectorizer_path)
        self.model = joblib.load(model_path)
        self.dl_vectorizer = embed(dl_vectorizer)
        self.dl_model = create_dl_model(MAX_SENTENCE_LENGTH, EMBEDDING_SIZE)
        self.dl_model.load_weights(dl_model_path)

    def classify(self, text):
        """
        classify the given text to the appropriate classes "multi class for each text"
        Args:
            text (str): represents text that we want to classify.
        Returns:
            list of 11 items "class" contains 0's and 1's, 1 means you could map the text to this class and 0 means that
            you couldn't map the text to this class.
            [
            'فن ومشاهير',
            'أخبار',
            'رياضة',
            'اقتصاد',
            'تكنولوجيا',
            'اسلام و أديان',
            'سيارات',
            'طقس',
            'منوعات أخرى',
            'صحة',
            'مطبخ'
        ]
        """
        transformed_text = self.vectroizer.transform([text])
        outputs = self.model.predict(transformed_text).tolist()[0]
        return outputs

    def dl_model_classify(self, text, normalize=True):
        """
        classify the given text to the appropriate classes "multi class for each text using the deep learning model"
        Args:
            text (str): represents text that we want to classify.
            normalize(bool): represents a flag if it true we will normalise the text before pass it to the model.
            Default True.
        Returns:
            list of 11 items "class" contains 0's and 1's, 1 means you could map the text to this class and 0 means that
            you couldn't map the text to this class.
            [
            'فن ومشاهير',
            'أخبار',
            'رياضة',
            'اقتصاد',
            'تكنولوجيا',
            'اسلام و أديان',
            'سيارات',
            'طقس',
            'منوعات أخرى',
            'صحة',
            'مطبخ'
        ]
        """
        if normalize:
            text = [normalize_text(text)]

        embedded_text = self.dl_vectorizer.embed_batch(text, MAX_SENTENCE_LENGTH)
        predictions = (self.dl_model.predict(embedded_text) > 0.5).astype(int)
        return predictions.tolist()[0]


# classifier = Classifier("models/tfidf_vectorizer.pkl", "models/svc.sav",
#                         "models/full_uni_sg_300_twitter.mdl", "models/bi_lstm.best.hdf5")
# print(classifier.dl_model_classify("ذهب احمد الي المدرسة"))
# print(classifier.classify("ذهب احمد الي المدرسة"))





