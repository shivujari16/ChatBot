import random
import json
import pickle
import numpy as np
import nltk
import torch
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

intents = json.loads(open('chatbot.json').read())

words = []
classes = []
documents = []  # Combination of words and classes
ignore = ['?', '!', ',', '.']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

lemmatizer = WordNetLemmatizer()
words = [lemmatizer.lemmatize(word) for word in words if word not in ignore]
words = sorted(set(words))
classes = sorted(set(classes))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

training = []
output = [0] * len(classes)

for document in documents:
    bag = []
    word_pattern = document[0]  # words only(not classes)
    word_pattern = [lemmatizer.lemmatize(word.lower()) for word in word_pattern]
    for word in words:
        if word in word_pattern:
            bag.append(1)
        else:
            bag.append(0)

    output_row = list(output)
    output_row[classes.index(document[1])] = 1  # particular class(tag) is marked as 1
    training.append([bag, output_row])
    # print(output_row)
    # print("-----------------------------------------------")

random.shuffle(training)
training = np.array(training)

x_train = list(training[:, 0])  # words
y_train = list(training[:, 1])  # classes

model = Sequential()
model.add(Dense(128, input_shape=(len(x_train[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(len(y_train[0]), activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
bot = model.fit(np.array(x_train), np.array(y_train), epochs=200, batch_size=5, verbose=1)
model.save("chatbot.h5", bot)


