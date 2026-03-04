import whois
import datetime
import requests
from urllib.parse import urlparse

def analyze_url(url: str) -> dict:
    result = {
        "url": url,
        "https": False,
        "domain_age_days": None,
        "suspicious_keywords": [],
        "risk_score": 0,
        "risk_level": "",
        "details": []
    }

    # ✅ 1. Vérifier HTTPS
    if url.startswith("https://"):
        result["https"] = True
        result["details"].append("✅ HTTPS présent")
    else:
        result["risk_score"] += 25
        result["details"].append("🚨 Pas de HTTPS")

    # ✅ 2. Extraire le domaine
    parsed = urlparse(url)
    domain = parsed.netloc

    # ✅ 3. Vérifier l'âge du domaine
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        age = (datetime.datetime.now() - creation_date).days
        result["domain_age_days"] = age
        if age < 180:
            result["risk_score"] += 30
            result["details"].append(f"🚨 Domaine très récent ({age} jours)")
        elif age < 365:
            result["risk_score"] += 15
            result["details"].append(f"⚠️ Domaine récent ({age} jours)")
        else:
            result["details"].append(f"✅ Domaine ancien ({age} jours)")
    except:
        result["risk_score"] += 20
        result["details"].append("⚠️ Impossible de vérifier l'âge du domaine")

    # ✅ 4. Mots-clés suspects dans l'URL
    keywords = ["login", "verify", "secure", "account", "update",
                "bank", "free", "winner", "password", "confirm"]
    for word in keywords:
        if word in url.lower():
            result["suspicious_keywords"].append(word)
            result["risk_score"] += 10
    if result["suspicious_keywords"]:
        result["details"].append(f"🚨 Mots suspects : {result['suspicious_keywords']}")

    # ✅ 5. URL trop longue (souvent suspect)
    if len(url) > 75:
        result["risk_score"] += 10
        result["details"].append("⚠️ URL anormalement longue")

    # ✅ 6. Présence d'une adresse IP dans l'URL
    import re
    if re.search(r'\d+\.\d+\.\d+\.\d+', url):
        result["risk_score"] += 30
        result["details"].append("🚨 URL contient une adresse IP")

    # ✅ 7. Calculer le niveau de risque final
    if result["risk_score"] <= 20:
        result["risk_level"] = "faible"
    elif result["risk_score"] <= 50:
        result["risk_level"] = "moyen"
    else:
        result["risk_level"] = "élevé"

    return result


# --- Test rapide dans le terminal ---
if __name__ == "__main__":
    url = input("Entrez une URL : ")
    rapport = analyze_url(url)
    print("\n--- Résultat ---")
    for key, value in rapport.items():
        print(f"{key} : {value}")