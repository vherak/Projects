import pandas as pd
import numpy as np
from modifiedfpgrowth import get_classification_association_rules
from sklearn.feature_selection import mutual_info_classif
from datapreprocess2 import preprocess_data
from sklearn.model_selection import train_test_split


def information_gain(data, class_column):
    target = data[class_column]
    features = data.drop(columns=class_column, axis=1) # dropping the class column
    feature_columns = list(features.columns) # reamining columns

    information_gain = mutual_info_classif(features.values.tolist(), target, discrete_features = True)
    average = sum(information_gain)/len(list(features.columns))

    info_gain = {}
    columns_removed = []
    print(information_gain)
    for index in range(len(information_gain)):
        info_gain[ feature_columns[index] ] = information_gain[index]

    print(info_gain)
    return info_gain # infomation gain of each column (we need to rank according to this)


def list_to_dict_IG(alist):
    """
    This function converts a list to a dictionary
    """
    dictionary = {}
    for i in range(len(alist)):
        info_gain = alist[i][0]
        antecedent = alist[i][1]
        consequent = alist[i][2]
        dictionary[antecedent] = (consequent,info_gain)
    return dictionary

def rankRule_IG(cars,info_gain,feature_info):
    ranked_list = []
    for rule in cars:
        consequent = cars.get(rule)[0]
        antecedant = rule
        key_list = []
        total = 0
        for feature in rule:
            for key in feature_info.keys():
               if feature in feature_info[key]:
                   key_list.append(key)
        for i in range(len(key_list)):
            for item in info_gain:
                if key_list[i] == item:
                    total += info_gain[item]
        average = total/len(key_list)
        ranked_list.append([average,antecedant,consequent])
    ranked_list.sort(reverse=True)
    ranked_dict = list_to_dict_IG((ranked_list))
    return ranked_dict

def list_to_dict_IG_conf_sup(alist):
    """
    This function converts a list to a dictionary
    """
    dictionary = {}
    for i in range(len(alist)):
        confidence = alist[i][0]
        support = alist[i][1]
        info_gain = alist[i][2]
        antecedent = alist[i][3]
        consequent = alist[i][4]
        dictionary[antecedent] = (consequent,info_gain,confidence,support)
    return dictionary

def list_to_dict_new(alist):
    """
    This function converts a list to a dictionary
    """
    dictionary = {}
    for i in range(len(alist)):
        info_gain = alist[i][0]
        conf = alist[i][1]
        sup = alist[i][2]
        length = alist[i][3]
        clas_freq = alist[i][4]
        antecedent = alist[i][5]
        consequent = alist[i][6]
        dictionary[antecedent] = (consequent,conf,sup,info_gain,length,clas_freq)
    return dictionary

def rankRules_cardinality(cars,class_freq,info_gain,feature_info):
    """
    This function ranks the rules according to confidence first, followed by support
    """
    cars_list = []
    #cars = {('Feature (3,) : 0-2', 'Feature (7,) : central'): (('Feature (9,) : no-recurrence-events',), 0.8, 0.04), ('Feature (3,) : 0-2', 'Feature (4,) : no', 'Feature (7,) : central'): (('Feature (9,) : no-recurrence-events',), 0.8, 0.04), ('Feature (3,) : 0-2', 'Feature (7,) : central', 'Feature (8,) : no'): (('Feature (9,) : no-recurrence-events',), 0.8, 0.04)}
    for rule in cars:
        consequent = cars.get(rule)[0]
        confidence = cars.get(rule)[1]
        support = cars.get(rule)[2]
        antecedant = rule
        key_list = []
        total = 0
        for feature in rule:
            for key in feature_info.keys():
                if feature in feature_info[key]:
                    key_list.append(key)
        for i in range(len(key_list)):
            for item in info_gain:
                if key_list[i] == item:
                    total += info_gain[item]
        average = total / len(key_list)
        length = len(antecedant)
        for key in class_freq:
            if key == consequent:
                freq = class_freq[key]
                break

        cars_list.append([average,confidence, support,length,freq, antecedant, consequent])

    print(cars_list)
    cars_list_sorted = sorted(sorted(sorted(sorted(cars_list,key= lambda x:x[3],reverse=True),
                                     key=lambda  x:x[2]),
                                key=lambda x:x[1],reverse=True),
                        key=lambda x:x[0],reverse=True)
    #print('SORTED',cars_list_sorted)
    cars_list_dict = list_to_dict_new(cars_list_sorted)
    return cars_list_dict

def get_cardinality(cars_list):
    cardinality_list =[]
    for i in range(len(cars_list)):
        antecedant = cars_list[i][2]
        consequent = cars_list[i][3]
        cardinality_list.append(len(antecedant))
    # cardinality_list.sort()
    return cardinality_list

def sort_class_frequency(cardinality_list,class_freq):
    # print(class_freq)
    # print(cardinality_list)
    sorted_list =[]
    for i in range(len(cardinality_list)):
        antecedant = cardinality_list[i][1]
        consequent = cardinality_list[i][2]
        #print(consequent)
        for key in class_freq:
            if key == consequent:
                freq = class_freq[key]
                sorted_list.append([freq, antecedant, consequent])
            break

    #print(sorted_list)




def rankRule_IG_conf_sup(cars, info_gain, feature_info):
    ranked_list = []
    for rule in cars:
        consequent = cars.get(rule)[0]
        confidence = cars.get(rule)[1]
        support = cars.get(rule)[2]
        antecedant = rule
        key_list = []
        total = 0
        for feature in rule:
            for key in feature_info.keys():
                if feature in feature_info[key]:
                    key_list.append(key)
        for i in range(len(key_list)):
            for item in info_gain:
                if key_list[i] == item:
                    total += info_gain[item]
        average = total / len(key_list)
        ranked_list.append([average,confidence,support, antecedant, consequent])
    ranked_list.sort(reverse=True)
    ranked_dict = list_to_dict_IG_conf_sup((ranked_list))

    return ranked_dict



def test_IG(data,min_support,min_confidence,class_freq):
    class_column = len(pd.DataFrame(data).columns) - 1

    # gets information gain for each attribute
    info_gain = information_gain(pd.DataFrame(data), class_column)
    training_data, testing_data, _, _ = train_test_split(
        data, range(len(data)), test_size=0.3, random_state=1998)
    training_data = list(training_data)
    # obtain information of the feature from the data
    data = pd.DataFrame(data)
    feature_info = {column: list(data[column].unique())
                    for column in data.columns}

    # Generate cars using FP-growth ARM algorithm
    CARs = get_classification_association_rules(
        training_data, feature_info[class_column], min_support, min_confidence)
    #print(CARs)

    #rankedCARs = rankRule_IG(CARs,info_gain,feature_info)
    rankedCARs = rankRules_cardinality(CARs,class_freq,info_gain,feature_info)
    print(rankedCARs)




# if __name__ == "__main__":
#     # Dataset imports
#     data_set = pd.read_csv('breast-cancer.data')
#     breast_cancer = preprocess_data("breast-cancer.data",0, missing_value_symbol='?')  # total = 286, training = 200, testing = 86
#
#     copy_data = pd.DataFrame(breast_cancer)
#     class_col = copy_data.iloc[:, [-1]]
#     class_freq = class_col.value_counts().to_dict()
#
#
#     test_IG(breast_cancer,8,0.5,class_freq)

    # print(pd.DataFrame(breast_cancer))
    # information_gain(pd.DataFrame(breast_cancer),9)

    # balance_scale = preprocess_data("./Datasets/balance-scale.data")
    # car = preprocess_data("./Datasets/car.data")   # class_column = 6
    # lymphography = preprocess_data("./Datasets/lymphography.data")
    # iris = preprocess_data("./Datasets/iris.data", numeric_columns = [0,1,2,3])
    # lymphography = pd.DataFrame(lymphography)
    # information_gain(lymphography, 0)




