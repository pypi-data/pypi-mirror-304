
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
import numpy as np
import logging

class Model:
    def __init__(self, feature_columns, target_column, model=RandomForestClassifier, model_name = "RandomForestClassifier", **model_params):
        """
        Initializes the model class with feature columns, target column, and model.
        
        Parameters:
        -----------
        feature_columns : list
            List of feature column names to be used for training and predicting.
        target_column : str
            The name of the target column.
        model : sklearn model class (default: RandomForestClassifier)
            The model class to be used (e.g., RandomForestClassifier, LogisticRegression).
        model_params : dict
            Additional hyperparameters to initialize the model.
        """
        self._feature_columns = feature_columns
        self._target_column = target_column
        self.model = model(**model_params)  # Initialize the model with hyperparameters
        self.model_name = model_name

    def train(self, df):
        """
        Train the model on the provided DataFrame using the selected features and target.
        
        Parameters:
        -----------
        df : pd.DataFrame
            The DataFrame containing the training data.
        
        Returns:
        --------
        None
        """
        try:
            X = df[self._feature_columns]
            y = df[self._target_column]

            self.model.fit(X, y)
            logging.info(f"Model {self.model_name} successfully trained.")
        
        except Exception as e:
            logging.error(f"An error occurred during training: {e}")
            raise
    

    def predict(self, df):
        """
        Predict the probabilities for the provided DataFrame.
        
        Parameters:
        -----------
        df : pd.DataFrame
            The DataFrame containing the data for prediction.
        
        Returns:
        --------
        predictions : np.ndarray
            The predicted probabilities for each class.
        """
        try:
            X = df[self._feature_columns]
            predictions = self.model.predict_proba(X)
            logging.info(f"Prediction with model {self.model_name} successful.")
            return predictions

        except Exception as e:
            logging.error(f"An error occurred during prediction: {e}")
            raise

    def get_roc_auc(self, y_train, y_test, train_predictions, test_predictions, round_digits=2, verbose=False):
        """
        Calculate ROC AUC scores for training and test datasets.
        
        Parameters:
        -----------
        y_train : array-like
            True labels for the training set.
        
        y_test : array-like
            True labels for the test set.
        
        train_predictions : array-like
            Predicted probabilities for the training set (for class 1).
        
        test_predictions : array-like
            Predicted probabilities for the test set (for class 1).
        
        round_digits : int, optional (default=2)
            Number of decimal places to round the ROC AUC score.
        
        verbose : bool, optional (default=False)
            If True, prints the ROC AUC scores.
        
        Returns:
        --------
        roc_auc_train : float
            ROC AUC score for the training set.
        
        roc_auc_test : float
            ROC AUC score for the test set.
        
        Raises:
        -------
        ValueError:
            If the input data has incorrect shape or invalid values.
        """
        try:
            # Ensure that predictions are not empty and are numeric
            if len(y_train) == 0 or len(y_test) == 0:
                raise ValueError("y_train and y_test must not be empty.")
            
            if len(train_predictions) != len(y_train) or len(test_predictions) != len(y_test):
                raise ValueError("The length of predictions must match the length of true labels.")
            
            if not (np.issubdtype(train_predictions.dtype, np.number) and np.issubdtype(test_predictions.dtype, np.number)):
                raise ValueError("Predictions must be numeric.")

            # Compute ROC AUC for the training set
            roc_auc_train = roc_auc_score(y_train, train_predictions).round(round_digits)
            
            # Compute ROC AUC for the test set
            roc_auc_test = roc_auc_score(y_test, test_predictions).round(round_digits)

            # Optionally print the results
            if verbose:
                logging.info(f"ROC AUC for Training Set: {roc_auc_train}")
                logging.info(f"ROC AUC for Test Set: {roc_auc_test}")
            
            return roc_auc_train, roc_auc_test
        
        except ValueError as e:
            logging.error(f"ValueError: {e}")
            return None, None
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return None, None
