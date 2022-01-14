import pandas as pd
from sklearn import metrics, svm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.utils import shuffle
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense
from collections import Counter

# Local imports
from datapreprocess import preprocess_data, encode_data
from modifiedfpgrowth import get_classification_association_rules

def neural_network(x_train,x_test,y_train,y_test):
    mlp = MLPClassifier(hidden_layer_sizes=(200),max_iter=1000,activation='relu',solver='adam',random_state=1)
    mlp.fit(x_train, y_train)
    predictions = mlp.predict(x_test)
    print(confusion_matrix(y_test, predictions))
    print(classification_report(y_test, predictions))

def preprocess_neuralNetwork(remaining_data,class_col):

    encoder = OneHotEncoder(sparse=False)
    scaled_data = encoder.fit_transform(remaining_data)

    lb_encoder = LabelEncoder()
    scaled_class_col = lb_encoder.fit_transform(class_col)

    x_train, x_test,y_train,y_test = train_test_split(scaled_data,scaled_class_col, test_size=0.3, random_state=1)
    return  x_train, x_test,y_train,y_test


def CARs_as_features(rankedCARs, feature_info, data, class_column):
    N = len(rankedCARs)
    print('Number of ranked CARs',N)
    top_k_rules = [antecedent for antecedent in list(rankedCARs)[:30]]

       # obtain the features used in the top k rules ( requires improvement for efficiency )
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
    return data_k



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

    ranked_CARs = rankRules(CARs)
    print("Done generating CARs")

    new_dataset = CARs_as_features(ranked_CARs, feature_info, data, class_column)
    class_col = new_dataset.iloc[:,[class_column]]
    new_dataset.drop(new_dataset.columns[class_column], axis=1, inplace=True)

    x_train, x_test, y_train, y_test = preprocess_neuralNetwork(new_dataset,class_col)
    neural_network(x_train, x_test, y_train, y_test)


if __name__ == "__main__":
    # Dataset imports
    #breast_cancer = preprocess_data("breast-cancer.data", missing_value_symbol='?')  # total = 286, training = 200, testing = 86
    #balance_scale = preprocess_data("balance-scale.data")
    #car = preprocess_data("car.data")   # class_column = 6
    lymphography = preprocess_data("lymphography.data")
    #iris = preprocess_data('iris.data')

    #test(breast_cancer, 0, 5, 0.8)
    #test(balance_scale, 0, 5, 0.8)
    #test(car, 6, 5, 0.8)
    #test(iris, 4, 5, 0.8)
    test(lymphography, 0, 9, 0.8)

