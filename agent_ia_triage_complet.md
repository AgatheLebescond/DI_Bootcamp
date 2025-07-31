
# 🧠 Agent IA pour la Régulation Médicale d’Urgence

Ce document présente la conception d’un agent intelligent capable de gérer les appels d’urgence médicale, d’analyser les symptômes, d’évaluer l’urgence et de déclencher les actions appropriées. Il inclut une simulation d’appel à une API de triage médical.

## 1. Environnement de l’Agent

L’agent perçoit les données suivantes :
- Transcription voix/texte de l’appel
- Localisation GPS ou adresse
- Identité et historique médical
- Heure de l’appel
- Données issues d’appels précédents (si pertinents)

## 2. Outils & Intégrations

1. **API Symptôme (ex. Infermedica)**  
   Entrée : symptômes, âge, sexe → Sortie : gravité, diagnostics, conseils

2. **Système de Dispatch Ambulancier**  
   Entrée : niveau d’urgence, adresse → Sortie : délai, confirmation

3. **Modèle de Triage IA (LLM spécialisé)**  
   Entrée : texte structuré, historique médical → Sortie : score d’urgence, justification

## 3. Exemple de Gestion d’État (JSON)

```json
{
  "caller_id": "FR‑0789X",
  "contact_info": {
    "name": "Marie Dupont",
    "phone": "+33…",
    "location": "12 Rue… Paris"
  },
  "medical_history": {
    "known_conditions": ["hypertension", "diabète"],
    "medications": ["metformine"]
  },
  "reported_symptoms": ["douleur thoracique", "essoufflement"],
  "urgency_score": 87,
  "decision": "Dispatch ambulance",
  "timestamp": "2025‑07‑31T14:37:00"
}
```

## 4. Processus de Prise de Décision

1. Extraction des symptômes depuis le texte  
2. Appel du modèle de triage → score d’urgence  
3. Classification :
   - Score > 80 : **Haute urgence** → ambulance
   - Score entre 50-80 : **Moyenne urgence** → orientation
   - Score < 50 : **Faible urgence** → auto-soins  
4. Action : dispatch, journalisation, feedback à l’appelant

## 5. Type d’Agent : Hybride

- Composante réactive : gestion immédiate de mots-clés critiques  
- Composante délibérative : analyse structurée via modèle IA  
- Utilisation de la mémoire pour prise de décision cohérente

## 6. Comparaison avec un Agent Réactif

| Critère        | Réactif         | Hybride                          |
|----------------|------------------|----------------------------------|
| Mémoire        | Aucune           | Oui                              |
| Planification  | Non              | Oui                              |
| Invocation     | Mots-clés        | Contexte + raisonnement          |
| Vitesse        | ⚡ Rapide        | 🕒 Plus lent                      |
| Fiabilité      | ⚠️ Moins fiable | ✅ Contextualisé et structuré    |
| Intelligence   | Limitée          | Haute                            |

## 7. Réflexions Critiques

### Sans gestion d’état :
- Pas de mémoire du patient
- Décisions incohérentes possibles
- Moins de sécurité et d’adaptabilité

### Importance des outils externes :
- Précision des diagnostics
- Automatisation des interventions
- Meilleure fiabilité dans les situations critiques

## 8. Simulation d’un Appel API - Scoring de Symptômes Médicaux

```python
# Symptômes rapportés par l'appelant
symptomes = ["douleur thoracique", "essoufflement", "étourdissement"]

# Simulation d'une API de triage médical
def simuler_api_triage(symptomes):
    gravite = {
        "douleur thoracique": 40,
        "essoufflement": 30,
        "étourdissement": 20,
        "fièvre": 10,
        "toux": 10,
        "maux de tête": 5
    }
    score = sum(gravite.get(symptome, 0) for symptome in symptomes)
    score = min(score, 100)
    return {
        "score": score,
        "niveau": ("Élevé" if score > 80 else "Moyen" if score >= 50 else "Faible")
    }

resultat = simuler_api_triage(symptomes)
print(resultat)

# Interprétation simple
if resultat["niveau"] == "Élevé":
    print("🚨 Urgence élevée : envoi ambulance immédiat.")
elif resultat["niveau"] == "Moyen":
    print("⏱️ Urgence modérée : recommander service de garde ou téléconsultation.")
else:
    print("✅ Faible urgence : conseiller auto-surveillance et repos.")
```
