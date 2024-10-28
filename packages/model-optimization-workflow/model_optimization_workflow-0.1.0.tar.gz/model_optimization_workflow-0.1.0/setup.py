from setuptools import setup, find_packages

setup(
    name='model_optimization_workflow',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'seaborn',
        'optuna~=4.0.0',
        'pyyaml',
        'market-data-assembler~=0.4.15',
        'scikit-learn',
        'plotly',
    ],
    author='Maksym Usanin (usanin.max@gmail.com)',
    description='model optimization workflow',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)
