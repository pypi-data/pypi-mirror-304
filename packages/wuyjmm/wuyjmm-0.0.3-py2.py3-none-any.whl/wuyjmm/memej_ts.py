def sktime_example():
    """
    pip install seaborn==0.13.2
    pip install sktime=='0.29.1
    import numpy as np
    import pandas as pd
    import seaborn as sns
    from datetime import timedelta
    from matplotlib import pyplot as plt
    from matplotlib.ticker import MaxNLocator
    from sklearn.svm import SVR
    from sklearn.neighbors import KNeighborsRegressor
    from sklearn.model_selection import GridSearchCV
    from sklearn.preprocessing import PowerTransformer, MinMaxScaler
    from sktime.forecasting.base import ForecastingHorizon
    from sktime.forecasting.compose import make_reduction, TransformedTargetForecaster
    from sktime.transformations.series.adapt import TabularToSeriesAdaptor
    from sktime.utils.plotting import plot_series
    from sktime.performance_metrics.forecasting import MeanAbsoluteError, mean_absolute_error, mean_absolute_percentage_error
    from sktime.forecasting.model_selection import temporal_train_test_split, SlidingWindowSplitter, ForecastingGridSearchCV
    from warnings import simplefilter

    def get_windows(y, cv):
        '''Generate windows'''
        train_windows = []
        test_windows = []
        for i, (train, test) in enumerate(cv.split(y)):
            train_windows.append(train)
            test_windows.append(test)
        return train_windows, test_windows
    
    def plot_windows(y, train_windows, test_windows, title=""):
        '''Visualize training and test windows'''

        simplefilter("ignore", category=UserWarning)

        def get_y(length, split):
            # Create a constant vector based on the split for y-axis.
            return np.ones(length) * split

        n_splits = len(train_windows)
        n_timepoints = len(y)
        len_test = len(test_windows[0])

        train_color, test_color = sns.color_palette("colorblind")[:2]

        fig, ax = plt.subplots(figsize=plt.figaspect(0.3))

        for i in range(n_splits):
            train = train_windows[i]
            test = test_windows[i]

            ax.plot(
                np.arange(n_timepoints), get_y(n_timepoints, i), marker="o", c="lightgray"
            )
            ax.plot(
                train,
                get_y(len(train), i),
                marker="o",
                c=train_color,
                label="Window",
            )
            ax.plot(
                test,
                get_y(len_test, i),
                marker="o",
                c=test_color,
                label="Forecasting horizon",
            )
        ax.invert_yaxis()
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set(
            title=title,
            ylabel="Window number",
            xlabel="Time",
            xticklabels=y.index,
        )
        # remove duplicate labels/handles
        handles, labels = [(leg[:2]) for leg in ax.get_legend_handles_labels()]
        ax.legend(handles, labels)

    df = pd.read_csv("datas/time_series/train.csv")

    col = "c1"
    y_df = df[["ID", "time", col]]
    horizon = 24

    for id_str, g_df in y_df.groupby("ID"):
        g_df["time"] = pd.to_datetime(g_df["time"])
        g_df = g_df.sort_values(by="time")
        g_df = g_df.drop(columns=["ID"])
        before = g_df["time"].iloc[:-1].values
        after = g_df["time"].iloc[1:].values
        seconds = int(pd.Series(after - before).dt.total_seconds().value_counts().idxmax())
        freq = timedelta(seconds=seconds)

        new_g_df = g_df.iloc[-500:].set_index("time").resample(freq).mean().interpolate()
        new_g_df.index = new_g_df.index.to_period(freq=freq)
        y = new_g_df[col]

        y_train, y_test = temporal_train_test_split(y, test_size=horizon)
        test_fh = ForecastingHorizon(y_test.index, is_relative=False)

        forecaster_y = pd.date_range(start=y.index.max().to_timestamp(), periods=horizon + 1, freq=freq)[1:].to_period(freq=freq)
        forecaster_fh = ForecastingHorizon(forecaster_y, is_relative=False)

        scoring_dict = {"mae": "neg_mean_absolute_error", "mape": "neg_mean_absolute_percentage_error"}
        # scoring = MeanAbsoluteError(multioutput="uniform_average")

        regressor_param_grid = {
            "C": (1, 5, 10, 50, 100, 500),
            "gamma": (0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1)
        }
        forecaster_param_grid = {
            "forecaster__window_length": range(12, 169, 12)
        }

        svr = SVR(cache_size=4096)
        regressor = GridSearchCV(svr, param_grid=regressor_param_grid, verbose=5, scoring=scoring_dict, refit="mae", n_jobs=5)
        forecaster = make_reduction(regressor, strategy="recursive", scitype="tabular-regressor")
        forecaster = TransformedTargetForecaster(
            [
                ("t1", TabularToSeriesAdaptor(PowerTransformer())),
                ("forecaster", make_reduction(regressor, strategy="recursive", scitype="tabular-regressor")),
            ]
        )
        cv = SlidingWindowSplitter(fh=list(range(1, 25)), window_length=200, step_length=24)
        train_windows, test_windows = get_windows(y_train, cv)
        plot_windows(y_train, train_windows, test_windows)
        break
    
    for id_str, g_df in y_df.groupby("ID"):
        g_df["time"] = pd.to_datetime(g_df["time"])
        g_df = g_df.sort_values(by="time")
        g_df = g_df.drop(columns=["ID"])
        before = g_df["time"].iloc[:-1].values
        after = g_df["time"].iloc[1:].values
        seconds = int(pd.Series(after - before).dt.total_seconds().value_counts().idxmax())
        freq = timedelta(seconds=seconds)

        new_g_df = g_df.iloc[-500:].set_index("time").resample(freq).mean().interpolate()
        new_g_df.index = new_g_df.index.to_period(freq=freq)
        y = new_g_df[col]

        y_train, y_test = temporal_train_test_split(y, test_size=horizon)
        test_fh = ForecastingHorizon(y_test.index, is_relative=False)

        forecaster_y = pd.date_range(start=y.index.max().to_timestamp(), periods=horizon + 1, freq=freq)[1:].to_period(freq=freq)
        forecaster_fh = ForecastingHorizon(forecaster_y, is_relative=False)

        scoring_dict = {"mae": "neg_mean_absolute_error", "mape": "neg_mean_absolute_percentage_error"}
        scoring = MeanAbsoluteError(multioutput="uniform_average")

        regressor_param_grid = {"n_neighbors": range(8, 33, 8)}
        forecaster_param_grid = {"window_length": range(12, 169, 12)}

        regressor = GridSearchCV(KNeighborsRegressor(), param_grid=regressor_param_grid, verbose=0, scoring=scoring_dict, refit="mae", n_jobs=5)
        forecaster = make_reduction(regressor, strategy="recursive", scitype="tabular-regressor")

        cv = SlidingWindowSplitter(fh=list(range(1, 25)), window_length=200, step_length=24)
        train_windows, test_windows = get_windows(y_train, cv)
        plot_windows(y_train, train_windows, test_windows)

        gscv = ForecastingGridSearchCV(forecaster, cv=cv, param_grid=forecaster_param_grid, scoring=scoring)
        gscv.fit(y_train)

        y_pred = gscv.best_forecaster_.predict(test_fh)
        y_result = gscv.best_forecaster_.predict(forecaster_fh)
        plot_series(y_test, y_pred, y_result, labels=["y_test", "y_pred", "y_result"])
        mae = mean_absolute_error(y_test, y_pred)
        mape = mean_absolute_percentage_error(y_test, y_pred)
        print(id_str.center(100, "-"))
        print("mae: ", mae)
        print("mape:", mape)
        print("best sklearn: ", gscv.best_forecaster_.estimator_.best_params_)
        print("best sktime: ", gscv.best_params_)
        print(id_str.center(100, "-"))
        break
    """
