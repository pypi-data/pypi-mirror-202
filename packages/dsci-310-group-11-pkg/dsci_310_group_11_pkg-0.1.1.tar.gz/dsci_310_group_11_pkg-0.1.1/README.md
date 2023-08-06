# dsci_310_group_11_pkg

This package contains functions used for generating dsci_310_group_11's report. The main functions inside this package is to 
split the data, generate pipeline for predictive models, conduct hyperparameter tunning and make graphs.

The main difference between our package to other similar functions is that the functions in our package is designed to improve the efficiency for analyzing the wine data. Using our pipeline generator as example, while directly using functions in sklearns can generate the same model, we simplifies this process by integrating repetitive steps into our functions. 

## Code Coverage Badge

[![codecov](https://codecov.io/gh/DSCI-310/dsci-310-group-11-pkg/branch/main/graph/badge.svg?token=e9QSz5vHox)](https://codecov.io/gh/DSCI-310/dsci-310-group-11-pkg)

## Installation

1. Clone the git repository onto your local machine using:
```
git clone https://github.com/DSCI-310/dsci-310-group-11-pkg.git
```

2. Navigate to the local repository through the terminal (this may differ based on your home directory setups):
```
cd dsci-310-group-11-pkg
```

3. Run pip to install the package locally (from [pypi](https://pypi.org/project/dsci-310-group-11-pkg/)):
```
pip install dsci-310-group-11-pkg
```

You should now be able to import the package into relevant projects and notebooks.

## Usage

The most basic usage of this package is to split the data into training or testing data:

```python
from dsci_310_group_11_pkg.preprocess import preprocessor

df # target dataframe
training_data = preprocessor(df, 0)
testing_data = preprocessor(df, 1)
```

One of the other usages of `dsci_310_group_11_pkg` is to generate pipeline for classification models as follows:

```python
from dsci_310_group_11_pkg.pipeline import pipe_build

x = X_training_data # training features data
y = Y_training data # training label data
model_type = 'lr' # types of model

model = pipe_build(model_type, x, y)

```
Another usage is to conduct hyperparameter tuning and return it as dataframe for different model as follows:

```python
from dsci_310_group_11_pkg.optimize import hy_optimizer

x = X_training_data # training features data
y = Y_training data # training label data
model_name = 'lr' # types of model

tuning_result = hp_optimize(model_name, x, y)
```

This package can also be used to generate different graphs for the analysis report, for example: 

```python
from dsci_310_group_11_pkg.grapher import correlation_table

ctb = correlation_table(df) # this generate the correlation table for dataframe df
```
Other functions and more detailed usage can be found in docs/example or in the [website documentation of the package](https://dsci-310-group11-pkg.readthedocs.io/en/latest/index.html).

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`dsci_310_group_11_pkg` was created by DSCI_310_Group_11. It is licensed under the terms of the MIT license.

## Credits

`dsci_310_group_11_pkg` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
