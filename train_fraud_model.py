import pickle
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

# Sample dataset (replace with real fraud/non-fraud messages)
messages = [
    ("You have won $1000! Click here to claim", 1), 
    ("Your bank account has been locked. Contact support", 1), 
    ("Meeting at 5 PM today?", 0),  
    ("Congratulations! You've been selected for a free gift", 1), 
    ("Can you call me later?", 0)
]

# Data Preparation
nltk.download('stopwords')
texts, labels = zip(*messages)
vectorizer = CountVectorizer(stop_words="english")
X = vectorizer.fit_transform(texts)
y = labels

# Train Model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = MultinomialNB()
model.fit(X_train, y_train)

# Save Model and Vectorizer
pickle.dump(model, open("fraud_sms_model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("✅ Model and Vectorizer saved successfully!")
