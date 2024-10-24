# UVCEML

![PyPI - License](https://img.shields.io/pypi/l/uvceml) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/uvceml)

A Python package that provides various machine learning algorithms, including Artificial Neural Networks (ANNs), Bayesian Networks, K-Means clustering, K-Nearest Neighbors (KNN), and decision trees (ID3). It also includes algorithms like Candidate Elimination, Find-S, and Naive Bayes, along with Local Weighted Regression.

## Features

- **ANN**: Implementation of an Artificial Neural Network with a single hidden layer.
- **Bayesian Network**: Build a Bayesian Network and perform inference using the `pgmpy` library.
- **K-Means Clustering**: Perform K-Means clustering using `scikit-learn`.
- **KNN**: K-Nearest Neighbors classification using `scikit-learn`.
- **Candidate Elimination Algorithm**: Perform hypothesis elimination to find the most specific/general hypothesis.
- **Find-S Algorithm**: Find the maximally specific hypothesis from training examples.
- **ID3 Decision Tree**: Build a decision tree using the ID3 algorithm.
- **Naive Bayes Classifier**: A simple Naive Bayes classifier.
- **Local Weighted Regression**: Perform regression using locally weighted linear regression.

## Installation

You can install the package using `pip`:

```bash
pip install uvceml
```
#### Usage
## Importing the package
import uvceml

## Example Usage
1. Artificial Neural Network (ANN)
```bash
from uvceml import ANN
ANN()
```
2. Bayesian Network
```bash
from uvceml import bayes_network
input_file = 'path_to_csv_file.csv'
bayes_network(input_file)
```
3. K-Means Clustering
```bash
from uvceml import k_means
k_means()
```
4. KNN
```bash
from uvceml import knn
knn()
```
5. Candidate Elimination
```bash
from uvceml import candidate
input_file = 'path_to_csv_file.csv'
candidate(input_file)
```
6. Find-S Algorithm
```bash
from uvceml import find_s
input_file = 'path_to_csv_file.csv'
find_s(input_file)
```
7. ID3 Decision Tree
```bash
from uvceml import ID3
input_file = 'path_to_csv_file.csv'
ID3(input_file)
```
8. Naive Bayes Classifier
```bash
from uvceml import NaiveBayes
input_file = 'path_to_csv_file.csv'
NaiveBayes(input_file)
```
9. Local Weighted Regression
```bash
from uvceml import regression
input_file = 'path_to_csv_file.csv'
regression(input_file)
```
## Dependencies
This package requires the following libraries:

numpy
pandas
scikit-learn
pgmpy
matplotlib
You can install these using pip: pip install numpy pandas scikit-learn pgmpy matplotlib

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing
Feel free to contribute by submitting a pull request or opening an issue.

Happy coding!