import numpy as np
import concurrent.futures
import time
import yaml
import logging
from itertools import product
from sklearn.ensemble import (
    RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor,
    ExtraTreesClassifier, ExtraTreesRegressor
)
from sklearn.linear_model import (
    LogisticRegression, LinearRegression, Ridge, Lasso, ElasticNet,
    SGDClassifier, SGDRegressor, RidgeClassifier, PassiveAggressiveClassifier, PassiveAggressiveRegressor
)
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering, Birch, MeanShift, SpectralClustering
from sklearn.decomposition import PCA, TruncatedSVD, FactorAnalysis, NMF
from sklearn.mixture import GaussianMixture
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.gaussian_process import GaussianProcessClassifier, GaussianProcessRegressor
from sklearn.metrics import (
    accuracy_score, confusion_matrix, classification_report,
    mean_squared_error, r2_score, mean_absolute_error,
    mean_squared_log_error, explained_variance_score, max_error,
    silhouette_score
)
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline

# Import additional libraries for XGBoost, LightGBM, CatBoost
try:
    import xgboost as xgb
    XGB_AVAILABLE = True
except ImportError:
    XGB_AVAILABLE = False

try:
    import lightgbm as lgb
    LGBM_AVAILABLE = True
except ImportError:
    LGBM_AVAILABLE = False

try:
    import catboost as cb
    CATBOOST_AVAILABLE = True
except ImportError:
    CATBOOST_AVAILABLE = False

# Import mlxtend for association rule learning if needed
try:
    from mlxtend.frequent_patterns import apriori, association_rules
except ImportError:
    apriori = None
    association_rules = None

# Import rich for enhanced printing
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

# Initialize Rich console
console = Console()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global dictionary to store trained models
MODELS = {}

# Define model dictionaries with availability checks
CLASSIFICATION_MODELS = {
    'rf': RandomForestClassifier,
    'lr': LogisticRegression,
    'svm': SVC,
    'knn': KNeighborsClassifier,
    'dt': DecisionTreeClassifier,
    'nb': GaussianNB,
    'gb': GradientBoostingClassifier,
    'xgb': xgb.XGBClassifier if XGB_AVAILABLE else None,
    'lgbm': lgb.LGBMClassifier if LGBM_AVAILABLE else None,
    'catboost': cb.CatBoostClassifier if CATBOOST_AVAILABLE else None,
    'sgd': SGDClassifier,
    'pa': PassiveAggressiveClassifier,
    'ridge_cls': RidgeClassifier,
    'mlp': MLPClassifier,
    'et': ExtraTreesClassifier,
    'gp': GaussianProcessClassifier,
    # Add other classification models as needed
}

REGRESSION_MODELS = {
    'rf': RandomForestRegressor,
    'lr': LinearRegression,
    'svm': SVR,
    'knn': KNeighborsRegressor,
    'dt': DecisionTreeRegressor,
    'ridge': Ridge,
    'lasso': Lasso,
    'elasticnet': ElasticNet,
    'gb': GradientBoostingRegressor,
    'xgb': xgb.XGBRegressor if XGB_AVAILABLE else None,
    'lgbm': lgb.LGBMRegressor if LGBM_AVAILABLE else None,
    'catboost': cb.CatBoostRegressor if CATBOOST_AVAILABLE else None,
    'sgd': SGDRegressor,
    'pa': PassiveAggressiveRegressor,
    'mlp': MLPRegressor,
    'et': ExtraTreesRegressor,
    'gp': GaussianProcessRegressor,
    # Add other regression models as needed
}

CLUSTERING_MODELS = {
    'kmeans': KMeans,
    'dbscan': DBSCAN,
    'agglomerative': AgglomerativeClustering,
    'gmm': GaussianMixture,
    'mean_shift': MeanShift,
    'spectral': SpectralClustering,
    'birch': Birch,
    # Add other clustering models as needed
}

DIMENSIONALITY_REDUCTION_MODELS = {
    'pca': PCA,
    'svd': TruncatedSVD,
    'factor_analysis': FactorAnalysis,
    'nmf': NMF,
    # Add other dimensionality reduction models as needed
}

# Define evaluation metrics for each task
EVALUATION_METRICS = {
    'classification': {
        'accuracy': accuracy_score,
        'confusion_matrix': confusion_matrix,
        'classification_report': classification_report
    },
    'regression': {
        'mse': mean_squared_error,
        'rmse': lambda y_true, y_pred: np.sqrt(mean_squared_error(y_true, y_pred)),
        'r2': r2_score,
        'mae': mean_absolute_error,
        'msle': mean_squared_log_error,
        'evs': explained_variance_score,
        'max_error': max_error
    },
    'clustering': {
        'silhouette_score': silhouette_score
        # Add other clustering metrics as needed
    },
    'dimensionality_reduction': {
        'reconstruction_error': lambda X, X_reduced: np.mean(np.abs(X - X_reduced))
        # Add other DR metrics as needed
    }
}

# Define model parameter grids
MODEL_PARAMS = {
    'classification': {
        'rf': {
            'n_estimators': [100, 200],
            'max_depth': [None, 10, 20],
            'min_samples_split': [2, 5]
        },
        'lr': {
            'C': [0.1, 1.0, 10.0],
            'penalty': ['l2']
        },
        'svm': {
            'C': [0.1, 1.0, 10.0],
            'kernel': ['linear', 'rbf']
        },
        'knn': {
            'n_neighbors': [3, 5, 7],
            'weights': ['uniform', 'distance']
        },
        'dt': {
            'max_depth': [None, 10, 20],
            'min_samples_split': [2, 5]
        },
        'nb': {},  # GaussianNB has no parameters to tune
        'gb': {
            'n_estimators': [100, 200],
            'learning_rate': [0.01, 0.1],
            'max_depth': [3, 5]
        },
        'xgb': {
            'n_estimators': [100, 200],
            'learning_rate': [0.01, 0.1],
            'max_depth': [3, 5]
        },
        'lgbm': {
            'n_estimators': [100, 200],
            'learning_rate': [0.01, 0.1],
            'num_leaves': [31, 50]
        },
        'catboost': {
            'iterations': [100, 200],
            'learning_rate': [0.01, 0.1],
            'depth': [6, 10]
        },
        'sgd': {
            'loss': ['hinge', 'log'],
            'alpha': [0.0001, 0.001]
        },
        'pa': {
            'C': [0.01, 0.1, 1.0]
        },
        'ridge_cls': {
            'alpha': [0.1, 1.0, 10.0]
        },
        'mlp': {
            'hidden_layer_sizes': [(100,), (100, 100)],
            'activation': ['relu', 'tanh']
        },
        'et': {
            'n_estimators': [100, 200],
            'max_depth': [None, 10, 20]
        },
        'gp': {
            'max_iter_predict': [100, 200]
        }
        # Add other classification models' parameters as needed
    },
    'regression': {
        'rf': {
            'n_estimators': [100, 200],
            'max_depth': [None, 10, 20],
            'min_samples_split': [2, 5]
        },
        'lr': {
            'fit_intercept': [True, False],
            'normalize': [True, False]  # Note: 'normalize' is deprecated in newer sklearn versions
        },
        'svm': {
            'C': [0.1, 1.0, 10.0],
            'kernel': ['linear', 'rbf']
        },
        'knn': {
            'n_neighbors': [3, 5, 7],
            'weights': ['uniform', 'distance']
        },
        'dt': {
            'max_depth': [None, 10, 20],
            'min_samples_split': [2, 5]
        },
        'ridge': {
            'alpha': [0.1, 1.0, 10.0],
            'solver': ['auto', 'svd']
        },
        'lasso': {
            'alpha': [0.1, 1.0, 10.0],
            'selection': ['cyclic', 'random']
        },
        'elasticnet': {
            'alpha': [0.1, 1.0, 10.0],
            'l1_ratio': [0.2, 0.5, 0.8]
        },
        'gb': {
            'n_estimators': [100, 200],
            'learning_rate': [0.01, 0.1],
            'max_depth': [3, 5]
        },
        'xgb': {
            'n_estimators': [100, 200],
            'learning_rate': [0.01, 0.1],
            'max_depth': [3, 5]
        },
        'lgbm': {
            'n_estimators': [100, 200],
            'learning_rate': [0.01, 0.1],
            'num_leaves': [31, 50]
        },
        'catboost': {
            'iterations': [100, 200],
            'learning_rate': [0.01, 0.1],
            'depth': [6, 10]
        },
        'sgd': {
            'loss': ['squared_error', 'huber'],
            'alpha': [0.0001, 0.001]
        },
        'pa': {
            'C': [0.01, 0.1, 1.0]
        },
        'mlp': {
            'hidden_layer_sizes': [(100,), (100, 100)],
            'activation': ['relu', 'tanh']
        },
        'et': {
            'n_estimators': [100, 200],
            'max_depth': [None, 10, 20]
        },
        'gp': {
            'alpha': [1e-10, 1e-2],
            'optimizer': ['fmin_l_bfgs_b', 'powell']
        }
        # Add other regression models' parameters as needed
    },
    'clustering': {
        'kmeans': {
            'n_clusters': [3, 5, 7],
            'init': ['k-means++', 'random']
        },
        'dbscan': {
            'eps': [0.3, 0.5, 0.7],
            'min_samples': [5, 10]
        },
        'agglomerative': {
            'n_clusters': [3, 5, 7],
            'linkage': ['ward', 'complete', 'average']
        },
        'gmm': {
            'n_components': [3, 5, 7],
            'covariance_type': ['full', 'tied', 'diag', 'spherical']
        },
        'mean_shift': {
            'bandwidth': [None, 1.0, 2.0]
        },
        'spectral': {
            'n_clusters': [3, 5, 7],
            'affinity': ['rbf', 'nearest_neighbors']
        },
        'birch': {
            'n_clusters': [3, 5, 7],
            'threshold': [0.5, 1.0]
        }
        # Add other clustering models' parameters as needed
    },
    'dimensionality_reduction': {
        'pca': {
            'n_components': [2, 3, 5],
            'svd_solver': ['auto', 'full']
        },
        'svd': {
            'n_components': [2, 3, 5],
            'n_iter': [5, 10]
        },
        'factor_analysis': {
            'n_components': [2, 3, 5],
            'max_iter': [100, 200]
        },
        'nmf': {
            'n_components': [2, 3, 5],
            'init': ['random', 'nndsvd']
        }
        # Add other dimensionality reduction models' parameters as needed
    }
}

def train_model(X_train, y_train, model_class, task, **params):
    """
    Trains a single model based on the provided class and parameters.
    """
    try:
        model = model_class(**params)
        model.fit(X_train, y_train)
        logging.info(f"Trained {model_class.__name__} with params: {params}")
        return model
    except Exception as e:
        logging.error(f"Error training {model_class.__name__} with params {params}: {e}")
        return None

def optimize_model(X_train, y_train, model_class, param_grid, task):
    """
    Optimizes model hyperparameters using GridSearchCV.
    """
    try:
        if task in ['classification', 'regression']:
            scoring = 'accuracy' if task == 'classification' else 'neg_mean_squared_error'
            grid_search = GridSearchCV(model_class(), param_grid, cv=3, scoring=scoring, n_jobs=1)
            grid_search.fit(X_train, y_train)
            best_model = grid_search.best_estimator_
            best_params = grid_search.best_params_
            best_score = grid_search.best_score_
            logging.info(f"Optimized {model_class.__name__} with best params: {best_params} and best score: {best_score}")
            return best_model, best_params, best_score
        elif task in ['clustering', 'dimensionality_reduction']:
            # Clustering and DR tasks may not benefit directly from GridSearchCV
            # Implement custom optimization if needed
            logging.warning(f"Optimization for task {task} is not implemented.")
            model = train_model(X_train, y_train, model_class, task)
            best_params = model.get_params()
            best_score = None
            return model, best_params, best_score
        else:
            logging.error(f"Unsupported task type for optimization: {task}")
            return None, None, None
    except Exception as e:
        logging.error(f"Error optimizing {model_class.__name__}: {e}")
        return None, None, None

def predict_model(model, X_test, task):
    """
    Makes predictions using the trained model.
    """
    try:
        if task in ['classification', 'regression', 'clustering']:
            predictions = model.predict(X_test)
            return predictions
        elif task == 'dimensionality_reduction':
            X_reduced = model.transform(X_test)
            return X_reduced
        else:
            logging.error(f"Unsupported task for prediction: {task}")
            return None
    except Exception as e:
        logging.error(f"Error during prediction with {model.__class__.__name__}: {e}")
        return None

def evaluate_model(y_test, predictions, task, X_test=None):
    """
    Evaluates the model's predictions using predefined metrics.
    """
    metrics = EVALUATION_METRICS.get(task, {})
    results = {}

    for metric_name, metric_func in metrics.items():
        try:
            if task == 'clustering' and metric_name == 'silhouette_score':
                score = metric_func(X_test, predictions)
            elif task == 'dimensionality_reduction' and metric_name == 'reconstruction_error':
                score = metric_func(X_test, predictions)
            elif task == 'classification':
                if metric_name == 'confusion_matrix':
                    score = metric_func(y_test, predictions)
                elif metric_name == 'classification_report':
                    score = metric_func(y_test, predictions, zero_division=0)
                else:
                    score = metric_func(y_test, predictions)
            else:
                score = metric_func(y_test, predictions)
            results[metric_name] = score
            logging.info(f"Evaluation {metric_name}: {score}")
        except Exception as e:
            logging.error(f"Error computing {metric_name}: {e}")
            results[metric_name] = None
    return results

def save_results_to_yaml(results, filename='model_results.yaml'):
    """
    Saves the evaluation results to a YAML file.
    """
    try:
        with open(filename, 'w') as file:
            yaml.dump(results, file)
        logging.info(f"Saved results to {filename}")
    except Exception as e:
        logging.error(f"Error saving results to YAML: {e}")

def train_and_evaluate(model_name, task, data, params):
    """
    Trains and evaluates a single model with given parameters.
    """
    X_train, X_test, y_train, y_test, df, target_column, numerical_columns, categorical_columns = data
    model_class = None

    # Select the appropriate model class based on the task
    if task == 'classification':
        model_class = CLASSIFICATION_MODELS.get(model_name)
    elif task == 'regression':
        model_class = REGRESSION_MODELS.get(model_name)
    elif task == 'clustering':
        model_class = CLUSTERING_MODELS.get(model_name)
    elif task == 'dimensionality_reduction':
        model_class = DIMENSIONALITY_REDUCTION_MODELS.get(model_name)
    else:
        logging.error(f"Unsupported task type: {task}")
        return None

    if model_class is None:
        logging.warning(f"Model {model_name} is not available for task {task}. Skipping.")
        return None

    start_time = time.time()
    model = train_model(X_train, y_train, model_class, task, **params)
    training_time = time.time() - start_time

    if model is None:
        return None

    # Make predictions
    predictions = predict_model(model, X_test, task)
    if predictions is None:
        return None

    # Evaluate predictions
    eval_results = evaluate_model(y_test, predictions, task, X_test if task == 'clustering' else None)
    eval_results['model'] = model_name
    eval_results['training_time'] = training_time
    eval_results['parameters'] = params

    return eval_results

def auto_train(data, task='classification', n_threads=1, optimize_models=False, save_yaml=True):
    """
    Automatically trains multiple models and selects the best one based on the evaluation metric.
    If optimize_models is True, uses GridSearchCV to optimize hyperparameters.

    Args:
        data (tuple): A tuple of (X_train, X_test, y_train, y_test, df, target_column, numerical_columns, categorical_columns).
        task (str, optional): The type of task ('classification', 'regression', 'clustering', 'dimensionality_reduction'). Defaults to 'classification'.
        n_threads (int, optional): Number of threads to use for parallel training. Defaults to 1.
        optimize_models (bool, optional): Whether to optimize models using GridSearchCV. Defaults to False.
        save_yaml (bool, optional): Whether to save the results to a YAML file. Defaults to True.

    Returns:
        dict: The best model's details.
    """
    models_to_train = []
    if task == 'classification':
        models_to_train = list(CLASSIFICATION_MODELS.keys())
    elif task == 'regression':
        models_to_train = list(REGRESSION_MODELS.keys())
    elif task == 'clustering':
        models_to_train = list(CLUSTERING_MODELS.keys())
    elif task == 'dimensionality_reduction':
        models_to_train = list(DIMENSIONALITY_REDUCTION_MODELS.keys())
    else:
        logging.error(f"Unsupported task type: {task}")
        return None

    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=n_threads) as executor:
        future_to_model_param = {}
        for model_name in models_to_train:
            param_grid = MODEL_PARAMS.get(task, {}).get(model_name, {})
            if not param_grid:
                # If no parameters to tune, use empty dict
                param_sets = [{}]
            else:
                # Create list of all possible parameter combinations
                param_sets = [dict(zip(param_grid.keys(), v)) for v in product(*param_grid.values())]

            for params in param_sets:
                if optimize_models and model_name in MODEL_PARAMS.get(task, {}):
                    future = executor.submit(optimize_model, data[0], data[2], CLASSIFICATION_MODELS.get(model_name)
                    if task == 'classification' else
                    REGRESSION_MODELS.get(model_name) if task == 'regression' else
                    CLUSTERING_MODELS.get(model_name) if task == 'clustering' else
                    DIMENSIONALITY_REDUCTION_MODELS.get(model_name),
                                             param_grid, task)
                    future_to_model_param[future] = (model_name, params, True)
                else:
                    future = executor.submit(train_and_evaluate, model_name, task, data, params)
                    future_to_model_param[future] = (model_name, params, False)

        # Use a progress bar
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task_progress = progress.add_task("[cyan]Training models...", total=len(future_to_model_param))
            for future in concurrent.futures.as_completed(future_to_model_param):
                model_name, params, optimized = future_to_model_param[future]
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                        if optimized:
                            console.print(f"[green]Optimized[/green] {model_name} with params: {params} -> Score: {result.get('accuracy') or result.get('mse')}")
                        else:
                            console.print(f"[green]Trained[/green] {model_name} with params: {params} -> Score: {result.get('accuracy') or result.get('mse')}")
                    else:
                        if optimized:
                            console.print(f"[red]Failed to optimize[/red] {model_name} with params: {params}")
                        else:
                            console.print(f"[red]Failed to train[/red] {model_name} with params: {params}")
                except Exception as exc:
                    console.print(f"[red]Model {model_name} with params {params} generated an exception: {exc}[/red]")
                progress.advance(task_progress)

    if not results:
        logging.error("No models were successfully trained.")
        return None

    # Determine the best model based on a primary metric
    primary_metric = None
    if task == 'classification':
        primary_metric = 'accuracy'
    elif task == 'regression':
        primary_metric = 'mse'  # Lower is better
    elif task == 'clustering':
        primary_metric = 'silhouette_score'
    elif task == 'dimensionality_reduction':
        primary_metric = 'reconstruction_error'  # Lower is better
    else:
        logging.error(f"No primary metric defined for task: {task}")
        return None

    # Handle cases where primary_metric might not be present
    filtered_results = [res for res in results if res.get(primary_metric) is not None]
    if not filtered_results:
        logging.error(f"No results with the primary metric '{primary_metric}' found.")
        return None

    # For metrics where higher is better
    if primary_metric in ['accuracy', 'silhouette_score']:
        best_model = max(filtered_results, key=lambda x: x[primary_metric])
    else:
        # For metrics where lower is better
        best_model = min(filtered_results, key=lambda x: x[primary_metric])

    logging.info(f"Best model: {best_model['model']} with {primary_metric}: {best_model[primary_metric]}")

    # Display results in a table
    table = Table(title="Model Training Results")

    table.add_column("Model", style="cyan", no_wrap=True)
    table.add_column("Parameters", style="magenta")
    for metric in EVALUATION_METRICS[task].keys():
        table.add_column(metric.capitalize(), justify="right", style="green")
    table.add_column("Training Time (s)", justify="right", style="yellow")

    for res in results:
        row = [
            res['model'],
            str(res['parameters']),
        ]
        for metric in EVALUATION_METRICS[task].keys():
            value = res.get(metric)
            if isinstance(value, float):
                value = f"{value:.4f}"
            row.append(str(value))
        row.append(f"{res['training_time']:.2f}")
        table.add_row(*row)

    console.print(table)

    # Optionally, save results to YAML
    if save_yaml:
        save_results_to_yaml(results)

    # Optionally, store the best model in the global MODELS dictionary
    MODELS[best_model['model']] = best_model['parameters']

    console.print(f"[bold green]Best model:[/bold green] {best_model['model']} with {primary_metric}: {best_model[primary_metric]}")
    return best_model

# ---- Usage Example ----
if __name__ == "__main__":
    # Example data preparation
    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split

    # Load dataset
    iris = load_iris()
    X, y = iris.data, iris.target
    df = None  # Replace with actual DataFrame if available
    target_column = 'target'
    numerical_columns = iris.feature_names
    categorical_columns = []

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Prepare data tuple
    data = (X_train, X_test, y_train, y_test, df, target_column, numerical_columns, categorical_columns)

    # Run auto_train with hyperparameter optimization
    best_model = auto_train(data, task='classification', n_threads=4, optimize_models=True)
    console.print("Best Model Details:")
    console.print(best_model)
