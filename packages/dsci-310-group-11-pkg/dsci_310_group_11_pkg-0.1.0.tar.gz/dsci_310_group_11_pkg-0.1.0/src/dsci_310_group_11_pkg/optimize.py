# Import Required Packages
import numpy as np
import pandas as pd

from sklearn.model_selection import cross_val_score, cross_validate, train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

def hp_optimizer(model, X_train, y_train):
    """DESCRIPTION: Maximizes model accuracy based on tuning hyperparameters of each model (respective if statements)
    
    ACTION: Loops over chosen hyperparemeters in a the scores_dict/param_grid dictionary
    and appends the mean cross validation score of each hyperparameter to the scores_dict dictionary
    
    INPUTS: model - an input string, referencing the specific model that the function should run.
            X_train - a dataframe object containing prediction features.
            y_train - a series object containing target variables.
    
    RETURNS: Dataframe containing the mean cross validation scores of each hyperparameter value
    
    TODO: Modularize param_grid values
    
    Logistic Regression model needs to optimize the "C" value (a value of model regularization)
    C: Regularization; penalty of wrongly classified examples
    Creates a simple ML pipeline that scales the data and applies LogisticRegression
    """
    
    if model == 'lr':
        scores_dict = {
        "C": 10.0**np.arange(-4, 6, 1),
        "mean_train_scores": list(),
        "mean_cv_scores": list(),
        }
        for C in scores_dict["C"]:
            pipe = make_pipeline(StandardScaler(),
                                 LogisticRegression(C=C, random_state=1234))
            scores = cross_validate(pipe, X_train, y_train, return_train_score=True)
            scores_dict["mean_train_scores"].append(scores["train_score"].mean())
            scores_dict["mean_cv_scores"].append(scores["test_score"].mean())

        results_df = pd.DataFrame(scores_dict)
        return results_df

    # Support Vector Machine model optimizes the 'C' and 'gamma' values.
    # C: Regularization; penalty of wrongly classified examples
    # Gamma: Strenghth of the influence of individual examples
    elif model == 'svm':
        param_grid = {
            "C": [0.001, 0.01, 0.1, 1, 10, 100],
            "gamma": [0.001, 0.01, 0.1, 1, 10, 100]
        }

        results_dict = {"C": [], "gamma": [], "mean_cv_score": []}

        for gamma in param_grid["gamma"]:
            for C in param_grid["C"]:  # for each combination of parameters, train an SVC
                pipe_svm = make_pipeline(StandardScaler(), SVC(gamma=gamma, C=C, class_weight='balanced', random_state=1234))
                scores = cross_val_score(pipe_svm, X_train, y_train, cv=5)
                mean_score = np.mean(scores)
            
                results_dict["C"].append(C)
                results_dict["gamma"].append(gamma)
                results_dict["mean_cv_score"].append(mean_score)


        results_df = pd.DataFrame(results_dict).head(10)
        return results_df

    # Decision Tree Classification optimizes the 'max depth' value
    # Max Depth: How many parameters (splits/decisions) to stop at
    elif model == 'dtc':

        param_grid = {"max_depth": np.arange(1, 20, 2)}

        results_dict = {"max_depth": [], "mean_cv_score": []}
        for depth in param_grid["max_depth"]:
            dtc = DecisionTreeClassifier(max_depth=depth, class_weight='balanced', random_state=1234)
            scores = cross_val_score(dtc, X_train, y_train)
            mean_score = np.mean(scores)

            results_dict["max_depth"].append(depth)
            results_dict["mean_cv_score"].append(mean_score)

        results_df = pd.DataFrame(results_dict)
        return results_df
    
    else:
        return 'Error: You need to input a proper model'