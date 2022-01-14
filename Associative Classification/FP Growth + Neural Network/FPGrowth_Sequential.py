import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.model_selection import train_test_split
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense
from collections import Counter
from datapreprocess import preprocess_data, encode_data
from modifiedfpgrowth import get_classification_association_rules

def neural_network(x_train,x_test,y_train,y_test,number_of_classes):
    model = Sequential()
    print(x_train.shape[1])
    # first hidden layer + input layer
    model.add(Dense(50,input_dim=x_train.shape[1],activation='sigmoid'))

    # output layer
    model.add(Dense(number_of_classes,activation='sigmoid'))

    model.compile(loss='mean_squared_error',optimizer='adam',metrics=['accuracy'])
    model.fit(x_train,y_train,epochs=200,batch_size=3,verbose=1)
    _,accuracy = model.evaluate(x_test,y_test)
    print('ACCURACY',accuracy*100)
    return accuracy

def preprocess_neuralNetwork(remaining_data,class_col):
    one_dim = []
    for i in range(len(class_col.values)):
        curr = class_col.values[i][0]
        one_dim.append(curr)

    # gets the number of different classes
    number_of_classes = len(Counter(one_dim).keys())
    print(number_of_classes)

    encoder = OneHotEncoder(sparse=False)
    scaled_data = encoder.fit_transform(remaining_data)

    lb_encoder = LabelEncoder()
    scaled_class_col = lb_encoder.fit_transform(class_col)
    scaled_class_col = np_utils.to_categorical(scaled_class_col)

    # scaled_data, scaled_class_col = encode_data(remaining_data,class_col)
    x_train, x_test,y_train,y_test = train_test_split(scaled_data,scaled_class_col, test_size=0.3, random_state=1)
    return  x_train, x_test,y_train,y_test,number_of_classes


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

    # Preparing data for Support Vector Machine
    # Support Vector Machine (SVM)
    new_dataset = CARs_as_features(ranked_CARs, feature_info, data, class_column)
    class_col = new_dataset.iloc[:,[class_column]]
    new_dataset.drop(new_dataset.columns[class_column], axis=1, inplace=True)

    x_train, x_test, y_train, y_test, number_of_classes = preprocess_neuralNetwork(new_dataset,class_col)
    accuracy = neural_network(x_train, x_test, y_train, y_test, number_of_classes)
    print("Neural Network : ", accuracy)


if __name__ == "__main__":
    # Dataset imports
    #breast_cancer = preprocess_data("breast-cancer.data", missing_value_symbol='?')  # total = 286, training = 200, testing = 86
    #balance_scale = preprocess_data("balance-scale.data")
    #car = preprocess_data("car.data")   # class_column = 6
    #lymphography = preprocess_data("lymphography.data")
    #iris = preprocess_data('iris.data')
    breast_wisconsion = preprocess_data('breast-cancer-wisconsin.data')

    #test(breast_cancer, 0, 5, 0.8)
    #test(balance_scale, 0, 5, 0.8)
    #test(car, 6, 5, 0.8)
    #test(iris, 4, 5, 0.8)
    test(breast_wisconsion, 10, 5, 0.8)

