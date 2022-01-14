"""
This python file is used to perform Associative Classification (AC) of the FP-growth ARM on different ways of classification approaches.

Author : Cheryl Neoh
"""
# In-built imports
import pandas as pd
from sklearn import metrics, svm
from sklearn.model_selection import train_test_split

# Local imports
from datapreprocess import preprocess_data, encode_data
from modifiedfpgrowth import get_classification_association_rules


def support_vector_machine(features, target):
    """ This function performs Support Vector Classification method on the data and provides the accuracy of the model.

    Args:
        features (list): A list of 0 and 1s, where each column represents a value of a feature.
        target (list): A list containing all the class labels of the target.

    Returns:
        float: The accuracy results
    """
    training_data, testing_data, training_target, testing_target = train_test_split(
        features, target, test_size=0.3, random_state=1998)

    # fitting the model using training data
    svm_classifier = svm.SVC(kernel='linear')
    svm_classifier.fit(training_data, training_target)

    # classifying/predicting the test data
    prediction = svm_classifier.predict(testing_data)

    # compare results and price accuracy
    return metrics.accuracy_score(prediction, testing_target)


def CARs_as_features(rankedCARs, feature_info, data, class_column):
    """ This function uses the CARs as features approach. By using the exhaustive approach on finding
    the best top k rules to obtain the best accuracy result when classified using the Support Vector Machine.
    The SVM model is fitted by extract the features used in the top k rules.

    Args:
        rankedCARs (dict): A dictionary containing all the CARs that satisfies the minimum support and confidence, where the CARs are ranked
        feature_info (dict): A dictionary containing all the unique values of each feature
        data (pdarray): the dataset
        class_column (int): The index column of the target

    Returns:
        float, int, list: (best accuracy, best k rules used, columns used)
    """
    previous_features = []
    best_results = (-1, None, None)  # (accuracy,k)
    N = len(rankedCARs)

    for num_rules in range(1, N+1):
        top_k_rules = [antecedent for antecedent in list(rankedCARs)[
            :num_rules]]

       # obtain the features used in the top k rules ( requires improvement for efficiency )
        features_to_extract = [class_column]
        for rule in top_k_rules:
            for feature in rule:
                for key in feature_info.keys():
                    if feature in feature_info[key]:
                        features_to_extract.append(key)
        features_to_extract = list(set(features_to_extract))

        # The check is to avoid performing SVM on features we had already performed on
        # filter the data to only remain the features used in the top k rules
        if features_to_extract not in previous_features:
            data_k = data.loc[:, data.columns.isin(features_to_extract)]
            features, target = encode_data(data_k, class_column)
            accuracy_k = support_vector_machine(features, target)
            previous_features.append(features_to_extract)

        # Updating the best_results
        if accuracy_k > best_results[0]:
            best_results = (accuracy_k, num_rules, features_to_extract)

        # Stopping the for loop early, when the all features of the dataset has been used
        if len(features_to_extract) == len(feature_info):
            break

    return best_results

def list_to_dict(alist):
    """
    This function converts a list to a dictionary
    """
    dictionary = {}
    #print(alist)
    print(len(alist))
    for i in range(len(alist)):
        confidence = alist[i][0]
        support = alist[i][1]
        antecedent = alist[i][2]
        consequent = alist[i][3]
        dictionary[antecedent] = (consequent,confidence,support)
    return dictionary

def rankRules(cars):
    """
    This function ranks the rules according to confidence first, followed by support
    """
    cars_list = []
    for rule in cars:
        consequent = cars.get(rule)[0]
        confidence = cars.get(rule)[1]
        support = cars.get(rule)[2]
        antecedant = rule
        cars_list.append([confidence, support, antecedant, consequent])
    cars_list.sort(reverse=True)
    cars_list = list_to_dict(cars_list)
    return cars_list

def test(data, class_column, min_support, min_confidence):
    # Splitting the data into 70:30 ratio for training and testing data
    training_data, testing_data, _, _ = train_test_split(
        data, range(len(data)), test_size=0.3, random_state=1998)

    # obtain information of the feature from the data
    data = pd.DataFrame(data)
    feature_info = {column: list(data[column].unique())
                    for column in data.columns}

    # Generate cars using FP-growth ARM algorithm

    CARs = get_classification_association_rules(
            training_data, feature_info[class_column], min_support, min_confidence)

    # ranked_CARs = {antecedent: consequent for antecedent, consequent in sorted(
    # CARs.items(), key=lambda item: item[1][1], reverse=True)}  # requires improvement

    ranked_CARs = rankRules(CARs)
    print("Done generating CARs")

    # Preparing testing data
    testing_data = pd.DataFrame(testing_data)
    testing_target = testing_data[class_column]
    testing_data.drop(testing_data.columns[class_column], axis=1, inplace=True)
    testing_data = testing_data.values.tolist()

    # Preparing data for Support Vector Machine
    # Support Vector Machine (SVM)
    features, target = encode_data(data, class_column)
    accuracy = support_vector_machine(features, target)
    print("SVM : ", accuracy)

    # CARs as Features approach
    accuracy, k_rules, columns_used = CARs_as_features(
        ranked_CARs, feature_info, data, class_column)
    print("CARs as features : ", accuracy, "[best k : ", k_rules, "]", "Columns used :", columns_used)


if __name__ == "__main__":
    # Dataset imports
    breast_cancer = preprocess_data("breast-cancer.data", missing_value_symbol='?')  # total = 286, training = 200, testing = 86
    # balance_scale = preprocess_data("C:/Users/Cheryl Neoh/Desktop/SEMESTER 2 2020/FIT3162 FYP 2/FIT3162-WhatOnEarth/Datasets/balance-scale.data")
    # car = preprocess_data("C:/Users/Cheryl Neoh/Desktop/SEMESTER 2 2020/FIT3162 FYP 2/FIT3162-WhatOnEarth/Datasets/car.data")   # class_column = 6
    #lymphography = preprocess_data("C:/Users/Cheryl Neoh/Desktop/SEMESTER 2 2020/FIT3162 FYP 2/FIT3162-WhatOnEarth/Datasets/lymphography.data")

    test(breast_cancer, 0, 5, 0.8)
