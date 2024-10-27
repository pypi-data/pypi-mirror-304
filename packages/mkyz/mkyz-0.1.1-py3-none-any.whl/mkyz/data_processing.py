# mkyz/data_processing.py dosyası içeriği
import io
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

from sklearn.base import BaseEstimator, TransformerMixin

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import logging
import warnings
warnings.filterwarnings("ignore")

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fill_missing_values(df, numerical_columns, categorical_columns):
    """
    Doldurulacak eksik değerler için imputer'ları uygular.
    
    Args:
        df (pd.DataFrame): Veri çerçevesi.
        numerical_columns (list): Sayısal sütunlar.
        categorical_columns (list): Kategorik sütunlar.
    
    Returns:
        pd.DataFrame: Eksik değerler doldurulmuş veri çerçevesi.
    """
    logger.info("Eksik değerler dolduruluyor...")

    # Sayısal sütunlar için ortalama ile doldurma
    for col in numerical_columns:
        if df[col].isnull().sum() > 0:
            mean_value = df[col].mean()
            df[col].fillna(mean_value, inplace=True)
            logger.debug(f"Sayısal sütun '{col}' için ortalama ({mean_value}) ile dolduruldu.")

    # Kategorik sütunlar için en sık değer ile doldurma
    for col in categorical_columns:
        if df[col].isnull().sum() > 0:
            mode_value = df[col].mode()[0]
            df[col].fillna(mode_value, inplace=True)
            logger.debug(f"Kategorik sütun '{col}' için en sık değer ({mode_value}) ile dolduruldu.")

    return df

def detect_outliers(df, numerical_columns, threshold=1.5):
    """
    Aykırı değerleri tespit eder.
    
    Args:
        df (pd.DataFrame): Veri çerçevesi.
        numerical_columns (list): Sayısal sütunlar.
        threshold (float, optional): Aykırı değer tespit eşiği. Defaults to 1.5.
    
    Returns:
        dict: Aykırı değerlerin bulunduğu sütunlar ve bu sütunlardaki aykırı değerlerin indeksleri.
    """
    logger.info("Aykırı değerler tespit ediliyor...")
    outliers = {}

    for col in numerical_columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        outlier_indices = df[(df[col] < lower_bound) | (df[col] > upper_bound)].index.tolist()

        if outlier_indices:
            outliers[col] = outlier_indices
            logger.debug(f"Sütun '{col}' için {len(outlier_indices)} aykırı değer tespit edildi.")

    logger.info(f"Toplam {len(outliers)} sütunda aykırı değer tespit edildi.")
    return outliers

def handle_outliers(df, outliers, strategy='remove'):
    """
    Aykırı değerleri işleme alır.
    
    Args:
        df (pd.DataFrame): Veri çerçevesi.
        outliers (dict): Aykırı değerlerin bulunduğu sütunlar ve indeksler.
        strategy (str, optional): 'remove' veya 'cap'. Defaults to 'remove'.
    
    Returns:
        pd.DataFrame: Aykırı değerler işlenmiş veri çerçevesi.
    """
    logger.info(f"Aykırı değerler '{strategy}' stratejisi ile işleniyor...")

    if strategy == 'remove':
        indices_to_remove = set()
        for indices in outliers.values():
            indices_to_remove.update(indices)
        df = df.drop(index=indices_to_remove)
        logger.info(f"{len(indices_to_remove)} satır aykırı değerler nedeniyle kaldırıldı.")
    elif strategy == 'cap':
        for col, indices in outliers.items():
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df.loc[df[col] < lower_bound, col] = lower_bound
            df.loc[df[col] > upper_bound, col] = upper_bound
            logger.debug(f"Sütun '{col}' için aykırı değerler sınırlandırıldı.")
    else:
        logger.warning(f"Belirtilen strateji '{strategy}' desteklenmiyor. Hiçbir şey yapılmadı.")

    return df

def transform_categorical(df, categorical_columns, method='onehot'):
    """
    Kategorik değişkenleri dönüştürür.
    
    Args:
        df (pd.DataFrame): Veri çerçevesi.
        categorical_columns (list): Kategorik sütunlar.
        method (str, optional): Dönüştürme yöntemi ('onehot', 'frequency', 'target'). Defaults to 'onehot'.
    
    Returns:
        pd.DataFrame: Dönüştürülmüş veri çerçevesi.
    """
    logger.info(f"Kategorik değişkenler '{method}' yöntemi ile dönüştürülüyor...")

    if method == 'onehot':
        # Güncellenmiş parametre: 'sparse_output' kullanılıyor
        encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        encoded_cols = pd.DataFrame(
            encoder.fit_transform(df[categorical_columns]),
            columns=encoder.get_feature_names_out(categorical_columns),
            index=df.index
        )
        df = pd.concat([df.drop(columns=categorical_columns), encoded_cols], axis=1)
        logger.debug("One-Hot Encoding uygulandı.")

    elif method == 'frequency':
        for col in categorical_columns:
            freq = df[col].value_counts() / len(df)
            df[col] = df[col].map(freq)
            logger.debug(f"Sütun '{col}' için frekans kodlaması uygulandı.")

    elif method == 'target':
        # Bu yöntem için hedef değişken gereklidir. Fonksiyon parametreleri güncellenebilir.
        logger.warning("Target encoding henüz desteklenmiyor.")

    else:
        logger.warning(f"Belirtilen yöntem '{method}' desteklenmiyor. Hiçbir şey yapılmadı.")

    return df

def prepare_data(filepath, target_column=None, numerical_columns=None, categorical_columns=None,
                 test_size=0.2, random_state=42, binary_threshold=2, low_cardinality_threshold=10,
                 drop_columns=None, outlier_strategy='remove', categorical_transform_method='onehot'):
    """
    Prepares and preprocesses data for machine learning tasks.

    This function loads a dataset from a CSV file, performs exploratory data analysis,
    handles missing values and outliers, transforms categorical variables, and splits the data
    into training and testing sets. It supports both classification and regression tasks
    by allowing customization of numerical and categorical columns, as well as various
    preprocessing strategies.

    Args:
        filepath (str): Path to the CSV file containing the dataset.
        target_column (str, optional): Name of the target column. 
            If not specified, the last column in the dataset is used as the target.
            Defaults to None.
        numerical_columns (list, optional): List of numerical feature column names.
            If not specified, columns with data types 'int64' and 'float64' are considered numerical.
            Defaults to None.
        categorical_columns (list, optional): List of categorical feature column names.
            If not specified, columns with data types 'object' and 'category' are considered categorical.
            Defaults to None.
        test_size (float, optional): Proportion of the dataset to include in the test split.
            Must be between 0.0 and 1.0. Defaults to 0.2.
        random_state (int, optional): Controls the shuffling applied to the data before splitting.
            Pass an int for reproducible output across multiple function calls. Defaults to 42.
        binary_threshold (int, optional): Maximum number of unique values in a numerical column
            to treat it as a binary categorical column. Defaults to 2.
        low_cardinality_threshold (int, optional): Maximum number of unique values in a numerical column
            to treat it as a low cardinality categorical column. Defaults to 10.
        drop_columns (list, optional): List of column names to drop from the dataset.
            Columns not present in the dataset will be ignored with a warning. Defaults to None.
        outlier_strategy (str, optional): Strategy to handle outliers in numerical columns.
            - 'remove': Remove outlier rows.
            - 'replace': Replace outliers with a specified value or statistic.
            Defaults to 'remove'.
        categorical_transform_method (str, optional): Method to transform categorical variables.
            - 'onehot': Apply One-Hot Encoding.
            - 'label': Apply Label Encoding.
            - 'frequency': Apply Frequency Encoding.
            Defaults to 'onehot'.

    Returns:
        tuple: A tuple containing the following elements:
            - X_train (np.ndarray): Preprocessed training feature set.
            - X_test (np.ndarray): Preprocessed testing feature set.
            - y_train (pd.Series or np.ndarray): Training target values.
            - y_test (pd.Series or np.ndarray): Testing target values.
            - df (pd.DataFrame): The original dataframe after preprocessing.
            - target_column (str): The name of the target column.
            - numerical_columns (list): List of numerical feature column names after preprocessing.
            - categorical_columns (list): List of categorical feature column names after preprocessing.

    Raises:
        ValueError:
            - If the target column is not found in the dataframe.
            - If an unsupported outlier strategy is provided.
            - If an unsupported categorical transformation method is specified.

    Examples:
        >>> # Example 1: Basic data preparation with default settings
        >>> X_train, X_test, y_train, y_test, df, target, num_cols, cat_cols = prepare_data(
        ...     filepath='data.csv'
        ... )

        >>> # Example 2: Specifying target column and dropping unnecessary columns
        >>> X_train, X_test, y_train, y_test, df, target, num_cols, cat_cols = prepare_data(
        ...     filepath='data.csv',
        ...     target_column='price',
        ...     drop_columns=['id', 'timestamp']
        ... )

        >>> # Example 3: Handling outliers by replacing them and using frequency encoding for categoricals
        >>> X_train, X_test, y_train, y_test, df, target, num_cols, cat_cols = prepare_data(
        ...     filepath='data.csv',
        ...     outlier_strategy='replace',
        ...     categorical_transform_method='frequency'
        ... )

        >>> # Example 4: Preparing data for a regression task with specified numerical and categorical columns
        >>> numerical = ['age', 'income', 'expenses']
        >>> categorical = ['gender', 'occupation', 'city']
        >>> X_train, X_test, y_train, y_test, df, target, num_cols, cat_cols = prepare_data(
        ...     filepath='data.csv',
        ...     target_column='salary',
        ...     numerical_columns=numerical,
        ...     categorical_columns=categorical,
        ...     test_size=0.3,
        ...     random_state=123
        ... )
    """
    # Load the dataset
    df = pd.read_csv(filepath)

    # Display dataset information
    logger.info("First 5 rows of the dataset:")
    logger.info(df.head())

    logger.info("Dataset information:")
    buffer = io.StringIO()
    df.info(buf=buffer)
    info = buffer.getvalue()
    logger.info(info)

    logger.info("Statistical summary of the dataset:")
    logger.info(df.describe().T)

    # Drop unnecessary columns if specified
    if drop_columns:
        missing_cols = [col for col in drop_columns if col not in df.columns]
        if missing_cols:
            logger.warning(f"Some columns to drop were not found in the dataset: {missing_cols}")
        existing_cols = [col for col in drop_columns if col in df.columns]
        df.drop(columns=existing_cols, inplace=True)
        logger.info(f"Dropped {len(existing_cols)} columns from the dataset: {existing_cols}")

    # If target_column is not specified, use the last column
    if target_column is None:
        target_column = df.columns[-1]
        logger.info(f"No target column specified. Using the last column '{target_column}' as the target.")

    # Ensure the target column exists in the dataframe
    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found in the dataframe.")

    # Separate features and target
    X = df.drop(columns=[target_column])
    y = df[target_column]

    # Initialize lists if not provided
    if numerical_columns is None:
        numerical_columns = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    if categorical_columns is None:
        categorical_columns = X.select_dtypes(include=['object', 'category']).columns.tolist()

    # Automatically detect additional categorical columns based on heuristics
    potential_categorical = []
    for col in numerical_columns.copy():  # Iterate over a copy since we might modify the list
        unique_values = X[col].nunique()
        if unique_values <= binary_threshold:
            logger.info(f"Column '{col}' has {unique_values} unique values. Treating as binary categorical.")
            potential_categorical.append(col)
        elif unique_values <= low_cardinality_threshold:
            logger.info(f"Column '{col}' has {unique_values} unique values. Treating as low cardinality categorical.")
            potential_categorical.append(col)

    # Move identified categorical columns from numerical_columns to categorical_columns
    for col in potential_categorical:
        numerical_columns.remove(col)
        categorical_columns.append(col)

    # Display the final lists of numerical and categorical columns
    logger.info(f"Numerical columns: {numerical_columns}")
    logger.info(f"Categorical columns: {categorical_columns}")

    # Handle missing values
    df = fill_missing_values(df, numerical_columns, categorical_columns)

    # Detect and handle outliers
    outliers = detect_outliers(df, numerical_columns)
    if outliers:
        if outlier_strategy == 'remove':
            df = handle_outliers(df, outliers, strategy='remove')
        elif outlier_strategy == 'replace':
            df = handle_outliers(df, outliers, strategy='replace')
        else:
            raise ValueError(f"Unsupported outlier strategy: {outlier_strategy}")

    # Transform categorical variables
    df = transform_categorical(df, categorical_columns, method=categorical_transform_method)

    # Update numerical and categorical columns after transformations
    numerical_columns = [col for col in numerical_columns if col in df.columns]
    # Assuming One-Hot Encoding added new columns, categorical_columns might have changed
    # For simplicity, we won't update categorical_columns after one-hot encoding

    # Define preprocessing pipelines
    numerical_pipeline = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())
    ])

    # Since categorical variables are already transformed, we may not need a separate pipeline
    # However, if frequency or target encoding is used, further preprocessing might be required

    # Combine preprocessing for numerical and categorical data
    preprocessor = ColumnTransformer(transformers=[
        ('num', numerical_pipeline, numerical_columns),
        # ('cat', categorical_pipeline, categorical_columns)  # Categorical transformation already done
    ], remainder='passthrough')  # 'passthrough' to keep other columns as they are

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    logger.info("Data has been split into training and testing sets.")

    # Fit and transform the training data, transform the testing data
    X_train = preprocessor.fit_transform(X_train)
    X_test = preprocessor.transform(X_test)

    logger.info("Preprocessing completed.")

    return X_train, X_test, y_train, y_test, df, target_column, numerical_columns, categorical_columns

# ---- Kullanım Örneği ----
if __name__ == "__main__":
 
    # Veri setini hazırlama
    data = prepare_data('data.csv')
