from sqlalchemy.orm import sessionmaker
import lib.etl.sqlConnection as sqlConnection
import numpy as np
from keras.utils import plot_model
from keras.models import Sequential
from keras.models import Model
from keras.layers import Input
from keras.layers import Dense

# Sequential NN for Classification of highlights - Does not include 'word' feature
def customSequentialNN(table_name):
    nnDf = sqlConnection.getTableAsDf(table_name)
    # Split into input (X) and output (y) variables
    X = nnDf[['excited_speech', 'pitch', 'amplitude', 'subjectivity', 'polarity']]
    y = nnDf[['highlight']]
    # Define the keras model
    model = Sequential()
    model.add(Dense(10, input_dim=5, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    # Compile the keras model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    # Fit the keras model on the dataset
    model.fit(X, y, epochs=150, batch_size=10)
    # Evaluate the keras model
    _, accuracy = model.evaluate(X, y)
    print('Accuracy: %.2f' % (accuracy*100))
    # Make class predictions with the model
    predictions = model.predict_classes(X)
    # Summarize the first 5 cases
    for i in range(5):
        print('%s => %d (expected %d)' % (X[i].tolist(), predictions[i], y[i]))
