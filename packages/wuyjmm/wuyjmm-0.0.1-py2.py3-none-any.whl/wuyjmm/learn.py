# -*- coding: utf8 -*-
def hello(param):
    """

    ################# 随机森林回归代码   baseline
            import numpy as np
            import pandas as pd
            from sklearn.ensemble import RandomForestRegressor
            from sklearn.model_selection import train_test_split
            from sklearn.preprocessing import MinMaxScaler

            # 假设数据已经被加载到dataframe df中，列包括'SalePrice'（目标列）和其他预测列
            # 示例数据
            data = {
                'MSSubClass': [100, 100, 20],
                'LotArea': [1100, 1200, 1780],
                'SalePrice': [200000, 180000, 220000]
            }
            df = pd.DataFrame(data)
            print (df)

            # 分离特征和目标
            X = df.drop('SalePrice', axis=1)
            y = df['SalePrice']

            # 划分训练集和测试集
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

            # 随机森林模型
            rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
            rf_regressor.fit(X_train, y_train)

            # 预测
            y_pred = rf_regressor.predict(X_test)
            # 输出RMSE
            from sklearn.metrics import mean_squared_error
            mse = mean_squared_error(y_test, y_pred)
            # # 展示预测结果
            print("预测房价：", y_pred[0])
            print (mse)
            ################################### 实际案例数据预测结果
            data1 = {
                'MSSubClass': [100, 100, 20],
                'LotArea': [1100, 1200, 1780],
            }

            df1 = pd.DataFrame(data1)
            y_pred1 = rf_regressor.predict(df1)

            dd = pd.DataFrame(y_pred1)
            dd.to_csv('./xxxx.csv',index=False)
            print (dd)
    ########################################## 分类模型 SVM支持向量机 鸢尾花分类任务
            # 导入必要的库
            import pandas as pd
            from sklearn.model_selection import train_test_split
            from sklearn import svm
            from sklearn import metrics

            # 从CSV文件读取鸢尾花数据集
            iris = pd.read_csv("datasets/iris.csv")
            X = iris[['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']]
            y = iris.target
            # 将数据集划分为训练集和测试集，测试集占总数据的20%
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # 创建支持向量机（SVM）分类器模型

            model = svm.SVC()

            # 在训练集上拟合SVM模型
            model.fit(X_train, y_train)

            # 使用训练好的模型对测试集进行预测
            prediction = model.predict(X_test)

            # 打印SVM模型的准确性
            print('The accuracy of the SVM is:', metrics.accuracy_score(prediction, y_test))
    ########################################## 分类模型    KNN分类器
            from sklearn.neighbors import KNeighborsClassifier
            # 创建KNN分类器对象
            knn = KNeighborsClassifier(n_neighbors=5)

            # 训练模型
            knn.fit(X_train, y_train)

            # 进行预测
            y_pred = knn.predict(X_test)

            # 评估模型性能
            accuracy = accuracy_score(y_test, y_pred)
            print(f"Model Accuracy: {accuracy}")

    ########################################### xgboot 分类
            import xgboost as xgb
            from sklearn.metrics import classification_report, accuracy_score
            xgb_model = xgb.XGBClassifier(reg_lambda=1, reg_alpha=0.5, use_label_encoder=False, eval_metric='logloss')
            xgb_model.fit(x_train, y_train)
            xgb_model.fit(x_train, y_train)
            xgb_model.score(x_test,y_test)
            xgb_pred = xgb_model.predict(x_test)
            accuracy_xgb = accuracy_score(y_test, xgb_pred)
            accuracy_xgb
    ########################################### xgboot 回归模型
            import xgboost as xgb
            from sklearn.metrics import classification_report, accuracy_score
            import xgboost as xgb
            xgb_model = xgb.XGBRFRegressor(max_depth = 3,learning_rate=0.1,
                               n_estimators= 100,objective='reg:squarederror',booster='gbtree',random_state=0)
            xgb_model.fit()
            print ('平均绝对误差：{}'.format(round(metrics.mean_squared_error(y,y_pred))))

            #############################################################################
            import xgboost as xgb
            from sklearn.model_selection import train_test_split
            from sklearn.metrics import mean_squared_error
            from sklearn.datasets import load_boston
            import numpy as np

            # 加载数据
            boston = load_boston()
            X, y = boston.data, boston.target

            # 划分训练集和测试集
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # 构建 DMatrix
            dtrain = xgb.DMatrix(X_train, label=y_train)
            dtest = xgb.DMatrix(X_test, label=y_test)

            print (dtrain)

            # 设置参数
            params = {
                'objective': 'reg:squarederror',
                'eval_metric': 'rmse',
                'max_depth': 6,
                'eta': 0.1,
                'subsample': 0.8,
                'colsample_bytree': 0.8,
                'seed': 42
            }

            # 训练模型
            num_rounds = 100
            bst = xgb.train(params, dtrain, num_rounds,verbose_eval=True,evals=[(dtrain, 'train1'), (dtest, 'test')])

            # 预测
            preds = bst.predict(dtest)

            # 评估模型
            rmse = np.sqrt(mean_squared_error(y_test, preds))
            print(f"RMSE: {rmse}")


    #############################################  数据处理pandas
            ###  字典设置
            result_dic=df[["号段","归属地市"]].set_index("号段").to_dict()['归属地市'] #号段字典
            ### isin  不包含
            df = df[-df["是否纯2g语音用户"].isin(["是"])]
            ### 填充数据
            values = {"是否纯2g语音用户": 0}
            df = df.fillna(value=values)
            ### 筛选行
            df = df.loc[(df["是否2I用户号码"]=="是")]
            ###  groupby agg
            df_g = df.groupby(['work_order','work_station'])
            df_g.size().reset_index()

            print(data.groupby('company').agg({'salary': 'median', 'age': 'mean'}))
    ###############################################   异常值填充处理  均值/中位数/众数填充
            import pandas as pd
            from scipy import stats

            # 读取Excel文件
            df = pd.read_excel("银行贷款审批数据.xlsx")

            # 定义连续变量和离散变量列表
            continuous_vars = ['x2', 'x3', 'x5', 'x6', 'x7', 'x10', 'x13', 'x14']  ### 列名
            discrete_vars = ['x1', 'x4', 'x8', 'x9', 'x11', 'x12']

            # 使用均值填充连续变量的缺失值
            for var in continuous_vars:
                df[var].fillna(df[var].mean(), inplace=True)

            # 或者使用中位数填充连续变量的缺失值
            # for var in continuous_vars:
            #    df[var].fillna(df[var].median(), inplace=True)

            # 使用众数填充离散变量的缺失值
            for var in discrete_vars:
                mode_value = stats.mode(df[var].dropna())[0][0]
                df[var].fillna(mode_value, inplace=True)

            # 检查是否还有缺失值
            missing_values = df.isnull().sum().sum()
            if missing_values == 0:
                print("所有缺失值已填充。")
            else:
                print("仍有缺失值未填充。")

            # 输出填充后的数据框的前几行
            print(df.head())
    ################################################## 数据查看
            # 1. 查看每列的基本统计信息
            print(df.describe())
            print(df.info())
            # 2. 查看列B的唯一值计数分布
            print(df['B'].value_counts())
            ### 统计空值个数
            print(df.isnull().sum())
    ################################################# 特征编码  将中文转换成数值代入训练
            from sklearn.preprocessing import LabelEncoder,StandardScaler
            df["bought"]=labelEncoder.fit_transform(df["bought"])
            ##### 逆转换
            labelEncoder.inverse_transform(df["bought"])
            ########################################### 特征编码
            y = pd.Categorical(df_iris['4']).codes  ### 类别转换成 数值  只能识别数值
            ########################################### one-hot 独热编码
            import pandas as pd
            from sklearn.preprocessing import OneHotEncoder

            # 创建示例数据
            data = {'color': ['red', 'blue', 'green', 'red', 'blue']}
            df = pd.DataFrame(data)

            print("原始数据:")
            print(df)

            # 创建 OneHotEncoder 对象
            encoder = OneHotEncoder(sparse=False)

            # 拟合并转换数据
            encoded_data = encoder.fit_transform(df[['color']])

            # 获取特征名称
            encoded_columns = encoder.get_feature_names_out(['color'])

            # 创建新的 DataFrame
            df_encoded = pd.DataFrame(encoded_data, columns=encoded_columns)

            print("One-Hot 编码后的数据:")
            print(df_encoded)

            # 合并原始数据和编码后的数据
            df_final = pd.concat([df, df_encoded], axis=1)

            print("最终数据:")
            print(df_final)

            原始数据:
               color
            0    red
            1   blue
            2  green
            3    red
            4   blue

            One-Hot 编码后的数据:
               color_blue  color_green  color_red
            0        0.0         0.0        1.0
            1        1.0         0.0        0.0
            2        0.0         1.0        0.0
            3        0.0         0.0        1.0
            4        1.0         0.0        0.0

            最终数据:
               color  color_blue  color_green  color_red
            0    red        0.0         0.0        1.0
            1   blue        1.0         0.0        0.0
            2  green        0.0         1.0        0.0
            3    red        0.0         0.0        1.0
            4   blue        1.0         0.0        0.0


    ################################################# 标准化
            from sklearn.preprocessing import LabelEncoder,StandardScaler
            scaler = StandardScaler()
            x_train = scaler.fit_transform(x_train)
            x_test = scaler.transform(x_test)
    ################################################ 画图
            import matplotlib.pyplot as plt
            # 验证集预测值与真实值的对比
            plt.plot(list(range(0,len(X_test))),y_test,marker='o')
            plt.plot(list(range(0,len(X_test))),y_test_pred,marker='*')
            plt.legend(['真实值','预测值'])
            plt.xlabel('序列')
            plt.ylabel('房价')
            plt.title('验证集预测值与真实值的对比')
            plt.show()
    ################################################ 时间序列  补全连续
            new_index = pd.date_range(start='20221101', end='20221110',  freq='d', inclusive='left')
            # 替换原有的时间索引
            df.index = new_index
    ################################################ 版本 # scikit-learn == 1.0.2  xgboost==1.7.6

    ################################################ 网格搜索
            # 定义参数网格
            param_grid = {
                'C': [0.001, 0.01, 0.1, 1, 10, 100],
                'penalty': ['l1', 'l2'],
                'solver': ['liblinear', 'saga']
            }

            # 进行网格搜索
            grid_search = GridSearchCV(lr, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
            grid_search.fit(X_train, y_train)

            # 获取最佳参数
            best_params = grid_search.best_params_
            print(f"Best parameters: {best_params}")

            # 获取最佳模型
            best_model = grid_search.best_estimator_

            # 预测
            y_pred = best_model.predict(X_test)

            # 评估模型
            accuracy = accuracy_score(y_test, y_pred)
            print(f"Accuracy: {accuracy:.4f}")

            ###################################################
            scoring参数输入形式
            包括字符串、可调用对象或评分函数。以下是常用的评分规则示例：
            使用预定义的字符串指定评分规则：
            'accuracy'：准确率（分类问题）
            'precision'：精确率（分类问题）
            'recall'：召回率（分类问题）
            'f1'：F1分数（分类问题）
            'r2'：R2分数（回归问题）
            'neg_mean_squared_error'：均方误差（回归问题）【为什么要使用负均方误差？这是因为在网格搜索过程中，Scikit-learn默认使用了负均方误差（negative mean squared error）作为评分指标。在网格搜索的目标是寻找最大化评分的最佳模型，而均方误差的计算结果越小越好。为了与最大化评分的目标一致，Scikit-learn将均方误差的值取负数，这样最大化负均方误差的结果就等价于最小化均方误差。所以，当使用 scoring='neg_mean_squared_error' 时，输出的评分值越接近于0，表示模型的性能越好。】
            'neg_root_mean_squared_error'均方根误差（回归问题）

            ######################################################## SVM 网格搜索
            import numpy as np
            from sklearn.svm import SVC
            from sklearn.model_selection import GridSearchCV, train_test_split
            from sklearn.datasets import load_iris
            from sklearn.metrics import accuracy_score

            # 加载 Iris 数据集
            iris = load_iris()
            X, y = iris.data, iris.target

            # 划分训练集和测试集
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # 定义 SVC 模型
            svm = SVC()

            # 定义参数网格
            param_grid = {
                    'C': [0.1, 1, 10, 100],
                    'kernel': ['linear', 'rbf', 'poly', 'sigmoid'],
                    'gamma': ['scale', 'auto'] + [0.001, 0.01, 0.1, 1]
                }

            # 进行网格搜索
            grid_search = GridSearchCV(svm, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
            grid_search.fit(X_train, y_train)

            # 获取最佳参数
            best_params = grid_search.best_params_
            print(f"Best parameters: {best_params}")

            # 获取最佳模型
            best_model = grid_search.best_estimator_

            # 预测
            y_pred = best_model.predict(X_test)

            # 评估模型
            accuracy = accuracy_score(y_test, y_pred)
            print(f"Accuracy: {accuracy:.4f}")
            #################################################  pandas
            # 拆分实验集和预测集
            known_df = tmp_age_df[tmp_age_df["Age"].notna()]
            unknown_df = tmp_age_df[tmp_age_df["Age"].isna()]
            all_df.loc[all_df["Age"].isna(), "Age"] = unknown_y
            all_df["Embarked"] = all_df["Embarked"].fillna(all_df["Embarked"].mode()[0])   ### 众数填充

            """

    return param + 1