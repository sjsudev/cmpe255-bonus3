from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix, classification_report

import pickle

import seaborn as sns
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def evaluate(model):
    
    # similar to the Neural Network above

    y_pred = model.predict(X_test)

    print(classification_report(y_test, y_pred))
    
    cf_matrix = confusion_matrix(y_test, y_pred)

    categories  = ['emergency','non-emergency']
    group_names = ['True emergency','False emergency', 'False non-emergency','True non-emergency']
    group_percentages = ['{0:.2%}'.format(value) for value in cf_matrix.flatten() / np.sum(cf_matrix)]

    labels = [f'{v1}\n{v2}' for v1, v2 in zip(group_names,group_percentages)]
    labels = np.asarray(labels).reshape(2,2)

    sns.heatmap(cf_matrix, annot = labels, cmap = 'Blues',fmt = '',
                xticklabels = categories, yticklabels = categories)

    plt.xlabel("Predicted values", fontdict = {'size':14}, labelpad = 10)
    plt.ylabel("Actual values"   , fontdict = {'size':14}, labelpad = 10)
    plt.title ("Confusion Matrix", fontdict = {'size':18}, pad = 20)

logreg_model = LogisticRegression(C = 2, max_iter = 1000, n_jobs=-1)
logreg_model.fit(X_train, y_train) # These variables are defined in my .ipynb notebook.
evaluate(logreg_model)