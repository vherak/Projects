"""
This python file is used to perform Associative Classification (AC) of the FP-growth ARM on different ways of classification approaches.

Author : Cheryl Neoh
"""
# In-built imports
import pandas as pd
from sklearn import metrics, svm
from sklearn.model_selection import train_test_split

# Local imports
from datapreprocess import preprocess_data, encode_data, information_gain
from modifiedfpgrowth import get_classification_association_rules


def strongest_rules(rankedCARs, testing_data, default):
    """ This function is using the strongest CARs approach, where the class label of the strongest CAR, which covers the conditions of a test instance will be used for classification.
    The strength of the CAR is measured using the confidence.

    Args:
        rankedCARs (dict): A dictionary containing all the CARs that satisfies the minimum support and confidence, where the CARs are ranked
        testing_data ([str]): A list of test instances to be used to evaluate the performance of the CARs produced
        default (str): The default value assigned if the test instance cannot be classified

    Returns:
        list: A list of the predicted class labels of the testing data
    """
    predicted_results = []

    for instance in testing_data:
        best_prediction = None
        best_confidence = -1

        for rule in rankedCARs:
            if all(x in instance for x in list(rule)):
                consequent, confidence = rankedCARs.get(rule)
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_prediction = consequent[0]

        if best_prediction == None:
            predicted_results.append(default)
        else:
            predicted_results.append(best_prediction)

    return predicted_results


def multiple_rules(rankedCARs, testing_data, default):
    """ This function is using the combination of multiple CARs to classify a test instance, When classifying a test instance, it will gather a subset of CARs
    that satisfy the instance, if all the CARs in the subset have the same class, then the class will be applied to the test instance. If the CARs have inconsistent
    classes, they will be divided into different groups according to their class labels. Then, the strongest group will be assigned to the test instance.

    Args:
        rankedCARs (dict): A dictionary containing all the CARs that satisfies the minimum support and confidence, where the CARs are ranked
        testing_data ([str]): A list of test instances to be used to evaluate the performance of the CARs produced
        default (str): The default value assigned if the test instance cannot be classified

    Returns:
        list: A list of the predicted class labels of the testing data
    """
    predicted_results = []

    for instance in testing_data:

        all_subset = []
        for rule in rankedCARs:
            if all(x in instance for x in list(rule)):
                consequent, _ = rankedCARs.get(rule)
                all_subset.append(consequent[0])

        if len(all_subset) == 0:
            predicted_results.append(default)
        elif all_subset[1:] == all_subset[:-1]:    # consistent class labels
            predicted_results.append(all_subset[0])
        else:                                      # inconsistent class labels
            all_subset = pd.DataFrame(all_subset, columns=['target'])
            most_frequent = all_subset["target"].value_counts().rename_axis(
                'target').reset_index(name='counts')['target'][0]
            predicted_results.append(most_frequent)

    return predicted_results


def support_vector_machine(features, target):
    """ This function performs Support Vector Classification method on the data and provides the accuracy of the model.

    Args:
        features ([str]): A list of 0 and 1s, where each column represents a value of a feature.
        target ([str]): A list containing all the class labels of the target.

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


def CARs_as_features_SVM(rankedCARs, feature_info, data, class_column):
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

    for num_rules in range(5, N+1):
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


def test(data, class_column, min_support, min_confidence):
    # filtering redundant features in the dataset using Information Gain (IG)
    data = pd.DataFrame(data)
    info_gain = information_gain(data, class_column)
    data_columns = list(data.columns)


    # obtain information of the feature from the data
    feature_info = {column: list(data[column].unique())
                    for column in data.columns}

    # Splitting the data into 70:30 ratio for training and testing data
    training_data, testing_data, _, _ = train_test_split(
        data.values.tolist(), range(len(data)), test_size=0.3, random_state=1998)

    # Generate cars using FP-growth ARM algorithm
    try:
        CARs = get_classification_association_rules(
            training_data, feature_info[class_column], min_support, min_confidence)
    except MemoryError:
        pass

    ranked_CARs = {antecedent: consequent for antecedent, consequent in sorted(
        CARs.items(), key=lambda item: item[1][1], reverse=True)}  # requires improvement
    default_value = list(ranked_CARs.values())[0][0][0]

    print("Done generating CARs")

    # Preparing testing data
    testing_data = pd.DataFrame(testing_data, columns = data_columns)
    testing_target = testing_data[class_column]
    testing_data.drop(columns=class_column, axis=1, inplace=True)
    testing_data = testing_data.values.tolist()

    # Strongest CARs approach
    predicted_target = strongest_rules(
        ranked_CARs, testing_data, default_value)
    accuracy = metrics.accuracy_score(predicted_target, testing_target)
    print("Strongest CARS : ", accuracy)

    # Combine Multiple CARs approach
    predicted_target_1 = multiple_rules(
        ranked_CARs, testing_data, default_value)
    accuracy = metrics.accuracy_score(predicted_target_1, testing_target)
    print("Combine Multiple CARS : ", accuracy)

    # Preparing data for Support Vector Machine
    # Support Vector Machine (SVM)
    features, target = encode_data(data, class_column)
    accuracy = support_vector_machine(features, target)
    print("SVM : ", accuracy)

    # CARs as Features approach
    accuracy, k_rules, columns_used = CARs_as_features_SVM(
        ranked_CARs, feature_info, data, class_column)
    print("CARs as features : ", accuracy, "[best k : ", k_rules, "]", "Columns used :", columns_used)


if __name__ == "__main__":
    # Dataset imports
    # breast_cancer = preprocess_data("./Datasets/breast-cancer.data", missing_value_symbol='?')  # total = 286, training = 200, testing = 86, min_supp = 10
    # balance_scale = preprocess_data("./Datasets/balance-scale.data") # 625 instances, min_supprt = 10
    # iris = preprocess_data("./Datasets/iris.data", numeric_columns = [0,1,2,3]) # 150 instances , min_supprt = 5
    # car = preprocess_data("./Datasets/car.data")   # class_column = 6, 1727 instances, min_support = 30
    lymphography = preprocess_data("./Datasets/lymphography.data") # 148 instances, min_support = 4

    test(lymphography, 0, 4, 0.8)
