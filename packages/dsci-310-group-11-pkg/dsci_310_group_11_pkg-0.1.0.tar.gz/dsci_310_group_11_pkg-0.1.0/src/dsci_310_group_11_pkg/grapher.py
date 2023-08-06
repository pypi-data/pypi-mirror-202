import altair as alt
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
import seaborn as sns
from sklearn.metrics import classification_report

def correlation_table(df):
    """DESCRIPTION: Displays a correlation table (correlation coefficient value
    of each variable to each other variable).
    
    INPUTS: df - A dataframe object containing prediction features.
    
    ACTION: Inputs a dataframe and displays the correlation coefficients in
    a square grid.
    
    RETURNS: The table as a display.
    """
    cor_data = (
        df.corr().stack().reset_index(
        )  # The stacking results in an index on the correlation values, we need the index as normal columns for Altair
        .rename(columns={
            0: 'correlation',
            'level_0': 'Variable 1',
            'level_1': 'Variable 2'
        }))
    cor_data['correlation_label'] = cor_data['correlation'].map(
        '{:.2f}'.format)  # Round to 2 decimal

    # This is the inter-related correlations of each chemical ingredient
    # Judging on the correlations we may be able to infer coefficient signage.

    table = alt.Chart(cor_data).mark_rect().encode(
        alt.X('Variable 1:O'),
        alt.Y('Variable 2:O'),
        alt.Color('correlation'),
        alt.Tooltip(['correlation_label']),
    ).interactive().properties(width=300, height=300)

    xy = table.to_json('corrtab.json')
    return xy

def bar_chart(df):
    """DESCRIPTION: Displays a simple bar chart of the count of the quality variable.
    
    ACTION: Inputs a dataframe and displays the bar chart.
    
    INPUTS: df - A dataframe object
    
    RETURNS: The bar chart as a display.
    
    TODO: 1. Modularize the variables that you can input into the chart
    2. Move from altair to matplotlib
    """
    x = alt.Chart(df).mark_bar().encode(alt.X('quality:O'),
                                        alt.Y('count()')).properties(width=200,
                                                                     height=100)
    xyy = x.to_json('bar.json')
    return xyy

def class_report(pipe, X_test, y_test):
    """DESCRIPTION: Displays a heatmap of the count of the predicted case.
    
    ACTION: Inputs a model, testing data and displays the heatmap.
    
    INPUTS: pipe - a model
            X_test - testing features data
            y_test - testing label data
    
    RETURNS: The heatmap as figure
    
    """
    clf_report = classification_report(y_test, pipe.predict(X_test), output_dict=True)
    report = sns.heatmap(pd.DataFrame(clf_report).iloc[:-1, :].T, annot=True, linewidth=.5, cmap="crest")
    fig = report.get_figure()
    return fig

def vis_tree(X_train, y_train):
    """DESCRIPTION: Displays a visual example of a decision tree for conceptual
    purposes. The max_depth variable is limited to 3 so that the visualization
    is interpretable.
    
    INPUTS: X_train - a dataframe object containing prediction features
            y_train - a series object containing target variables.
    
    ACTION: Inputs an X_train dataframe and y_train series and displays the 
    decision tree model and each of its chosen parameter splits.
    
    RETURNS: The decisision tree model as a display.
    """
    vistree = DecisionTreeClassifier(max_depth=3,
                              random_state=1234,
                              class_weight='balanced')

    model2 = vistree.fit(X_train, y_train)

    fig = plt.figure(figsize=(15, 5))
    plot_tree(vistree, feature_names=X_train.columns, class_names='target', filled=True, fontsize=7)

def compare_scores(lst):
    """DESCRIPTION: Displays a bar chart comparing the accuracy scores of each
    ML model in the 'lst' list.
    
    INPUTS: lst - a list of floats (accuracy scores) of each model.
    
    ACTION: Inputs a list (lst) of ML model accuracy scores, generates a
    dataframe named 'report' and turns this dataframe into a bar chart.
    
    RETURNS: The bar chart where the highlighted bar is the highest score.
    """
    
    cscores = lst


    report = pd.DataFrame(
        [cscores], columns=['Baseline', 'LR', 'SVC', 'DT', 'NB'])

    report.index = ['Score']
    report = report.T.reset_index()

    y = alt.Chart(report).mark_bar().encode(
    alt.X('Score:Q'),
    alt.Y('index:N'),
    color=alt.condition(
        alt.datum.Score == max(
            report['Score']),  # If the year is 1810 this test returns True,
        alt.value('red'),  # which sets the bar orange.
        alt.value(
            'steelblue')  # And if it's not true it sets the bar steelblue.
    )).properties(width=500, height=200).configure(background='lightgrey')

    y = y.to_json('scores.json')
    return y

def show_coefficients(pipe, X_train):
    """DESCRIPTION: Displays a dataframe with the coefficients of the Logistic
    Regression model.
    
    INPUTS: pipe - a pipeline object containing scikit-learn model transformers, and a scikit-learn model.
            X_train - a dataframe object containing prediction features.
    
    ACTION: Inputs a LogisticRegression model, and an X_train dataset.
    Names the pipe variables given the named_steps in the logistic regression
    in an array called 'flatten'. Returns the dataframe 'coeffs' with the
    model's features versus their coefficients. Sorts the values descendingly.
   
    RETURNS: The dataframe, sorted descending by coefficients value.

    Printing out coefficients of the regression model for values influencing the model.
    """
    flatten = pipe.named_steps["logisticregression"].coef_  # 2-D Array
    flatten = flatten.flatten()  # Converting 2-D Array to 1-D Array

    coeffs = pd.DataFrame(
        data={
            "features": X_train.columns,  # 1-D Array
            "coefficients": flatten,  # 1-D Array
        })

    # intercept = pipe.named_steps["logisticregression"].intercept_
    # print(f"The intercept is: {intercept}")
    return coeffs.sort_values('coefficients', ascending=False)

def show_correct(pipe, X_test, y_test):
    """ DESCRIPTION: Displays a dataframe with the True Positive + True Negative
    versus the False Positive + False Negative ratio of the classifier model.
    
    INPUTS: pipe - a pipeline object containing scikit-learn model transformers, and a scikit-learn model.
            X_test - a dataframe object containing prediction features.
            y_test - a series object containing target variables.
    
    ACTION: Inputs a model (pipe), and testing data; calls predict on the 
    test data and reports the correct classifications versus the incorrect
    classifications.
    
    RETURNS: A dataframe with the correct classifications versus incorrect
    classifications.
    """

    ax = pd.DataFrame(data={'actual': y_test, 'predicted': pipe.predict(X_test)})
    ax['correct'] = ax['actual'] == ax['predicted']

    return ax.correct.value_counts()