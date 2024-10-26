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

def classify_titanic():
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

    train = pd.read_csv("datas/titanic/train.csv")
    test = pd.read_csv("datas/titanic/test.csv")
    all_df = pd.concat([train, test], ignore_index=True)

    all_df.loc[all_df["Fare"].isna(), "Fare"] = 7.75

    ticket_list = []
    for ticket, g_df in all_df.groupby("Ticket"):
        ticket_num = g_df["Fare"].shape[0]
        ticket_dict = {
            "Ticket": ticket,
            "EachFare": 0
        }
        if ticket_num > 1:
            if not (g_df["Fare"] == g_df["Fare"].iloc[0]).all():
                ticket_dict["EachFare"] = g_df["Fare"].sum() / ticket_num
            else:
                ticket_dict["EachFare"] = g_df["Fare"].iloc[0] / ticket_num
        else:
            ticket_dict["EachFare"] = g_df["Fare"].iloc[0]
        ticket_list.append(ticket_dict)
    ticket_df = pd.DataFrame(ticket_list)
    all_df = pd.merge(all_df, ticket_df, on="Ticket")
    all_df = all_df.drop(columns=["Fare"]).rename(columns={"EachFare": "Fare"}).sort_values(by="PassengerId")
    all_df["Fare"] = all_df["Fare"].map(lambda x: np.log(x) if x > 0 else 0)
    all_df["Cabin"] = all_df["Cabin"].fillna("U")
    all_df["Embarked"] = all_df["Embarked"].fillna(all_df["Embarked"].mode()[0])

    name_list = []
    for index, row_se in all_df.iterrows():
        suffix_list = row_se["Name"].split(",")
        suffix_str = suffix_list[0] if len(suffix_list) < 2 else suffix_list[1]
        symbol_str = punctuation + hanzi.punctuation
        new_name = re.sub(f"[{symbol_str}]+", "", suffix_str)
        prefix_list = new_name.strip().split()
        name_list.append(prefix_list[0])
    all_df = all_df.assign(**{"Title": name_list})

    title_mapper={
        "Mr": "Mr",
        "Mlle": "Miss",
        "Miss": "Miss",
        "Master": "Master",
        "Jonkheer": "Master",
        "Mme": "Mrs",
        "Ms": "Mrs",
        "Mrs": "Mrs",
        "Don": "Royalty",
        "Sir": "Royalty",
        "the": "Royalty",
        "Dona": "Royalty",
        "Lady": "Royalty",
        "Capt": "Officer",
        "Col": "Officer",
        "Major": "Officer",
        "Dr": "Officer",
        "Rev": "Officer"
    }
    all_df["Title"].apply(lambda x: title_mapper[x])

    all_df["FamilyNum"] = all_df["Parch"] + all_df["SibSp"] + 1

    def family_size(family_num):
        if family_num == 1:
            return 0
        elif (family_num >= 2) & (family_num <= 4):
            return 1
        else:
            return 2
    all_df = all_df.assign(**{"FamilySize": all_df["FamilyNum"].map(family_size)})

    all_df["Deck"] = all_df["Cabin"].map(lambda x: x[0])
    ticket_num_mapper = all_df["Ticket"].value_counts()
    all_df["TicketNum"] = all_df["Ticket"].map(ticket_num_mapper)

    # 按照TicketNum大小，将TicketNumGroup分为三类。
    def ticket_num_group(num):
        if (num >= 2) & (num <= 4):
            return 0
        elif (num == 1) | ((num >= 5) & (num <= 8)):
            return 1
        else:
            return 2
    # 得到各位乘客TicketNumGroup的类别
    all_df["TicketNumGroup"] = all_df["TicketNum"].map(ticket_num_group)

    # 筛选数据集
    age_df = all_df[["Age","Parch", "Pclass", "SibSp", "Title", "FamilyNum", "TicketNum"]]
    # 进行one-hot编码
    tmp_age_df = pd.get_dummies(age_df)
    parch_age_df = pd.get_dummies(tmp_age_df["Parch"], prefix="Parch")
    sib_age_df = pd.get_dummies(tmp_age_df["SibSp"], prefix="SibSp")
    pclass_age_df = pd.get_dummies(tmp_age_df["Pclass"], prefix="Pclass")
    # 查看变量间相关性
    corr_age_df = pd.DataFrame()
    corr_age_df = tmp_age_df.corr()

    tmp_age_df = pd.concat([tmp_age_df, parch_age_df, sib_age_df, pclass_age_df], axis=1)

    parmas_dict = {
        "n_estimators": range(70, 210, 10),
        "criterion": ["squared_error", "absolute_error", "poisson"],
        "max_depth": range(10, 22, 2),
        "max_features": ["sqrt", "log2", 1]
    }
    # 拆分实验集和预测集
    known_df = tmp_age_df[tmp_age_df["Age"].notna()]
    unknown_df = tmp_age_df[tmp_age_df["Age"].isna()]

    # 生成实验数据的特征和标签
    known_X = known_df.drop(columns=["Age"])
    known_y = known_df["Age"]

    # 生成预测数据的特征
    unknown_X = unknown_df.drop(columns=["Age"])

    # 利用随机森林构建模型
    rfr = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    rfr.fit(known_X, known_y)

    pred_y = rfr.predict(known_X)
    r2_score(known_y, pred_y)

    unknown_y = rfr.predict(unknown_X)
    all_df.loc[all_df["Age"].isna(), "Age"] = unknown_y

    name_list = []
    for index, row_se in all_df.iterrows():
        suffix_list = row_se["Name"].split(",")
        suffix_str = suffix_list[0] if len(suffix_list) < 2 else suffix_list[1]
        symbol_str = punctuation + hanzi.punctuation
        new_name = re.sub(f"[{symbol_str}]+", "", suffix_str)
        prefix_list = new_name.strip().split()
        name_list.append(prefix_list[1])
    all_df = all_df.assign(**{"Surname": name_list})

    # 提取乘客的姓氏及相应的乘客数
    surname_mapper = all_df["Surname"].value_counts(dropna=False)
    all_df["SurnameNum"] = all_df["Surname"].map(surname_mapper)

    # 将数据分为两组
    male_df = all_df[(all_df["Sex"] == "male") & (all_df["Age"] > 12) & (all_df["FamilyNum"] >= 2)]
    female_child_df = all_df[((all_df["Sex"] == "female") | (all_df["Age"] <= 12)) & (all_df["FamilyNum"] >= 2)]

    male_surname_df = male_df.groupby(by="Surname").agg({"Survived": "mean"})
    male_surname_mapper = male_surname_df[male_surname_df["Survived"] == 1].index.values
    female_child_surname_df = female_child_df.groupby(by="Surname").agg({"Survived": "mean"})
    female_child_surname_mapper = female_child_surname_df[female_child_surname_df["Survived"] == 1].index.values
    # 对数据集中这些姓氏的男性数据进行修正：1、性别改为女；2、年龄改为5。
    all_df.loc[(all_df["Survived"].isna()) & (all_df["Surname"].isin(male_surname_mapper)) & (all_df["Sex"] == "male"), "Age"] = 5
    all_df.loc[(all_df["Survived"].isna()) & (all_df["Surname"].isin(male_surname_mapper)) & (all_df["Sex"] == "male"), "Sex"] = "female"
    # 对数据集中这些姓氏的女性及儿童的数据进行修正：1、性别改为男；2、年龄改为60。
    all_df.loc[(all_df["Survived"].isna()) & (all_df["Surname"].isin(female_child_surname_mapper)) & ((all_df["Sex"] == "female") | (all_df["Age"] <= 12)), "Age"] = 60
    all_df.loc[(all_df["Survived"].isna()) & (all_df['Surname'].isin(female_child_surname_mapper)) & ((all_df['Sex'] == 'female') | (all_df['Age'] <= 12)), "Sex"] = "male"

    o = OrdinalEncoder()
    o_array = o.fit_transform(all_df[["Sex", "Title", "Deck"]])
    all_df.loc[:, ["Sex", "Title", "Deck"]] = o_array

    filter_df = all_df.drop(columns=["Cabin", "Name", "Ticket", "PassengerId", "Surname", "SurnameNum", "Embarked"])
    corr_df = filter_df.corr(method="pearson")

    filter_df = filter_df.drop(columns=["FamilyNum", "SibSp", "TicketNum", "Parch"])
    filter_df = pd.get_dummies(filter_df)
    for col in ["Pclass", "TicketNumGroup", "FamilySize"]:
        tmp_df = pd.get_dummies(all_df[col], prefix=col)
        filter_df = pd.concat([filter_df, tmp_df], axis=1)
    
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

    # 不同机器学习交叉验证结果汇总
    cv_results=[]
    for classifier in classifiers:
        result = cross_val_score(classifier, X, y, scoring="accuracy", cv=5, n_jobs=-1)
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

    pred_y = gbc_gvc.predict(pred_X)

    #导出预测结果
    result_df = pd.DataFrame()
    result_df = result_df.assign(**{
        "PassengerId": all_df[all_df['Survived'].isna()]['PassengerId'],
        "Survived": pred_y
    })
    #将预测结果导出为csv文件
    result_df.to_csv(f"datas/titanic/gbc_result.csv", index=False)
    """
