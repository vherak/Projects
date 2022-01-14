"""
This file contains the following methods :
    a) preprocess_data :- reads in a DATA file or csv file and preprocesses the data
    b) clean_data :- impute missing values in an item
    c) attributize_data :- concat attribute names to their values, to ensure they are differentiable in the rules.
    d) encode_data :- convert features in dataset into seperate columns, where each value becomes 0 and 1 and encode the class label (binary)
    e) min_max :- scales numerical attributes to a range from 0 to 1
    f) dicretize_data :- discretize the numerical attribute to convert into categorical data
    g) information_gain :- find the information gain of each feature with the target of the dataset, used in preprocessing dataset and ranking of CARS

Author : Cheryl Neoh, Yi Xian
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, KBinsDiscretizer, minmax_scale
from sklearn.feature_selection import mutual_info_classif


def preprocess_data(path_to_data, header=None, missing_value_symbol=None, numeric_columns=None):
    """ This function reads a file from the path provided, it can only read DATA Files (attributes seperated by commas (,) only)
    and csv files. It will also check for any missing values, and perform imputation. File must only contain categorical features.

    Args:
        path_to_data (str): the path to the file
        header (bool/int, optional): If the file contains a header, supply with the index of the header in the file. Defaults to None.
        missing_value_symbol (char, optional): If there is missing values, input the symbol used to indicate a missing value. Defaults to None.
        numeric_columns ([int], optional): If there are numerical attributes in the data then it will be used to identify the numerical columns. Defaults to None.

    Returns:
        list: A python list array of the data
    """
    data = pd.read_csv(path_to_data, header=header, dtype="str")

    # convert any missing values in the data into NULL, so that it recognizable by python
    # then, replace the missing values in the data by imputing
    if missing_value_symbol is not None:
        data.replace(to_replace=[missing_value_symbol],
                     value=np.nan, inplace=True)
        clean_data(data)

    # scalling using min-max normalization and
    # change numerical attribute columns into categorical attributes
    # numeric_columns = list(data._get_numeric_data().columns)
    # print(numeric_columns)
    if numeric_columns is not None:
        min_max(data, numeric_columns)
        discretize_data(data, numeric_columns)

    attributize_data(data)
    return data.values.tolist()


def clean_data(data):
    """ This function deals with missing values in a dataset, the imputing works on two types of
    data: categorical and numerical. For the categorical missing value, it will impute using the
    most frequent value. As for the numerical missing value, it will impute using the mean value.

    Args:
        data (pdarray): The dataset which could contain some missing values.

    Returns:
        pdarray: The dataset with no missing values.
    """
    # get categorical columns and columns with missing values
    categorical_columns = list(
        set(data.columns) - set(data._get_numeric_data().columns))
    missing_values = list(data.isnull().any())

    for column in range(len(missing_values)):
        if missing_values[column]:
            if column in categorical_columns:
                imputer = SimpleImputer(strategy='most_frequent')
            else:
                imputer = SimpleImputer(strategy='mean')
            imputer.fit(data)
            imputed_data = pd.DataFrame(imputer.transform(data))
            data[column] = imputed_data[column]


def attributize_data(data):
    """ This function adds concatenates the column name with the values, so that when it is used for frequent itemset mining and generation of Classification
    Association Rules (CARs), it will be able to differentiate which column it is taken from. Since, each column has a different meaning.

    Args:
        data (pdarray): The dataset.
    """
    for column in data.columns:
        data[column] = "Feature " + str(column) + " : " + data[column]


def encode_data(data, class_column):
    """ This function discretizes the features and encodes the target column in the dataset. For the features, it converts all the categorical columns in dataset
    into seperate columns, where each value becomes 0 and 1. As for the target column, it will only be bina encode a categorical attribute ( for class labels )

    Args:
        data (pdarray): The data to be discretized and encoded and seperated into target and features
        class_column (int): The index of the class column

    Returns:
        list, list:  two list containing the discretized features and encoded target
    """
    # Encoding target
    target = data[class_column]
    lb_encoder = LabelEncoder()
    target = lb_encoder.fit_transform(target)

    # Discretizing features
    features = data.drop(columns=class_column, axis=1)
    encoder = OneHotEncoder(sparse=False, dtype=int)
    features = encoder.fit_transform(features)

    return features, target


def min_max(data, numeric_columns):
    """ This function scales the numerical attributes into the range of 0 to 1 using the Min-Max Normalisation method.
    This is used before the discretization of the attributes method to reduce the number of categorical attributes produced.

    Args:
        data (pdarray): The data which contains the numerical attributes.
        numeric_columns ([int]): A list containing the indexes of the numerical attributes in the data.
    """
    numeric_data = data.iloc[:, numeric_columns]
    scaled_data = minmax_scale(numeric_data)

    for i in range(len(numeric_columns)):
        data.iloc[:, numeric_columns[i]] = scaled_data[:, i]


def discretize_data(data, numeric_columns):
    """ This function takes the scaled numerical attributes and discretizes the attributes. The number of bins used by the
    discretization method depends on the largest value in all the numerical attributes, to ensure that the number of bins
    is generalised to each dataset.

    Args:
        data (pdarray): The data which contains the scaled numerical attributes.
        numeric_columns ([int]): A list containing the indexes of the numerical attributes in the data.
    """
    numeric_data = data.iloc[:, numeric_columns]
    discretizer = KBinsDiscretizer(n_bins=max(
        numeric_data), encode='ordinal', strategy='quantile')
    discretized_data = discretizer.fit_transform(numeric_data)
    discretized_data = discretized_data.astype(int).astype(
        str)  # convert it to string, as categorical

    for i in range(len(numeric_columns)):
        data.iloc[:, numeric_columns[i]] = discretized_data[:, i]


def information_gain(data, class_column):
    """ This function calculates the information gain (IG) of each feature with the target in the dataset, it is used in preprocessing
    of the dataset, which is feature selection. It removes redundant features in the dataset which has an information gain lower than the
    average of the information gain.

    Args:
        data (pdarray): The dataset which has been preprocessed to contain only categorical attributes
        class_column (int): The index of the target in the dataset

    Returns:
        dict: A dictionary where the key is the index of the column and the value is the information gain.
    """
    target = data[class_column]
    features = data.drop(columns=class_column, axis=1)
    feature_columns = list(features.columns)

    # calculating information gain of the features with the target
    information_gain = mutual_info_classif(
        features.values.tolist(), target, discrete_features=True)
    average = sum(information_gain)/len(list(features.columns))

    # make a dictionary and obtain the columns of the features to be removed from the dataset
    info_gain = {}
    columns_removed = []
    for index in range(len(information_gain)):
        if information_gain[index] >= average:
            info_gain[feature_columns[index]] = information_gain[index]
        else:
            columns_removed.append(feature_columns[index])

    # remove the redundant features
    data.drop(columns=columns_removed, axis=1, inplace=True)
    print(columns_removed)
    return info_gain
