from scipy.stats import chi2
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import chi2, mutual_info_regression
import numpy as np
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from scipy.signal import periodogram
from sklearn.cluster import KMeans

"""Predictive Analysis - Answer the question (What is likely to Happen?)

     The module is divided to three parts:
     
             1. Regression  
             2. Forcasting 
             3. Classification  
             4. Clustering 
             
     Regression vs Classification
     regression algorithms are used to predict the continuous values and classification algorithms are used to
     predict/ classify the discrete values 
     *      Types of Classification Algorithms                           *     Types of Regression Algorithms 
            Logistic Regression                                                Simple Linear Regression              
            K_Nearest Neighbours                                               Multiple Linear Regression   
            Support Vector Machine                                             Polynomial Regression  
            Kernel SVM                                                         Support Vector Regression   
            Decision Tree Classification                                       Decision Tree Regression   
            Random Forest Classification and more ...                          Random Forest Regression           


"""
#                   ---------------  REGRESSION     ---------------


def calculate_slope(data, independent_column: str, predicted_column: str) -> float:
    """
    Calculate slope.

    :param data: variable

    :param independent_column: string

    :param predicted_column: string

    :return: slope value
    """
    if len(data[independent_column]) != len(data[predicted_column]):
        raise ValueError(f"length of {data[independent_column]} is not equal to length of{data[predicted_column]}")
    data[independent_column] = np.array(data[independent_column])
    data[predicted_column] = np.array(data[predicted_column])
    n = len(data[independent_column])
    n_sum_x_y = n * np.sum(data[independent_column] * data[predicted_column])
    sum_x_sum_y = data[independent_column].sum() * data[predicted_column].sum()
    n_sum_x_exp2 = n * np.sum(data[independent_column] ** 2)
    sum_x_exp2 = data[independent_column].sum() ** 2
    slope = (n_sum_x_y - sum_x_sum_y) / (n_sum_x_exp2 - sum_x_exp2)
    # print(f"slope : {np.round(slope, 4)}")
    return np.round(slope, 4)


def calculate_intercept_of_y(data, independent_column: str, predicted_column: str) -> float:
    """
    Calculate y - intercept.

    :param data: variable

    :param independent_column: string

    :param predicted_column: string

    :return: y_intercept value
    """
    if len(data[independent_column]) != len(data[predicted_column]):
        raise ValueError(f"length of {data[independent_column]} is not equal to length of{data[predicted_column]}")

    n, slope = len(data[independent_column]), calculate_slope(data, independent_column, predicted_column)
    sum_y = data[predicted_column].sum()
    m_sum_x = slope * data[independent_column].sum()
    y_intercept = (sum_y - m_sum_x) / n
    # print(f"y intercept: {np.round(y_intercept, 4)}")
    return np.round(y_intercept, 4)


def plot_linear_equation(data, independent_column: str, predicted_column: str):
    """
    Visualize a linear equation.

    :param data: variable

    :param independent_column: string

    :param predicted_column: string

    :return: scatter plot

    """
    slope = calculate_slope(data, independent_column, predicted_column)
    y_intercept = calculate_intercept_of_y(data, independent_column, predicted_column)
    data["predicted"] = data[independent_column].map(lambda x: slope * x + y_intercept)
    sns.scatterplot(x=independent_column, y=predicted_column, data=data)
    sns.lineplot(x=independent_column, y=data["predicted"], color="orange", lw=4, data=data)
    plt.show()


def split_data_into_training_and_test(data, independent_colum: list, dependent_column: str):
    """
    Split data to training and test 80 % train and 20 % test.

    :param data: variable

    :param independent_colum: list

    :param dependent_column: string

    :return: dataframe

    """
    x = data[independent_colum]
    y = data[dependent_column]
    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.80, test_size=0.20, random_state=0)
    return x_train, x_test, y_train, y_test


def plot_polynomial_regression(data, independent_colum, dependent_column, degree: int):
    """
    Visualize and display polynomial regression.

    :param data: variable

    :param independent_colum: string

    :param dependent_column: list

    :param degree: integer

    :return: model

    """
    series = pd.Series(data[independent_colum])
    arr = series.values
    x = arr.reshape((-1, 1))
    y = data[dependent_column]
    x_ = PolynomialFeatures(degree=degree, include_bias=False).fit_transform(x)
    model = LinearRegression().fit(x_, y)
    r_sq = model.score(x_, y)
    print(f"coefficient of determination: {r_sq}\nintercept: {model.intercept_}\ncoefficients: {model.coef_}")
    plt.scatter(x=data[independent_colum], y=data[dependent_column], color="blue")
    plt.plot(x, model.predict(x_), color="red")
    plt.title("Polynomial Regression")
    plt.xlabel(f"{independent_colum}")
    plt.ylabel(f"{dependent_column}")
    plt.show()
    return model


def multi_linear_regression(data, independent_colum: list, dependent_column: str):
    """
    Implementing MLR, implement independent column as a list.

    :param data: variable

    :param independent_colum: list

    :param dependent_column: string

    :return: MLR & printing out the intercept_, coef_, R2(coefficient of determination)

    """
    x = data[independent_colum]
    y = data[dependent_column]
    model = LinearRegression().fit(x, y)
    r_sq = model.score(x, y)
    print(f"coefficient of determination: {r_sq}\nintercept: {model.intercept_}\ncoefficients: {model.coef_}")
    return model


def display_ols_summary(data, x_input: list, y_output: str):
    """
    Display ols summary.

    :param data: variable

    :param x_input: list

    :param y_output: str

    :return: display ols

    """
    x = sm.add_constant(data[x_input])
    model = sm.OLS(data[y_output], x)
    results = model.fit()
    print(results.summary())
    # print(f"coefficient of determination: {results.rsquared}\nadjust coefficient of determination: "
    #       f"{results.rsquared_adj}\nregression coefficients: {results.params}")


def make_mi_score(x, y):
    """
    Mutual information.

    :param x:

    :param y:

    :return: mi_score
    """
    for colname in x.select_dtypes(["object", "category"]):
        x[colname], _ = x[colname].factorize()
    discrete_features = [pd.api.types.is_integer_dtype(t) for t in x.dtypes]
    mi_scores = mutual_info_regression(x, y, discrete_features=discrete_features, random_state=0)
    mi_scores = pd.Series(mi_scores, name="MI Scores", index=x.columns)
    mi_scores = mi_scores.sort_values(ascending=False)
    return mi_scores


def plot_mi_scores(mi_score):
    """
    Plot sorted score.

    :param mi_score: variable

    :return: bar chart

    """
    mi_score = mi_score.sort_values(ascending=True)
    width = pd.Series(mi_score)
    ticks = mi_score.index
    plt.barh(width, mi_score)
    plt.yticks((width, ticks))
    plt.title("Mutual Information Scores")
    plt.show()

#                   ---------------  FORCASTING     ---------------


def set_index_to_date(data, date_column: str):
    """
    Set index to date.

    :param data: variable

    :param date_column: str

    :return: dataframe

    """
    data = data.set_index(date_column)
    set_index_data = pd.to_datetime(data.index, infer_datetime_format=True)
    return set_index_data


def test_stationarity(timeseries):
    """

    Plot rolling statistics.

    Perform dickey-fuller test.

    :param timeseries: variable
    :return: dickey-fuller test

    """
    moving_average = timeseries.rolling(window=12).mean()
    moving_std = timeseries.rolling(window=12).std()

    plt.plot(timeseries, color="blue", label="Original")
    plt.plot(moving_average, color="red", label="Rolling Mean")
    plt.plot(moving_std, color="black", label="Rolling STD")
    plt.legend(loc="best")
    plt.title("Rolling Mean & Standard Deviation")
    plt.show()

    print("Results of Dickey-Fuller Test:")
    dftest = adfuller(timeseries.values, autolag="AIC")
    dfoutput = pd.Series(dftest[0:4], index=["Test Statistic", "p-value", "#Lags Used", "Number of Observations Used"])
    for key, value in dftest[4].items():
        dfoutput["Critical Value (%s)" % key] = value
    print(dfoutput)


def create_date_range(start_date: str, end_date: str, freq: str):
    """
    Create date range.

    :param start_date: str

    :param end_date: str

    :param freq: str

    :return: dataframe
    """
    data_sequence = pd.date_range(start=start_date, end=end_date, freq=freq)
    return data_sequence


def create_date_features(data, date_column: str):
    """
    Create date features.

    :param data: variable

    :param date_column: string

    :return: dataframe with date features
    """
    data[date_column] = pd.to_datetime(data[date_column], format="%Y-%m-%d", errors="coerce",
                                       infer_datetime_format=True)
    data["dayOfWeek"] = data[date_column].dt.dayofweek
    data["Quarter"] = data[date_column].dt.quarter
    data["Month"] = data[date_column].dt.month
    data["Year"] = data[date_column].dt.year
    data["dayOfYear"] = data[date_column].dt.dayofyear
    return data


def create_hourly_feature(data, date_column: str):
    """
    Create hourly feature.

    :param data: data variable

    :param date_column: string

    :return: dataframe
    """
    data[date_column] = pd.to_datetime(data[date_column], format="%Y-%m-%d %H:%M:%S", errors="coerce",
                                       infer_datetime_format=True)
    data["hour"] = data[date_column].dt.hour
    return data


def seasonal_plot(data, column_name: str, period_column: str, freq: str, ax=None):
    """
    Seasonal plot.

    example:
    seasonal_plot(data, "passengers_column", period_column="Year", freq="dayOfYear")

    :param data: variable

    :param column_name: str

    :param period_column: str

    :param freq: str

    :param ax: None

    :return: chart
    """
    if ax is None:
        _, ax = plt.subplots()
    palette = sns.color_palette("husl", n_colors=data[period_column].nunique())
    ax = sns.lineplot(
        x=freq,
        y=column_name,
        hue=period_column,
        data=data,
        errorbar=("ci", False),
        ax=ax,
        palette=palette,
        legend=False,
    )
    ax.set_title(f"Seasonal Plot ({period_column}/{freq})")
    for line, name in zip(ax.lines, data[period_column].unique()):
        y_ = line.get_ydata()[-1]
        ax.annotate(
            name,
            xy=(1, y_),
            xytext=(6, 0),
            color=line.get_color(),
            xycoords=ax.get_yaxis_transform(),
            textcoords="offset points",
            size=14,
            va="center",
        )
    plt.show()


def plot_periodogram(data, column_name: str, detrend='linear', ax=None):
    """
    Periodogram plot.

    example:
    plot_periodogram(data, "column_name")

    :param data: variable

    :param column_name: str

    :param detrend: 'linear'

    :param ax: None

    :return: chart
    """
    fs = pd.Timedelta("1Y") / pd.Timedelta("1D")
    freqencies, spectrum = periodogram(
        data[column_name],
        fs=fs,
        detrend=detrend,
        window="boxcar",
        scaling='spectrum',
    )
    if ax is None:
        _, ax = plt.subplots()
    ax.step(freqencies, spectrum, color="purple")
    ax.set_xscale("log")
    ax.set_xticks([1, 2, 4, 6, 12, 26, 52, 104])
    ax.set_xticklabels(
        [
            "Annual (1)",
            "Semiannual (2)",
            "Quarterly (4)",
            "Bimonthly (6)",
            "Monthly (12)",
            "Biweekly (26)",
            "Weekly (52)",
            "Semiweekly (104)",
        ],
        rotation=30,
    )
    ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    ax.set_ylabel("Variance")
    ax.set_title("Periodogram")
    plt.show()


#                   ---------------  Classification     ---------------
def chi_value_plot(data):
    """
    Plot the variable importance by ch2 for binary classification.

    :param data: variable

    :return: bar chart

    """
    for col in data:
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col])
    x = data.iloc[:, : -1]
    y = data.iloc[:, -1]
    # Higher the chi value , higher the importance
    chi_scores = chi2(x, y)
    chi_values = pd.Series(chi_scores[0], index=x.columns)
    chi_values.sort_values(ascending=False, inplace=True)
    chi_values.plot.bar()
    plt.show()


def p_value_plot(data):
    """
    Plot the variable importance by p-value for binary classification.

    :param data: variable

    :return: bar chart

    """
    for col in data:
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col])
    x = data.iloc[:, : -1]
    y = data.iloc[:, -1]
    # if p-value > 0.5, lower the importance
    chi_scores = chi2(x, y)
    chi_values = pd.Series(chi_scores[1], index=x.columns)
    chi_values.sort_values(ascending=False, inplace=True)
    chi_values.plot.bar()
    plt.show()


#                   ---------------  Clustering     ---------------

def visualize_cluster_sse(scaled_features):
    """
    Visualize sse scaled column.

    :param scaled_features: variable

    :return: chart

    """
    kmean_kwargs = {
        "init": "random",
        "n_init": 10,
        "max_iter": 300,
        "random_state": 42
    }
    sse = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, **kmean_kwargs)
        kmeans.fit(scaled_features)
        sse.append(kmeans.inertia_)
    plt.style.use("fivethirtyeight")
    plt.plot(range(1, 11), sse, marker="o")
    plt.xticks(range(1, 11))
    plt.xlabel("Number of Clusters")
    plt.ylabel("SSE")
    plt.show()