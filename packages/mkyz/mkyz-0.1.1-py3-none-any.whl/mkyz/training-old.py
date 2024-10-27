from sklearn.ensemble import (
    RandomForestClassifier, RandomForestRegressor, BaggingClassifier, BaggingRegressor,
    AdaBoostClassifier, AdaBoostRegressor, StackingClassifier, StackingRegressor,
    GradientBoostingClassifier, GradientBoostingRegressor, ExtraTreesClassifier, ExtraTreesRegressor,
    VotingClassifier, VotingRegressor
)
from sklearn.linear_model import (
    LogisticRegression, LinearRegression, Ridge, Lasso, ElasticNet,
    SGDClassifier, SGDRegressor, RidgeClassifier, PassiveAggressiveClassifier, PassiveAggressiveRegressor
)
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor, KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering, Birch, MeanShift, SpectralClustering
from sklearn.decomposition import PCA, TruncatedSVD, FactorAnalysis, NMF
from sklearn.mixture import GaussianMixture
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, mean_squared_error, r2_score, \
    mean_absolute_error , mean_squared_log_error, explained_variance_score, max_error
from sklearn.pipeline import make_pipeline
import numpy as np


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

from mlxtend.frequent_patterns import apriori, association_rules

# Global variable to store trained models
MODELS = {}

# ---- CLASSIFICATION ----
def train_random_forest_classification(X_train, y_train, **model_params):
    n_estimators = model_params.get('n_estimators', 100)
    clf = RandomForestClassifier(n_estimators=n_estimators, random_state=42, **model_params)
    clf.fit(X_train, y_train)
    return clf

def train_logistic_regression(X_train, y_train, **model_params):
    clf = LogisticRegression(**model_params)
    clf.fit(X_train, y_train)
    return clf

def train_svm_classification(X_train, y_train, **model_params):
    clf = SVC(**model_params)
    clf.fit(X_train, y_train)
    return clf

def train_knn_classification(X_train, y_train, **model_params):
    n_neighbors = model_params.get('n_neighbors', 5)
    clf = KNeighborsClassifier(n_neighbors=n_neighbors, **model_params)
    clf.fit(X_train, y_train)
    return clf

def train_decision_tree_classification(X_train, y_train, **model_params):
    clf = DecisionTreeClassifier(**model_params)
    clf.fit(X_train, y_train)
    return clf

def train_naive_bayes_classification(X_train, y_train, model_type='gaussian', **model_params):
    if model_type == 'gaussian':
        clf = GaussianNB(**model_params)
    elif model_type == 'multinomial':
        clf = MultinomialNB(**model_params)
    elif model_type == 'bernoulli':
        clf = BernoulliNB(**model_params)
    else:
        raise ValueError(f"Unsupported Naive Bayes type: {model_type}")
    clf.fit(X_train, y_train)
    return clf

def train_gradient_boosting_classification(X_train, y_train, **model_params):
    clf = GradientBoostingClassifier(**model_params)
    clf.fit(X_train, y_train)
    return clf

def train_xgboost_classification(X_train, y_train, **model_params):
    if xgb is None:
        raise ImportError("xgboost is not installed.")
    clf = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss', **model_params)
    clf.fit(X_train, y_train)
    return clf

def train_lightgbm_classification(X_train, y_train, **model_params):
    if lgb is None:
        raise ImportError("lightgbm is not installed.")
    clf = lgb.LGBMClassifier(**model_params)
    clf.fit(X_train, y_train)
    return clf

def train_catboost_classification(X_train, y_train, **model_params):
    if cb is None:
        raise ImportError("catboost is not installed.")
    clf = cb.CatBoostClassifier(verbose=0, **model_params)
    clf.fit(X_train, y_train)
    return clf

def train_sgd_classification(X_train, y_train, **model_params):
    clf = SGDClassifier(**model_params)
    clf.fit(X_train, y_train)
    return clf

def train_passive_aggressive_classification(X_train, y_train, **model_params):
    clf = PassiveAggressiveClassifier(**model_params)
    clf.fit(X_train, y_train)
    return clf

def train_ridge_classifier(X_train, y_train, **model_params):
    clf = RidgeClassifier(**model_params)
    clf.fit(X_train, y_train)
    return clf

def train_mlp_classification(X_train, y_train, **model_params):
    clf = MLPClassifier(**model_params)
    clf.fit(X_train, y_train)
    return clf

def train_extra_trees_classification(X_train, y_train, **model_params):
    clf = ExtraTreesClassifier(**model_params)
    clf.fit(X_train, y_train)
    return clf

def train_gaussian_process_classification(X_train, y_train, **model_params):
    from sklearn.gaussian_process import GaussianProcessClassifier
    clf = GaussianProcessClassifier(**model_params)
    clf.fit(X_train, y_train)
    return clf

# ---- REGRESSION ----
def train_random_forest_regression(X_train, y_train, **model_params):
    n_estimators = model_params.get('n_estimators', 100)
    reg = RandomForestRegressor(n_estimators=n_estimators, random_state=42, **model_params)
    reg.fit(X_train, y_train)
    return reg

def train_linear_regression(X_train, y_train, **model_params):
    reg = LinearRegression(**model_params)
    reg.fit(X_train, y_train)
    return reg

def train_svm_regression(X_train, y_train, **model_params):
    reg = SVR(**model_params)
    reg.fit(X_train, y_train)
    return reg

def train_knn_regression(X_train, y_train, **model_params):
    n_neighbors = model_params.get('n_neighbors', 5)
    reg = KNeighborsRegressor(n_neighbors=n_neighbors, **model_params)
    reg.fit(X_train, y_train)
    return reg

def train_decision_tree_regression(X_train, y_train, **model_params):
    reg = DecisionTreeRegressor(**model_params)
    reg.fit(X_train, y_train)
    return reg

def train_ridge_regression(X_train, y_train, **model_params):
    reg = Ridge(**model_params)
    reg.fit(X_train, y_train)
    return reg

def train_lasso_regression(X_train, y_train, **model_params):
    reg = Lasso(**model_params)
    reg.fit(X_train, y_train)
    return reg

def train_elastic_net_regression(X_train, y_train, **model_params):
    reg = ElasticNet(**model_params)
    reg.fit(X_train, y_train)
    return reg

def train_gradient_boosting_regression(X_train, y_train, **model_params):
    reg = GradientBoostingRegressor(**model_params)
    reg.fit(X_train, y_train)
    return reg

def train_xgboost_regression(X_train, y_train, **model_params):
    if xgb is None:
        raise ImportError("xgboost is not installed.")
    reg = xgb.XGBRegressor(**model_params)
    reg.fit(X_train, y_train)
    return reg

def train_lightgbm_regression(X_train, y_train, **model_params):
    if lgb is None:
        raise ImportError("lightgbm is not installed.")
    reg = lgb.LGBMRegressor(**model_params)
    reg.fit(X_train, y_train)
    return reg

def train_catboost_regression(X_train, y_train, **model_params):
    if cb is None:
        raise ImportError("catboost is not installed.")
    reg = cb.CatBoostRegressor(verbose=0, **model_params)
    reg.fit(X_train, y_train)
    return reg

def train_sgd_regression(X_train, y_train, **model_params):
    reg = SGDRegressor(**model_params)
    reg.fit(X_train, y_train)
    return reg

def train_passive_aggressive_regression(X_train, y_train, **model_params):
    reg = PassiveAggressiveRegressor(**model_params)
    reg.fit(X_train, y_train)
    return reg

def train_mlp_regression(X_train, y_train, **model_params):
    reg = MLPRegressor(**model_params)
    reg.fit(X_train, y_train)
    return reg

def train_extra_trees_regression(X_train, y_train, **model_params):
    reg = ExtraTreesRegressor(**model_params)
    reg.fit(X_train, y_train)
    return reg

def train_gaussian_process_regression(X_train, y_train, **model_params):
    from sklearn.gaussian_process import GaussianProcessRegressor
    reg = GaussianProcessRegressor(**model_params)
    reg.fit(X_train, y_train)
    return reg

# ---- CLUSTERING ----
def train_kmeans_clustering(X_train, **model_params):
    n_clusters = model_params.get('n_clusters', 3)
    cluster = KMeans(n_clusters=n_clusters, random_state=42, **model_params)
    cluster.fit(X_train)
    return cluster

def train_dbscan_clustering(X_train, **model_params):
    eps = model_params.get('eps', 0.5)
    min_samples = model_params.get('min_samples', 5)
    cluster = DBSCAN(eps=eps, min_samples=min_samples, **model_params)
    cluster.fit(X_train)
    return cluster

def train_agglomerative_clustering(X_train, **model_params):
    n_clusters = model_params.get('n_clusters', 3)
    cluster = AgglomerativeClustering(n_clusters=n_clusters, **model_params)
    cluster.fit(X_train)
    return cluster

def train_gaussian_mixture_clustering(X_train, **model_params):
    n_components = model_params.get('n_components', 3)
    cluster = GaussianMixture(n_components=n_components, random_state=42, **model_params)
    cluster.fit(X_train)
    return cluster

def train_mean_shift_clustering(X_train, **model_params):
    cluster = MeanShift(**model_params)
    cluster.fit(X_train)
    return cluster

def train_spectral_clustering(X_train, **model_params):
    n_clusters = model_params.get('n_clusters', 3)
    cluster = SpectralClustering(n_clusters=n_clusters, random_state=42, **model_params)
    cluster.fit(X_train)
    return cluster

def train_birch_clustering(X_train, **model_params):
    n_clusters = model_params.get('n_clusters', 3)
    cluster = Birch(n_clusters=n_clusters, **model_params)
    cluster.fit(X_train)
    return cluster

# ---- ASSOCIATION RULE LEARNING ----
def train_apriori(X_train, **model_params):
    min_support = model_params.get('min_support', 0.1)
    frequent_itemsets = apriori(X_train, min_support=min_support, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5)
    return rules

# ---- DIMENSIONALITY REDUCTION ----
def train_pca(X_train, **model_params):
    n_components = model_params.get('n_components', 2)
    pca = PCA(n_components=n_components, **model_params)
    X_reduced = pca.fit_transform(X_train)
    return pca, X_reduced

def train_truncated_svd(X_train, **model_params):
    n_components = model_params.get('n_components', 2)
    svd = TruncatedSVD(n_components=n_components, **model_params)
    X_reduced = svd.fit_transform(X_train)
    return svd, X_reduced

def train_factor_analysis(X_train, **model_params):
    n_components = model_params.get('n_components', 2)
    fa = FactorAnalysis(n_components=n_components, **model_params)
    X_reduced = fa.fit_transform(X_train)
    return fa, X_reduced

def train_nmf(X_train, **model_params):
    n_components = model_params.get('n_components', 2)
    nmf = NMF(n_components=n_components, **model_params)
    X_reduced = nmf.fit_transform(X_train)
    return nmf, X_reduced

# ---- ENSEMBLING METHODS ----
def train_bagging_classification(X_train, y_train, base_estimator=DecisionTreeClassifier(), **model_params):
    clf = BaggingClassifier(base_estimator=base_estimator, **model_params)
    clf.fit(X_train, y_train)
    return clf

def train_bagging_regression(X_train, y_train, base_estimator=DecisionTreeRegressor(), **model_params):
    reg = BaggingRegressor(base_estimator=base_estimator, **model_params)
    reg.fit(X_train, y_train)
    return reg

def train_adaboost_classification(X_train, y_train, **model_params):
    clf = AdaBoostClassifier(**model_params)
    clf.fit(X_train, y_train)
    return clf

def train_adaboost_regression(X_train, y_train, **model_params):
    reg = AdaBoostRegressor(**model_params)
    reg.fit(X_train, y_train)
    return reg

def train_stacking_classification(X_train, y_train, estimators, final_estimator, **model_params):
    clf = StackingClassifier(estimators=estimators, final_estimator=final_estimator, **model_params)
    clf.fit(X_train, y_train)
    return clf

def train_stacking_regression(X_train, y_train, estimators, final_estimator, **model_params):
    reg = StackingRegressor(estimators=estimators, final_estimator=final_estimator, **model_params)
    reg.fit(X_train, y_train)
    return reg

def train_voting_classification(X_train, y_train, estimators, voting='hard', **model_params):
    clf = VotingClassifier(estimators=estimators, voting=voting, **model_params)
    clf.fit(X_train, y_train)
    return clf

def train_voting_regression(X_train, y_train, estimators, voting='hard', **model_params):
    reg = VotingRegressor(estimators=estimators, **model_params)
    reg.fit(X_train, y_train)
    return reg

# ---- GENERAL TRAIN FUNCTION ----
def train(data, task='classification', model='rf', **model_params):
    """
    Trains a machine learning model based on the task and model specified.

    Args:
        data (tuple): A tuple of (X, y) containing the training data and target labels.
        task (str, optional): The type of task ('classification', 'regression', or 'clustering'). Defaults to 'classification'.
        model (str, optional): The model to be trained (e.g., 'rf' for Random Forest, 'svm' for Support Vector Machine). Defaults to 'rf'.
        **model_params: Additional model-specific parameters.

    Returns:
        object: The trained model object.

    Usage:
        >>> from mkyz import training as tr
        >>> model = tr.train(data=data, task='classification', model='rf', n_estimators=100)
    """
    
    
    X_train, X_test, y_train, y_test, df, target_column , numerical_columns, categorical_columns = data

    # Classification
    if task == 'classification':
        if model == 'rf':
            clf = train_random_forest_classification(X_train, y_train, **model_params)
        elif model == 'lr':
            clf = train_logistic_regression(X_train, y_train, **model_params)
        elif model == 'svm':
            clf = train_svm_classification(X_train, y_train, **model_params)
        elif model == 'knn':
            clf = train_knn_classification(X_train, y_train, **model_params)
        elif model == 'dt':
            clf = train_decision_tree_classification(X_train, y_train, **model_params)
        elif model == 'nb':
            clf = train_naive_bayes_classification(X_train, y_train, **model_params)
        elif model == 'gb':
            clf = train_gradient_boosting_classification(X_train, y_train, **model_params)
        elif model == 'xgb':
            clf = train_xgboost_classification(X_train, y_train, **model_params)
        elif model == 'lgbm':
            clf = train_lightgbm_classification(X_train, y_train, **model_params)
        elif model == 'catboost':
            clf = train_catboost_classification(X_train, y_train, **model_params)
        elif model == 'sgd':
            clf = train_sgd_classification(X_train, y_train, **model_params)
        elif model == 'pa':
            clf = train_passive_aggressive_classification(X_train, y_train, **model_params)
        elif model == 'ridge_cls':
            clf = train_ridge_classifier(X_train, y_train, **model_params)
        elif model == 'mlp':
            clf = train_mlp_classification(X_train, y_train, **model_params)
        elif model == 'et':
            clf = train_extra_trees_classification(X_train, y_train, **model_params)
        elif model == 'gp':
            clf = train_gaussian_process_classification(X_train, y_train, **model_params)
        elif model == 'voting':
            estimators = model_params.get('estimators', [])
            voting_type = model_params.get('voting', 'hard')
            clf = train_voting_classification(X_train, y_train, estimators, voting=voting_type, **model_params)
        elif model == 'bagging':
            clf = train_bagging_classification(X_train, y_train, **model_params)
        elif model == 'boosting':
            clf = train_adaboost_classification(X_train, y_train, **model_params)
        elif model == 'stacking':
            estimators = model_params.get('estimators', [])
            final_estimator = model_params.get('final_estimator', LogisticRegression())
            clf = train_stacking_classification(X_train, y_train, estimators, final_estimator, **model_params)
        else:
            raise ValueError(f"Unsupported model type for classification: {model}")
        MODELS[model] = clf
        return clf

    # Regression
    elif task == 'regression':
        if model == 'rf':
            reg = train_random_forest_regression(X_train, y_train, **model_params)
        elif model == 'lr':
            reg = train_linear_regression(X_train, y_train, **model_params)
        elif model == 'svm':
            reg = train_svm_regression(X_train, y_train, **model_params)
        elif model == 'knn':
            reg = train_knn_regression(X_train, y_train, **model_params)
        elif model == 'dt':
            reg = train_decision_tree_regression(X_train, y_train, **model_params)
        elif model == 'ridge':
            reg = train_ridge_regression(X_train, y_train, **model_params)
        elif model == 'lasso':
            reg = train_lasso_regression(X_train, y_train, **model_params)
        elif model == 'elasticnet':
            reg = train_elastic_net_regression(X_train, y_train, **model_params)
        elif model == 'gb':
            reg = train_gradient_boosting_regression(X_train, y_train, **model_params)
        elif model == 'xgb':
            reg = train_xgboost_regression(X_train, y_train, **model_params)
        elif model == 'lgbm':
            reg = train_lightgbm_regression(X_train, y_train, **model_params)
        elif model == 'catboost':
            reg = train_catboost_regression(X_train, y_train, **model_params)
        elif model == 'sgd':
            reg = train_sgd_regression(X_train, y_train, **model_params)
        elif model == 'pa':
            reg = train_passive_aggressive_regression(X_train, y_train, **model_params)
        elif model == 'mlp':
            reg = train_mlp_regression(X_train, y_train, **model_params)
        elif model == 'et':
            reg = train_extra_trees_regression(X_train, y_train, **model_params)
        elif model == 'gp':
            reg = train_gaussian_process_regression(X_train, y_train, **model_params)
        elif model == 'voting':
            estimators = model_params.get('estimators', [])
            reg = train_voting_regression(X_train, y_train, estimators, **model_params)
        elif model == 'bagging':
            reg = train_bagging_regression(X_train, y_train, **model_params)
        elif model == 'boosting':
            reg = train_adaboost_regression(X_train, y_train, **model_params)
        elif model == 'stacking':
            estimators = model_params.get('estimators', [])
            final_estimator = model_params.get('final_estimator', LinearRegression())
            reg = train_stacking_regression(X_train, y_train, estimators, final_estimator, **model_params)
        else:
            raise ValueError(f"Unsupported model type for regression: {model}")
        MODELS[model] = reg
        return reg

    # Clustering
    elif task == 'clustering':
        if model == 'kmeans':
            cluster = train_kmeans_clustering(X_train, **model_params)
        elif model == 'dbscan':
            cluster = train_dbscan_clustering(X_train, **model_params)
        elif model == 'agglomerative':
            cluster = train_agglomerative_clustering(X_train, **model_params)
        elif model == 'gmm':
            cluster = train_gaussian_mixture_clustering(X_train, **model_params)
        elif model == 'mean_shift':
            cluster = train_mean_shift_clustering(X_train, **model_params)
        elif model == 'spectral':
            cluster = train_spectral_clustering(X_train, **model_params)
        elif model == 'birch':
            cluster = train_birch_clustering(X_train, **model_params)
        else:
            raise ValueError(f"Unsupported model type for clustering: {model}")
        MODELS[model] = cluster
        return cluster

    # Association Rule Learning
    elif task == 'association':
        if model == 'apriori':
            rules = train_apriori(X_train, **model_params)
            return rules
        else:
            raise ValueError(f"Unsupported model type for association rule learning: {model}")

    # Dimensionality Reduction
    elif task == 'dimensionality_reduction':
        if model == 'pca':
            pca, X_reduced = train_pca(X_train, **model_params)
            return pca, X_reduced
        elif model == 'svd':
            svd, X_reduced = train_truncated_svd(X_train, **model_params)
            return svd, X_reduced
        elif model == 'factor_analysis':
            fa, X_reduced = train_factor_analysis(X_train, **model_params)
            return fa, X_reduced
        elif model == 'nmf':
            nmf, X_reduced = train_nmf(X_train, **model_params)
            return nmf, X_reduced
        else:
            raise ValueError(f"Unsupported model type for dimensionality reduction: {model}")

    else:
        raise ValueError(f"Unsupported task type: {task}")

# ---- PREDICT FUNCTION ----
def predict(data, fitted_model=None, task='classification', model='rf'):
    """
    Makes predictions on the provided data using the fitted model.

    Args:
        data (array-like): Data to make predictions on.
        fitted_model (object, optional): The pre-trained model to use for predictions. Defaults to None.
        task (str, optional): The type of task ('classification', 'regression'). Defaults to 'classification'.
        model (str, optional): The model type (e.g., 'rf' for Random Forest). Defaults to 'rf'.

    Returns:
        array-like: The predicted labels or values.

    Usage:
        >>> predictions = tr.predict(data=data, fitted_model=model, task='classification')
    """
    X_train, X_test, y_train, y_test, df, target_column , numerical_columns, categorical_columns = data

    # Use fitted model if provided, otherwise retrieve from MODELS
    clf = fitted_model if fitted_model else MODELS.get(model)

    if clf:
        if task in ['classification', 'regression']:
            predictions = clf.predict(X_test)
            return predictions
        elif task == 'clustering':
            if hasattr(clf, 'predict'):
                predictions = clf.predict(X_test)
            elif hasattr(clf, 'labels_'):
                predictions = clf.fit_predict(X_test)
            else:
                raise AttributeError("Clustering model does not have a predict method.")
            return predictions
        elif task == 'association':
            raise ValueError("Association rule learning does not support predictions.")
        elif task == 'dimensionality_reduction':
            X_reduced = clf.transform(X_test)
            return X_reduced
    else:
        raise ValueError(f"Model {model} is not trained yet.")

# ---- EVALUATE FUNCTION ----
def evaluate(data, predictions=None, task='classification', model='rf'):
    """
    Evaluates the model's performance on the provided data.

    Args:
        data (tuple): A tuple of (X_test, y_test) containing the test data and true labels.
        predictions (array-like, optional): Predictions from the model. If not provided, they will be calculated internally. Defaults to None.
        task (str, optional): The type of task ('classification', 'regression'). Defaults to 'classification'.
        model (str, optional): The model used for evaluation (e.g., 'rf' for Random Forest). Defaults to 'rf'.

    Returns:
        dict: A dictionary containing evaluation metrics such as accuracy, precision, recall, etc.

    Usage:
        >>> results = tr.evaluate(data=data, predictions=predictions, task='classification')
        >>> print(results)
    """

    X_train, X_test, y_train, y_test, df, target_column , numerical_columns, categorical_columns = data

    # Explicitly check if predictions is None
    if predictions is None:
        predictions = predict(data, task=task, model=model)

    if task == 'classification':
        acc = accuracy_score(y_test, predictions)
        cm = confusion_matrix(y_test, predictions)
        report = classification_report(y_test, predictions)
        print(f"Accuracy: {acc}")
        print("Confusion Matrix:")
        print(cm)
        print("Classification Report:")
        print(report)

    elif task == 'regression':
        mse = mean_squared_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)
        mae = mean_absolute_error(y_test, predictions)
        rmse = np.sqrt(mse)
        msle = mean_squared_log_error(y_test, predictions)
        evs = explained_variance_score(y_test, predictions)
        max_err = max_error(y_test, predictions)
        
        
        print(f"Mean Squared Error: {mse}")
        print(f"R2 Score: {r2}")
        print(f"Mean Absolute Error: {mae}")
        print(f"Root Mean Squared Error: {rmse}")
        print(f"Mean Squared Log Error: {msle}")
        print(f"Explained Variance Score: {evs}")
        print(f"Max Error: {max_err}")

    elif task == 'clustering':
        print("Clustering completed. Use cluster labels for analysis.")
        # Optionally, you can add more evaluation metrics like silhouette score

    elif task == 'association':
        print("Association Rule Learning: No evaluation metrics available.")

    elif task == 'dimensionality_reduction':
        print("Dimensionality Reduction completed. The reduced dataset is returned.")


# buraya bir auto train fonksiyonu yazacağız
# train işlevini multithread yaparak yapacak
# bu fonksiyonun amacı verilen bir dataseti otomatik olarak train edip en iyi modeli seçmek olacak
#eğitim yapılırken modelin eğitim süresini ve sonuç metirkleri yazdıracak ardından parametreler ile yaml dosyasına yazcak 
# bunu yaparken seçilen task ne ise o taska ait bütün modelleri train edecek en iyi sonucu veren parametreli bulur
# ve o modeli döndürür

# kullanımı şu şekilde olacak
# best_model = auto_train(data, task='classification', n_threads=8)

# ---- AUTO TRAIN FUNCTION ----
