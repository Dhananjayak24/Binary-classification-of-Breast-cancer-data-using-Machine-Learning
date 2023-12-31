# -*- coding: utf-8 -*-
"""binary_classification_breast_cancer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HzLd9KcRTfIZlKHRn7Wp3UL1OliB9BTR
"""

#importing everything

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np

"""importing data"""

file=pd.read_csv("/content/drive/MyDrive/Colab Notebooks/data breastcancer/data.csv")

"""printing data"""

#print(file.describe().T)
#print(file['diagnosis'].unique())
file.dropna(axis=1, inplace=True)
print(file)

"""check for Null data and remove"""

nan_values = file.isna().any().any()
if nan_values:
    print("There are NaN values in the DataFrame.")
else:
    print("No NaN values in the DataFrame.")

total_missing_values = file.isna().sum().sum()

print("Total number of missing values: ", total_missing_values)

# Load your data into a DataFrame
#df = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/data breastcancer/data.csv")  # Replace 'your_data.csv' with your data file

file.dropna(inplace=True)  # Modifies the original DataFrame in place

nan_values = file.isna().any().any()
if nan_values:
    print("There are NaN values in the DataFrame.")
else:
    print("No NaN values in the DataFrame.")

print(file)

"""Rename dataset to label to make it easy to understand"""

file=file.rename(columns={'diagnosis':'label'})
print(file.dtypes)

"""Plotting the labels"""

print(file['label'].unique())

sns.countplot(x="label",data=file)

"""replacing Categorical values with integers"""

print("Distribution of data :", file['label'].value_counts())
#define the dependent variable to be predicted
y=file["label"].values
print("Labels before encoding are :",np.unique(y))

"""Encoding B and M to integers"""

from sklearn.preprocessing import LabelEncoder
labelencoder=LabelEncoder()
y=labelencoder.fit_transform(y)
print("Labels after encoding are : ",np.unique(y))

"""define x or independent variable"""

x=file.drop(labels=["label","id"],axis=1)
print(x.describe().T)

"""Scale or normalise"""

from sklearn.preprocessing import MinMaxScaler
scaler=MinMaxScaler()
scaler.fit(x)
x=scaler.transform(x)
print(x)

"""splitting data into test and train sets"""

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test= train_test_split(x,y,test_size=0.25, random_state=42)
print("Shape of the training data is : ", x_train.shape)
print("Shape of testing data is : ", x_test.shape)

"""importing libraries"""

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout

"""Building model"""

model= Sequential()
model.add(Dense(16,input_dim=30, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(1))
model.add(Activation('sigmoid'))
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
print(model.summary())

"""#Fit model
###here we used history dictionary to save it to it and at the end we can plot the graph
###here verbose is kept 1 to print progress id set to "0" to not to display anything
###epochs is used to iterate over everything in data
"""

history= model.fit(x_train, y_train, verbose=1,epochs=100,batch_size=64,validation_data=(x_test,y_test))

print(history.history)

"""Plotting
plotting training and validation loss
"""

loss = history.history['loss']
validation_loss = history.history['val_loss']
epochs = range(1,len(loss)+1)

plt.plot(epochs, loss, 'y', label='Training loss')
plt.plot(epochs, validation_loss, 'g', label='Validation loss')
plt.title("Training and Validation Loss")
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

"""This is using different library"""

import plotly.express as px
import pandas as pd

# Create a DataFrame for the loss and validation_loss data
loss_df = pd.DataFrame({'Epochs': epochs, 'Training Loss': loss, 'Validation Loss': validation_loss})

# Create a line plot using Plotly
fig = px.line(loss_df, x='Epochs', y=['Training Loss', 'Validation Loss'], title="Training and Validation Loss")
fig.update_xaxes(title_text='Epochs')
fig.update_yaxes(title_text='Loss')

# Show the plot
fig.show()

"""Plotting Training and Validation Accuracy"""

accuracy = history.history['accuracy']
validation_accuracy = history.history['val_accuracy']
epochs = range(1,len(loss)+1)

plt.plot(epochs, accuracy, 'y', label='Training accuracy')
plt.plot(epochs, validation_accuracy, 'g', label='Validation Accuracy')
plt.title("Training and Validation Accuracy")
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

"""Predicting test set results
convert it to 0 and 1 values
"""

y_pred=model.predict(x_test)
y_pred=(y_pred > 0.5)
print(y_test)

"""Preparing Confusion Matrix"""

from sklearn.metrics import confusion_matrix
cm=confusion_matrix(y_test,y_pred)
sns.heatmap(cm,annot=True)