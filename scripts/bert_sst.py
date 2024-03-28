import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import pandas as pd

tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

#tokenizer.save_pretrained('embed_python/distilbert-base-uncased-finetuned-sst-2-english')
#model.save_pretrained('embed_python/distilbert-base-uncased-finetuned-sst-2-english')

print(type(model))

df = pd.read_csv('dev.tsv', sep='\t')
features = df['sentence']
label = df['label']

correct = 0
num = 0

tp = 0
fp = 0
tn = 0
fn = 0

for i in range(len(features)):
    #print("Completed: " + str((num / len(features)) * 100))
    inputs = tokenizer(features[i], return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
    pred = logits.argmax().item()
    if label[i] == 0 and pred == 0:
        tn += 1
    if label[i] == 0 and pred == 1:
        fp += 1
    if label[i] == 1 and pred == 0:
        fn += 1
    if label[i] == 1 and pred == 1:
        tp += 1

print("Accuracy: " + str(((tp + tn) / (tp + fp + tn + fn)) * 100))
print("TPR: " + str((tp / (tp + fn)) * 100))
print("FPR: " + str((fp / (fp + tn)) * 100))