from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.utils import shuffle

def load_dataset(filename,class_col_number):
    dataset = pd.read_csv(filename)
    # separates class and rest of the data
    class_col = dataset.iloc[:,[class_col_number]]
    dataset.drop(dataset.columns[class_col_number],axis =1, inplace=True)
    return dataset,class_col

def preprocess_data(class_col,dataset):
    encoder = OneHotEncoder(sparse=False)
    scaled_data = encoder.fit_transform(dataset)
    lb_encoder = LabelEncoder()
    scaled_target_column = lb_encoder.fit_transform(class_col)

    print(scaled_data)

    return scaled_data,scaled_target_column


# multilayer perceptron classifier
# MLP implements backpropagation
# 3 layers with 13 neurons each for 500 iterations
def mlp_classify(x_train, x_test, y_train, y_test):
    mlp = MLPClassifier(hidden_layer_sizes=(100,100,100), max_iter=2000,activation='relu',solver='adam',random_state=1)
    mlp.fit(x_train,y_train)
    predictions = mlp.predict(x_test)
    print(confusion_matrix(y_test,predictions))
    print(classification_report(y_test,predictions))

def run():
    #data,class_col = load_dataset('breast-cancer.data',0)
    #data,class_col = load_dataset('car.data',6)
    #data, class_col = load_dataset('iris.data', 4)
    #data, class_col = load_dataset('balance-scale.data', 0)
    data, class_col = load_dataset('seeds.csv', 7)
    #data, class_col = load_dataset('wine.data', 0)

    scaled_data,scaled_target_column= preprocess_data(class_col,data)

    # splits the data according to train and test data
    x_train, x_test, y_train, y_test = train_test_split(scaled_data, scaled_target_column, test_size=0.3, random_state=1)

    scaler = StandardScaler()
    scaler.fit(x_train)
    x_train = scaler.transform(x_train)
    x_test = scaler.transform(x_test)

    mlp_classify(x_train, x_test, y_train, y_test)

run()
#precision = TP/Actual Results
# recall = TP/Predicted results (how many are correctly classified)
# f1 score: mean between recall and precision
# support: number of occurecne