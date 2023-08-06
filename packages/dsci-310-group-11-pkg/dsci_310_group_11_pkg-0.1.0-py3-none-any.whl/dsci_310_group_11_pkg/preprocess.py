import numpy as np
from sklearn.model_selection import train_test_split

def preprocessor(df, tort):
    """DESCRIPTION: Splits the dataset of the specified 'df' (dataframe) into
    training and testing data, generates a 'target' variable for the ML
    model to classify given the value of the quality of each example.
    
    INPUTS: df - a dataframe object that contains the entirety of the dataset, for splitting.
            tort - a binary value (0, 1) that specifies whether to return the train or test dataframe.
    
    ACTION: Splits the dataset of the specified 'df' (dataframe) into
    training and testing data, uses np.where to assign a 0 to the target
    column of examples that have quality < 5, assigns a 1 to the target
    column of examples that have quality > 5.
    
    RETURNS: IF the function calls 0, then returns the training data, ELSE IF
    function calls, returns the testing data
    
    TODO: Modularize param_grid values
    """
    
    train_df, test_df = train_test_split(df, test_size=0.30, random_state=123)
    train_df['target'] = np.where(train_df['quality'] > 5, 1, 0)
    test_df['target'] = np.where(test_df['quality'] > 5, 1, 0)

    if tort == 0:
        return train_df
    elif tort == 1:
        return test_df