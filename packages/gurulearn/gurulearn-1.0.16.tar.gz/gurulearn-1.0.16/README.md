python setup.py sdist bdist_wheel

# ######                                                                      MLModelAnalysis                                                                 ###### #

MLModelAnalysis is a flexible, reusable class for training, evaluating, and making predictions with various machine learning regression models. This tool allows easy switching between models, consistent preprocessing, model evaluation, and prediction for a variety of machine learning tasks.

Supported Models
Linear Regression (linear_regression)
Decision Tree Regressor (decision_tree)
Random Forest Regressor (random_forest)
Support Vector Machine (svm)
Gradient Boosting Regressor (gradient_boosting)
K-Nearest Neighbors (knn)
AdaBoost Regressor (ada_boost)
Neural Network (MLP Regressor) (mlp)
XGBoost Regressor (xgboost)
Usage
1. Initializing the Model
Initialize the MLModelAnalysis class by specifying the model_type parameter, which defines the machine learning model you want to use. Below are examples of initializing with various models:

python
Copy code
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor

# Initialize with Linear Regression
analysis = MLModelAnalysis(model_type='linear_regression')

# Initialize with Random Forest
analysis = MLModelAnalysis(model_type='random_forest')

# Initialize with XGBoost
analysis = MLModelAnalysis(model_type='xgboost')
2. Training and Evaluating the Model
The train_and_evaluate method preprocesses the data, trains the model, and displays evaluation metrics. Optionally, it saves the trained model, scaler, and encoders for later use.

Parameters:
csv_file: Path to the CSV file containing the dataset.
x_elements: List of feature columns.
y_element: Name of the target column.
model_save_path (Optional): Path to save the trained model, scaler, and encoders.
Example:
# Set the parameters
csv_file = 'data.csv'          # Path to the data file
x_elements = ['feature1', 'feature2']  # List of feature columns
y_element = 'target'            # Target column name

# Initialize the model
analysis = MLModelAnalysis(model_type='random_forest')

# Train and evaluate the model
analysis.train_and_evaluate(csv_file=csv_file, x_elements=x_elements, y_element=y_element, model_save_path='random_forest_model.pkl')
After running this code, the model will display R-squared and Mean Squared Error (MSE) metrics for both training and test sets. If model_save_path is specified, it saves the model for future predictions.

3. Loading the Model and Making Predictions
The load_model_and_predict method loads a saved model and makes predictions on new input data.

Parameters:
model_path: Path to the saved model file (created in the previous step).
input_data: Dictionary of feature names and values representing a single input instance for prediction.
Example:
# Define input data for prediction
input_data = {
    'feature1': 5.1,
    'feature2': 2.3
}

# Load the model and make a prediction
prediction = analysis.load_model_and_predict(model_path='random_forest_model.pkl', input_data=input_data)
print(f'Prediction: {prediction}')
4. Visualization
When using a linear_regression or svm model with only one feature, the train_and_evaluate method will automatically generate a Plotly plot of actual vs. predicted values for simple visualization.

Example Use Cases
Regression Analysis with Random Forest:


analysis = MLModelAnalysis(model_type='random_forest')
analysis.train_and_evaluate(csv_file='data.csv', x_elements=['feature1', 'feature2'], y_element='target', model_save_path='random_forest_model.pkl')
Quick Prediction with a Pre-trained Model:


prediction = analysis.load_model_and_predict(model_path='random_forest_model.pkl', input_data={'feature1': 5.1, 'feature2': 2.3})
print(f'Prediction: {prediction}')
Switching Models Effortlessly:


# Simply specify a new model type to use a different algorithm
analysis = MLModelAnalysis(model_type='xgboost')
Additional Notes
Plotting: Visualizations are supported for linear models and SVM with single-feature datasets.
Model Saving: The model_save_path in train_and_evaluate stores the model, scaler, and encoders, allowing consistent predictions when reloading the model later.
Dependencies: Ensure required libraries (scikit-learn, pandas, numpy, plotly, and xgboost) are installed.








# ######                                                                      image_classify:                                                                  ###### #

# example usages:

image_classifier = ImageClassifier()
image_classifier.img_train(
    train_dir='train',
    test_dir='test',  # Optional, can be None to split training data
    epochs=1,
    device='cpu',
    force='vgg16',
    finetune=True
)


image_classifier = ImageClassifier()
image_classifier.img_train(
    train_dir='train',
    test_dir='test',  # Optional, can be None to split training data
    epochs=1,
    device='cpu',
    force='vgg16'
)


# Using directory data
image_classifier = ImageClassifier()
image_classifier.img_train(
    train_dir='path/to/train',
    test_dir='path/to/test',
    epochs=10,
    device='cuda',
    force='resnet50',
    finetune=True
)

# Using CSV data
image_classifier.img_train(
    csv_file='path/to/data.csv',
    img_column='image_path',  # Column name in CSV containing image paths
    label_column='label',      # Column name in CSV containing labels
    epochs=10,
    device='cuda',
    force='resnet50',
    finetune=True
)


consist of 20 cnn architecture excluding finetuning
# Instantiate and train the classifier with a specific model and fine-tuning enabled
image_classifier = ImageClassifier()
image_classifier.img_train("path_to_train_dir", "path_to_test_dir", epochs=10, device="cuda", force="efficientnet", finetune=True)
