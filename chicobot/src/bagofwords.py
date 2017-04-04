import csv
import random
import sklearn


from sklearn.model_selection import cross_val_score
from sklearn.metrics import f1_score, classification_report, accuracy_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC, SVC


def perform_crossval(cls, data, target):
   print cls.__class__.__name__  
   def scorer(estimator, X, y):
       pred = estimator.predict(X)
       return f1_score(y, pred, average='micro')
   
   def scorer_macro(estimator, X, y):
       pred = estimator.predict(X)
       print classification_report(y, pred)
       print accuracy_score(y, pred)
       return f1_score(y, pred, average='micro')
   
   scores = cross_val_score(cls, data, target, scoring=scorer_macro, cv=3)
   print scores
   return scores
def evaluate_models(data, target):
   gb = GaussianNB()
   logistic_reg = LogisticRegression(class_weight='balanced')
   linear_svm = LinearSVC(class_weight='balanced')
   #svm = SVC(class_weight='balanced',probability=True)
   best = 0
   ret_val = None
   
   for cls in [gb, logistic_reg, linear_svm]:
       scores = perform_crossval(cls, data, target)
       sum_score = sum(list(scores)) / len(scores)
       print "avg score: " + str(sum_score)
       if sum_score > best:
           ret_val = cls
           best = sum_score
   print "winner: " + ret_val.__class__.__name__
   ret_val.fit(data, target)
   return ret_val
'''
Created on March 25, 2017

@author: ThomasC
'''

subjectList = []
labelList = []
classiferList = [GaussianNB, LogisticRegression, LinearSVC, SVC]
counts = {}
thresh = 50

with open('../data/result.tsv','rb') as tsvin:
    tsvin = [r for r in csv.reader(tsvin, delimiter='\t')]
    
    for row in tsvin:
        print(row)
        if row[0] in counts:
            counts[row[0]] += 1
        else:
            counts[row[0]] = 1
 
        
    for row in tsvin:
        if counts[row[0]] > thresh:
            labelList.append(row[0])
            subjectList.append(row[1])

    


print "Creating the bag of words...\n"

# Initialize the "CountVectorizer" object, which is scikit-learn's
# bag of words tool.  
vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 5000) 

# fit_transform() does two functions: First, it fits the model
# and learns the vocabulary; second, it transforms our training data
# into feature vectors. The input to fit_transform should be a list of 
# strings.

train_data_features = vectorizer.fit_transform(subjectList)
#labelList

# Numpy arrays are easy to work with, so convert the result to an 
# array
train_data_features = train_data_features.toarray()


print train_data_features.shape

# Take a look at the words in the vocabulary
vocab = vectorizer.get_feature_names()
print vocab


#perform_crossval(gb, train_data_features, labelList)

evaluate_models(train_data_features, labelList)
# clf = evaluate_models(train_data_features, labelList)



clf = LinearSVC()
clf.fit(train_data_features, labelList)


def pred_newemail(email_subj):
    v = vectorizer.transform(email_subj)
    return clf.predict(v)

print pred_newemail(["iphone"])
