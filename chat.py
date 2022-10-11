import random
from textblob import TextBlob
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import nltk_utils
import model as model
import json
import torch
import js2py
nltk.download('omw-1.4')


import os
nltk.download('averaged_perceptron_tagger')

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('chatbot.json', 'r') as f:
    intents = json.load(f)

FILE = "data.pth"  #pth is a machine learning model created using pyTorch that consists of pre-existing algorithms
data = torch.load(FILE)
print(data["tags"])


input_size = data["input_size"]
output_size = data["output_size"]
hidden_size = data["hidden_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]


model = model.NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Bot"
main_noun=['marksheet','okay','thank','gtu','fields','event','lab','ncc','canteen','placement','student','sts','nss','bonafide','fee','i-card','icard','id-card','card','id','idcard','admission','detention','scholarship','principal','sport','bot','branch','facility','medical','faculty','department','hostel','mess','library']

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

def get_response(message):

    flag=False

    sentence = nltk_utils.tokenize(message)
    # str1=' '.join(sentence)
    # CorrectWords = nltk_utils.SpellCorrect(str1)
    noun = [lemmatizer.lemmatize(w.lower()) for (w, pos) in TextBlob(message).pos_tags if pos[0] == 'N']

    print(noun)
    # print(list(CorrectWords.split(" ")))
    X = nltk_utils.bag_of_word(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X)


    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]


    print(tag)
    print(prob.item())
    if tag == "okay":
        for intent in intents['intents']:
            if tag == intent['tag']:
                return random.choice(intent['responses'])
    else:
        if prob.item() > 0.60:

            # print(tag)
            # print(intent)
            if tag == "greeting_hello":
                # print("hello")
                for intent in intents['intents']:
                    if tag == intent['tag']:
                        return random.choice(intent['responses'])
            elif tag == "greeting_bye":
                # print("hello")
                for intent in intents['intents']:
                    if tag == intent['tag']:
                        return random.choice(intent['responses'])
            else:
                #  print("else part")
                for i in noun:
                    print(i)
                    if i.lower() in main_noun:
                        flag = True

                print(flag)
                if flag == False:
                    for i in  sentence:
                        #print(f'second: ".format{i.lower()}')
                        if(i.lower() in main_noun):
                            flag = True

                print(flag)
                if flag == True:
                    #     print("inside true")
                    print(tag)
                    # print(intent['tag'])
                    for intent in intents['intents']:
                        if tag == intent['tag']:
                            return random.choice(intent['responses'])

                return "Ask appropriate question"
        else:
            return "Ask appropriate question"
