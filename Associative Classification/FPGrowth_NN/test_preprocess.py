from datapreprocess3 import preprocess_data
import pandas as pd

if __name__ == "__main__":
    # Dataset imports
    breast_cancer = preprocess_data("breast-cancer.data", 0,missing_value_symbol='?')  # total = 286, training = 200, testing = 86
    breast_cancer = pd.DataFrame(breast_cancer)
    breast_cancer.to_csv('testing')
    #balance_scale = preprocess_data("balance-scale.data",0)
    #car = prep