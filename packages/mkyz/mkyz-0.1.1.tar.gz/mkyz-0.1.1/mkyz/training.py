from sklearn.ensemble import (
    RandomForestClassifier, RandomForestRegressor, BaggingClassifier, BaggingRegressor,
    AdaBoostClassifier, AdaBoostRegressor, StackingClassifier, StackingRegressor,
    GradientBoostingClassifier, GradientBoostingRegressor, ExtraTreesClassifier, ExtraTreesRegressor,
    VotingClassifier, VotingRegressor
)
from sklearn.gaussian_process import GaussianProcessClassifier, GaussianProcessRegressor
from sklearn.linear_model import (
    LogisticRegression, LinearRegression, Ridge, Lasso, ElasticNet,
    SGDClassifier, SGDRegressor, RidgeClassifier, PassiveAggressiveClassifier, PassiveAggressiveRegressor
)
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering, Birch, MeanShift, SpectralClustering
from sklearn.decomposition import PCA, TruncatedSVD, FactorAnalysis, NMF
from sklearn.mixture import GaussianMixture
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, mean_squared_error, r2_score, \
    mean_absolute_error, mean_squared_log_error, explained_variance_score, max_error, silhouette_score, f1_score, \
    precision_score, recall_score, roc_auc_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import make_pipeline

import numpy as np

import optuna
from sklearn.model_selection import cross_val_score
# Additional libraries for XGBoost, LightGBM, CatBoost
try:
    import xgboost as xgb
except ImportError:
    xgb = None

try:
    import lightgbm as lgb
except ImportError:
    lgb = None

try:
    import catboost as cb
except ImportError:
    cb = None

import optuna
from sklearn.model_selection import cross_val_score

from mlxtend.frequent_patterns import apriori, association_rules

# Libraries for enhanced output
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.table import Table
from rich import box
import concurrent.futures
import time
import yaml

import time
import concurrent.futures
import yaml
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, TextColumn, BarColumn, TimeRemainingColumn
from rich import box

import warnings
warnings.filterwarnings("ignore")

import logging

# Initialize Rich Console
console = Console()

# Suppress logging from XGBoost, LightGBM, and CatBoost
logging.getLogger('xgboost').setLevel(logging.ERROR)
logging.getLogger('lightgbm').setLevel(logging.ERROR)
logging.getLogger('catboost').setLevel(logging.ERROR)



#-----------------------------------------------------------------------------------------------------------------------
# Global dictionary to store trained models
MODELS = {}

# Dictionary of classification models
CLASSIFICATION_MODELS = {
    'rf': RandomForestClassifier,
    'lr': LogisticRegression,
    'svm': SVC,
    'knn': KNeighborsClassifier,
    'dt': DecisionTreeClassifier,
    'nb': GaussianNB,
    'gb': GradientBoostingClassifier,
    #'xgb': xgb.XGBClassifier if xgb else None,
    #'lgbm': lgb.LGBMClassifier if lgb else None,
    #'catboost': cb.CatBoostClassifier if cb else None,
    #'sgd': SGDClassifier,
    #'pa': PassiveAggressiveClassifier,
    #'ridge_cls': RidgeClassifier,
    #'mlp': MLPClassifier,
    #'et': ExtraTreesClassifier,
    #'gp': GaussianProcessClassifier,
    # Add other classification models if needed
}

# Dictionary of regression models
REGRESSION_MODELS = {
    'rf': RandomForestRegressor,
    'lr': LinearRegression,
    'svm': SVR,
    'knn': KNeighborsRegressor,
    'dt': DecisionTreeRegressor,
    #'ridge': Ridge,
    #'lasso': Lasso,
    #'elasticnet': ElasticNet,
    #'gb': GradientBoostingRegressor,
    #'xgb': xgb.XGBRegressor if xgb else None,
    #'lgbm': lgb.LGBMRegressor if lgb else None,
    #'catboost': cb.CatBoostRegressor if cb else None,
    #'sgd': SGDRegressor,
    #'pa': PassiveAggressiveRegressor,
    #'mlp': MLPRegressor,
    #'et': ExtraTreesRegressor,
    #'gp': GaussianProcessRegressor,
    # Add other regression models
}

# Dictionary of clustering models
CLUSTERING_MODELS = {
    'kmeans': KMeans,
    'dbscan': DBSCAN,
    'agglomerative': AgglomerativeClustering,
    'gmm': GaussianMixture,
    'mean_shift': MeanShift,
    'spectral': SpectralClustering,
    'birch': Birch,
    # Add other clustering models
}

# Dictionary of dimensionality reduction models
DIMENSIONALITY_REDUCTION_MODELS = {
    'pca': PCA,
    'svd': TruncatedSVD,
    'factor_analysis': FactorAnalysis,
    'nmf': NMF,
    # Add other dimensionality reduction models
}

# Dictionary of model training functions
TRAIN_FUNCTIONS = {
    'classification': lambda X, y, model, **params: model(**params).fit(X, y),
    'regression': lambda X, y, model, **params: model(**params).fit(X, y),
    'clustering': lambda X, model, **params: model(**params).fit(X),
    'dimensionality_reduction': lambda X, model, **params: model(**params).fit_transform(X),
}

# Dictionary of model hyperparameter grids for optimization
PARAM_GRIDS = {
    'rf': {
        'n_estimators': [100, 200, 300],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'bootstrap': [True, False]
    },
    'lr': [
        {
            'C': [0.001, 0.01, 0.1, 1, 10, 100],
            'penalty': ['l2'],
            'solver': ['lbfgs'],
            'max_iter': [1000]
        },
        {
            'C': [0.001, 0.01, 0.1, 1, 10, 100],
            'penalty': ['l1'],
            'solver': ['saga'],
            'max_iter': [1000]
        }
    ],
    'svm': {
        'C': [0.1, 1, 10],
        'kernel': ['rbf', 'linear', 'poly'],
        'gamma': ['scale', 'auto']
    },
    'knn': {
        'n_neighbors': [3, 5, 7, 9],
        'weights': ['uniform', 'distance'],
        'metric': ['euclidean', 'manhattan']
    },
    'dt': {
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'criterion': ['gini', 'entropy']
    },
    'nb': {
        'var_smoothing': [1e-09, 1e-08, 1e-07]
    },
    'gb': {
        'n_estimators': [100, 200, 300],
        'learning_rate': [0.01, 0.1, 0.2],
        'max_depth': [3, 5, 7],
        'subsample': [0.8, 1.0]
    },
    'xgb': {
        'n_estimators': [100, 200, 300],
        'learning_rate': [0.01, 0.1, 0.2],
        'max_depth': [3, 5, 7],
        'subsample': [0.8, 1.0],
        'colsample_bytree': [0.8, 1.0],
        'verbosity': [0]  # XGBoost için verbosity parametresi
    },
    'lgbm': {
        'n_estimators': [100, 200, 300],
        'learning_rate': [0.01, 0.1, 0.2],
        'max_depth': [3, 5, 7],
        'num_leaves': [31, 50, 100],
        'boosting_type': ['gbdt', 'dart'],
        'verbose': [-1]  # LightGBM için verbose parametresi
    },
    'catboost': {
        'iterations': [100, 200, 300],
        'learning_rate': [0.01, 0.1, 0.2],
        'depth': [3, 5, 7],
        'l2_leaf_reg': [1, 3, 5, 7, 9],
        'logging_level': ['Silent']  # CatBoost için logging_level parametresi
    },
    'sgd': {
        'loss': ['hinge', 'log', 'modified_huber'],
        'penalty': ['l2', 'l1', 'elasticnet'],
        'alpha': [0.0001, 0.001, 0.01],
        'max_iter': [1000, 2000, 3000]
    },
    'pa': {
        'C': [0.1, 1.0, 10.0],
        'loss': ['hinge', 'squared_hinge']
    },
    'ridge_cls': {
        'alpha': [0.1, 1.0, 10.0],
        'solver': ['auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg']
    },
    'mlp': {
        'hidden_layer_sizes': [(100,), (50, 50), (100, 50)],
        'activation': ['relu', 'tanh', 'logistic'],
        'solver': ['adam', 'sgd'],
        'alpha': [0.0001, 0.001, 0.01],
        'learning_rate': ['constant', 'adaptive']
    },
    'et': {
        'n_estimators': [100, 200, 300],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'bootstrap': [True, False]
    },
    'gp': {
        'kernel': [None, 'rbf', 'linear'],
        'optimizer': ['fmin_l_bfgs_b', 'lbfgs']
    },
    'linear_regression': {
        'fit_intercept': [True, False],
        'normalize': [True, False],
        'copy_X': [True, False]
    },
    'ridge': {
        'alpha': [0.1, 1.0, 10.0],
        'solver': ['auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg']
    },
    'lasso': {
        'alpha': [0.1, 1.0, 10.0],
        'selection': ['cyclic', 'random']
    },
    'elasticnet': {
        'alpha': [0.1, 1.0, 10.0],
        'l1_ratio': [0.1, 0.5, 0.9],
        'selection': ['cyclic', 'random']
    },
    'svr': {
        'C': [0.1, 1, 10],
        'kernel': ['rbf', 'linear', 'poly'],
        'gamma': ['scale', 'auto']
    },
    'kmeans': {
        'n_clusters': [3, 5, 7, 9],
        'init': ['k-means++', 'random'],
        'n_init': [10, 20, 30],
        'max_iter': [300, 600, 900]
    },
    'dbscan': {
        'eps': [0.3, 0.5, 0.7],
        'min_samples': [5, 10, 15],
        'metric': ['euclidean', 'manhattan']
    },
    'agglomerative': {
        'n_clusters': [2, 3, 4, 5],
        'affinity': ['euclidean', 'manhattan', 'cosine'],
        'linkage': ['ward', 'complete', 'average']
    },
    'gmm': {
        'n_components': [1, 2, 3, 4, 5],
        'covariance_type': ['full', 'tied', 'diag', 'spherical'],
        'max_iter': [100, 200, 300]
    },
    'mean_shift': {
        'bandwidth': [1, 2, 3, 4],
        'seeds': [None, 'k-means'],
        'bin_seeding': [True, False]
    },
    'spectral': {
        'n_clusters': [2, 3, 4, 5],
        'affinity': ['nearest_neighbors', 'rbf'],
        'n_neighbors': [5, 10, 15]
    },
    'birch': {
        'n_clusters': [None, 2, 3, 4, 5],
        'threshold': [0.5, 1.0, 1.5],
        'branching_factor': [20, 30, 40]
    },
    'pca': {
        'n_components': [2, 5, 10, 15],
        'svd_solver': ['auto', 'full', 'arpack', 'randomized'],
        'whiten': [True, False]
    },
    'svd': {
        'n_components': [2, 5, 10, 15],
        'n_iter': [5, 10, 20],
        'random_state': [42]
    },
    'factor_analysis': {
        'n_components': [2, 5, 10, 15],
        'tol': [0.001, 0.01, 0.1],
        'max_iter': [100, 200, 300]
    },
    'nmf': {
        'n_components': [2, 5, 10, 15],
        'init': ['random', 'nndsvd'],
        'solver': ['cd', 'mu'],
        'beta_loss': ['frobenius', 'kullback-leibler', 'itakura-saito']
    },
    # Diğer modeller için hiperparametre ızgaralarını ekleyin
}

# Dictionary of model evaluation functions
EVALUATE_FUNCTIONS = {
    'classification': lambda y_true, y_pred: {
        'accuracy': accuracy_score(y_true, y_pred),
        'f1_score': f1_score(y_true, y_pred, average='weighted'),
        'precision': precision_score(y_true, y_pred, average='weighted'),
        'recall': recall_score(y_true, y_pred, average='weighted'),
        'roc_auc': roc_auc_score(y_true, y_pred, average='weighted', multi_class='ovr') if len(set(y_true)) > 2 else roc_auc_score(y_true, y_pred)
    },
    'regression': lambda y_true, y_pred: {
        'mean_squared_error': mean_squared_error(y_true, y_pred),
        'r2_score': r2_score(y_true, y_pred),
        'mean_absolute_error': mean_absolute_error(y_true, y_pred),
        'mean_squared_log_error': mean_squared_log_error(y_true, y_pred),
        'explained_variance_score': explained_variance_score(y_true, y_pred),
        'max_error': max_error(y_true, y_pred)
    },
    'clustering': lambda X, labels: {
        'silhouette_score': silhouette_score(X, labels) if len(set(labels)) > 1 else -1
    },
    'dimensionality_reduction': lambda X, X_reduced: {
        'reconstruction_error': np.mean(np.abs(X - X_reduced))
    }
    # Additional evaluation metrics can be added as needed
}

# Dictionary of verbosity parameters for models when optimize_models=False
VERBOSITY_PARAMS = {
    'xgb': {'verbosity': 0},
    'lgbm': {'verbose': -1},
    'catboost': {'logging_level': 'Silent'},
    # Diğer modeller için boş sözlük veya ilgili verbosity parametrelerini ekleyin
}
#
def train(data, task='classification', model='rf', **model_params):
    """
    Trains a machine learning model based on the specified task and model type.

    This function handles different machine learning tasks such as classification, regression,
    clustering, and dimensionality reduction. It selects the appropriate model class and training
    function based on the task and model type provided. The trained model is then stored in a
    global `MODELS` dictionary for later use.

    Args:
        data (tuple): A tuple containing the following elements in order:
            - X_train (pd.DataFrame): Training feature set.
            - X_test (pd.DataFrame): Testing feature set.
            - y_train (pd.Series): Training labels.
            - y_test (pd.Series): Testing labels.
            - df (pd.DataFrame): The original dataframe.
            - target_column (str): The name of the target column.
            - numerical_columns (list): List of numerical feature column names.
            - categorical_columns (list): List of categorical feature column names.
        task (str, optional): The machine learning task to perform. 
            Defaults to 'classification'. 
            Supported tasks:
            - 'classification'
            - 'regression'
            - 'clustering'
            - 'dimensionality_reduction'
        model (str, optional): The type of model to train. Defaults to 'rf' (Random Forest).
            Supported models depend on the specified task.
        **model_params: Additional keyword arguments to pass to the model constructor.

    Returns:
        Trained model object: The trained machine learning model.

    Raises:
        ValueError: If an unsupported task type or model type is provided.

    Examples:
        >>> # Example for classification task with Random Forest
        >>> trained_rf = train(data, task='classification', model='rf', n_estimators=100, random_state=42)

        >>> # Example for regression task with Linear Regression
        >>> trained_lr = train(data, task='regression', model='linear', fit_intercept=True)

        >>> # Example for clustering task with K-Means
        >>> trained_km = train(data, task='clustering', model='kmeans', n_clusters=5)

        >>> # Example for dimensionality reduction with PCA
        >>> trained_pca = train(data, task='dimensionality_reduction', model='pca', n_components=2)
    """
    X_train, X_test, y_train, y_test, df, target_column, numerical_columns, categorical_columns = data

    if task == 'classification':
        model_class = CLASSIFICATION_MODELS.get(model)
    elif task == 'regression':
        model_class = REGRESSION_MODELS.get(model)
    elif task == 'clustering':
        model_class = CLUSTERING_MODELS.get(model)
    elif task == 'dimensionality_reduction':
        model_class = DIMENSIONALITY_REDUCTION_MODELS.get(model)
    else:
        raise ValueError(f"Unsupported task type: {task}")

    if model_class is None:
        raise ValueError(f"Unsupported model type for {task}: {model}")

    train_func = TRAIN_FUNCTIONS[task]

    if task in ['classification', 'regression']:
        trained_model = train_func(X_train, y_train, model_class, **model_params)
    else:
        trained_model = train_func(X_train, model_class, **model_params)

    MODELS[model] = trained_model
    return trained_model

def predict(data, fitted_model=None, task='classification', model='rf'):
    """
    Makes predictions on the provided data using a trained machine learning model.

    This function utilizes a pre-trained model to generate predictions for the test dataset.
    It supports various machine learning tasks such as classification, regression, clustering,
    and dimensionality reduction. If no fitted model is provided, it retrieves the model
    from the global `MODELS` dictionary based on the specified model type.

    Args:
        data (tuple): A tuple containing the following elements in order:
            - X_train (pd.DataFrame): Training feature set.
            - X_test (pd.DataFrame): Testing feature set.
            - y_train (pd.Series): Training labels.
            - y_test (pd.Series): Testing labels.
            - df (pd.DataFrame): The original dataframe.
            - target_column (str): The name of the target column.
            - numerical_columns (list): List of numerical feature column names.
            - categorical_columns (list): List of categorical feature column names.
        fitted_model (object, optional): A pre-trained machine learning model.
            If not provided, the model specified by the `model` parameter will be used.
        task (str, optional): The machine learning task to perform predictions for.
            Defaults to 'classification'.
            Supported tasks:
            - 'classification'
            - 'regression'
            - 'clustering'
            - 'dimensionality_reduction'
        model (str, optional): The type of model to use for predictions.
            Defaults to 'rf' (Random Forest).
            Supported models depend on the specified task.

    Returns:
        np.ndarray or pd.DataFrame: The prediction results.
            - For 'classification', 'regression', and 'clustering' tasks, returns a NumPy array of predictions.
            - For 'dimensionality_reduction' tasks, returns a transformed Pandas DataFrame.

    Raises:
        ValueError: If the specified model has not been trained or is not available.

    Examples:
        >>> # Example using a trained Random Forest classifier from MODELS dictionary
        >>> predictions = predict(data, task='classification', model='rf')

        >>> # Example using a provided fitted model for regression
        >>> from sklearn.linear_model import LinearRegression
        >>> lr_model = LinearRegression().fit(X_train, y_train)
        >>> predictions = predict(data, fitted_model=lr_model, task='regression')

        >>> # Example for clustering task with K-Means
        >>> predictions = predict(data, task='clustering', model='kmeans')

        >>> # Example for dimensionality reduction with PCA
        >>> transformed_data = predict(data, task='dimensionality_reduction', model='pca')
    """
    X_train, X_test, y_train, y_test, df, target_column, numerical_columns, categorical_columns = data

    clf = fitted_model if fitted_model else MODELS.get(model)

    if clf:
        if task in ['classification', 'regression', 'clustering']:
            return clf.predict(X_test)
        elif task == 'dimensionality_reduction':
            return clf.transform(X_test)
    else:
        raise ValueError(f"The {model} model has not been trained yet.")

def evaluate(data, predictions=None, task='classification', model='rf'):
    """
    Evaluates the performance of a machine learning model on the provided data.

    This function assesses the performance of a trained model by comparing its predictions
    against the true labels or by evaluating the quality of dimensionality reduction or clustering.
    It supports various machine learning tasks including classification, regression, clustering,
    and dimensionality reduction. If predictions are not provided, the function will generate
    them using the specified or default model.

    Args:
        data (tuple): A tuple containing the following elements in order:
            - X_train (pd.DataFrame): Training feature set.
            - X_test (pd.DataFrame): Testing feature set.
            - y_train (pd.Series): Training labels.
            - y_test (pd.Series): Testing labels.
            - df (pd.DataFrame): The original dataframe.
            - target_column (str): The name of the target column.
            - numerical_columns (list): List of numerical feature column names.
            - categorical_columns (list): List of categorical feature column names.
        predictions (np.ndarray or pd.DataFrame, optional): The predictions made by the model.
            If not provided, predictions will be generated using the `predict` function.
        task (str, optional): The machine learning task to evaluate. 
            Defaults to 'classification'.
            Supported tasks:
            - 'classification'
            - 'regression'
            - 'clustering'
            - 'dimensionality_reduction'
        model (str, optional): The type of model to evaluate.
            Defaults to 'rf' (Random Forest).
            Supported models depend on the specified task.

    Returns:
        dict or float or pd.DataFrame: The evaluation metrics.
            - For 'classification' and 'regression' tasks, returns a dictionary of evaluation metrics.
            - For 'clustering', returns a float representing the clustering score.
            - For 'dimensionality_reduction', returns a DataFrame with evaluation scores.

    Raises:
        ValueError: 
            - If an unsupported task type is provided.
            - If evaluation metrics for the specified task are not defined.

    Examples:
        >>> # Example for evaluating a classification model
        >>> scores = evaluate(data, task='classification', model='rf')
        >>> print(scores)
        {'accuracy': 0.95, 'precision': 0.93, 'recall': 0.94}

        >>> # Example for evaluating a regression model
        >>> scores = evaluate(data, task='regression', model='linear')
        >>> print(scores)
        {'mean_squared_error': 10.5, 'r2_score': 0.89}

        >>> # Example for evaluating a clustering model
        >>> scores = evaluate(data, task='clustering', model='kmeans')
        >>> print(scores)
        0.75

        >>> # Example for evaluating dimensionality reduction with PCA
        >>> scores = evaluate(data, task='dimensionality_reduction', model='pca')
        >>> print(scores)
           explained_variance_ratio
        0                       0.8
        1                       0.15
    """
    X_train, X_test, y_train, y_test, df, target_column, numerical_columns, categorical_columns = data

    if predictions is None:
        predictions = predict(data, task=task, model=model)

    evaluate_func = EVALUATE_FUNCTIONS.get(task)
    if evaluate_func:
        if task == 'dimensionality_reduction':
            X_reduced = predictions
            scores = evaluate_func(X_test, X_reduced)
        elif task == 'clustering':
            scores = evaluate_func(X_test, predictions)
        else:
            scores = evaluate_func(y_test, predictions)
        return scores
    else:
        raise ValueError(f"Unsupported task type for evaluation: {task}")

def optimize_model(X, y, model_class, param_grid, cv=5, method='grid_search', task='classification'):
    """
    Optimizes model hyperparameters using GridSearchCV or Optuna.

    This function performs hyperparameter optimization for a given machine learning model
    using either GridSearchCV or Bayesian optimization with Optuna. It supports both
    classification and regression tasks. The optimized model, along with the best parameters
    and score, is returned for further use.

    Args:
        X (pd.DataFrame or np.ndarray): Training feature set.
        y (pd.Series or np.ndarray): Target variable.
        model_class (class): The machine learning model class (e.g., `RandomForestClassifier`).
        param_grid (dict): Hyperparameter grid for optimization.
            - Keys are parameter names.
            - Values are lists or tuples specifying the parameter range.
        cv (int, optional): Number of cross-validation folds. Defaults to 5.
        method (str, optional): Optimization method.
            - 'grid_search' for GridSearchCV.
            - 'bayesian' for Bayesian optimization using Optuna.
            Defaults to 'grid_search'.
        task (str, optional): Machine learning task.
            - 'classification' for classification tasks.
            - 'regression' for regression tasks.
            Defaults to 'classification'.

    Returns:
        tuple:
            - best_estimator (object): The model instance with the best found parameters.
            - best_params (dict): The best hyperparameters found during optimization.
            - best_score (float): The best cross-validation score achieved.

    Raises:
        ValueError:
            - If an unsupported optimization method is provided.
            - If an unsupported task type is specified.

    Examples:
        >>> from sklearn.ensemble import RandomForestClassifier
        >>> param_grid = {
        ...     'n_estimators': [100, 200],
        ...     'max_depth': [None, 10, 20],
        ...     'min_samples_split': [2, 5]
        ... }
        >>> best_model, best_params, best_score = optimize_model(
        ...     X_train, y_train, RandomForestClassifier, param_grid,
        ...     cv=5, method='grid_search', task='classification'
        ... )
        >>> print(best_params)
        {'n_estimators': 200, 'max_depth': 20, 'min_samples_split': 2}

        >>> import optuna
        >>> from sklearn.linear_model import Ridge
        >>> param_grid = {
        ...     'alpha': (0.1, 10.0),
        ...     'fit_intercept': [True, False]
        ... }
        >>> best_model, best_params, best_score = optimize_model(
        ...     X_train, y_train, Ridge, param_grid,
        ...     cv=5, method='bayesian', task='regression'
        ... )
        >>> print(best_params)
        {'alpha': 5.3, 'fit_intercept': True}
    """
    if method == 'grid_search':
        grid_search = GridSearchCV(model_class(), param_grid, cv=cv, n_jobs=-1)
        grid_search.fit(X, y)
        return grid_search.best_estimator_, grid_search.best_params_, grid_search.best_score_

    elif method == 'bayesian':
        # Ensure Optuna is installed
        try:
            import optuna
        except ImportError:
            raise ImportError("Optuna is not installed. Please install it using 'pip install optuna'.")

        from sklearn.model_selection import cross_val_score

        def objective(trial):
            params = {}
            for param, values in param_grid.items():
                if isinstance(values, list):
                    params[param] = trial.suggest_categorical(param, values)
                elif isinstance(values, tuple):
                    if all(isinstance(x, float) for x in values):
                        params[param] = trial.suggest_float(param, values[0], values[1])
                    else:
                        params[param] = trial.suggest_int(param, values[0], values[1])
                else:
                    params[param] = values  # Fixed parameters

            model = model_class(**params)
            if task == 'classification':
                score = cross_val_score(model, X, y, cv=cv, scoring='accuracy').mean()
            elif task == 'regression':
                score = cross_val_score(model, X, y, cv=cv, scoring='neg_mean_squared_error').mean()
            else:
                raise ValueError(f"Unsupported task type: {task}")
            return score

        direction = 'maximize' if task == 'classification' else 'minimize'
        study = optuna.create_study(direction=direction)
        study.optimize(objective, n_trials=50)  # Adjust the number of trials as needed

        best_params = study.best_params
        best_score = study.best_value
        best_estimator = model_class(**best_params).fit(X, y)

        return best_estimator, best_params, best_score

    else:
        raise ValueError("Unsupported optimization method. Use 'grid_search' or 'bayesian'.")

def auto_train(data, task='classification', n_threads=1, optimize_models=False, optimization_method='grid_search'):
    """
    Automatically trains multiple machine learning models and selects the best one based on evaluation metrics.
    
    If `optimize_models` is set to True, the function performs hyperparameter optimization using GridSearchCV
    or Bayesian optimization with Optuna. The optimization method can be specified via the `optimization_method` parameter.
    
    The function supports various tasks including classification, regression, clustering, and dimensionality reduction.
    It trains each model, evaluates its performance, and identifies the best-performing model. Results are saved to a 
    YAML file and displayed in a formatted table.
    
    Args:
        data (tuple): A tuple containing the following elements in order:
            - X_train (pd.DataFrame or np.ndarray): Training feature set.
            - X_test (pd.DataFrame or np.ndarray): Testing feature set.
            - y_train (pd.Series or np.ndarray): Training labels.
            - y_test (pd.Series or np.ndarray): Testing labels.
            - df (pd.DataFrame): The original dataframe.
            - target_column (str): The name of the target column.
            - numerical_columns (list): List of numerical feature column names.
            - categorical_columns (list): List of categorical feature column names.
        task (str, optional): The machine learning task to perform.
            Defaults to 'classification'.
            Supported tasks:
                - 'classification'
                - 'regression'
                - 'clustering'
                - 'dimensionality_reduction'
        n_threads (int, optional): The number of parallel threads to use for training.
            Defaults to 1.
        optimize_models (bool, optional): Whether to perform hyperparameter optimization.
            If True, uses the specified `optimization_method` to optimize model hyperparameters.
            Defaults to False.
        optimization_method (str, optional): The method to use for hyperparameter optimization.
            - 'grid_search' for GridSearchCV.
            - 'bayesian' for Bayesian optimization using Optuna.
            Defaults to 'grid_search'.
    
    Returns:
        object or None: The best trained machine learning model based on evaluation metrics.
            Returns `None` if no model is successfully trained.
    
    Raises:
        ValueError:
            - If an unsupported task type is provided.
            - If an unsupported optimization method is specified.
        ImportError:
            - If Optuna is not installed when `optimization_method` is set to 'bayesian'.
    
    Examples:
        >>> # Example for automatic training without hyperparameter optimization
        >>> best_model = auto_train(
        ...     data,
        ...     task='classification',
        ...     n_threads=4,
        ...     optimize_models=False,
        ...     optimization_method='grid_search'
        ... )
        >>> print(best_model)
        RandomForestClassifier(n_estimators=100, random_state=42)
    
        >>> # Example for automatic training with GridSearchCV hyperparameter optimization
        >>> best_model = auto_train(
        ...     data,
        ...     task='regression',
        ...     n_threads=2,
        ...     optimize_models=True,
        ...     optimization_method='grid_search'
        ... )
        >>> print(best_model)
        Ridge(alpha=5.3, fit_intercept=True)
    
        >>> # Example for automatic training with Bayesian optimization using Optuna
        >>> best_model = auto_train(
        ...     data,
        ...     task='regression',
        ...     n_threads=3,
        ...     optimize_models=True,
        ...     optimization_method='bayesian'
        ... )
        >>> print(best_model)
        Ridge(alpha=5.3, fit_intercept=True)
    """
    def train_and_evaluate(model_name):
        # Notify that model training has started
        console.print(f"[bold blue]Model '{model_name}' training started.[/bold blue]")

        start_time = time.time()
        X_train, X_test, y_train, y_test, df, target_column, numerical_columns, categorical_columns = data

        try:
            if task == 'classification':
                model_class = CLASSIFICATION_MODELS[model_name]
            elif task == 'regression':
                model_class = REGRESSION_MODELS[model_name]
            elif task == 'clustering':
                model_class = CLUSTERING_MODELS[model_name]
            elif task == 'dimensionality_reduction':
                model_class = DIMENSIONALITY_REDUCTION_MODELS[model_name]
            else:
                raise ValueError(f"Unsupported task type: {task}")

            if optimize_models and model_name in PARAM_GRIDS:
                param_grid = PARAM_GRIDS[model_name]
                model, best_params, best_score = optimize_model(
                    X_train, y_train, model_class, param_grid,
                    method=optimization_method, task=task
                )
            else:
                # Add verbosity parameters if not optimizing
                verbosity_params = VERBOSITY_PARAMS.get(model_name, {})
                model = train(data, task=task, model=model_name, **verbosity_params)
                best_params = model.get_params()
                best_score = None

            predictions = predict(data, fitted_model=model, task=task)
            if task in ['classification', 'regression']:
                scores = evaluate(data, predictions, task=task, model=model_name)
                # Main score for comparison
                if task == 'classification':
                    main_score = scores['accuracy']
                elif task == 'regression':
                    main_score = -scores['mean_squared_error']  # Lower MSE is better
            elif task == 'clustering':
                scores = evaluate(data, predictions, task=task, model=model_name)
                main_score = scores['silhouette_score']
            elif task == 'dimensionality_reduction':
                scores = evaluate(data, predictions, task=task, model=model_name)
                main_score = -scores['reconstruction_error']  # Lower error is better
            end_time = time.time()

            # Notify that model training has completed
            console.print(f"[bold green]Model '{model_name}' training completed.[/bold green]")

            return {
                'model': model_name,
                'score': main_score,
                'detailed_scores': scores,
                'best_score': best_score,
                'training_time': end_time - start_time,
                'parameters': best_params
            }
        except Exception as e:
            # Notify in case of an error
            console.print(f"[bold red]An error occurred while training model '{model_name}': {e}[/bold red]")
            return {
                'model': model_name,
                'score': None,
                'detailed_scores': {},
                'best_score': None,
                'training_time': time.time() - start_time,
                'parameters': {}
            }

    if task == 'classification':
        models_to_train = [m for m in CLASSIFICATION_MODELS.keys() if CLASSIFICATION_MODELS[m] is not None]
    elif task == 'regression':
        models_to_train = [m for m in REGRESSION_MODELS.keys() if REGRESSION_MODELS[m] is not None]
    elif task == 'clustering':
        models_to_train = list(CLUSTERING_MODELS.keys())
    elif task == 'dimensionality_reduction':
        models_to_train = list(DIMENSIONALITY_REDUCTION_MODELS.keys())
    else:
        raise ValueError(f"Unsupported task type: {task}")

    total_models = len(models_to_train)
    console.print(f"[bold green]Starting training of {total_models} models...[/bold green]")

    results = []
    with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.1f}%",
            TimeRemainingColumn(),
            console=console
    ) as progress:
        task_progress = progress.add_task("[cyan]Training models...", total=total_models)

        with concurrent.futures.ThreadPoolExecutor(max_workers=n_threads) as executor:
            future_to_model = {executor.submit(train_and_evaluate, model_name): model_name for model_name in models_to_train}
            for future in concurrent.futures.as_completed(future_to_model):
                result = future.result()
                results.append(result)
                progress.advance(task_progress)

    # Save results to a YAML file
    try:
        with open('model_results.yaml', 'w') as file:
            yaml.dump(results, file)
    except Exception as e:
        console.print(f"[bold red]An error occurred while saving results to YAML: {e}[/bold red]")

    # Determine the best model
    # Exclude models that encountered errors (score is None)
    valid_results = [res for res in results if res['score'] is not None]
    if valid_results:
        best_model_info = max(valid_results, key=lambda x: x['score'])
    else:
        best_model_info = None

    # Display results in a rich table
    table = Table(title="Model Training Results", box=box.MINIMAL_DOUBLE_HEAD)
    table.add_column("Model", style="cyan", no_wrap=True)
    table.add_column("Score", style="magenta")
    table.add_column("Training Time (s)", style="green")
    table.add_column("Best CV Score", style="yellow")
    table.add_column("Parameters", style="white")

    for res in results:
        model_name = res['model']
        score = f"{res['score']:.4f}" if res['score'] is not None else "Error"
        training_time = f"{res['training_time']:.2f}"
        best_score = f"{res['best_score']:.4f}" if res['best_score'] is not None else "N/A"
        parameters = ', '.join([f"{k}={v}" for k, v in res['parameters'].items()]) if res['parameters'] else "N/A"

        if res == best_model_info:
            table.add_row(
                f"[bold green]{model_name}[/bold green]",
                f"[bold green]{score}[/bold green]",
                f"[bold green]{training_time}[/bold green]",
                f"[bold green]{best_score}[/bold green]",
                f"[bold green]{parameters}[/bold green]"
            )
        else:
            table.add_row(model_name, score, training_time, best_score, parameters)

    console.print(table)

    if best_model_info:
        console.print(f"[bold underline green]Best Model: {best_model_info['model']}[/bold underline green]")
        console.print(f"Score: [bold]{best_model_info['score']:.4f}[/bold]")
        if best_model_info['best_score'] is not None:
            console.print(f"Best CV Score: [bold]{best_model_info['best_score']:.4f}[/bold]")
        console.print(f"Training Time: [bold]{best_model_info['training_time']:.2f} seconds[/bold]")
        console.print(f"Parameters: [bold]{best_model_info['parameters']}[/bold]\n")
    else:
        console.print("[bold red]No models were successfully trained.[/bold red]")

    return MODELS.get(best_model_info['model']) if best_model_info else None




# ---- Kullanım Örneği ----
if __name__ == "__main__":


    import data_processing as dp

    data= dp.prepare_data('data.csv')

    # Hiperparametre optimizasyonu olmadan auto_train çalıştır
    best_model = auto_train(data, task='classification', n_threads=3, optimize_models=True , optimization_method='bayesian')



