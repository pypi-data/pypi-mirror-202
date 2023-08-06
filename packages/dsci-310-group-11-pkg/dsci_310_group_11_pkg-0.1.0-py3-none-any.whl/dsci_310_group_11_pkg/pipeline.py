# Import required sklearn packages for model construction
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.dummy import DummyClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


def pipe_build(model, X_train, y_train):
    """ DESCRIPTION: Generates specified ML model based on 'model' as a string
    
    INPUTS: model - an input string, referencing the specific model that the function should run.
            X_train - a dataframe object containing prediction features.
            y_train - a series object containing target variables.
    
    
    
    
    
    ACTION: Creates a pipeline with appropriate transformations (scaling, etc.)
    and fits the specified model with optimized hyperparameters to the training data
    
    RETURNS: the pipeline object (model) for evaluation in wineclassification.ipynb
    
    TODO: Modularize hyperparameter values 
    """
    
    if model == 'dummy':
        baseline = DummyClassifier(strategy='most_frequent')
        pipe = baseline.fit(X_train, y_train)
        
    elif model == 'lr':
        pipe = make_pipeline(
                    StandardScaler(),
                    LogisticRegression(C=0.01, class_weight='balanced', random_state=1234))
        pipe.fit(X_train, y_train)

    elif model == 'svm':
        pipe = make_pipeline(
                StandardScaler(),
                SVC(C=1, gamma=0.1, class_weight='balanced', random_state=1234))
        pipe.fit(X_train, y_train)

    elif model == 'dtc':
        clf = DecisionTreeClassifier(max_depth=7,
                             random_state=1234,
                             class_weight='balanced')
        pipe = clf.fit(X_train, y_train)

    elif model == 'bayes':
        pipe = GaussianNB()
        pipe.fit(X_train, y_train)  

    return pipe