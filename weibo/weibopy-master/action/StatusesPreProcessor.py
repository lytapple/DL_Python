import jieba
#import nltk
import re

#import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt


def hasEmotionalWords(text):
    emotion_dict = pd.read_csv('../emotion_dict.csv', index_col='words')
    words = jieba.cut(text)

    words_list = [w.encode('utf-8') for w in words]
    print ','.join(words_list)

    return True in emotion_dict.index.isin(words_list)


class StatusesPreProcessor:
    @staticmethod
    def process(statuses):
        # hasURL
        pattern = re.compile(r'http://[\w./]+')
        statuses['hasURL'] = statuses['text'].map(lambda text:
                                                  bool(pattern.search(text)))
        # isTextPicMix
        statuses['isTextPicMix'] = statuses['bmiddle_pic'].notnull()
        # hasAt
        pattern = re.compile(r'(?<!\\)@')
        statuses['hasAt'] = statuses['text'].map(lambda text:
                                                 bool(pattern.search(text)))
        # isRetweet
        statuses['isRetweet'] = statuses['retweetOfId'].notnull()
        # hasQuestionMark
        statuses['hasQuestionMark'] = statuses['text'].map(
            lambda text: '!' in text)
        # hasExclamationMark
        statuses['hasExclamationMark'] = statuses['text'].map(
            lambda text: '?' in text)
        # hasTopic
        pattern = re.compile(r'#.{1,30}#')
        statuses['hasTopic'] = statuses['text'].map(lambda text:
                                                    bool(pattern.search(text)))
        # hasBraket
        pattern = re.compile(r'【.{1,60}】')
        statuses['hasBraket'] = statuses['text'].map(
            lambda text: bool(pattern.search(text)))
        # cascadeNum
        statuses['cascadeNum'] = statuses['text'].map(
            lambda text: text.count(r'\\@'))
        # hasEmotionalWords
        statuses['hasEmotionalWords'] = statuses['text'].map(hasEmotionalWords)
        # UC
        # users = pd.read_csv('../sample/users.csv',index_col='userid')
        # statuses['UC'] = statuses['userid'].map(
        #     lambda ids : users.ix[ids, 'credibility'])

# read data
raw_statuses1 = pd.read_csv('../sample/final/statuses-uc-dd.csv', index_col=0)
raw_statuses2 = pd.read_csv('../sample/final/statuses-uc-dd2.csv', index_col=0)
StatusesPreProcessor.process(raw_statuses1)
StatusesPreProcessor.process(raw_statuses2)

raw_statuses1.columns
raw_statuses1.head()
raw_statuses2.head()

raw_statuses2.columns
#raw_statuses.ix[:, -10:].apply(pd.value_counts)

# select columns to train
columns = {'reposts_count': 'repostsCount', 'comments_count': 'commentsCount'}
raw_statuses1.rename(columns=columns, inplace=True)
raw_statuses2.rename(columns=columns, inplace=True)
raw_statuses2.rename(columns={'credibility': 'IC'}, inplace=True)
statuses1 = raw_statuses1.ix[:, ['hasURL', 'isTextPicMix', 'hasEmotionalWords',
                                 'hasAt', 'isRetweet', 'hasQuestionMark',
                                 'hasExclamationMark', 'hasTopic', 'hasBraket',
                                 'cascadeNum', 'repostsCount', 'commentsCount',
                                 'UC', 'IC']]
statuses2 = raw_statuses2.ix[:, ['hasURL', 'isTextPicMix', 'hasEmotionalWords',
                                 'hasAt', 'isRetweet', 'hasQuestionMark',
                                 'hasExclamationMark', 'hasTopic', 'hasBraket',
                                 'cascadeNum', 'repostsCount', 'commentsCount',
                                 'UC', 'IC']]
statuses1.columns
statuses1.head()
statuses2.head()
statuses2.columns

# merge data and show distribution of IC
statuses = pd.concat([statuses1, statuses2], ignore_index=True)
statuses.head()
statuses.describe()
statuses.notnull()
statuses['IC'].value_counts().plot(kind='barh')

# probe the inter relationship between UC and IC
users_statuses = statuses[['UC', 'IC']]
users_statuses.columns
users_statuses.plot(kind='scatter')

# SVC
from sklearn import svm

clf = svm.SVC()
clf.fit(statuses.ix[:, :-1], statuses.ix[:, -1])

# metrics
predicted = clf.predict(statuses.ix[:, :-1])
predicted
from sklearn import metrics
print metrics.classification_report(statuses.ix[:, -1],  predicted)
print metrics.confusion_matrix(statuses.ix[:, -1], predicted)

# DecisionTree
from sklearn.tree import DecisionTreeClassifier
from sklearn import cross_validation
from sklearn.cross_validation import train_test_split
from sklearn import metrics
X_train, X_test, y_train, y_test = train_test_split(statuses.ix[:, :-2],
                                                    statuses.ix[:, -1],
                                                    test_size=0.25)
clf = DecisionTreeClassifier()
scores = cross_validation.cross_val_score(clf, X_train, y_train, cv=3)
scores
scores.mean()
scores.std()
clf = clf.fit(X_train, y_train)
predicted = clf.predict(X_test)
print metrics.classification_report(y_test, predicted)
print metrics.confusion_matrix(y_test, predicted)

# Naive Bayes
from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()
