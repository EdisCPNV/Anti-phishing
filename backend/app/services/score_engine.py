def calculate_score(score: int) -> str:
    if score <= 20:
        return "faible"
    elif score <= 50:
        return "moyen"
    else:
        return "élevé"


def generate_recommendation(result: dict) -> list:
    recommendations = []

    if result["risk_level"] == "élevé":
        recommendations.append("🚫 Ne saisissez aucune information personnelle sur ce site")
        recommendations.append("📧 Si reçu par email, signalez-le comme phishing")
        recommendations.append("🔒 Ne cliquez sur aucun lien de cette page")

    elif result["risk_level"] == "moyen":
        recommendations.append("⚠️ Vérifiez bien l'expéditeur avant d'aller sur ce lien")
        recommendations.append("🔍 Cherchez le site officiel directement sur Google")
        recommendations.append("💬 En cas de doute, contactez l'entreprise directement")

    else:
        recommendations.append("✅ Ce lien semble fiable")
        recommendations.append("💡 Restez toujours vigilant même sur des sites connus")

    return recommendations


def generate_summary(result: dict) -> str:
    score = result["risk_score"]
    level = result["risk_level"]
    keywords = result["suspicious_keywords"]
    https = result["https"]

    if level == "élevé":
        summary = f"⛔ Ce lien est très probablement dangereux (score {score}/100)."
    elif level == "moyen":
        summary = f"⚠️ Ce lien présente des signes suspects (score {score}/100)."
    else:
        summary = f"✅ Ce lien semble sûr (score {score}/100)."

    if not https:
        summary += " La connexion n'est pas sécurisée."
    if keywords:
        summary += f" Mots suspects détectés : {', '.join(keywords)}."

    return summary