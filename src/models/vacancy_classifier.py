import os
import re
import pickle

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression


class Classifier:

    labels = ['информационные технологии,'
              ' интернет, телеком',
              'строительство, недвижимость',
              'спортивные клубы, фитнес, салоны красоты',
              'маркетинг, реклама, pr',
              'медицина, фармацевтика',
              'консультирование',
              'бухгалтерия, управленческий учет, финансы предприятия',
              'рабочий персонал',
              'наука, образование',
              'автомобильный бизнес',
              'управление персоналом, тренинги',
              'транспорт, логистика',
              'производство',
              'туризм, гостиницы, рестораны',
              'продажи',
              'юристы', 'банки, инвестиции, лизинг',
              'административный персонал',
              'начало карьеры, студенты',
              'искусство, развлечения, масс-медиа']
    saved_path = os.path.join("saved_models", "classifiers.dat")

    def __init__(self, vect_path=os.path.join("classifier_train_data",
                                              "vectorizer_tfidf.dat"),
                 train_path=os.path.join("classifier_train_data",
                                         "hh_dataset_all_uniq_text.csv"),
                 load=False, save=False):
        """
        :param vect_path:
        :param train_path:
        :param bool load: if True, load classifiers from file
        """
        self.name = "Vacancy classifier"
        self.classifiers = {}
        with open(vect_path, "rb") as inf:
            self.vectorizer_tfidf = pickle.load(inf)
        self.train = pd.read_csv(train_path, sep="\t")

        if load:
            with open(Classifier.saved_path, "rb") as inf:
                self.classifiers = pickle.load(inf)
        else:
            self.classifiers = self.train_classifiers(save=save)

    def train_classifiers(self, save):
        X, Y = self.prepare_data()
        counts = []
        for i in range(len(Classifier.labels)):
            print(i, ' Label {} appears {} times'.format(Classifier.labels[i],
                                                         np.sum(Y[:, i])))
            counts.append(np.sum(Y[:, i]))

        classifiers = {}
        for i in range(len(Classifier.labels)):
            num_pos = np.sum(Y[:, i])
            num_neg = len(Y[:, i]) - num_pos
            sample_weights = np.ones(Y[:, i].shape)
            sample_weights[Y[:, i] == 1] = num_neg / num_pos
            y_train_for_label = Y[:, i]

            new_classifier = LogisticRegression()
            new_classifier.fit(X, y_train_for_label, sample_weight=sample_weights)
            classifiers[Classifier.labels[i]] = new_classifier
            print("Training for class ", i, Classifier.labels[i],
                  "... Weight for class =", num_neg / num_pos)

        if save:
            with open(Classifier.saved_path, "wb") as ouf:
                pickle.dump(classifiers, ouf)
        return classifiers

    def prepare_data(self):
        n_classes = len(Classifier.labels)
        n_examples = len(self.train)
        Y = np.zeros((n_examples, n_classes))
        corpus = [text for text in self.train.loc[:, "text_normalized"]]
        X = self.vectorizer_tfidf.transform(corpus)

        for i, row in self.train.iterrows():
            specs = row["profarea_names"].lower()
            specs = specs.split("', ")
            for spec in specs:
                spec = re.sub('[\[\'\]]', '', spec)
                if spec in Classifier.labels:
                    pos = Classifier.labels.index(spec.strip())
                    Y[i][pos] = 1

        assert (X.shape[0] == Y.shape[0])
        return X, Y

    def predict(self, text):
        """

        :param str text:
        :return: list of str predictions:
        """
        text_vect = self.vectorizer_tfidf.transform([text])
        predictions = []
        for i, label in enumerate(Classifier.labels):
            predict = self.classifiers[label].predict(text_vect)
            if predict == 1:
                predictions.append(label)

        return predictions


# classif = Classifier(load=True)
# print(classif.predict(text="менеджмент продаж водител"))
