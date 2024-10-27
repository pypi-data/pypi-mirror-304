from setuptools import setup, find_packages

setup(
    name='mkyz',  # Kütüphane adınız
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'pandas',  # Veri işlemleri için
        'scikit-learn',  # ML modelleri ve işlem desteği için
        'seaborn',  # Görselleştirme için
        'matplotlib',  # Grafikler için
        'mlxtend',  # Association Rule Learning ve apriori algoritması için
        'numpy',  # Sayısal işlemler
        'plotly',  # Görselleştirme için
        'statsmodels',  # İstatistiksel işlemler için
        'xgboost',  # Gradient Boosting için
        'lightgbm',  # Gradient Boosting için
        'catboost',  # Gradient Boosting için
        'rich',  # Gelişmiş konsol çıktıları için
    ],
    description='MKYZ is a Python library for classification, regression, clustering, association rule learning, dimensionality reduction, bagging, boosting, and stacking.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Mustafa Kapıcı',  # Yazar isminiz
    author_email='m.mustafakapici@gmail.com',  # E-posta adresiniz
    url='https://github.com/mmustafakapici/mkyz',  # GitHub veya proje URL'niz
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
