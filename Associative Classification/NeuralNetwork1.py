from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.utils import shuffle
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense



def load_data(filename,class_col_number):
    dataset = pd.read_csv(filename)

    class_col = dataset.iloc[:, [class_col_number]]
    dataset.drop(dataset.columns[class_col_number], axis=1, inplace=True)

    # rest = dataset.astype(str)
    #class_col = class_col.values.reshape((len(class_col)),1)

    return dataset,class_col

def preprocess(dataset,class_col):
    encoder = OneHotEncoder(sparse=False)
    scaled_data = encoder.fit_transform(dataset)

    lb_encoder = LabelEncoder()
    scaled_target_column = lb_encoder.fit_transform(class_col)
    scaled_target_column = np_utils.to_categorical(scaled_target_column)

    return scaled_data, scaled_target_column

def neural_network(x_train,x_test,y_train,y_test,number_of_classes):
    if number_of_classes == 2:
        number_of_classes = 1

    model = Sequential()
    print(x_train.shape[1])
    model.add(Dense(100,input_dim=x_train.shape[1],activation='relu'))
    model.add(Dense(number_of_classes,activation='sigmoid'))
    model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
    model.fit(x_train,y_train,epochs=50,batch_size=16)
    _,accuracy = model.evaluate(x_test,y_test)
    print('ACCURACY',accuracy*100)

def run():
    #rest,class_col = load_data('breast-cancer.data',0)
    #rest,class_col = load_data('car.data',6)
    #rest,class_col = load_data('iris.data', 4)
    #rest,class_col = load_data('balance-scale.data', 0)
    rest,class_col = load_data('seeds.csv', 7)
    # rest,class_col = load_data('wine.data', 0)
    print(class_col)
    number_of_classes = pd.Index(class_col).nunique()

    scaled_data, scaled_target_column = preprocess(rest,class_col)
    x_train, x_test,y_train,y_test = train_test_split(scaled_data,scaled_target_column, test_size=0.3, random_state=1)
    neural_network(x_train, x_test,y_train,y_test,number_of_classes)

run()