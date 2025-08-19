#!/usr/bin/env python3
"""
Chatbot utilisant Transformers et Gradio
Modèle: Facebook BlenderBot-400M-distill
Interface: Gradio ChatInterface
"""

# Installation des dépendances (à exécuter en premier)
import subprocess
import sys

def install_requirements():
    """Installe les dépendances nécessaires"""
    try:
        import transformers
        import gradio
        print("✅ Toutes les dépendances sont déjà installées")
    except ImportError:
        print("📦 Installation des dépendances...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "transformers"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "gradio"])
        print("✅ Installation terminée")

# Installation automatique si nécessaire
install_requirements()

# Imports principaux
from transformers import pipeline, Conversation
import gradio as gr
import time

# Configuration du chatbot
print("🤖 Initialisation du chatbot BlenderBot...")

# Étape 2: Configuration du chatbot avec le modèle spécifié
try:
    # Utilisation du modèle facebook/blenderbot-400M-distill
    chatbot = pipeline("conversational", model="facebook/blenderbot-400M-distill")
    print("✅ Modèle BlenderBot chargé avec succès")
except Exception as e:
    print(f"⚠️ Erreur lors du chargement du modèle: {e}")
    print("🔄 Utilisation d'un chatbot simulé...")
    
    # Chatbot simulé en cas d'erreur
    class SimulatedChatbot:
        def __call__(self, conversation):
            # Réponses simulées intelligentes
            user_message = conversation.new_user_input.lower() if hasattr(conversation, 'new_user_input') else ""
            
            responses = {
                "bonjour": "Bonjour ! Comment allez-vous aujourd'hui ?",
                "salut": "Salut ! Ravi de vous parler !",
                "comment": "Je vais très bien, merci ! Et vous ?",
                "quoi": "C'est une excellente question ! Pouvez-vous me donner plus de détails ?",
                "pourquoi": "C'est intéressant que vous demandiez cela. Que pensez-vous de la situation ?",
                "merci": "De rien ! Je suis là pour vous aider.",
                "au revoir": "Au revoir ! J'ai pris plaisir à discuter avec vous !",
            }
            
            # Recherche de mots-clés dans le message
            for keyword, response in responses.items():
                if keyword in user_message:
                    conversation.generated_responses.append(response)
                    return conversation
            
            # Réponse par défaut
            default_responses = [
                "C'est vraiment intéressant ! Pouvez-vous m'en dire plus ?",
                "Je vois ce que vous voulez dire. Qu'est-ce qui vous fait penser cela ?",
                "Hmm, c'est une perspective intéressante ! Comment êtes-vous arrivé à cette conclusion ?",
                "Pouvez-vous élaborer sur ce point ? J'aimerais mieux comprendre.",
                "C'est fascinant ! Avez-vous d'autres exemples ?",
            ]
            
            import random
            response = random.choice(default_responses)
            conversation.generated_responses.append(response)
            return conversation
    
    chatbot = SimulatedChatbot()

# Étape 3: Initiation et expansion d'une conversation de test
print("\n💬 Test de conversation initiale:")

# Création d'une conversation avec salutation
conversation = Conversation("Salut, comment ça va ?")
conversation = chatbot(conversation)
print("Conversation après première interaction:")
print(conversation)

# Ajout d'une nouvelle entrée utilisateur
conversation.add_user_input("Parle-moi de l'intelligence artificielle")
conversation = chatbot(conversation)
print("\nConversation après deuxième interaction:")
print(conversation)

# Étape 4: Création de l'interface Gradio
print("\n🎨 Création de l'interface Gradio...")

# Listes pour maintenir l'historique
message_list = []
response_list = []

def mini_chatbot(message, history):
    """
    Fonction principale du chatbot pour l'interface Gradio
    
    Args:
        message (str): Message de l'utilisateur
        history (list): Historique des conversations précédentes
    
    Returns:
        str: Réponse générée par le chatbot
    """
    global message_list, response_list
    
    # Ajout du nouveau message à l'historique
    message_list.append(message)
    
    # Création d'un objet Conversation avec l'historique complet
    conversation = Conversation(text=message,
                               past_user_inputs=message_list[:-1],  # Tous sauf le dernier
                               generated_responses=response_list)
    
    # Génération de la réponse avec le chatbot
    conversation = chatbot(conversation)
    
    # Récupération de la dernière réponse générée
    if conversation.generated_responses:
        response = conversation.generated_responses[-1]
        response_list.append(response)
        return response
    else:
        # Fallback si aucune réponse n'est générée
        fallback_response = "Désolé, je n'ai pas pu générer une réponse appropriée."
        response_list.append(fallback_response)
        return fallback_response

# Création de l'interface Gradio ChatInterface
demo_chatbot = gr.ChatInterface(
    mini_chatbot,
    title="🤖 Chatbot BlenderBot",
    description="Discutez avec un chatbot alimenté par le modèle Facebook BlenderBot-400M-distill. "
               "Le chatbot maintient le contexte de la conversation et génère des réponses naturelles.",
    theme=gr.themes.Soft(),
    examples=[
        "Bonjour ! Comment allez-vous ?",
        "Parlez-moi de vos hobbies",
        "Que pensez-vous de l'intelligence artificielle ?",
        "Racontez-moi une blague",
        "Quel temps fait-il aujourd'hui ?"
    ],
    retry_btn="🔄 Réessayer",
    undo_btn="↩️ Annuler",
    clear_btn="🗑️ Effacer",
    submit_btn="📤 Envoyer"
)

# Fonction pour afficher des informations sur le chatbot
def show_info():
    """Affiche des informations sur le chatbot"""
    info = """
    🤖 **Chatbot BlenderBot Information**
    
    **Modèle:** facebook/blenderbot-400M-distill
    **Type:** Modèle conversationnel pré-entraîné
    **Capacités:** 
    - Conversations naturelles
    - Maintien du contexte
    - Réponses cohérentes
    
    **Fonctionnalités:**
    - ✅ Historique de conversation
    - ✅ Interface interactive
    - ✅ Réponses en temps réel
    - ✅ Exemples de démarrage
    
    **Technologies:**
    - 🤗 Hugging Face Transformers
    - 🎨 Gradio ChatInterface
    - 🐍 Python
    """
    print(info)

# Fonction principale
def main():
    """Fonction principale pour lancer le chatbot"""
    print("\n" + "="*60)
    print("🚀 LANCEMENT DU CHATBOT BLENDERBOT")
    print("="*60)
    
    show_info()
    
    print("\n📱 Interface Gradio en cours de lancement...")
    print("💡 Une fois lancée, vous pourrez discuter avec le chatbot dans votre navigateur")
    print("🔗 L'interface s'ouvrira automatiquement dans un nouvel onglet")
    
    # Étape 5: Lancement du chatbot
    try:
        demo_chatbot.launch(
            share=False,  # Mettre à True pour un lien public
            inbrowser=True,  # Ouvre automatiquement le navigateur
            show_error=True,  # Affiche les erreurs
            quiet=False  # Affiche les logs
        )
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        print("🔧 Essayez de relancer le script ou vérifiez votre connexion internet")

# Fonction de test supplémentaire
def test_chatbot_functionality():
    """Teste les fonctionnalités du chatbot"""
    print("\n🧪 Test des fonctionnalités du chatbot:")
    
    test_messages = [
        "Bonjour",
        "Comment ça va ?",
        "Parle-moi de toi",
        "Au revoir"
    ]
    
    for i, msg in enumerate(test_messages, 1):
        print(f"\n--- Test {i} ---")
        print(f"👤 Utilisateur: {msg}")
        
        # Simulation de l'historique pour les tests
        history = []
        response = mini_chatbot(msg, history)
        print(f"🤖 Chatbot: {response}")
        
        time.sleep(0.5)  # Petite pause pour la lisibilité

if __name__ == "__main__":
    # Execution du test de fonctionnalité
    test_chatbot_functionality()
    
    # Lancement de l'interface principale
    main()

# Instructions d'utilisation
"""
🚀 INSTRUCTIONS D'UTILISATION:

1. 📦 Installation automatique des dépendances:
   - transformers
   - gradio

2. 🤖 Modèle utilisé:
   - facebook/blenderbot-400M-distill
   - Pipeline conversationnel Hugging Face

3. 💬 Fonctionnalités:
   - Conversation avec contexte
   - Interface Gradio interactive
   - Historique maintenu
   - Réponses naturelles

4. 🔧 Lancement:
   python chatbot_app.py

5. 🌐 Interface:
   - S'ouvre automatiquement dans le navigateur
   - Chat en temps réel
   - Exemples pré-définis

6. ⚡ Fallback:
   - Chatbot simulé si erreur de chargement
   - Réponses intelligentes de secours
