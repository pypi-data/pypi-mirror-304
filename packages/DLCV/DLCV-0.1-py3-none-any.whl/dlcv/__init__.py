# code of dual leaf cross validation
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score,recall_score,f1_score
import numpy as np
def dual_leaf_cross_score(model=None,x=None,y=None,cv=None,verbose=0,metric="mean"):
    """
Evaluate  score by dual-leaf-cross-validation.

Parameters
----------
model : estimator object implementing 'fit', default=None
    The model or estimator to be used for fitting the data.

x : {array-like, sparse matrix} of shape (n_samples, n_features), default=None
    The input data to fit, such as a list or array.

y : array-like of shape (n_samples,) or (n_samples, n_outputs), default=None
    The target variable to predict in supervised learning.

cv : int, cross-validation generator or an iterable, default=None
    Determines the cross-validation splitting strategy.
    Possible values:
    - None: Use the default 5-fold cross-validation.
    - int: Specify the number of folds for cross-validation.
    - CV splitter: Use a custom cross-validation splitter.
    - Iterable: Generate (train, test) splits using arrays of indices.

metric : str, default='mean'
    The metric used for scoring the model. Options might include 
    'mean', 'median', or other custom scoring functions.

Returns
-------
scores : array of float
    Array of cross-validation scores for each split.
    
Examples
--------
>>> from sklearn import datasets, linear_model
>>> from dlcv import dual_leaf_cross_score
>>> diabetes = datasets.load_diabetes()
>>> X = diabetes.data[:150]
>>> y = diabetes.target[:150]
>>> model = linear_model.Lasso()
>>> scores = dual_leaf_cross_score(model, X, y, cv=3, metric='mean')
>>> print(scores)
[0.3315057  0.08022103 0.03531816]
"""

    # scalling the inputs
    def scaled(data):
        data_scaled=data/np.max(data)
        return data_scaled
    # shuffling the dataset
    def shuffle(data):
        ind=np.arange(data.shape[0])
        np.random.shuffle(ind)
        return ind
    accu=[]
    for i in range(cv):
        x_scaled=scaled(x)
        ind=shuffle(x_scaled)
        x_shuffled=x_scaled[ind]
        y_shuffled=y[ind]
        # dual leaf split
        xdat1,xdat2,ydat1,ydat2=train_test_split(x_shuffled,y_shuffled,test_size=0.5,random_state=10)
        x_train,x_test,y_train,y_test=train_test_split(xdat1,ydat1,test_size=0.25,random_state=10)
        # prediction for first leaf
        model.fit(x_train,y_train)
        pred1=model.score(x_test,y_test)
        xtrain,xtest,ytrain,ytest=train_test_split(xdat2,ydat2,test_size=0.25,random_state=10)
        # prediction for second leaf
        model.fit(xtrain,ytrain)
        pred2=model.score(xtest,ytest)
        # mean the values
        if metric=="mean":
            mean=np.mean([pred1,pred2])
        # append them to an accu list
            accu.append(mean)
        elif metric=="median":
            accu.append(np.median([pred1,pred2]))
    return accu
        
        

    
