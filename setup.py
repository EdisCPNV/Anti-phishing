import os

folders = [
    "backend/app/routes",
    "backend/app/services",
    "backend/app/ml",
    "backend/app/tests",
    "frontend/src/components",
    "frontend/src/pages",
    "frontend/src/services",
]

files = [
    "backend/app/__init__.py",
    "backend/app/main.py",
    "backend/app/routes/__init__.py",
    "backend/app/routes/analyze.py",
    "backend/app/services/__init__.py",
    "backend/app/services/url_analyzer.py",
    "backend/app/services/score_engine.py",
    "backend/app/ml/__init__.py",
    "backend/app/ml/model.py",
    "backend/app/tests/test_analyzer.py",
    "backend/requirements.txt",
    "frontend/src/components/UrlInput.jsx",
    "frontend/src/components/ScoreCard.jsx",
    "frontend/src/components/RiskBadge.jsx",
    "frontend/src/pages/Home.jsx",
    "frontend/src/services/api.js",
    "frontend/src/App.jsx",
    "README.md",
    ".gitignore",
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"✅ Dossier créé : {folder}")

for file in files:
    with open(file, "w") as f:
        pass
    print(f"📄 Fichier créé : {file}")

print("\n🎉 Structure du projet créée avec succès !")