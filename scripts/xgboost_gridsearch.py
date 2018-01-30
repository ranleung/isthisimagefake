import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from xgboost import XGBClassifier
from bayes_opt import BayesianOptimization
from datetime import datetime

def xgboostcv(max_depth,
              learning_rate,
              n_estimators,
              gamma,
              min_child_weight,
              max_delta_step,
              subsample,
              colsample_bytree,
              silent =True,
              nthread = -1,
              seed = 1234):
    return cross_val_score(XGBClassifier(max_depth = int(max_depth),
                                         learning_rate = learning_rate,
                                         n_estimators = int(n_estimators),
                                         silent = silent,
                                         nthread = nthread,
                                         gamma = gamma,
                                         min_child_weight = min_child_weight,
                                         max_delta_step = max_delta_step,
                                         subsample = subsample,
                                         colsample_bytree = colsample_bytree,
                                         seed = seed,
                                         objective = "binary:logistic"),
                           X_train,
                           y_train,
                           scoring='roc_auc',
                           cv=5).mean()


def bayOpt():
    xgboostBO = BayesianOptimization(xgboostcv,
                                     {'max_depth': (5, 10),
                                      'learning_rate': (0.01, 0.3),
                                      'n_estimators': (50, 1000),
                                      'gamma': (0.01, 1.),
                                      'min_child_weight': (2, 10),
                                      'max_delta_step': (0, 0.1),
                                      'subsample': (0.7, 0.8),
                                      'colsample_bytree' :(0.5, 0.99)
                                     })

    xgboostBO.maximize()
    print('Final Results')

    print('-'*53)
    print('Best XGBOOST parameters: %f' % xgboostBO.res['max']['max_params'])

    print('-'*53)
    print('XGBOOST: %f' % xgboostBO.res['max']['max_val'])

    # Finally, we take a look at the final results.


if __name__ == '__main__':
    start = datetime.now()
    print "START TIME ", str(start)

    np.random.seed(0)

    X = np.load('ela_X.npy')
    y = np.load('ela_y.npy')

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=.2)
    bayOpt()

    print "Finished ", str(datetime.now())
    print 'Took ', datetime.now() - start
