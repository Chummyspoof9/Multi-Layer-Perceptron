"""
CS340 Course Project

This program will offer a 6 option menu that reads data from
a txt file and trains an ANN for pattern classification.

Open source code, released under the GNU Public License
Pavlos Constantinou, 20210366@student.act.edu 09/05/2023
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler

import matplotlib.pyplot as plt


def menuoptions():
    print("==================================================")
    print("USER MENU: MLP CLASSIFICATION OF THE WINE DATA SET (UCI REPOSITORY)")
    print("==================================================")
    print("1. Read the labelled text data file, display the first 5 lines")
    print("2. Choose the size of the hidden layers of the MLP topology (e.g. 6-?-?-2)")
    print("3. Choose the size of the training step (0.001 - 0.5, [ENTER] for adaptable)")
    print("4. Train on 80% of labeled data, display progress graph")
    print("5. Classify the unlabeled data, output training report and confusion matrix")
    print("6. Exit the program")


# for global variable usage
data = open("original_labeled_data.txt", "r")
names = ['Buying', 'Maintenance', 'Doors', 'Persons', 'Magnesium', 'Trunk Size', 'Safety']
cardata = pd.read_csv(data, names=names)

y = cardata.select_dtypes(include=[object])  # select the last column

le = preprocessing.LabelEncoder()
cardata['Safety'] = le.fit_transform(cardata['Safety'])

categorical_columns = ['Buying', 'Maintenance', 'Doors', 'Persons', 'Magnesium', 'Trunk Size']
for column in cardata.columns[:-1]:
    cardata[column] = le.fit_transform(cardata[column])

x = cardata.drop('Safety', axis=1)
y = cardata['Safety']
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.20)
"""scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)"""


def option1():
    data = open("original_labeled_data.txt", "r")
    cardata_unlabelled = pd.read_csv(data, names=names)
    print(cardata_unlabelled.head(5))


def option2():
    mlp = MLPClassifier(hidden_layer_sizes=(6, 4, 4, 2), max_iter=1000)
    mlp.fit(X_train, y_train)
    training_data = pd.concat([X_train, y_train], axis=1)
    training_data.to_csv('training_data.txt', index=False, sep='\t')

def option3():
    mlp = MLPClassifier(hidden_layer_sizes=(6, 4, 4, 2),
                        activation='relu',
                        solver= 'adam',
                        learning_rate = 'constant',
                        learning_rate_init = 0.001,
                        max_iter = 500)
    mlp.fit(X_train, y_train)

def option4():
    mlp = MLPClassifier(hidden_layer_sizes=(6, 4, 4, 2),
                        activation='relu',
                        solver='adam',
                        learning_rate='constant',
                        learning_rate_init=0.001,
                        max_iter=500)
    mlp.fit(X_train, y_train)
    X_train_partial, _, y_train_partial, _ = train_test_split(X_train, y_train, train_size=0.8, random_state=42)
    training_progress = mlp.fit(X_train_partial, y_train_partial)
    plt.plot(training_progress.loss_curve_)
    plt.title('Training Loss Curve')
    plt.xlabel('Iteration')
    plt.ylabel('Loss')
    plt.show()


def option5():
    mlp = MLPClassifier(hidden_layer_sizes=(6, 4, 4, 2),
                        activation='relu',
                        solver='adam',
                        learning_rate='constant',
                        learning_rate_init=0.001,
                        max_iter=500)
    mlp.fit(X_train, y_train)
    predict_train = mlp.predict(X_train)
    predict_test = mlp.predict(X_test)

    print('===================================')
    print('EVALUATION AGAINST TRAINING DATASET:')
    print('===================================')
    print(confusion_matrix(y_train, predict_train))
    print(classification_report(y_train, predict_train))

    print('===============================')
    print('EVALUATION AGAINST TEST DATASET:')
    print('===============================')
    print(confusion_matrix(y_test, predict_test))
    print(classification_report(y_test, predict_test))


menuoptions()
option = int(input("Please select an option: "))

while option != 6:
    if option == 1:
        option1()
    elif option == 2:
        option2()
    elif option == 3:
        option3()
    elif option == 4:
        option4()
    elif option == 5:
        option5()
    else:
        print("Invalid option, try again.")

    print()
    menuoptions()
    option = int(input("Please select an option: "))

print("Thank you for using this program!")
