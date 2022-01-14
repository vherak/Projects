"""
This file contains the following methods :
    a) preprocess_data :- reads in a DATA file or csv file and preprocesses the data
    b) clean_data :- impute missing values in an item
    c) attributize_data :- concat attribute names to their values, to ensure they are differentiable in the rules.
    d) encode_data :- convert features in dataset into seperate columns, where each value becomes 0 and 1 and encode the class label (binary)


Author : Cheryl Neoh
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder


def preprocess_data(path_to_data, header=None, missing_value_symbol=None):
    """ This function reads a file from the path provided, it can only read DATA Files (attributes seperated by commas (,) only)
    and csv files. It will also check for any missing values, and perform imputation. File must only contain categorical features.

    Args:
        path_to_data (str): the path to the file
        header (bool/int, optional): If the file contains a header, supply with the index of the header in the file. Defaults to None.
        missing_value_symbol (char, optional): If there is missing values, input the symbol used to indicate a missing value. Defaults to None.

    Returns:
        list: A python list array of the data
    """
    data = pd.read_csv(path_to_data, header=header, dtype=str)

    # convert any missing values in the data into NULL, so that it recognizable by python
    # then, replace the missing values in the data by imputing
    if missing_value_symbol is not None:
        data.replace(to_replace=[missing_value_symbol],
                     value=np.nan, inplace=True)
        clean_data(data)

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
