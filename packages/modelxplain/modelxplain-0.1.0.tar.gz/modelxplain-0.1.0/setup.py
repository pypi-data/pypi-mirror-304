# setup.py

from setuptools import setup, find_packages

setup(
    name='modelxplain',
    version='0.1.0',
    description='A package for enhancing model interpretability for machine learning models.',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'scikit-learn>=0.24.0',
        'xgboost>=1.3.0',
        'tensorflow>=2.4.0',
        'shap>=0.39.0',
        'lime>=0.2.0.1',
        'eli5>=0.11.0',
        'dash>=2.0.0',
        'plotly>=5.0.0',
        'pandas>=1.1.0',
        'numpy>=1.19.0'
    ],
    url='https://github.com/yourusername/modelinsightharsh',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
