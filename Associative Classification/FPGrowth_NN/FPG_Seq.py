# Inbuilt Imports
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import EarlyStopping

# Local Imports
from datapreprocess import preprocess_data, encode_data, information_gain, chi_square
from modifiedfpgrowth import get_classification_association_rules, rankRule_IG


def SEQ_DNN(X_train,  y_train, X_test, y_test, X_valid, y_valid, number_of_classes, hidden_nodes):
    # building the model
    model = Sequential()
    model.add(Dense(hidden_nodes, input_dim = X_train.shape[1], activation='sigmoid'))
    model.add(Dense(number_of_classes, activation='softmax'))

    #model.summary()

    # creating early stopping optimizer to avoid overfitting
    earlystop_callback = EarlyStopping(monitor='val_loss', min_delta=0.0001, patience=5)

    # fitting the model with the data
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs = 100, validation_data=(X_valid, y_valid), callbacks=[earlystop_callback])

    loss, accuracy = model.evaluate(X_test,y_test)

    print(y_test)

    return (accuracy*100, loss,model)

def feature_selection(rankedCARs, feature_info, data, class_column, k):
    # extracting the top k rules
    top_k_rules = [antecedent for antecedent in list(rankedCARs)[:k]]

    # extracting the columns from these k rules
    features_to_extract = [class_column]
    for rule in top_k_rules:
        for feature in rule:
            for key in feature_info.keys():
                if feature in feature_info[key]:
                    features_to_extract.append(key)
    features_to_extract = list(set(features_to_extract))

    # filtered dataset
    data_k = data.loc[:, data.columns.isin(features_to_extract)]
    return data_k, features_to_extract


def test(data, class_column, min_support, min_confidence):
    info_gain = information_gain(pd.DataFrame(data), class_column)
    # chi_2 = chi_square(pd.DataFrame(data), class_column)
    # return None
    # Splitting the data into 70:15:15 ratio for training data : testing data : validation
    training_data, testing_data, train_rows, test_rows = train_test_split(data, range(len(data)), test_size=0.3, random_state = 1998)

    # obtain information of the feature from the data
    data = pd.DataFrame(data)
    feature_info = {column: list(data[column].unique())
                    for column in data.columns}

    # Generate cars using FP-growth ARM algorithm and ranking them
    CARs = get_classification_association_rules(training_data, feature_info[class_column], min_support, min_confidence)
    ranked_CARs = rankRule_IG(training_data, CARs, info_gain, class_column, feature_info, use_conf_supp=True)
    print("Done generating CARs...")

    # Feature selection using Top k CARs and setting up the training data to fit the NN classifier
    topkdata, columns_used = feature_selection(ranked_CARs, feature_info, data, class_column, 50)
    topkdata, target = encode_data(topkdata, class_column)  # encoding

    # preparing the training data
    training_data = topkdata[train_rows]
    training_target = target[train_rows]

    # preparing validation data and testing data
    testing_data, validation_data, testing_target, validation_target = train_test_split(topkdata[test_rows], target[test_rows], test_size=0.5, random_state = 1998)
    # Fitting the NN classifier
    number_of_classes = len(feature_info[class_column])
    # accuracy_sgd, loss = SDG_DNN(training_data, training_target , testing_data, testing_target, validation_data, validation_target, number_of_classes, hidden_nodes = 50)
    accuracy_seq, loss,model = SEQ_DNN(training_data, training_target , testing_data, testing_target, validation_data, validation_target, number_of_classes, hidden_nodes = 50)

    r = model.predict(testing_data)
    print(r)

    # print("DNN with Stochastic Gradient Descent : ", accuracy_sgd, "Columns used :", columns_used)
    print("Sequential DNN: ", accuracy_seq, "Columns used :", columns_used)



if __name__ == "__main__":
    # Dataset imports
    # total = 286, training = 200, testing = 86, min_supp = 10
    #breast_cancer = preprocess_data("breast-cancer.data", missing_value_symbol='?')
    # balance_scale = preprocess_data("./Datasets/balance-scale.data") # 625 instances, min_supprt = 10
    # iris = preprocess_data("./Datasets/iris.data", numeric_columns = [0,1,2,3]) # 150 instances , min_supprt = 5
    # car = preprocess_data("./Datasets/car.data")   # class_column = 6, 1727 instances, min_support = 30
    # lymphography = preprocess_data("./Datasets/lymphography.data") # 148 instances, min_support = 4
    breast_cancer_wisconsin = preprocess_data("breast-cancer-wisconsin.data", missing_value_symbol='?') #class_column = 10
    # hayes_roth = preprocess_data("./Datasets/hayes-roth.data", remove_columns = [0])
    # wdbc = preprocess_data("./Datasets/wdbc.data", numeric_columns = range(2,32), remove_columns = [0])
    # glass = preprocess_data("./Datasets/glass.data", numeric_columns=range(1,10), remove_columns=[0])
    # krvskp = preprocess_data("./Datasets/kr-vs-kp.data") # takes very long to run
    # tictactoe = preprocess_data("./Datasets/tic-tac-toe.data")
    # nursery = preprocess_data("./Datasets/nursery.data")

    # print(pd.DataFrame(nursery))

    #test(breast_cancer, 0, 20, 0.8)
    # test(balance_scale, 0, 10, 0)
    # test(iris, 4, 5, 0)
    # test(car, 6, 30, 0)
    # test(lymphography, 0, 30, 0)
    test(breast_cancer_wisconsin, 10, 20, 0)
    # test(hayes_roth, 4, 5, 0 ) # 132 instances
    # test(wdbc, 0, 20, 0)
    # test(glass, 9, 5, 0)
    # test(krvskp, 36, 120, 0)
    # test(tictactoe, 9, 30, 0)
    # test(nursery, 8, 450, 0)