import json
from nltk_utils import tokenize, stemming, bag_of_word
import numpy as np
import torch
import torch.nn  as nn
from torch.utils.data import Dataset, DataLoader
import model

with open('chatbot.json', 'r') as f:
    intents = json.load(f)

all_words = []
tags = []
tag_word = []

for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        w = tokenize(pattern)
        all_words.extend(w)
        tag_word.append((w, tag))
        

# print(all_words)
# print(tag_word)
# print(tags)

ignore_word = ['!', '?', '.', ',']

all_words = [stemming(w) for w in all_words if w not in ignore_word]
all_words = sorted(set(all_words))

X_train = []
y_train = []

for (pattern, tag) in tag_word:
    bag = bag_of_word(pattern, all_words)
    X_train.append(bag)

    label = tags.index(tag)
    y_train.append(label) 

X_train = np.array(X_train)
y_train = np.array(y_train)

# print(X_train)
# print(y_train)

class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.n_samples

# HyperParameters
batch_size = 8
hidden_size = 10
output_size = len(tags)
input_size = len(all_words)
learning_rate = 0.001
num_epochs = 500


dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.NeuralNet(input_size, hidden_size, output_size).to(device)

# loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(device, dtype=torch.long)

        # forward
        output = model(words)
        loss = criterion(output, labels)

        # backward and optimizer step
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if (epoch + 1) % 100 == 0:
        print(f'epoch {epoch+1}/{num_epochs}, loss={loss.item():.4f}')


print(f'final loss, loss={loss.item():.4f}')

data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "output_size": output_size,
    "hidden_size": hidden_size,
    "all_words": all_words,
    "tags": tags
}

FILE = "data.pth"
torch.save(data, FILE)

print(f'Training Completed. File saved to {FILE}')
