import pandas as pd
import lightgbm as lgb
import warnings
warnings.filterwarnings('ignore')

class FeatureGbdt:
    def __init__(self):
        self.category_cols = None
        self.used_cols = None
        self.num_of_features = None

    def fit(self, X, y, objective, category_cols = [], used_cols = [], num_of_features = 30):

        self.category_cols = category_cols
        self.used_cols = used_cols
        self.num_of_features = num_of_features

        assert(objective in ['binary', 'regression'])

        params = {'objective': objective,
                  'boosting': 'gbdt',
                  'learning_rate': 0.01,
                  'num_leaves': 2 ** 5,
                  'bagging_fraction': 0.95,
                  'bagging_freq': 1,
                  'bagging_seed': 66,
                  'feature_fraction': 0.7,
                  'feature_fraction_seed': 66,
                  'max_bin': 100,
                  'max_depth': 5
                  }
        self.N_round = int(num_of_features)
        if len(self.used_cols) > 0:
            trn_data = lgb.Dataset(X[self.used_cols], label=y, categorical_feature=category_cols)
        else:
            trn_data = lgb.Dataset(X, label=y, categorical_feature=category_cols)
        self.clf = lgb.train(params, trn_data, num_boost_round=self.N_round, valid_sets=[trn_data], verbose_eval=10)

    def transform(self, X):
        if len(self.used_cols) > 0:
            lgb_feature = pd.DataFrame(self.clf.predict(X[self.used_cols], pred_leaf=True))
        else:
            lgb_feature = pd.DataFrame(self.clf.predict(X, pred_leaf=True))

        feas_name = ["lgb_" + str(i) for i in range(1, self.N_round + 1)]
        lgb_feature.columns = feas_name

        return lgb_feature

    def fit_transform(self, X, y, objective, category_cols = [], used_cols = [], num_of_features = 300):
        self.fit(X, y, objective, category_cols = category_cols, used_cols = used_cols, num_of_features = num_of_features)
        return self.transform(X)