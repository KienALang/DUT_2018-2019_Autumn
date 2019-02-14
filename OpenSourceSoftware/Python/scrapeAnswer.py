import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
# from sklearn.neighbors import KNeighborsClassifier
# Create dataframe contain .csv
url = './data_mobile.csv'
df = pd.read_csv(url, encoding='utf-8')
X = df.iloc[:, 1] # Get all data at column 1; iloc[:,:4] => get from column 1 -> 3
Y = df.iloc[:, 2] # Get all data at column 2

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2) # test size 20%
cls = DecisionTreeClassifier()
cls.fit(X_train, Y_train) # X_train, Y_train must be number
comment = ['Điện thoại màn hình quá tệ']