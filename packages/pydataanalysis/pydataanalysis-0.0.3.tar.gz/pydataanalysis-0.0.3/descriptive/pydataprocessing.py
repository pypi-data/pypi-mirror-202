import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler, Normalizer, KBinsDiscretizer, MinMaxScaler, RobustScaler
from sklearn.preprocessing import PowerTransformer, QuantileTransformer
from scipy.stats import boxcox
from collections import Counter

#                 ----------------  DATA PREPROCESSING  ----------------


def unique_values(data, categorical_column: str):
    """
    Print out all the unique values in a categorical column.

    :param data: variable

    :param categorical_column:string

    :return:unique values in dataset
    """
    cat_col = data[categorical_column].unique()
    cat_col.sort()
    return cat_col


def columns_with_missing_values(data) -> list:
    """
    Missing values.

    :param data:variable

    :return:a list of columns with missing values
    """
    cols_with_missing = [col for col in data.columns if data[col].isnull().any()]
    return cols_with_missing


def replace_NaN_value(data, column_name: str, value_by: str):
    """
    Replace value by median, mode or mean.

    :param data:variable

    :param column_name: str

    :param value_by: str

    :return: column

    """
    if value_by.lower() == "median":
        return data[column_name].fillna(data[column_name].median(), inplace=True)
    elif value_by.lower() == "mean":
        return data[column_name].fillna(data[column_name].mean(), inplace=True)
    elif value_by.lower() == "mode":
        return data[column_name].fillna(data[column_name].mode(), inplace=True)
    else:
        print("Enter mean, median or mode to fill in the missing values")


def drop_missing_rows(data):
    """
    Drop rows with missing values.

    :param data:variable

    :return:dataframe

    """
    dataframe_without_missing_rows = data.copy()
    dataframe_without_missing_rows.dropna(inplace=True)
    return dataframe_without_missing_rows


def replace_missing_values_with_zero(data):
    """
    Replace all NaN values with 0.

    :param data:variable

    :return:dataframe

    """
    data_filled_with_zero = data.copy()
    data_filled_with_zero.fillna(0, inplace=True)
    return data_filled_with_zero


def replace_missing_values_with_what_comes_after_it(data):
    """
    Replace missing values that comes directly after it in the same column.

    :param data:variable

    :return:filled dataframe
    """
    bfill_data = data.copy()
    bfill_data.fillna(method="bfill", axis=0, inplace=True)
    return bfill_data


def replace_missing_values_with_string(data, column_name: str, my_string: str):
    """
     Replace missing value by string.

    :param data: variable

    :param column_name: string

    :param my_string: string

    :return: dataframe
    """

    data[column_name].fillna(my_string, axis=0, inplace=True)
    return data


def remove_duplicated_columns(data):
    """
    Removes duplicated columns(based on column names).

    :param data: variable

    :return: data
    """
    data_without_duplicates = data.loc[:, ~data.columns.duplicated()]
    return data_without_duplicates


def one_hot_encoding(data, categorical_col: list):
    """
    Encode categorical variables using one-hot encoding.

    :param data:variable

    :param categorical_col:list

    :return: dataframe
    """
    try:
        one_hot_encoded_data = pd.get_dummies(data, columns=categorical_col)

    except TypeError:
        print("categorical column Input must be a list")
    except KeyError:
        print("None of type ='object' are in the [columns]")
    else:
        return one_hot_encoded_data


def label_encoding(data, categorical_col: list):
    """
    Encode categorical variables using label encoder.

    :param data:variable

    :param categorical_col:list

    :return:  dataframe
    """
    try:
        label_encoder = LabelEncoder()
        data[categorical_col] = data[categorical_col].apply(label_encoder.fit_transform)
    except ValueError:
        print("categorical column Input must be a list")
    except KeyError:
        print("None of type ='object' are in the [columns]")
    else:
        return data


def standardization_numerical_columns(data, numerical_column: list):
    """
    Scale values of a numeric column so that they have zero mean and unit variance.

    :param data: variable

    :param numerical_column:String

    :return: scale dataframe
    """
    std_scaler = StandardScaler()
    df_scaled = std_scaler.fit_transform(data[numerical_column])
    df_scaled = pd.DataFrame(df_scaled, columns=numerical_column)
    return df_scaled


def normalize_numerical_column(data, numerical_column: str):
    """
    Scale values of a numeric column so that they have a minimum value of 0 and a maximum value of 1.

    :param data: variable

    :param numerical_column: str

    :return: data
    """
    normalizer = Normalizer()
    data[numerical_column] = normalizer.fit_transform(data[[numerical_column]])
    return data


def divide_num_col_into_cat_col_using_bins(data, numerical_col: str, number_bins: int):
    """
    Divide the values of a continuous numeric column into categorical column using bins.

    :param data: variable

    :param numerical_col: string

    :param number_bins: integer

    :return: dataframe
    """
    discretizer = KBinsDiscretizer(n_bins=number_bins, encode="ordinal")
    data[numerical_col] = discretizer.fit_transform(data[[numerical_col]])
    return data


def min_max_scaler_to_numerical_column(data, numerical_column: list):
    """
    Scale the values of a numeric column so that they have a minimum value of 0 and a maximum value of 1.

    :param data: variable

    :param numerical_column:string

    :return:dataframe
    """
    scaler = MinMaxScaler()
    df_scaled = scaler.fit_transform(data.to_numpy())
    df_scaled = pd.DataFrame(df_scaled, columns=numerical_column)
    return df_scaled


def robust_scaling_to_numerical_column(data, numerical_column: str):
    """
    Scale values of a numeric column using the median and interquartile range.

    :param data:variable

    :param numerical_column:string

    :return:dataframe
    """
    scaler = RobustScaler()
    data[numerical_column] = scaler.fit_transform(data[[numerical_column]])
    return data


def power_transformation_to_numerical_column(data, numerical_column: str):
    """
    Transform values of a numeric column in order to stabilize or improve the assumptions of certain statistical models.

    :param data:variable

    :param numerical_column:string

    :return:dataframe
    """
    transformer = PowerTransformer()
    data[numerical_column] = transformer.fit_transform(data[[numerical_column]])
    return data


def quantile_transformation_to_numerical_column(data, numerical_column: str):
    """
    Transform column value so that they have a uniform or normal distribution.

    :param data:variable

    :param numerical_column: string

    :return:dataframe

    """
    transformer = QuantileTransformer()
    data[numerical_column] = transformer.fit_transform(data[[numerical_column]])
    return data


def box_cox_transformation_to_numerical_column(data, numerical_column: str):
    """
    Box cox transformation.

    :param data:variable

    :param numerical_column: string

    :return: dataframe

    """
    data[numerical_column], lambda_ = boxcox(data[numerical_column])
    return data


def cumulatively_categories(data, variable_column: str, threshold: float):
    """
    Cumulatively

    :param data: variable

    :param variable_column: string

    :param threshold: float

    :return: dataframe

    """
    threshold_value = int(threshold * len(data[variable_column]))
    categories_list = []
    s = 0
    counts = Counter(data[variable_column])
    for i, j in counts.most_common():
        s += dict(counts)[i]
        categories_list.append(i)
        if s >= threshold_value:
            break
    categories_list.append("Other")
    data[variable_column] = data[variable_column].apply(lambda x: x if x in categories_list else "Other")
    return data


def detect_outliers(data):
    """
    Detect outliers in a data.

    :param data: variable

    :return: dataframe

    """
    outlier_percents = {}
    for column in data.columns:
        if data[column].dtype != object:
            q1 = np.quantile(data[column], 0.25)
            q3 = np.quantile(data[column], 0.75)
            iqr = q3 - q1
            upper_bound = q3 + (1.5 * iqr)
            lower_bound = q1 - (1.5 * iqr)
            outliers = data[(data[column] > upper_bound) | (data[column] < lower_bound)][column]
            outlier_percentage = len(outliers) / len(data[column]) * 100
            outlier_percents[column] = outlier_percentage
    outlier_dataframe = pd.DataFrame(data=outlier_percents.values(), index=list(outlier_percents.keys()),
                                     columns=['Outlier_percentage'])
    return outlier_dataframe.sort_values(by='Outlier_percentage', ascending=False)


def handle_outliers(data, column_name: str):
    """
    Handle outliers in a column.

    :param data: variable

    :param column_name: str

    :return: column

    """
    ninetieth = np.percentile(data[column_name], 90)
    data[column_name] = np.where(data[column_name] > ninetieth, ninetieth, data[column_name])
    return data[column_name]


def age_range(data, age_column: str):
    """
    Split age column to bins.

    :param data: dataframe variable

    :param age_column: age column as a string

    :return: age bins column
    """
    data[age_column] = pd.cut(x=data[age_column], bins=[0, 18, 30, 40, 50, 60, 70, 80, 90, 100])
    return data[age_column]


def concat_data(data_one, data_two):
    """
    Concat data.

    :param data_one: variable

    :param data_two: variable

    :return: concat dataframe
    """
    frames = [data_one, data_two]
    concat_df = pd.concat(frames, axis=1)
    return concat_df