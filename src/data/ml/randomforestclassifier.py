from typing import Optional
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from scipy.sparse import spmatrix


RANDOM_STATE: int = 42


def split_data(X: np.ndarray, y: np.ndarray) -> list:
    return train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE)


def train_random_forest(
    X_train: spmatrix | np.ndarray,
    y_train: spmatrix | np.ndarray,
    n_estimators: int = 100,
) -> RandomForestClassifier:

    clf = RandomForestClassifier(n_estimators=n_estimators, random_state=RANDOM_STATE)
    clf.fit(X_train, y_train)
    return clf


def evaluate_model(
    model: RandomForestClassifier,
    X_test: spmatrix | np.ndarray,
    y_test: spmatrix | np.ndarray,
) -> None:
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions)
    print(f"Accuracy: {accuracy*100:.2f}%")
    print("Classification Report:\n", report)


def train_and_test(
    X: np.ndarray,
    y: np.ndarray,
    save_vectorizer_file: Optional[str] = None,
    save_model_file: Optional[str] = None,
) -> None:
    X_train, X_test, y_train, y_test = split_data(X, y)

    vectorizer = CountVectorizer()
    X_train = vectorizer.fit_transform(X_train)
    X_test: spmatrix = vectorizer.transform(X_test)

    if save_vectorizer_file:
        joblib.dump(vectorizer, save_vectorizer_file)

    model: RandomForestClassifier = train_random_forest(X_train, y_train)
    evaluate_model(model, X_test, y_test)

    if save_model_file:
        joblib.dump(model, save_model_file)
