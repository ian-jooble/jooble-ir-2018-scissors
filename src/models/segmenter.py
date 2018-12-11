"""Segmenter package contains model Segmenter that finds the text segments
that relate to the requirements or responsibilities"""

import numpy as np
from keras.preprocessing import sequence
from keras.models import model_from_json
from keras.models import load_model


class Segmenter:

    def __init__(self, vectorizer):
        self.name = "Segmenter"

        self.encoder_model = load_model('encoder_model.json',
                                        'encoder_model_weights.h5')
        self.decoder_model = load_model('decoder_model.json',
                                        'decoder_model_weights.h5')

        self.num_decoder_tokens = 2
        self.max_decoder_seq_length = 200
        self.max_len = 200
        self.vectorizer = vectorizer

    def load_model(self, model_filename, model_weights_filename):
        with open(model_filename, 'r', encoding='utf8') as f:
            model = model_from_json(f.read())
        model.load_weights(model_weights_filename)
        return model

    def decode_sequence(self, input_seq):
        # Encode the input as state vectors.
        states_value = self.encoder_model.predict(input_seq)

        # Generate empty target sequence of length 1.
        target_seq = np.zeros((1, 1, self.num_decoder_tokens))
        target_seq[0, 0, 0] = 1.

        # Sampling loop for a batch of sequences
        stop_condition = False
        decoded_sentence = []
        while not stop_condition:
            output_tokens, h, c = self.decoder_model.predict([target_seq] + states_value)

            # Sample a token
            sampled_token_index = np.argmax(output_tokens[0, -1, :])
            decoded_sentence.append(sampled_token_index)

            # Exit condition: either hit max length
            if len(decoded_sentence) >= self.max_decoder_seq_length:
                stop_condition = True

            # Update the target sequence (of length 1).
            target_seq = np.zeros((1, 1, self.num_decoder_tokens))
            target_seq[0, 0, sampled_token_index] = 1.

            # Update states
            states_value = [h, c]
        return decoded_sentence


    def get_training_sample(self, vect, text):
        """
        Gets 1 sample of training data

        :param  vectorizer w2v vect:
        :param str text:
        """
        tagged_list = text.split(" ")

        vec_list = []
        # converting word2vec
        for word in tagged_list:
            try:
                vec_list.append(vect[word])
            except:
                # print("Word " + word + " isn't in vocab. Embeding as zeros")
                vec_list.append(np.zeros(300))
        return vec_list

    def get_sample_nonlabeled(self, text):
        """

        :param text:
        :return:
        """

        x_sample = self.get_training_sample(self.vectorizer, text)
        x_sample = sequence.pad_sequences([x_sample], maxlen=self.max_len,
                                          dtype='float', padding="post",
                                          truncating="post")
        x_sample = np.array(x_sample)
        return x_sample

    def segmantation(self, text_norm):
        text_vect = self.get_sample_nonlabeled(text_norm)
        decoded_sequence = self.decode_sequence(text_vect)

        return decoded_sequence
