import pandas as pd
import matplotlib.pyplot as plt


class UsersPreProcessor:
    users = None

    @staticmethod
    def authenticityGen(users):
        handler = lambda x: int(x)
        users['gender'] = users['gender'].replace({'m': 0, 'f': 1})
        users['hasDesc'] = users['description'].notnull().map(handler)
        users['hasDomain'] = users['user_domain'].notnull().map(handler)
        users['hasWeihao'] = users['weihao'].notnull().map(handler)
        users['wage'] = users['ucreate_at'].map(lambda s: 2015 - int(s[-4:]))

    @staticmethod
    def authorityGen(users):
        users['FoPd'] = users['followers_count'] / (365 * (users['wage'] + 1))
        users['FrFo'] = (users['friends_count'] + 1) / (
            users['followers_count'] + 1)
        users['BiFo'] = (users['bi_followers_count'] + 1) / \
            (users['followers_count'] + 1)
        users['BiFr'] = (users['bi_followers_count'] + 1) / \
            (users['friends_count'] + 1)
        users['StPd'] = users['statuses_count'] / (365 * (users['wage'] + 1))
        users['FavPm'] = users['favourites_count'] / (12 * (users['wage'] + 1))

    @classmethod
    def process(cls, users):
        cls.authenticityGen(users)
        cls.authorityGen(users)

    @classmethod
    def load_users(cls, ufilename):
        raw_users = pd.read_csv(ufilename, index_col=0)
        cls.process(raw_users)
        # select columns to train
        cls.users = raw_users.ix[:, ['hasDesc', 'hasDomain', 'hasWeihao',
                                     'gender', 'allow_all_act_msg',
                                     'geo_enabled', 'allow_all_comment',
                                     'verified', 'wage', 'FoPd', 'StPd',
                                     'FavPm', 'FrFo', 'BiFo', 'BiFr',
                                     'credibility']]
        columns = {'allow_all_act_msg': 'allowAllMsg',
                   'geo_enabled': 'allowGeo',
                   'allow_all_comment': 'allowAllComment'}
        cls.users.rename(columns=columns, inplace=True)
        return cls.users


# read data
raw_users0 = pd.read_csv('../sample/users00.1-m.csv', index_col=0)
raw_users1 = pd.read_csv('../sample/users01.2-m.csv', index_col=0)
raw_users2 = pd.read_csv('../sample/users02.2-m.csv', index_col=0)
raw_users3 = pd.read_csv('../sample/users03.2-m.csv', index_col=0)

# merge data and prepocess
raw_users = pd.concat([raw_users0, raw_users1, raw_users2, raw_users3],
                      ignore_index=True)
UsersPreProcessor.process(raw_users)

# show distribution of users credibility
raw_users['credibility'].value_counts().plot(kind='barh')

# select columns to train
users = raw_users.ix[:, ['hasDesc', 'hasDomain', 'hasWeihao', 'gender',
                         'allow_all_act_msg', 'geo_enabled',
                         'allow_all_comment', 'verified', 'wage',
                         'FoPd', 'StPd', 'FavPm', 'FrFo', 'BiFo',
                         'BiFr', 'credibility']]
columns = {'allow_all_act_msg': 'allowAllMsg', 'geo_enabled': 'allowGeo',
           'allow_all_comment': 'allowAllComment'}
users.rename(columns=columns, inplace=True)

users.columns
users.head()
users.shape


from sklearn import preprocessing
users_standardization = preprocessing.scale(users.ix[:, -1])
users_standardization

# probe features ability to distinguish

raw_authenticity = [[333./1137., 411./1059., 1353./117., 1268./202.,
                    1309./161., 843./627., 961./509.],
                    [49./27., 67./9., 20./56., 56./20., 67./9.,
                     71./5., 62./19.]]
df = pd.DataFrame(
    raw_authenticity,
    columns=['hasDomain', 'hasWeihao', 'allowMsg',
             'allowGeo', 'allowComment', 'hasDesc', 'gender'],
    index=['not verified', 'verified'])
df.T.plot(kind='bar', stacked=True)

authenticity_cols = ['hasDesc', 'hasDomain', 'hasWeihao', 'gender',
                     'allowAllMsg', 'allowGeo', 'allowAllComment',
                     'verified', 'hasVerifiedReason', 'wage']
authority_cols = ['FoPd', 'StPd', 'FavPm', 'BiFo', 'credibility']
users[authenticity_cols].plot(kind='box')
users[authority_cols].plot(kind='box')

users['credibility'] = users['credibility'].apply(
    lambda x: [1 if x == 0 or x == 1 else 2][0])
users.head()
users.boxplot(by='credibility')

from pandas.tools.plotting import parallel_coordinates
from pandas.tools.plotting import radviz

plt.figure()
radviz(users, 'credibility')
parallel_coordinates(users, 'credibility')

# SVC
from sklearn import svm

clf = svm.SVC()
clf.fit(users.ix[:, :-1], users.ix[:, -1])
predicted = clf.predict(users.ix[:, :-1])
predicted.shape

from sklearn import metrics

print metrics.classification_report(users.ix[:, -1].astype(int), predicted)
print metrics.confusion_matrix(users.ix[:, -1], predicted)


# preprocessing and gridsearchCV with SVC
from sklearn.decomposition import RandomizedPCA
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVC

pca = RandomizedPCA(n_components=12)
pca.fit(users.ix[:, :-1])


X_train, X_test, y_train, y_test = train_test_split(
    users.ix[:, :-1], users.ix[:, -1], test_size=0.30)
users_train_pca = pca.transform(X_train)

param_grid = {'C': [1e3, 5e3, 1e4, 5e4, 1e5],
              'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1]}
clf = GridSearchCV(SVC(kernel='rbf', class_weight='auto'), param_grid)
clf = clf.fit(users_train_pca, y_train)
clf.best_estimator_
clf.best_score_

predicted = clf.predict(pca.transform(X_test))
print metrics.classification_report(y_test, predicted)
print metrics.confusion_matrix(y_test, predicted)


# Bayes
from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()
clf = clf.fit(users_train_pca, y_train)

# Desicion Tree
from sklearn.tree import DecisionTreeClassifier
from sklearn import cross_validation
from sklearn.cross_validation import train_test_split
from sklearn import metrics
X_train, X_test, y_train, y_test = train_test_split(
    users.ix[:, :-1], users.ix[:, -1], test_size=0.25)
clf = DecisionTreeClassifier()
scores = cross_validation.cross_val_score(clf, X_train, y_train, cv=3)
scores
scores.mean()
scores.std()
clf = clf.fit(X_train, y_train)
predicted = clf.predict(X_test)
print metrics.classification_report(y_test, predicted)
print metrics.confusion_matrix(y_test, predicted)

# apply to raw data
users_2predict = pd.read_csv('../sample/final/users_final.csv', index_col=0)
UsersPreProcessor.process(users_2predict)
users_2predict.head()
users_2predict = users_2predict.ix[:, [
    'hasDesc', 'hasDomain', 'hasWeihao', 'gender', 'allow_all_act_msg',
    'geo_enabled', 'allow_all_comment', 'verified', 'wage', 'FoPd',
    'StPd', 'FavPm', 'FrFo', 'BiFo', 'BiFr', 'credibility']]
columns = {'allow_all_act_msg': 'allowAllMsg', 'geo_enabled': 'allowGeo',
           'allow_all_comment': 'allowAllComment'}
users_2predict.rename(columns=columns, inplace=True)
users_2predict.shape
users_2predict.columns

# to predict
predicted = clf.predict(users_2predict.ix[:, :-1])
predicted.shape
users_2predict.shape
users_2predict['credibility'] = predicted

raw_users2predict = pd.read_csv('../sample/final/users_final.csv', index_col=0)
raw_users2predict.shape
raw_users2predict.head()
raw_users2predict.columns
raw_users2predict['credibility'] = users_2predict['credibility']
raw_users2predict.to_csv('../sample/final/users_final_marked.csv')

# to mark comments user credibility
comments = pd.read_csv('../sample/final/comments_final.csv')
comments.columns
marked_comments = pd.merge(comments, raw_users2predict, left_on='userid',
                           right_index=True, how='left')
marked_comments.rename(columns={'credibility': 'UC'}, inplace=True)
marked_comments.columns
marked_comments.shape
export_cols = ['cid', 'sid', 'screen_name', 'reply2Id', 'ctext',
               'csource', 'create_at', 'UC']
marked_comments[export_cols] \
    .to_csv('../sample/final/comments_final_marked.csv')
marked_comments[export_cols].head()

# to mark statuses user credibility
statuses = pd.read_csv('../sample/final/status_final.csv')
statuses.columns
marked_statuses = pd.merge(statuses, raw_users2predict, left_on='userid',
                           right_index=True, how='left')
marked_statuses.columns
marked_statuses.rename(columns={'credibility': 'UC'}, inplace=True)
marked_comments[marked_comments['sid'] ==
                marked_statuses['sid'][0]][export_cols]
export_cols = ['sid', 'screen_name', 'retweetOfId', 'text', 'source',
               'create_at', 'reposts_count', 'comments_count',
               'attitude_count', 'bmiddle_pic', 'UC']
marked_statuses[export_cols].to_csv('../sample/final/ \
     statuses_final_marked.csv')
