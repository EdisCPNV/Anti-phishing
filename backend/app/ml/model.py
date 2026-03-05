import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
import os

# 📁 Chemin vers le dataset
DATASET_PATH = os.path.join(os.path.dirname(__file__), "dataset.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")


def train_model():
    print("📦 Chargement du dataset...")
    df = pd.read_csv(DATASET_PATH)

    print(f"✅ {len(df)} lignes chargées")
    print(f"Colonnes : {list(df.columns)}")

    # La colonne cible est souvent "status" ou "label" ou "phishing"
    # On cherche automatiquement laquelle existe
    target_col = None
    for col in ["status", "label", "phishing", "Result"]:
        if col in df.columns:
            target_col = col
            break

    if target_col is None:
        print("❌ Colonne cible introuvable. Colonnes disponibles :", list(df.columns))
        return

    print(f"🎯 Colonne cible trouvée : {target_col}")

    # Séparer les features (X) et la cible (y)
    X = df.drop(columns=[target_col])
    y = df[target_col]

    # Garder uniquement les colonnes numériques
    X = X.select_dtypes(include=["number"])

    print(f"📊 {X.shape[1]} features utilisées pour l'entraînement")

    # Diviser en train/test (80% entraînement, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("🤖 Entraînement du modèle Random Forest...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Évaluer la précision
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"🎯 Précision du modèle : {accuracy * 100:.2f}%")

    # Sauvegarder le modèle dans un fichier
    with open(MODEL_PATH, "wb") as f:
        pickle.dump((model, list(X.columns)), f)

    print(f"✅ Modèle sauvegardé dans {MODEL_PATH}")
    return model


def load_model():
    if not os.path.exists(MODEL_PATH):
        print("⚠️ Modèle non trouvé, entraînement en cours...")
        train_model()

    with open(MODEL_PATH, "rb") as f:
        model, feature_columns = pickle.load(f)

    return model, feature_columns

def predict_url(features: dict) -> dict:
    model, feature_columns = load_model()

    df = pd.DataFrame([features])

    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0

    df = df[feature_columns]

    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0]

    is_phishing = prediction == "phishing"
    confidence = round(max(probability) * 100, 2)

    return {
        "ml_prediction": "phishing" if is_phishing else "légitime",
        "ml_confidence": confidence,
        "ml_is_phishing": is_phishing
    }


if __name__ == "__main__":
    train_model()

