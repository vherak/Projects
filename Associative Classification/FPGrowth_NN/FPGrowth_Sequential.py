import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.model_selection import train_test_split
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense
from collections import Counter
from datapreprocess2 import preprocess_data, encode_data
from modifiedfpgrowth import get_classification_association_rules
import information_gain as ig

def neural_network(x_train,x_test,y_train,y_test,number_of_classes,hidden_nodes,ig_list):

    for i in range(len(ig_list)):
        ig_list[i] = ig_list[i].astype('float32',casting = 'same_kind')

    model = Sequential()
    # first hidden layer + input layer
    model.add(Dense(hidden_nodes,input_dim=x_train.shape[1],activation='sigmoid'))
    # output layer
    model.add(Dense(number_of_classes,activation='softmax'))

    for layer in range(len(model.layers)):
        if layer == 0:
            print(model.layers[0].get_weights()[0])

    model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

    # trains neural network 100 times
    model.fit(x_train,y_train,epochs = 100,verbose=0)

    _,accuracy = model.evaluate(x_test,y_test)
    print('ACCURACY',accuracy*100)
    return accuracy

def get_ig(data,info_gain):
    columns_used = [2, 3, 4, 5, 8]
    print(data)
    info_gain_list = []
    i=0
    for col in range(len(columns_used)):
        values = data.iloc[:,col]
        unique = len(pd.unique(values))
        ig_value = info_gain[columns_used[col]]
        for i in range(unique):
            info_gain_list.append(ig_value)
    return info_gain_list


def preprocess_neuralNetwork(remaining_data,class_col,info_gain):
    ig_list = get_ig(remaining_data, info_gain)

    one_dim = []
    for i in range(len(class_col.values)):
        curr = class_col.values[i][0]
        one_dim.append(curr)

    # gets the number of different classes
    number_of_classes = len(Counter(one_dim).keys())

    # encodes the attribute columns
    encoder = OneHotEncoder(sparse=False)
    scaled_data = encoder.fit_transform(remaining_data)

    # encodes class column
    lb_encoder = LabelEncoder()
    scaled_class_col = lb_encoder.fit_transform(class_col)
    scaled_class_col = np_utils.to_categorical(scaled_class_col)

    # converting into an array
    scaled_data = np.array(scaled_data)
    scaled_class_col = np.array(scaled_class_col)

    # splitting into test and train
    x_train, x_test,y_train,y_test = train_test_split(scaled_data,scaled_class_col, test_size=0.3, random_state=1)
    return  x_train, x_test,y_train,y_test,number_of_classes,ig_list


def CARs_as_features(rankedCARs, feature_info, data, class_column):
    N = len(rankedCARs)
    top_k_rules = [antecedent for antecedent in list(rankedCARs)[:50]]

    features_to_extract = [class_column]
    for rule in top_k_rules:
        for feature in rule:
            for key in feature_info.keys():
                if feature in feature_info[key]:
                    features_to_extract.append(key)
    features_to_extract = list(set(features_to_extract))

    data_k = data.loc[:, data.columns.isin(features_to_extract)] # this is the column that is filtered.

    # for printing purposes
    pd.DataFrame(data_k).to_csv('test.csv',index=False,header=False)
    print(features_to_extract)
    return data_k

def CARs_as_features_test(rankedCARs, feature_info, data, class_column):
    previous_features = []
    best_results = (-1, None, None)  # (accuracy,k)
    N = len(rankedCARs)

    for num_rules in range(1, 200):
        top_k_rules = [antecedent for antecedent in list(rankedCARs)[:num_rules]]

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
            data_k = data.loc[:, data.columns.isin(features_to_extract)]  # this is the column that is filtered.
            class_col = data_k.iloc[:, [-1]]
            data_k.drop(data_k.columns[-1], axis=1, inplace=True)
            x_train, x_test, y_train, y_test, number_of_classes = preprocess_neuralNetwork(data_k, class_col)
            accuracy_k = neural_network(x_train, x_test, y_train, y_test, number_of_classes, 50)
            previous_features.append(features_to_extract)

        if accuracy_k > best_results[0]:
            best_results =  (accuracy_k, num_rules, features_to_extract)

        if len(features_to_extract) == len(feature_info):
            break

    return best_results

def list_to_dict(alist):
    """
    This function converts a list to a dictionary
    """
    dictionary = {}
    #print(alist)
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

def test(data, min_support, min_confidence):
    class_column = len(pd.DataFrame(data).columns) -1
    print('CLASS COL',class_column)

    info_gain = ig.information_gain(pd.DataFrame(data), class_column)
    print('INFO GAIN',info_gain)
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

    ranked_CARs = ig.rankRule_IG_conf_sup(CARs,info_gain,feature_info)
    new_ranked = ranked_CARs[::50]
    print('RANKED',len(new_ranked))
    print("Done generating CARs")

    new_dataset = CARs_as_features(ranked_CARs, feature_info, data, class_column)
    class_col = new_dataset.iloc[:,[-1]]
    new_dataset.drop(new_dataset.columns[-1], axis=1, inplace=True)

    hidden_nodes = 5
    x_train, x_test, y_train, y_test, number_of_classes,ig_list = preprocess_neuralNetwork(new_dataset, class_col,info_gain)
    accuracy = neural_network(x_train, x_test, y_train, y_test, number_of_classes,hidden_nodes,ig_list)
    print("Neural Network : ", accuracy)


if __name__ == "__main__":
    # Dataset imports
    breast_cancer = preprocess_data("breast-cancer.data", 0,missing_value_symbol='?')  # total = 286, training = 200, testing = 86
    # print(breast_cancer)
    #balance_scale = preprocess_data("balance-scale.data",0)
    #car = preprocess_data("car.data",6)   # class_column = 6
    #balance_scale = preprocess_data("balance-scale.data",0)
    #lymphography = preprocess_data("lymphography.data",0)
    #iris = preprocess_data('iris.data',4,numeric_columns=[0,1,2,3])
    #breast_wisconsion = preprocess_data('breast-cancer-wisconsin.data',10)

    test(breast_cancer, 5, 0.8)
    #test(balance_scale, 5, 0.8)
    #test(car, 5, 0.8)
    #test(iris, 5, 0.8)
    #test(breast_wisconsion, 5, 0.8)
    #test(lymphography,30,0.8)


