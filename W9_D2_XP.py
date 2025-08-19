#!/usr/bin/env python3
"""
5 Exercices Complets : Gradio, Streamlit, FastAPI
Exercices XP - Juillet 2025
"""

import subprocess
import sys
import os
from typing import Optional

# Installation automatique des dépendances
def install_dependencies():
    """Installe toutes les dépendances nécessaires"""
    packages = [
        "gradio",
        "streamlit", 
        "fastapi",
        "uvicorn",
        "pydantic",
        "numpy",
        "requests"
    ]
    
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            print(f"📦 Installation de {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    print("✅ Toutes les dépendances sont installées")

# Installation
install_dependencies()

# ================================================================
# 🌟 EXERCICE 1 : GRADIO INTERFACE - MULTI-FUNCTION TOOLKIT
# ================================================================

import gradio as gr
import numpy as np

def multi_function_toolkit(function_choice, user_input):
    """
    Fonction backend pour l'outil multi-fonctions
    
    Args:
        function_choice: "Greet", "Echo", ou "Square a Number"
        user_input: Entrée utilisateur (texte ou nombre)
    
    Returns:
        str: Résultat selon la fonction choisie
    """
    if function_choice == "Greet":
        return f"Bonjour, {user_input} !"
    
    elif function_choice == "Echo":
        return f"Vous avez dit : {user_input}"
    
    elif function_choice == "Square a Number":
        try:
            number = float(user_input)
            result = number ** 2
            return f"Le carré de {number} est {result}"
        except ValueError:
            return "Erreur : Veuillez entrer un nombre valide"
    
    else:
        return "Fonction non reconnue"

def create_gradio_interface():
    """Crée l'interface Gradio multi-outils"""
    
    # Création de l'interface avec gr.Interface
    interface = gr.Interface(
        fn=multi_function_toolkit,
        inputs=[
            gr.Dropdown(
                choices=["Greet", "Echo", "Square a Number"],
                label="Choisissez une fonction",
                value="Greet"
            ),
            gr.Textbox(
                label="Votre entrée",
                placeholder="Tapez votre texte ou nombre ici..."
            )
        ],
        outputs=gr.Textbox(label="Résultat"),
        title="🛠️ Boîte à Outils Multi-Fonctions",
        description="Choisissez une fonction et entrez votre données pour voir le résultat !",
        examples=[
            ["Greet", "Alice"],
            ["Echo", "Bonjour le monde !"],
            ["Square a Number", "5"]
        ],
        theme=gr.themes.Soft()
    )
    
    return interface

# ================================================================
# 🌟 EXERCICE 2 : GRADIO BLOCKS - CALCULATRICE DEUX ÉTAPES  
# ================================================================

def create_gradio_calculator():
    """Crée une calculatrice avec l'API Gradio Blocks"""
    
    def calculate(num1, num2, operation):
        """Fonction de calcul"""
        try:
            if operation == "Addition":
                result = num1 + num2
                return f"Résultat : {num1} + {num2} = {result}"
            elif operation == "Multiplication":
                result = num1 * num2
                return f"Résultat : {num1} × {num2} = {result}"
            else:
                return "Opération non supportée"
        except Exception as e:
            return f"Erreur de calcul : {e}"
    
    # Création du layout avec Blocks
    with gr.Blocks(title="Calculatrice Simple", theme=gr.themes.Soft()) as calculator:
        
        # Instructions en markdown
        gr.Markdown("""
        # 🧮 Calculatrice Simple
        
        **Instructions :**
        1. Entrez deux nombres dans les champs ci-dessous
        2. Choisissez l'opération (Addition ou Multiplication)  
        3. Cliquez sur "Calculer" pour voir le résultat
        """)
        
        # Layout en ligne avec gr.Row()
        with gr.Row():
            num1_input = gr.Number(label="Premier nombre", value=0)
            num2_input = gr.Number(label="Deuxième nombre", value=0)
        
        # Sélecteur radio pour l'opération
        operation_radio = gr.Radio(
            choices=["Addition", "Multiplication"],
            label="Choisissez l'opération",
            value="Addition"
        )
        
        # Bouton de calcul
        calculate_btn = gr.Button("🧮 Calculer", variant="primary")
        
        # Affichage du résultat
        result_label = gr.Label(label="Résultat du calcul")
        
        # Liaison événementielle
        calculate_btn.click(
            fn=calculate,
            inputs=[num1_input, num2_input, operation_radio],
            outputs=result_label
        )
    
    return calculator

# ================================================================
# 🌟 EXERCICE 3 : STREAMLIT CHAT - BOT AVEC MÉMOIRE
# ================================================================

def create_streamlit_chat():
    """Code pour le chatbot Streamlit avec mémoire"""
    
    streamlit_code = '''
import streamlit as st

# Configuration de la page
st.set_page_config(page_title="ChatBot avec Mémoire", page_icon="🤖")

st.title("🤖 ChatBot avec Mémoire Stateful")
st.caption("Un chatbot qui se souvient de vos conversations précédentes")

# Initialisation de l'état de session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Fonction pour effacer le chat
def clear_chat():
    st.session_state.chat_history = []
    st.rerun()

# Bouton pour effacer le chat
col1, col2 = st.columns([3, 1])
with col2:
    if st.button("🗑️ Effacer Chat", on_click=clear_chat):
        pass

# Affichage de l'historique des messages
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Interface de saisie
if prompt := st.chat_input("Tapez votre message ici..."):
    
    # Affichage du message utilisateur
    with st.chat_message("user"):
        st.write(prompt)
    
    # Ajout à l'historique
    st.session_state.chat_history.append({
        "role": "user", 
        "content": prompt
    })
    
    # Génération de la réponse du bot (écho pour l'instant)
    bot_response = f"Vous avez dit : {prompt}"
    
    # Affichage de la réponse du bot
    with st.chat_message("assistant"):
        st.write(bot_response)
    
    # Ajout de la réponse à l'historique
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": bot_response
    })

# Informations sur la session
st.sidebar.header("📊 Informations de Session")
st.sidebar.write(f"Messages dans l'historique : {len(st.session_state.chat_history)}")

if st.session_state.chat_history:
    st.sidebar.write("Dernier message :")
    st.sidebar.write(st.session_state.chat_history[-1]["content"][:50] + "...")
'''
    
    return streamlit_code

# ================================================================
# 🌟 EXERCICE 4 : STREAMLIT UI + LOGIC COMBO
# ================================================================

def create_streamlit_dashboard():
    """Code pour le mini-dashboard Streamlit dynamique"""
    
    streamlit_dashboard_code = '''
import streamlit as st
import numpy as np
import json

# Configuration de la page
st.set_page_config(page_title="Dashboard Dynamique", page_icon="📊", layout="wide")

# Titre principal
st.title("📊 Mini-Dashboard Dynamique")

# Génération et affichage d'un graphique linéaire aléatoire
st.header("📈 Graphique Linéaire Aléatoire")

# Génération de données aléatoires avec NumPy
random_data = np.random.randn(50, 3)
chart_data = np.cumsum(random_data, axis=0)

# Affichage du graphique
st.line_chart(chart_data)

# Sélecteur radio pour le contenu dynamique
st.header("🎛️ Contenu Dynamique")
content_choice = st.radio(
    "Choisissez le type de contenu à afficher :",
    ["Show Code", "Show JSON"]
)

# Affichage conditionnel basé sur le choix
if content_choice == "Show Code":
    st.subheader("💻 Code Python")
    
    code_example = """
# Exemple de code Python simple
import numpy as np
import matplotlib.pyplot as plt

def generate_data(n=100):
    x = np.linspace(0, 10, n)
    y = np.sin(x) + np.random.normal(0, 0.1, n)
    return x, y

# Génération et affichage des données
x, y = generate_data()
plt.plot(x, y)
plt.title("Données sinusoïdales avec bruit")
plt.show()
"""
    
    st.code(code_example, language="python")

elif content_choice == "Show JSON":
    st.subheader("📋 Objet JSON Formaté")
    
    json_example = {
        "application": "Mini-Dashboard Streamlit",
        "version": "1.0.0",
        "features": [
            "Graphiques dynamiques",
            "Interface interactive", 
            "Contenu conditionnel"
        ],
        "data": {
            "chart_points": len(chart_data),
            "dimensions": chart_data.shape,
            "last_update": "2025-07-30"
        },
        "config": {
            "theme": "default",
            "layout": "wide",
            "sidebar": True
        }
    }
    
    st.json(json_example)

# Bonus : Affichage d'une image depuis une URL publique
st.header("🖼️ Image Bonus")
try:
    st.image(
        "https://via.placeholder.com/600x300/FF6B6B/FFFFFF?text=Dashboard+Image", 
        caption="Image d'exemple depuis une URL publique",
        width=600
    )
except:
    st.warning("Impossible de charger l'image depuis l'URL publique")

# Sidebar avec informations
st.sidebar.header("ℹ️ Informations")
st.sidebar.info("""
Cette application démontre :
- Graphiques avec NumPy
- Contenu conditionnel
- Code et JSON formatés
- Images externes
""")

st.sidebar.metric("Points de données", len(chart_data))
st.sidebar.metric("Choix utilisateur", content_choice)
'''
    
    return streamlit_dashboard_code

# ================================================================
# 🌟 EXERCICE 5 : FASTAPI - SMART RESPONDER
# ================================================================

def create_fastapi_app():
    """Code pour l'application FastAPI Smart Responder"""
    
    fastapi_code = '''
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# Création de l'application FastAPI
app = FastAPI(
    title="Smart Responder API",
    description="API qui répond intelligemment selon le contenu du message",
    version="1.0.0"
)

# Modèle Pydantic pour le corps de la requête
class MessageRequest(BaseModel):
    message: str

class MessageResponse(BaseModel):
    response: str
    detected_intent: str

# Endpoint racine
@app.get("/")
def root():
    return {
        "message": "Bienvenue sur Smart Responder API",
        "endpoints": ["/respond"],
        "description": "Envoyez un POST sur /respond avec {'message': 'votre texte'}"
    }

# Endpoint principal /respond
@app.post("/respond", response_model=MessageResponse)
def smart_respond(request: MessageRequest):
    """
    Endpoint qui retourne des réponses différentes selon le contenu du message
    
    Args:
        request: Objet contenant le message utilisateur
    
    Returns:
        MessageResponse: Réponse avec le texte et l'intention détectée
    """
    message = request.message.lower()
    
    # Logique conditionnelle basée sur les mots-clés
    if "math" in message or "calcul" in message or any(op in message for op in ["+", "-", "*", "/", "="]):
        return MessageResponse(
            response="Utilisation de l'outil calculatrice...",
            detected_intent="calculator"
        )
    
    elif "date" in message or "heure" in message or "quand" in message:
        return MessageResponse(
            response="Récupération de la date actuelle...",
            detected_intent="datetime"
        )
    
    elif "météo" in message or "temps" in message or "temperature" in message:
        return MessageResponse(
            response="Consultation des données météorologiques...",
            detected_intent="weather"
        )
    
    else:
        return MessageResponse(
            response="Réponse LLM par défaut.",
            detected_intent="general"
        )

# Endpoint de test avec différents exemples
@app.get("/test")
def test_examples():
    """Endpoint pour tester différents exemples"""
    examples = [
        {"message": "Combien fait 5+5?", "expected": "calculator"},
        {"message": "Quelle est la date d'aujourd'hui?", "expected": "datetime"},
        {"message": "Quel temps fait-il?", "expected": "weather"},
        {"message": "Bonjour comment allez-vous?", "expected": "general"}
    ]
    
    return {
        "test_examples": examples,
        "instructions": "Utilisez POST /respond pour tester ces exemples"
    }

# Point d'entrée pour le serveur
if __name__ == "__main__":
    print("🚀 Lancement du serveur FastAPI Smart Responder")
    print("📍 URL: http://localhost:8000")
    print("📖 Documentation: http://localhost:8000/docs")
    print("🧪 Tests: http://localhost:8000/test")
    
    uvicorn.run(
        "exercices_complets:app",  # Remplacez par le nom de votre fichier
        host="0.0.0.0",
        port=8000,
        reload=True
    )
'''
    
    return fastapi_code

# ================================================================
# FONCTION PRINCIPALE ET MENU INTERACTIF
# ================================================================

def main():
    """Menu principal pour lancer les différents exercices"""
    
    print("🎯 5 Exercices Complets : Gradio, Streamlit, FastAPI")
    print("=" * 60)
    
    while True:
        print("\n📋 Menu des Exercices :")
        print("1. 🛠️  Gradio Interface - Multi-Function Toolkit")
        print("2. 🧮 Gradio Blocks - Calculatrice Simple") 
        print("3. 🤖 Streamlit Chat - Bot avec Mémoire")
        print("4. 📊 Streamlit Dashboard - UI Dynamique")
        print("5. 🚀 FastAPI - Smart Responder")
        print("6. 📝 Générer tous les fichiers séparés")
        print("0. ❌ Quitter")
        
        choice = input("\n👉 Choisissez un exercice (0-6) : ").strip()
        
        if choice == "1":
            print("\n🛠️ Lancement de l'interface Gradio Multi-Outils...")
            interface = create_gradio_interface()
            interface.launch(share=False, inbrowser=True)
        
        elif choice == "2":
            print("\n🧮 Lancement de la calculatrice Gradio Blocks...")
            calculator = create_gradio_calculator()
            calculator.launch(share=False, inbrowser=True)
        
        elif choice == "3":
            print("\n🤖 Code Streamlit Chat généré !")
            print("Copiez le code suivant dans un fichier 'streamlit_chat.py' :")
            print("-" * 50)
            print(create_streamlit_chat())
            print("-" * 50)
            print("Puis lancez : streamlit run streamlit_chat.py")
        
        elif choice == "4":
            print("\n📊 Code Streamlit Dashboard généré !")
            print("Copiez le code suivant dans un fichier 'streamlit_dashboard.py' :")
            print("-" * 50)
            print(create_streamlit_dashboard())
            print("-" * 50)
            print("Puis lancez : streamlit run streamlit_dashboard.py")
        
        elif choice == "5":
            print("\n🚀 Code FastAPI généré !")
            print("Copiez le code suivant dans un fichier 'fastapi_app.py' :")
            print("-" * 50)
            print(create_fastapi_app())
            print("-" * 50)
            print("Puis lancez : python fastapi_app.py")
        
        elif choice == "6":
            generate_separate_files()
        
        elif choice == "0":
            print("👋 Au revoir !")
            break
        
        else:
            print("❌ Choix invalide, veuillez réessayer.")

def generate_separate_files():
    """Génère tous les fichiers séparés pour chaque exercice"""
    
    files = {
        "streamlit_chat.py": create_streamlit_chat(),
        "streamlit_dashboard.py": create_streamlit_dashboard(), 
        "fastapi_app.py": create_fastapi_app()
    }
    
    print("\n📁 Génération des fichiers séparés...")
    
    for filename, content in files.items():
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ {filename} créé avec succès")
        except Exception as e:
            print(f"❌ Erreur lors de la création de {filename}: {e}")
    
    print(f"\n📋 Instructions de lancement :")
    print(f"• streamlit run streamlit_chat.py")
    print(f"• streamlit run streamlit_dashboard.py") 
    print(f"• python fastapi_app.py")

# Test des applications FastAPI avec requests
def test_fastapi():
    """Teste l'API FastAPI avec des requêtes"""
    try:
        import requests
        
        # Tests de l'API
        test_messages = [
            "Combien fait 5+5?",
            "Quelle est la date aujourd'hui?", 
            "Quel temps fait-il?",
            "Bonjour comment ça va?"
        ]
        
        print("\n🧪 Test de l'API FastAPI...")
        
        for message in test_messages:
            response = requests.post(
                "http://localhost:8000/respond",
                json={"message": message}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ '{message}' → {result['response']}")
            else:
                print(f"❌ Erreur pour '{message}': {response.status_code}")
                
    except Exception as e:
        print(f"⚠️ Impossible de tester l'API : {e}")
        print("Assurez-vous que l'API FastAPI est lancée sur localhost:8000")

if __name__ == "__main__":
    main()

# ================================================================
# INSTRUCTIONS COMPLÈTES
# ================================================================
"""
🎯 INSTRUCTIONS COMPLÈTES POUR LES 5 EXERCICES

📦 Installation :
pip install gradio streamlit fastapi uvicorn pydantic numpy requests

🚀 Lancement :
python exercices_complets.py

🛠️ Exercice 1 - Gradio Interface :
✅ Dropdown avec "Greet", "Echo", "Square a Number"
✅ Input adaptatif (texte/nombre)
✅ Logique backend avec dispatch de fonctions
✅ Exemples intégrés pour chaque fonction

🧮 Exercice 2 - Gradio Blocks :
✅ Layout custom avec gr.Row() pour 2 inputs côte à côte
✅ Radio selector pour Addition/Multiplication
✅ Button de calcul et gr.Label() pour résultat
✅ Instructions markdown en haut

🤖 Exercice 3 - Streamlit Chat :
✅ st.chat_message() pour bulles de chat
✅ st.session_state["chat_history"] pour mémoire
✅ Boucle d'affichage des messages précédents
✅ Bouton "Clear Chat" qui reset la conversation
✅ Bot qui echo les messages utilisateur

📊 Exercice 4 - Streamlit Dashboard :
✅ Titre + graphique aléatoire avec NumPy
✅ Radio selector "Show Code"/"Show JSON"
✅ Affichage conditionnel avec st.code() et st.json()
✅ Image bonus depuis URL publique
✅ Layout dynamique

🚀 Exercice 5 - FastAPI Smart Responder :
✅ Endpoint POST /respond avec Pydantic model
✅ Logique conditionnelle sur mots-clés :
   - "math" → "Utilisation de l'outil calculatrice..."
   - "date" → "Récupération de la date actuelle..."  
   - Autres → "Réponse LLM par défaut."
✅ JSON request/response
✅ Serveur Uvicorn intégré

🧪 Tests :
• Gradio : Interface automatique avec exemples
• Streamlit : streamlit run [fichier].py
• FastAPI : Docs auto sur /docs + tests /test
