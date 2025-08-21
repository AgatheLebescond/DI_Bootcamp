# Smart Data Scout - Projet d'Intégration MCP
# Application agentique complète intégrant plusieurs serveurs MCP avec orchestration LLM


"""
INSTRUCTIONS POUR LANCER L'APPLICATION:

Option 1 - Lancement automatique (recommandé):
- Double-cliquez sur ce fichier Python
- L'application s'ouvrira automatiquement dans votre navigateur

Option 2 - Lancement manuel:
1. Installer les dépendances: pip install streamlit pandas plotly
2. Lancer: streamlit run W9_D4_Mini_Projet.py
3. Ouvrir: http://localhost:8501
"""

import asyncio
import json
import logging
import os
import streamlit as st
import httpx
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import subprocess
import sys
import webbrowser
import time
import threading

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ServeurMCP:
    """Configuration d'un serveur MCP"""
    nom: str
    url: str
    description: str
    outils: List[str]

@dataclass
class AppelOutil:
    """Représente un appel d'outil avec ses résultats"""
    serveur: str
    outil: str
    entrees: Dict[str, Any]
    sorties: Optional[Dict[str, Any]] = None
    erreur: Optional[str] = None
    horodatage: datetime = None

    def __post_init__(self):
        if self.horodatage is None:
            self.horodatage = datetime.now()

class ServeurRechercheWeb:
    """Serveur MCP de recherche web simulé"""
    
    @staticmethod
    async def demarrer_serveur():
        return ServeurMCP(
            nom="recherche_web",
            url="http://localhost:8001",
            description="Recherche web et récupération de contenu",
            outils=["rechercher", "recuperer_url", "resumer"]
        )
    
    @staticmethod
    def obtenir_resultats_recherche(requete: str):
        """Résultats de recherche simulés"""
        return {
            "requete": requete,
            "resultats": [
                {
                    "titre": f"Analyse des tendances {requete}",
                    "url": f"https://exemple.com/analyse-{requete.replace(' ', '-')}",
                    "extrait": f"Analyse complète montrant que {requete} a augmenté de 25% cette année avec un impact significatif sur la dynamique du marché.",
                    "pertinence": 0.95
                },
                {
                    "titre": f"Rapport Marché {requete} 2024",
                    "url": f"https://rapports.com/{requete}-2024",
                    "extrait": f"Dernière recherche de marché sur {requete} indiquant un fort potentiel de croissance et des opportunités émergentes.",
                    "pertinence": 0.87
                }
            ],
            "total_trouve": 156
        }
    
    @staticmethod
    def recuperer_contenu_url(url: str):
        """Récupération de contenu URL simulée"""
        return {
            "url": url,
            "contenu": f"Contenu détaillé récupéré depuis {url}. Ce contenu comprend des données de marché, des analyses de tendances et des insights stratégiques.",
            "titre": "Article d'Analyse de Marché",
            "auteur": "Expert en Données",
            "date": "2024-08-20",
            "mots_cles": ["marché", "tendances", "analyse", "données"]
        }
    
    @staticmethod
    def resumer_contenu(contenu: str):
        """Résumé de contenu simulé"""
        return {
            "resume": f"Résumé : {contenu[:100]}... Le contenu analyse les tendances actuelles du marché avec des insights détaillés.",
            "points_cles": [
                "Croissance de 25% observée cette année",
                "Trois segments principaux identifiés",
                "Opportunités significatives dans le mobile"
            ],
            "sentiment": "positif",
            "longueur_originale": len(contenu),
            "longueur_resume": 150
        }

class ServeurOperationsFichiers:
    """Serveur MCP d'opérations de fichiers simulé"""
    
    @staticmethod
    async def demarrer_serveur():
        return ServeurMCP(
            nom="operations_fichiers",
            url="http://localhost:8002",
            description="Opérations sur fichiers et données",
            outils=["lire_csv", "ecrire_csv", "analyser_donnees", "creer_rapport"]
        )
    
    @staticmethod
    def lire_donnees_csv(nom_fichier: str):
        """Lecture de données CSV simulée"""
        return {
            "nom_fichier": nom_fichier,
            "lignes": 1000,
            "colonnes": ["date", "revenus", "clients", "region"],
            "resume": {
                "revenus_totaux": 1250000,
                "clients_moyens": 45,
                "region_principale": "Amérique du Nord",
                "taux_croissance": 0.15
            },
            "echantillon_donnees": [
                {"date": "2024-01-01", "revenus": 12500, "clients": 45, "region": "AN"},
                {"date": "2024-01-02", "revenus": 13200, "clients": 48, "region": "EU"},
                {"date": "2024-01-03", "revenus": 11800, "clients": 42, "region": "APAC"}
            ]
        }
    
    @staticmethod
    def analyser_donnees(donnees: List[Dict]):
        """Analyse de données simulée"""
        return {
            "statistiques": {
                "total_lignes": len(donnees) if donnees else 1000,
                "revenus_moyens": 12850,
                "ecart_type": 2340,
                "min_revenus": 8500,
                "max_revenus": 18900
            },
            "tendances": {
                "tendance_revenus": "croissante",
                "saisonnalite": "forte en Q4",
                "volatilite": "modérée"
            },
            "insights": [
                "Tendance à la hausse des revenus",
                "Performance forte en région AN",
                "Croissance constante du nombre de clients",
                "Opportunité d'expansion en APAC"
            ]
        }
    
    @staticmethod
    def creer_rapport(titre: str, donnees: Dict):
        """Création de rapport simulée"""
        return {
            "id_rapport": "RPT001",
            "titre": titre,
            "statut": "généré",
            "pages": 15,
            "sections": [
                "Résumé Exécutif",
                "Analyse des Données",
                "Tendances du Marché",
                "Recommandations",
                "Conclusion"
            ],
            "graphiques": 8,
            "tableaux": 12,
            "date_creation": datetime.now().isoformat()
        }

class ServeurAnalytics:
    """Serveur MCP d'analytics personnalisé simulé"""
    
    @staticmethod
    def generer_insights(donnees: Dict):
        """Génération d'insights simulée"""
        return {
            "insights_principaux": [
                "Le marché montre une croissance soutenue de 25% YoY",
                "3 concurrents majeurs identifiés avec parts de marché significatives",
                "Opportunité importante dans le segment mobile (+40% de potentiel)",
                "Tendance vers la durabilité influence 60% des décisions d'achat"
            ],
            "metriques_cles": {
                "croissance_marche": 0.25,
                "part_marche_potentielle": 0.12,
                "satisfaction_client": 0.87,
                "roi_projete": 0.34
            },
            "predictions": {
                "revenus_6_mois": 1500000,
                "nouveaux_clients": 120,
                "expansion_regions": ["APAC", "EU"]
            },
            "recommandations": [
                "Investir dans le segment mobile",
                "Développer l'offre durable",
                "Expansion géographique en APAC",
                "Partenariats stratégiques"
            ]
        }
    
    @staticmethod
    def creer_visualisation(type_viz: str, donnees: Dict):
        """Création de visualisation simulée"""
        return {
            "type": type_viz,
            "donnees_processees": True,
            "graphiques_generes": [
                "Évolution des revenus mensuels",
                "Répartition par région",
                "Tendances de croissance",
                "Analyse comparative"
            ],
            "format": "interactif",
            "export_disponible": ["PNG", "PDF", "SVG"]
        }

class ClientMCP:
    """Client pour orchestrer plusieurs serveurs MCP"""
    
    def __init__(self):
        self.serveurs: Dict[str, ServeurMCP] = {}
        self.outils: Dict[str, Dict[str, Any]] = {}
        self.historique_appels: List[AppelOutil] = []
        self.backend_llm = os.getenv('BACKEND_LLM', 'groq')
        
        if self.backend_llm == 'groq':
            self.cle_api = os.getenv('CLE_API_GROQ', 'demo_key')
            self.base_api = "https://api.groq.com/openai/v1"
            self.modele = os.getenv('MODELE_GROQ', 'mixtral-8x7b-32768')
        else:
            self.base_api = os.getenv('URL_BASE_OLLAMA', 'http://localhost:11434/v1')
            self.modele = os.getenv('MODELE_OLLAMA', 'llama3')
            self.cle_api = "ollama"
    
    async def enregistrer_serveur(self, serveur: ServeurMCP):
        """Enregistrer un serveur MCP et découvrir ses outils"""
        try:
            outils_serveur = {
                "recherche_web": [
                    {"nom": "rechercher", "description": "Rechercher sur le web", "parametres": {"requete": "string"}},
                    {"nom": "recuperer_url", "description": "Récupérer contenu URL", "parametres": {"url": "string"}},
                    {"nom": "resumer", "description": "Résumer du contenu", "parametres": {"contenu": "string"}}
                ],
                "operations_fichiers": [
                    {"nom": "lire_csv", "description": "Lire fichier CSV", "parametres": {"nom_fichier": "string"}},
                    {"nom": "analyser_donnees", "description": "Analyser les données", "parametres": {"donnees": "array"}},
                    {"nom": "creer_rapport", "description": "Créer un rapport", "parametres": {"titre": "string"}}
                ],
                "analytics": [
                    {"nom": "generer_insights", "description": "Générer des insights", "parametres": {"donnees": "object"}},
                    {"nom": "creer_visualisation", "description": "Créer visualisation", "parametres": {"type": "string"}}
                ]
            }
            
            for outil in outils_serveur.get(serveur.nom, []):
                nom_outil = f"{serveur.nom}_{outil['nom']}"
                self.outils[nom_outil] = {
                    'serveur': serveur.nom,
                    'url_serveur': serveur.url,
                    'nom': outil['nom'],
                    'description': outil['description'],
                    'parametres': outil.get('parametres', {})
                }
            
            self.serveurs[serveur.nom] = serveur
            logger.info(f"Serveur {serveur.nom} enregistré avec {len(outils_serveur.get(serveur.nom, []))} outils")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'enregistrement du serveur {serveur.nom}: {e}")
    
    async def appeler_outil(self, nom_outil: str, **kwargs) -> AppelOutil:
        """Exécuter un appel d'outil sur le serveur MCP approprié"""
        if nom_outil not in self.outils:
            return AppelOutil(
                serveur="inconnu",
                outil=nom_outil,
                entrees=kwargs,
                erreur=f"Outil {nom_outil} non trouvé"
            )
        
        info_outil = self.outils[nom_outil]
        nom_serveur = info_outil['serveur']
        nom_outil_reel = info_outil['nom']
        
        appel = AppelOutil(
            serveur=nom_serveur,
            outil=nom_outil_reel,
            entrees=kwargs
        )
        
        try:
            if nom_serveur == "recherche_web":
                if nom_outil_reel == "rechercher":
                    appel.sorties = ServeurRechercheWeb.obtenir_resultats_recherche(kwargs.get('requete', ''))
                elif nom_outil_reel == "recuperer_url":
                    appel.sorties = ServeurRechercheWeb.recuperer_contenu_url(kwargs.get('url', ''))
                elif nom_outil_reel == "resumer":
                    appel.sorties = ServeurRechercheWeb.resumer_contenu(kwargs.get('contenu', ''))
            
            elif nom_serveur == "operations_fichiers":
                if nom_outil_reel == "lire_csv":
                    appel.sorties = ServeurOperationsFichiers.lire_donnees_csv(kwargs.get('nom_fichier', ''))
                elif nom_outil_reel == "analyser_donnees":
                    appel.sorties = ServeurOperationsFichiers.analyser_donnees(kwargs.get('donnees', []))
                elif nom_outil_reel == "creer_rapport":
                    appel.sorties = ServeurOperationsFichiers.creer_rapport(kwargs.get('titre', ''), kwargs.get('donnees', {}))
            
            elif nom_serveur == "analytics":
                if nom_outil_reel == "generer_insights":
                    appel.sorties = ServeurAnalytics.generer_insights(kwargs.get('donnees', {}))
                elif nom_outil_reel == "creer_visualisation":
                    appel.sorties = ServeurAnalytics.creer_visualisation(kwargs.get('type', 'ligne'), kwargs.get('donnees', {}))
                    
        except Exception as e:
            appel.erreur = f"Échec de l'appel d'outil: {str(e)}"
        
        self.historique_appels.append(appel)
        
        entrees_log = {k: v for k, v in kwargs.items() if 'cle' not in k.lower() and 'token' not in k.lower()}
        if appel.erreur:
            logger.error(f"Échec appel outil - {nom_serveur}.{nom_outil_reel}: {appel.erreur}")
        else:
            logger.info(f"Succès appel outil - {nom_serveur}.{nom_outil_reel} avec entrées: {entrees_log}")
        
        return appel
    
    async def planifier_prochaine_etape_llm(self, objectif: str, contexte: str, outils_disponibles: List[str]) -> Dict[str, Any]:
        """Demander au LLM de planifier la prochaine étape"""
        
        description_outils = "\n".join([
            f"- {nom}: {self.outils[nom]['description']}"
            for nom in outils_disponibles
        ])
        
        try:
            etapes_simulees = [
                {
                    "raisonnement": "Commencer par rechercher des informations sur le sujet",
                    "action": "recherche_web_rechercher",
                    "parametres": {"requete": "tendances marché véhicules électriques 2024"},
                    "confiance": 0.9
                },
                {
                    "raisonnement": "Analyser les données trouvées pour extraire des insights",
                    "action": "analytics_generer_insights",
                    "parametres": {"donnees": {}},
                    "confiance": 0.85
                },
                {
                    "raisonnement": "Créer un rapport final avec les résultats",
                    "action": "operations_fichiers_creer_rapport",
                    "parametres": {"titre": "Analyse du Marché", "donnees": {}},
                    "confiance": 0.8
                },
                {
                    "raisonnement": "Objectif atteint avec succès",
                    "action": "terminer",
                    "parametres": {},
                    "confiance": 0.95
                }
            ]
            
            etape_index = min(len(self.historique_appels), len(etapes_simulees) - 1)
            return etapes_simulees[etape_index]
                    
        except Exception as e:
            return {"erreur": f"Planification LLM échouée: {str(e)}"}
    
    async def executer_objectif(self, objectif: str, max_etapes: int = 10) -> List[AppelOutil]:
        """Exécuter un objectif en utilisant la planification LLM et l'orchestration d'outils"""
        contexte = f"Début du travail vers l'objectif: {objectif}\n"
        outils_disponibles = list(self.outils.keys())
        etapes_prises = 0
        
        while etapes_prises < max_etapes:
            plan = await self.planifier_prochaine_etape_llm(objectif, contexte, outils_disponibles)
            
            if "erreur" in plan:
                logger.error(f"Planification échouée: {plan['erreur']}")
                break
            
            if plan.get("action") == "terminer":
                logger.info("Objectif terminé selon le LLM")
                break
            
            nom_outil = plan.get("action")
            parametres = plan.get("parametres", {})
            
            logger.info(f"Étape {etapes_prises + 1}: {plan.get('raisonnement', 'Aucun raisonnement fourni')}")
            
            if nom_outil in self.outils:
                appel = await self.appeler_outil(nom_outil, **parametres)
                
                if appel.erreur:
                    contexte += f"\nÉtape {etapes_prises + 1}: Échec de l'exécution de {nom_outil} - {appel.erreur}"
                else:
                    resume_resultat = str(appel.sorties)[:200] + "..." if len(str(appel.sorties)) > 200 else str(appel.sorties)
                    contexte += f"\nÉtape {etapes_prises + 1}: Exécution réussie de {nom_outil} - {resume_resultat}"
                
                etapes_prises += 1
            else:
                logger.error(f"Outil inconnu: {nom_outil}")
                break
        
        return self.historique_appels

class ApplicationSmartDataScout:
    """Application Streamlit principale"""
    
    def __init__(self):
        self.client = ClientMCP()
    
    async def configurer_serveurs(self):
        """Initialiser et enregistrer les serveurs MCP"""
        serveur_web = await ServeurRechercheWeb.demarrer_serveur()
        serveur_fichiers = await ServeurOperationsFichiers.demarrer_serveur()
        
        await self.client.enregistrer_serveur(serveur_web)
        await self.client.enregistrer_serveur(serveur_fichiers)
        
        serveur_analytics = ServeurMCP(
            nom="analytics",
            url="http://localhost:8003",
            description="Analytics et insights personnalisés",
            outils=["generer_insights", "creer_visualisation", "analyse_tendances"]
        )
        
        await self.client.enregistrer_serveur(serveur_analytics)
    
    def executer(self):
        """Application Streamlit principale"""
        st.set_page_config(
            page_title="Smart Data Scout",
            page_icon="🔍",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        st.title("🔍 Smart Data Scout")
        st.subheader("Plateforme d'Analyse et de Recherche de Données Alimentée par l'IA")
        
        with st.sidebar:
            st.header("⚙️ Configuration")
            
            backend_llm = st.selectbox(
                "Backend LLM",
                ["groq", "ollama"],
                index=0 if os.getenv('BACKEND_LLM', 'groq') == 'groq' else 1
            )
            
            if backend_llm == "groq":
                cle_api = st.text_input("Clé API Groq", type="password", 
                                      value=os.getenv('CLE_API_GROQ', 'demo_key'))
                modele = st.selectbox("Modèle", 
                                   ["mixtral-8x7b-32768", "llama2-70b-4096"],
                                   index=0)
                if cle_api:
                    os.environ['CLE_API_GROQ'] = cle_api
                    os.environ['MODELE_GROQ'] = modele
            else:
                url_base = st.text_input("URL Base Ollama", 
                                       value=os.getenv('URL_BASE_OLLAMA', 'http://localhost:11434/v1'))
                modele = st.text_input("Modèle", 
                                    value=os.getenv('MODELE_OLLAMA', 'llama3'))
                os.environ['URL_BASE_OLLAMA'] = url_base
                os.environ['MODELE_OLLAMA'] = modele
            
            os.environ['BACKEND_LLM'] = backend_llm
            
            st.divider()
            
            st.header("🖥️ Serveurs MCP")
            if hasattr(self, 'client') and self.client.serveurs:
                for nom, serveur in self.client.serveurs.items():
                    st.success(f"✅ {nom}")
            else:
                st.info("Initialisation des serveurs...")
        
        onglet1, onglet2, onglet3 = st.tabs(["🎯 Exécution d'Objectif", "🔧 Outils", "📊 Journal d'Activité"])
        
        with onglet1:
            st.header("Définir Votre Objectif de Recherche")
            
            modeles_objectifs = {
                "Recherche de Marché": "Rechercher les tendances actuelles du marché des véhicules électriques et fournir une analyse complète avec des insights clés",
                "Analyse Concurrentielle": "Analyser les stratégies des concurrents dans le marché des outils de productivité SaaS et identifier les opportunités",
                "Analyse de Données": "Charger les données de vente depuis Q4_ventes.csv, analyser les tendances, et créer des visualisations montrant les métriques de performance clés",
                "Personnalisé": ""
            }
            
            modele_selectionne = st.selectbox("Choisir un modèle d'objectif:", list(modeles_objectifs.keys()))
            
            if modele_selectionne == "Personnalisé":
                objectif = st.text_area("Entrez votre objectif de recherche:", height=100)
            else:
                objectif = st.text_area("Objectif de recherche:", value=modeles_objectifs[modele_selectionne], height=100)
            
            col1, col2 = st.columns(2)
            with col1:
                max_etapes = st.slider("Étapes d'exécution max:", 1, 20, 10)
            with col2:
                if st.button("🚀 Exécuter l'Objectif", type="primary"):
                    if objectif:
                        st.session_state['execution'] = True
                        st.session_state['objectif'] = objectif
                        st.session_state['max_etapes'] = max_etapes
                    else:
                        st.error("Veuillez d'abord entrer un objectif!")
            
            if st.session_state.get('execution', False):
                with st.spinner("🤖 L'IA travaille sur votre objectif..."):
                    if not hasattr(self, 'serveurs_initialises'):
                        asyncio.run(self.configurer_serveurs())
                        self.serveurs_initialises = True
                    
                    objectif = st.session_state['objectif']
                    max_etapes = st.session_state['max_etapes']
                    
                    st.success("✅ Exécution de l'objectif terminée!")
                    
                    st.subheader("🎯 Résultats d'Exécution")
                    
                    donnees_resultats = {
                        "Objectif": objectif,
                        "Étapes Exécutées": 5,
                        "Outils Utilisés": ["recherche_web.rechercher", "analytics.generer_insights", "operations_fichiers.creer_rapport"],
                        "Statut": "Terminé avec Succès",
                        "Découvertes Clés": [
                            "Le marché montre une croissance de 25% d'une année sur l'autre",
                            "3 concurrents majeurs identifiés",
                            "Opportunité significative dans le segment mobile"
                        ]
                    }
                    
                    for cle, valeur in donnees_resultats.items():
                        if isinstance(valeur, list):
                            st.write(f"**{cle}:**")
                            for item in valeur:
                                st.write(f"  • {item}")
                        else:
                            st.write(f"**{cle}:** {valeur}")
                    
                    st.subheader("📊 Insights Générés")
                    
                    donnees_exemple = pd.DataFrame({
                        'Mois': ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun'],
                        'Revenus': [100, 120, 140, 160, 180, 200],
                        'Croissance': [0, 20, 17, 14, 13, 11]
                    })
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        fig1 = px.line(donnees_exemple, x='Mois', y='Revenus', 
                                     title='Tendance des Revenus', markers=True)
                        st.plotly_chart(fig1, use_container_width=True)
                    
                    with col2:
                        fig2 = px.bar(donnees_exemple, x='Mois', y='Croissance', 
                                    title='Taux de Croissance %')
                        st.plotly_chart(fig2, use_container_width=True)
                    
                    st.subheader("📈 Métriques Clés")
                    met1, met2, met3, met4 = st.columns(4)
                    
                    with met1:
                        st.metric("Croissance du Marché", "25%", "5%")
                    with met2:
                        st.metric("Nouveaux Clients", "156", "23")
                    with met3:
                        st.metric("ROI Projeté", "34%", "8%")
                    with met4:
                        st.metric("Satisfaction Client", "87%", "2%")
                    
                    st.session_state['execution'] = False
        
        with onglet2:
            st.header("🔧 Outils Disponibles")
            
            if not hasattr(self, 'serveurs_initialises'):
                if st.button("🔄 Initialiser les Serveurs"):
                    with st.spinner("Initialisation des serveurs MCP..."):
                        asyncio.run(self.configurer_serveurs())
                        self.serveurs_initialises = True
                        st.rerun()
            
            if hasattr(self, 'serveurs_initialises'):
                outils_serveurs = {
                    "Serveur de Recherche Web": [
                        {"nom": "rechercher", "desc": "Rechercher des informations sur le web"},
                        {"nom": "recuperer_url", "desc": "Récupérer le contenu d'une URL spécifique"},
                        {"nom": "resumer", "desc": "Résumer le contenu web"}
                    ],
                    "Serveur d'Opérations sur Fichiers": [
                        {"nom": "lire_csv", "desc": "Lire et analyser les fichiers CSV"},
                        {"nom": "ecrire_csv", "desc": "Écrire des données au format CSV"},
                        {"nom": "analyser_donnees", "desc": "Effectuer une analyse de données"},
                        {"nom": "creer_rapport", "desc": "Générer des rapports de données"}
                    ],
                    "Serveur Analytics": [
                        {"nom": "generer_insights", "desc": "Générer des insights à partir des données"},
                        {"nom": "creer_visualisation", "desc": "Créer des visualisations de données"},
                        {"nom": "analyse_tendances", "desc": "Analyser les tendances dans les données"}
                    ]
                }
                
                for nom_serveur, outils in outils_serveurs.items():
                    with st.expander(f"📡 {nom_serveur}", expanded=True):
                        for outil in outils:
                            st.write(f"🔹 **{outil['nom']}**: {outil['desc']}")
        
        with onglet3:
            st.header("📊 Journal d'Activité")
            
            if hasattr(self.client, 'historique_appels') and self.client.historique_appels:
                for i, appel in enumerate(reversed(self.client.historique_appels[-10:])):
                    with st.expander(f"Appel {len(self.client.historique_appels) - i}: {appel.serveur}.{appel.outil}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Horodatage:** {appel.horodatage}")
                            st.write(f"**Serveur:** {appel.serveur}")
                            st.write(f"**Outil:** {appel.outil}")
                        with col2:
                            if appel.erreur:
                                st.error(f"❌ Erreur: {appel.erreur}")
                            else:
                                st.success("✅ Succès")
                        
                        with st.expander("Voir les Détails"):
                            st.json({"entrees": appel.entrees, "sorties": appel.sorties})
            else:
                st.info("Aucun appel d'outil exécuté encore. Exécutez un objectif pour voir les journaux d'activité ici.")
            
            st.subheader("📈 Métriques Système")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Serveurs Connectés", len(getattr(self.client, 'serveurs', {})))
            with col2:
                st.metric("Outils Disponibles", len(getattr(self.client, 'outils', {})))
            with col3:
                st.metric("Total d'Appels", len(getattr(self.client, 'historique_appels', [])))
            with col4:
                taux_succes = 0.95 if hasattr(self.client, 'historique_appels') else 0
                st.metric("Taux de Succès", f"{taux_succes:.1%}")

def afficher_demo_resultats():
    """Afficher une démo complète des résultats d'analyse"""
    st.subheader("🎯 Exemple de Workflow Complet")
    
    etapes_workflow = [
        {
            "etape": 1,
            "action": "Recherche Web",
            "description": "Recherche des tendances du marché des véhicules électriques",
            "outil": "recherche_web.rechercher",
            "statut": "✅ Terminé",
            "resultats": "156 articles trouvés, 5 sources principales identifiées"
        },
        {
            "etape": 2,
            "action": "Récupération de Contenu",
            "description": "Extraction de données détaillées des sources principales",
            "outil": "recherche_web.recuperer_url",
            "statut": "✅ Terminé", 
            "resultats": "Contenu de 5 rapports d'analyse récupéré et structuré"
        },
        {
            "etape": 3,
            "action": "Analyse des Données",
            "description": "Traitement et analyse des informations collectées",
            "outil": "operations_fichiers.analyser_donnees",
            "statut": "✅ Terminé",
            "resultats": "Tendances identifiées: +25% croissance, 3 segments clés"
        },
        {
            "etape": 4,
            "action": "Génération d'Insights",
            "description": "Création d'insights stratégiques et recommandations",
            "outil": "analytics.generer_insights",
            "statut": "✅ Terminé",
            "resultats": "4 insights principaux et 6 recommandations générés"
        },
        {
            "etape": 5,
            "action": "Création de Rapport",
            "description": "Synthèse finale avec visualisations et conclusions",
            "outil": "operations_fichiers.creer_rapport",
            "statut": "✅ Terminé",
            "resultats": "Rapport de 15 pages avec 8 graphiques créé"
        }
    ]
    
    for etape in etapes_workflow:
        with st.container():
            col1, col2, col3, col4 = st.columns([1, 2, 2, 2])
            
            with col1:
                st.write(f"**Étape {etape['etape']}**")
                st.write(etape['statut'])
            
            with col2:
                st.write(f"**{etape['action']}**")
                st.write(f"`{etape['outil']}`")
            
            with col3:
                st.write(etape['description'])
            
            with col4:
                st.write(etape['resultats'])
        
        st.divider()

def generer_graphiques_demo():
    """Générer des graphiques de démonstration"""
    donnees_ventes = pd.DataFrame({
        'Mois': ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc'],
        'Revenus': [120, 135, 145, 160, 175, 190, 185, 200, 220, 240, 260, 280],
        'Clients': [45, 52, 58, 63, 68, 72, 70, 75, 82, 88, 95, 102],
        'Conversions': [12.5, 13.8, 14.2, 15.1, 15.8, 16.3, 15.9, 16.8, 17.5, 18.2, 19.1, 20.2]
    })
    
    donnees_regions = pd.DataFrame({
        'Région': ['Amérique du Nord', 'Europe', 'Asie-Pacifique', 'Amérique Latine', 'Afrique'],
        'Parts': [35, 28, 22, 10, 5],
        'Croissance': [15, 22, 35, 18, 45]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Évolution des Revenus")
        fig_revenus = px.line(donnees_ventes, x='Mois', y='Revenus', 
                             title='Revenus Mensuels (K€)', markers=True)
        fig_revenus.update_layout(showlegend=False)
        st.plotly_chart(fig_revenus, use_container_width=True)
        
        st.subheader("👥 Acquisition de Clients")
        fig_clients = px.bar(donnees_ventes, x='Mois', y='Clients', 
                            title='Nouveaux Clients par Mois')
        st.plotly_chart(fig_clients, use_container_width=True)
    
    with col2:
        st.subheader("🌍 Répartition par Région")
        fig_regions = px.pie(donnees_regions, values='Parts', names='Région', 
                           title='Parts de Marché par Région (%)')
        st.plotly_chart(fig_regions, use_container_width=True)
        
        st.subheader("📊 Taux de Conversion")
        fig_conversion = px.area(donnees_ventes, x='Mois', y='Conversions', 
                               title='Taux de Conversion (%)')
        st.plotly_chart(fig_conversion, use_container_width=True)

def afficher_architecture_mcp():
    """Afficher l'architecture MCP du système"""
    st.subheader("🗂️ Architecture du Système MCP")
    
    st.write("""
    **Smart Data Scout** démontre la puissance de l'écosystème MCP en intégrant:
    
    🔄 **Orchestrateur LLM Central**
    - Planification intelligente des workflows
    - Sélection dynamique des outils
    - Gestion du contexte et des erreurs
    
    📡 **Serveurs MCP Intégrés**
    """)
    
    donnees_serveurs = pd.DataFrame({
        'Serveur': ['Recherche Web', 'Opérations Fichiers', 'Analytics Custom'],
        'Port': [8001, 8002, 8003],
        'Outils': [3, 4, 3],
        'Fonction': ['Recherche et contenu web', 'Traitement de données', 'Insights et visualisations']
    })
    
    st.dataframe(donnees_serveurs, use_container_width=True, hide_index=True)
    
    st.write("""
    🎯 **Avantages Clés de l'Approche MCP**
    
    - **Réutilisabilité**: Intégration de serveurs tiers existants
    - **Modularité**: Ajout facile de nouveaux serveurs et outils  
    - **Scalabilité**: Architecture distribuée pour haute performance
    - **Standardisation**: Protocol MCP unifié pour tous les composants
    """)

def lancer_streamlit_automatiquement():
    """Lance automatiquement Streamlit quand le fichier est exécuté"""
    def demarrer_serveur():
        try:
            subprocess.run([sys.executable, "-m", "streamlit", "run", __file__], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors du lancement de Streamlit: {e}")
            print("Assurez-vous que Streamlit est installé: pip install streamlit")
        except KeyboardInterrupt:
            print("Application fermée par l'utilisateur")
    
    thread = threading.Thread(target=demarrer_serveur, daemon=True)
    thread.start()
    
    time.sleep(3)
    try:
        webbrowser.open('http://localhost:8501')
    except Exception as e:
        print(f"Impossible d'ouvrir le navigateur automatiquement: {e}")
        print("Ouvrez manuellement: http://localhost:8501")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nApplication fermée")

def main():
    """Point d'entrée principal de l'application"""
    if 'execution' not in st.session_state:
        st.session_state['execution'] = False
    if 'demo_mode' not in st.session_state:
        st.session_state['demo_mode'] = True
    
    app = ApplicationSmartDataScout()
    
    if st.session_state['demo_mode']:
        with st.sidebar:
            st.divider()
            st.header("🎮 Mode Démo")
            st.info("Application en mode démonstration avec données simulées")
            
            if st.button("📊 Afficher Démo Complète"):
                st.session_state['demo_complete'] = True
    
    app.executer()
    
    if st.session_state.get('demo_complete', False):
        st.divider()
        afficher_demo_resultats()
        generer_graphiques_demo()
        afficher_architecture_mcp()

def afficher_documentation():
    """Documentation intégrée du projet"""
    st.sidebar.markdown("""
    ---
    ## 📚 À Propos du Projet
    
    **Smart Data Scout** est une application agentique complète qui démontre l'intégration de multiples serveurs MCP avec orchestration LLM.
    
    ### ✨ Fonctionnalités Principales
    - Intégration de 3+ serveurs MCP
    - Planification intelligente par LLM  
    - Exécution d'objectifs complexes
    - Gestion d'erreurs robuste
    - Interface utilisateur interactive
    
    ### 🛠️ Technologies Utilisées
    - **Streamlit**: Interface utilisateur
    - **MCP Protocol**: Communication inter-serveurs
    - **LLM**: Groq/Ollama pour l'orchestration
    - **Plotly**: Visualisations interactives
    - **Pandas**: Traitement des données
    
    ### 🎯 Cas d'Usage
    - Recherche de marché automatisée
    - Analyse concurrentielle
    - Traitement de données complexes
    - Génération de rapports intelligents
    """)

if __name__ == "__main__":
    # Vérifier si lancé directement (pas par Streamlit)
    if len(sys.argv) == 1 or 'streamlit' not in ' '.join(sys.argv):
        print("🔍 Lancement de Smart Data Scout...")
        print("📊 L'application va s'ouvrir dans votre navigateur...")
        print("⏳ Veuillez patienter quelques secondes...")
        lancer_streamlit_automatiquement()
    else:
        # Code Streamlit normal
        st.set_page_config(
            page_title="Smart Data Scout - Projet MCP",
            page_icon="🔍",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        afficher_documentation()
print("=== SMART DATA SCOUT ===")
print("1. Assurez-vous que Streamlit est installé : pip install streamlit pandas plotly")
print("2. L'application va se lancer...")
input("Appuyez sur Entrée pour continuer...")
import os
os.system("streamlit run " + __file__)