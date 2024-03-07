from pathlib import Path
from typing import Any, Optional
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


RANDOM_STATE: int = 42


def save_model(model: RandomForestClassifier, file: str | Path) -> None:
    joblib.dump(model, file)


def save_vectorizer(vectorizer: CountVectorizer, file: str | Path) -> None:
    joblib.dump(vectorizer, file)


def split_data(X: np.ndarray, y: np.ndarray) -> list:
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
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions)
    print(f"Accuracy: {accuracy*100:.2f}%")
    print("Classification Report:\n", report)


def train_and_test(X: np.ndarray, y: np.ndarray) -> None:
    print(X.dtype, y.dtype)
    X_train, X_test, y_train, y_test = split_data(X, y)
    vectorizer = CountVectorizer()
    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)
    model = train_random_forest(X_train_vectorized, y_train)
    evaluate_model(model, X_test_vectorized, y_test)
    # save_model(model, MODEL_FILE)
    # save_vectorizer(vectorizer, VECTORIZER_FILE)


def load_model(model_file: str | Path) -> RandomForestClassifier:
    return joblib.load(model_file)


def load_vectorizer(vector_file: str | Path) -> CountVectorizer:
    return joblib.load(vector_file)


def predict(
    X: np.ndarray,
    model: RandomForestClassifier,
    vectorizer: Optional[CountVectorizer] = None
) -> np.ndarray:
    if vectorizer is not None:
        X_vectorized = vectorizer.transform(X)
        return model.predict(X_vectorized)
    return model.predict(X)
