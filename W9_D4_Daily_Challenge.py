#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
W9_D4_Daily_Challenge.py
========================

LangChain Conversational Memory - Daily Challenge
Semaine 9, Jour 4 - Défi Quotidien

Objectif : Créer un buffer de mémoire pour un chatbot contextuel

Requirements:
pip install langchain>=0.1.0 langchain-core>=0.1.0 langchain-community>=0.0.20

Auteur : Challenge LangChain
Date : 28 juillet 2025
Fichier : W9_D4_Daily_Challenge.py
"""

print("🧠 W9_D4 Daily Challenge : Mémoire Conversationnelle avec LangChain")
print("=" * 65)

# ===== 1. IMPORTATION DU MODULE MÉMOIRE =====
print("\n📥 Étape 1 : Importation du module mémoire")

try:
    from langchain.memory import ConversationBufferMemory
    print("✅ ConversationBufferMemory importé avec succès")
except ImportError as e:
    print(f"❌ Erreur d'importation : {e}")
    print("💡 Installez les dépendances avec : pip install langchain langchain-core")
    exit(1)

# ===== 2. INITIALISATION DE LA MÉMOIRE =====
print("\n🔧 Étape 2 : Initialisation de la mémoire")

# Création d'une instance de la mémoire conversationnelle
memory = ConversationBufferMemory()

print("✅ Instance de mémoire créée")
print(f"   Type : {type(memory).__name__}")
print(f"   Clé par défaut : {memory.memory_key}")

# ===== 3. SIMULATION DE LA PREMIÈRE INTERACTION =====
print("\n💬 Étape 3 : Simulation de la première interaction")

# Première échange utilisateur-bot
user_input_1 = "Hello, how are you?"
bot_output_1 = "I'm fine, thank you. How can I assist you today?"

# Sauvegarde du contexte de la première interaction
memory.save_context(
    {"input": user_input_1}, 
    {"output": bot_output_1}
)

print("✅ Première interaction sauvegardée :")
print(f"   👤 Utilisateur : {user_input_1}")
print(f"   🤖 Bot : {bot_output_1}")

# ===== 4. SIMULATION DU MESSAGE DE SUIVI =====
print("\n💬 Étape 4 : Simulation du message de suivi")

# Deuxième échange utilisateur-bot
user_input_2 = "Tell me a joke."
bot_output_2 = "Why did the chicken cross the road? To get to the other side."

# Sauvegarde du contexte de la deuxième interaction
memory.save_context(
    {"input": user_input_2}, 
    {"output": bot_output_2}
)

print("✅ Deuxième interaction sauvegardée :")
print(f"   👤 Utilisateur : {user_input_2}")
print(f"   🤖 Bot : {bot_output_2}")

# ===== 5. RÉCUPÉRATION DE L'HISTORIQUE CONVERSATIONNEL =====
print("\n📚 Étape 5 : Récupération de l'historique conversationnel")

# Chargement de toutes les variables de mémoire stockées
conversation_history = memory.load_memory_variables({})

print("✅ Historique conversationnel récupéré")
print(f"   Clés disponibles : {list(conversation_history.keys())}")
print(f"   Type de l'historique : {type(conversation_history)}")

# ===== 6. AFFICHAGE DE LA MÉMOIRE =====
print("\n🖨️ Étape 6 : Affichage de la mémoire complète")

print("📋 Historique complet de la conversation :")
print("-" * 40)
print(conversation_history)

# Affichage formaté pour plus de lisibilité
print("\n📋 Historique formaté :")
print("-" * 25)
if 'history' in conversation_history:
    print(conversation_history['history'])

# ===== DÉMONSTRATION AVANCÉE =====
print("\n🔍 Démonstration avancée : Fonctionnalités supplémentaires")
print("=" * 50)

# Vérification du buffer de messages
print("📊 Statistiques de la mémoire :")
print(f"   - Nombre total de messages : {len(memory.chat_memory.messages)}")
print(f"   - Type des messages : {[type(msg).__name__ for msg in memory.chat_memory.messages]}")

# Affichage détaillé des messages
print("\n📨 Messages individuels :")
for i, msg in enumerate(memory.chat_memory.messages):
    role = "👤 Humain" if msg.type == "human" else "🤖 IA"
    print(f"   {i+1}. {role}: {msg.content}")

# Test d'une troisième interaction pour voir l'accumulation
print("\n💡 Test d'une troisième interaction :")
memory.save_context(
    {"input": "What's the weather like?"}, 
    {"output": "I don't have access to real-time weather data, but I hope it's nice where you are!"}
)

# Récupération mise à jour
updated_history = memory.load_memory_variables({})
print("✅ Historique après 3 interactions :")
print(updated_history['history'])

# ===== EXEMPLE D'UTILISATION PRATIQUE =====
print("\n🚀 Exemple d'utilisation pratique")
print("=" * 35)

def chatbot_with_memory():
    """
    Exemple pratique d'un chatbot utilisant la mémoire conversationnelle
    
    Returns:
        ConversationBufferMemory: Instance de mémoire avec conversation complète
    """
    # Initialisation d'une nouvelle mémoire pour l'exemple
    chatbot_memory = ConversationBufferMemory()
    
    print("🤖 Chatbot avec mémoire initialisé")
    print("   (Simulation d'une conversation)")
    
    # Simulation d'une conversation multi-tours
    conversations = [
        ("Bonjour, je m'appelle Alice", "Bonjour Alice ! Ravi de vous rencontrer. Comment puis-je vous aider aujourd'hui ?"),
        ("Quelle est ma profession ?", "Je ne connais pas encore votre profession, Alice. Pourriez-vous me la dire ?"),
        ("Je suis développeuse", "C'est fantastique, Alice ! En tant que développeuse, vous devez travailler avec beaucoup de technologies intéressantes."),
        ("Rappelez-moi mon nom", "Bien sûr ! Votre nom est Alice, et vous êtes développeuse.")
    ]
    
    for i, (user_msg, bot_msg) in enumerate(conversations, 1):
        # Sauvegarde de chaque interaction
        chatbot_memory.save_context({"input": user_msg}, {"output": bot_msg})
        
        print(f"\n--- Tour {i} ---")
        print(f"👤 Alice : {user_msg}")
        print(f"🤖 Bot : {bot_msg}")
    
    # Affichage de l'historique complet
    final_history = chatbot_memory.load_memory_variables({})
    print(f"\n📚 Historique complet du chatbot :")
    print(final_history['history'])
    
    return chatbot_memory

# Exécution de l'exemple pratique
example_memory = chatbot_with_memory()

# ===== VARIANTES DE MÉMOIRE =====
print("\n🔬 Exploration des variantes de mémoire")
print("=" * 40)

def demonstrate_memory_variants():
    """Démontre différents types de mémoire LangChain"""
    
    print("1️⃣ ConversationBufferMemory (mémoire complète)")
    buffer_memory = ConversationBufferMemory()
    buffer_memory.save_context({"input": "Test 1"}, {"output": "Réponse 1"})
    buffer_memory.save_context({"input": "Test 2"}, {"output": "Réponse 2"})
    print(f"   Contenu: {buffer_memory.load_memory_variables({})['history']}")
    
    try:
        from langchain.memory import ConversationBufferWindowMemory
        print("\n2️⃣ ConversationBufferWindowMemory (fenêtre limitée)")
        window_memory = ConversationBufferWindowMemory(k=1)  # Garde seulement 1 interaction
        window_memory.save_context({"input": "Test 1"}, {"output": "Réponse 1"})
        window_memory.save_context({"input": "Test 2"}, {"output": "Réponse 2"})
        print(f"   Contenu: {window_memory.load_memory_variables({})['history']}")
    except ImportError:
        print("\n2️⃣ ConversationBufferWindowMemory non disponible")
    
    try:
        from langchain.memory import ConversationSummaryMemory
        print("\n3️⃣ ConversationSummaryMemory (résumé automatique)")
        print("   Note: Nécessite un LLM pour fonctionner")
    except ImportError:
        print("\n3️⃣ ConversationSummaryMemory non disponible")

demonstrate_memory_variants()

# ===== INTÉGRATION AVEC UN LLM (EXEMPLE CONCEPTUEL) =====
print("\n🔗 Intégration avec un LLM (exemple conceptuel)")
print("=" * 45)

def llm_integration_example():
    """
    Exemple conceptuel d'intégration de la mémoire avec un LLM
    """
    print("💡 Comment intégrer cette mémoire avec un LLM :")
    print("""
    # Exemple d'utilisation avec un LLM
    from langchain.llms import OpenAI  # ou autre LLM
    from langchain.chains import ConversationChain
    
    # Initialisation
    llm = OpenAI(temperature=0.7)
    memory = ConversationBufferMemory()
    
    # Création d'une chaîne conversationnelle
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=True
    )
    
    # Utilisation
    response1 = conversation.predict(input="Bonjour, je m'appelle Jean")
    response2 = conversation.predict(input="Comment je m'appelle ?")
    # Le LLM se souviendra que vous vous appelez Jean !
    """)

llm_integration_example()

# ===== FONCTIONS UTILITAIRES =====
print("\n🛠️ Fonctions utilitaires")
print("=" * 25)

def memory_stats(memory_instance):
    """
    Affiche les statistiques d'une instance de mémoire
    
    Args:
        memory_instance: Instance de ConversationBufferMemory
    """
    stats = {
        "nombre_messages": len(memory_instance.chat_memory.messages),
        "taille_historique": len(memory_instance.load_memory_variables({})['history']),
        "types_messages": [msg.type for msg in memory_instance.chat_memory.messages]
    }
    return stats

def clear_memory(memory_instance):
    """
    Vide la mémoire d'une instance
    
    Args:
        memory_instance: Instance de ConversationBufferMemory
    """
    memory_instance.clear()
    print("🧹 Mémoire vidée")

# Test des fonctions utilitaires
print("📊 Statistiques de la mémoire principale :")
stats = memory_stats(memory)
for key, value in stats.items():
    print(f"   {key}: {value}")

# ===== EXERCICES PRATIQUES BONUS =====
print("\n🎯 Exercices pratiques bonus")
print("=" * 30)

def bonus_exercises():
    """Exercices pratiques pour approfondir la compréhension"""
    
    print("💪 Exercice 1 : Créer une mémoire de support client")
    support_memory = ConversationBufferMemory()
    
    # Simulation d'un support client
    support_conversation = [
        ("J'ai un problème avec mon compte", "Je comprends votre préoccupation. Pouvez-vous me donner plus de détails ?"),
        ("Je n'arrive pas à me connecter", "D'accord, problème de connexion. Avez-vous essayé de réinitialiser votre mot de passe ?"),
        ("Oui, mais ça ne marche pas", "Je vois. Étant donné que la réinitialisation n'a pas fonctionné, je vais créer un ticket pour notre équipe technique."),
        ("Combien de temps ça va prendre ?", "Concernant votre problème de connexion, notre équipe technique répond généralement sous 24h.")
    ]
    
    for user_msg, agent_msg in support_conversation:
        support_memory.save_context({"input": user_msg}, {"output": agent_msg})
    
    print("✅ Conversation de support simulée")
    print(f"📞 Contexte maintenu sur {len(support_conversation)} échanges")
    
    print("\n💪 Exercice 2 : Analyser l'évolution de la conversation")
    history = support_memory.load_memory_variables({})['history']
    print("📈 Analyse : La mémoire permet au support de :")
    print("   - Se souvenir du problème initial (connexion)")
    print("   - Référencer les solutions tentées (réinitialisation)")
    print("   - Maintenir le contexte pour le suivi")

bonus_exercises()

# ===== RÉCAPITULATIF ET CONCLUSION =====
print("\n🎉 W9_D4 Daily Challenge terminé avec succès !")
print("=" * 45)

print("🧠 Vous avez appris à :")
print("   ✅ Importer ConversationBufferMemory")
print("   ✅ Initialiser une instance de mémoire")
print("   ✅ Sauvegarder des contextes avec save_context()")
print("   ✅ Récupérer l'historique avec load_memory_variables()")
print("   ✅ Créer un chatbot avec mémoire contextuelle")
print("   ✅ Explorer les variantes de mémoire")
print("   ✅ Intégrer la mémoire dans des applications réelles")

print("\n💡 Points clés à retenir :")
print("   🔹 La mémoire préserve le contexte entre les interactions")
print("   🔹 save_context() stocke chaque échange utilisateur-bot")
print("   🔹 load_memory_variables() récupère l'historique complet")
print("   🔹 Cette base peut être intégrée dans n'importe quel LLM")
print("   🔹 Différents types de mémoire existent selon les besoins")

print("\n🚀 Prochaines étapes :")
print("   📚 Explorez ConversationBufferWindowMemory pour limiter la taille")
print("   🤖 Intégrez cette mémoire avec un vrai LLM (OpenAI, Anthropic, etc.)")
print("   🔄 Testez ConversationSummaryMemory pour les longues conversations")
print("   💾 Découvrez la persistance de mémoire avec des bases de données")

print("\n" + "=" * 65)
print("🏆 Félicitations ! W9_D4 Daily Challenge complété !")
print("   Vous maîtrisez maintenant les bases de la mémoire conversationnelle !")
print("=" * 65)

# ===== INFORMATIONS DE DEBUG =====
if __name__ == "__main__":
    print(f"\n🔧 Informations de debug :")
    print(f"   - Fichier : W9_D4_Daily_Challenge.py")
    print(f"   - Script exécuté directement")
    print(f"   - Version Python : {__import__('sys').version}")
    
    try:
        import langchain
        print(f"   - Version LangChain : {langchain.__version__}")
    except:
        print(f"   - Version LangChain : Non disponible")
    
    print(f"   - Mémoire finale : {len(memory.chat_memory.messages)} messages stockés")
    print(f"   - Challenge W9_D4 : ✅ Complété")