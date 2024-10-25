def classify_example():
    """
    import re
    import optuna
    import numpy as np
    import pandas as pd
    import seaborn as sns
    from matplotlib import pyplot as plt
    from string import punctuation
    from zhon import hanzi
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import GridSearchCV, cross_val_score, StratifiedKFold, train_test_split
    from sklearn.metrics import mean_absolute_error, make_scorer, r2_score, roc_curve, auc, roc_auc_score, f1_score, accuracy_score, log_loss
    from sklearn.preprocessing import OrdinalEncoder
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, ExtraTreesClassifier
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
    from sklearn.linear_model import LogisticRegression
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.svm import SVC
    import warnings
    warnings.filterwarnings("ignore")

    # 拆分实验数据与预测数据
    train_df = filter_df[filter_df["Survived"].notna()]
    test_df = filter_df[filter_df["Survived"].isna()]

    X = train_df.drop(columns=["Survived"])
    y = train_df["Survived"]
    pred_X = test_df.drop(columns=["Survived"])

    classifiers=[]
    classifiers.append(SVC())
    classifiers.append(DecisionTreeClassifier())
    classifiers.append(RandomForestClassifier())
    classifiers.append(ExtraTreesClassifier())
    classifiers.append(GradientBoostingClassifier())
    classifiers.append(KNeighborsClassifier())
    classifiers.append(LogisticRegression())
    classifiers.append(LinearDiscriminantAnalysis())

    new_score = make_scorer(f1_score, greater_is_better=True, average="macro")

    cv_results=[]
    for classifier in classifiers:
        result = cross_val_score(classifier, X, y, scoring=new_score, cv=5, n_jobs=-1)
        cv_results.append(result)
    
    cv_means = []
    cv_std = []
    cv_name = []
    for i, cv_result in enumerate(cv_results):
        cv_means.append(cv_result.mean())
        cv_std.append(cv_result.std())
        cv_name.append(re.match("<method-wrapper '__str__' of (.*?) object at *", str(classifiers[i].__str__)).group(1))
    
    cv_res_df = pd.DataFrame({
        "cv_mean": cv_means,
        "cv_std": cv_std,
        "algorithm": cv_name
    })

    # GradientBoostingClassifier模型
    gbc = GradientBoostingClassifier()
    gb_param_dict = {
        "loss": ["log_loss", "exponential"],
        "n_estimators": [100, 200, 300],
        "learning_rate": [0.1, 0.05, 0.01],
        "max_depth": [4, 8],
        "min_samples_leaf": [100, 150],
        "max_features": [0.3, 0.1] 
    }
    gbc_gvc = GridSearchCV(gbc, param_grid=gb_param_dict, cv=5, scoring="accuracy", n_jobs=-1, verbose=1, error_score='raise')
    gbc_gvc.fit(X, y)

    # LogisticRegression模型
    lr = LogisticRegression()
    lr_param_dict = {
        "C": [1, 2, 3],
        "penalty": ["l1", "l2"]
    }
    lr_gvc = GridSearchCV(lr, param_grid=lr_param_dict, cv=5, scoring="accuracy", n_jobs=-1, verbose=1)
    lr_gvc.fit(X, y)

    print(f"gbc 模型得分为：{gbc_gvc.best_score_:.2%}")
    print(f"lr 模型得分为：{lr_gvc.best_score_:.2%}")
    """