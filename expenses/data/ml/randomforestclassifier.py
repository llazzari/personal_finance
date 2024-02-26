from pathlib import Path
from typing import Any
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

from data.schema import DataSchema


RANDOM_STATE: int = 42
MODEL_FILE: Path = Path.cwd() / 'data' / 'ml' / 'model.joblib'
VECTORIZER_FILE: Path = Path.cwd() / 'data' / 'ml' / 'vectorizer.joblib'


def save_model(
    model: RandomForestClassifier,
    vectorizer: CountVectorizer
) -> None:
    joblib.dump(model, MODEL_FILE)
    joblib.dump(vectorizer, VECTORIZER_FILE)


def split_data(df: pd.DataFrame) -> list:
    """
    Split the data into training and testing sets.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the data.

    Returns:
    - list: X_train, X_test, y_train, y_test
    """
    X = df[DataSchema.CLEANED_DESCRIPTION]
    y = df[DataSchema.SUBCATEGORY]
    return train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE
    )


def train_random_forest(
    X_train: Any,
    y_train: Any,
    n_estimators: int = 100
) -> RandomForestClassifier:
    """
    Train a Random Forest Classifier.

    Parameters:
    - X_train (pd.Series): Vectorized training data.
    - y_train (pd.Series): Training labels.
    - n_estimators (int): The number of trees in the forest.
    - random_state (int): Seed for random number generation.

    Returns:
    - RandomForestClassifier: Trained Random Forest model.
    """
    clf = RandomForestClassifier(
        n_estimators=n_estimators,
        random_state=RANDOM_STATE
    )
    clf.fit(X_train, y_train)
    return clf


def evaluate_model(
    model: RandomForestClassifier,
    X_test: Any,
    y_test: np.ndarray
) -> None:
    """
    Evaluate the performance of the model on the test set.

    Parameters:
    - model (RandomForestClassifier): Trained Random Forest model.
    - X_test (pd.Series): Vectorized test data.
    - y_test (pd.Series): Test labels.
    """
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions)
    print(f"Accuracy: {accuracy*100:.2f}%")
    print("Classification Report:\n", report)


def train_and_test(df: pd.DataFrame) -> None:
    X_train, X_test, y_train, y_test = split_data(df)
    vectorizer = CountVectorizer()
    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)
    model = train_random_forest(X_train_vectorized, y_train)
    evaluate_model(model, X_test_vectorized, y_test)
    save_model(model, vectorizer)


def load_model() -> tuple:
    model = joblib.load(MODEL_FILE)
    vectorizer = joblib.load(VECTORIZER_FILE)
    return model, vectorizer


def predict(descriptions: pd.Series) -> list[str]:
    model, vectorizer = load_model()
    X_vectorized = vectorizer.transform(descriptions)
    return model.predict(X_vectorized)
