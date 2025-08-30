#!/usr/bin/env python3
"""
SCRIPT SIMPLE POUR TÉLÉCHARGER TOUT LE PROJET
Il suffit de lancer ce script et tout sera créé automatiquement !

Usage: python3 telecharger_projet.py
"""

import os
import stat
from pathlib import Path

print("🎉 CRÉATION AUTOMATIQUE DU PROJET PDF-TO-PARQUET")
print("=" * 50)
print("Ce script va créer TOUS les fichiers nécessaires !")
print()

# Créer les dossiers
print("📁 Création des dossiers...")
folders = ["Test", "out_test", "logs"]
for folder in folders:
    Path(folder).mkdir(exist_ok=True)
    print(f"  ✅ {folder}/")

print()
print("📝 Création des fichiers...")

# 1. Configuration simple
config_content = '''"""Configuration du projet - MODIFIEZ ICI VOS PARAMÈTRES"""

import os
from dotenv import load_dotenv

load_dotenv()

# VOS CLÉS API (à remplir dans le fichier .env)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

# PARAMÈTRES POUR DÉBUTER (commencez avec ces valeurs)
PARALLEL_INSTANCES = 5        # Peu d'instances pour éviter les problèmes
REQUESTS_PER_SECOND = 10      # Lent mais sûr
CHUNK_SIZE = 10               # Petits lots
ZOOM_FACTOR = 1.2             # Qualité correcte

# DOSSIERS
INPUT_FOLDER = "Test"         # Mettez vos PDFs ici
OUTPUT_FOLDER = "out_test"    # Les résultats iront ici
PARQUET_SIZE = 100           # Petits fichiers pour commencer
FILE_NAMES = "train"

GEMINI_MODEL = "openrouter/google/gemini-2.0-flash-lite-001"

def validate_config():
    if not GEMINI_API_KEY or "your_" in str(GEMINI_API_KEY):
        print("❌ Configurez GEMINI_API_KEY dans .env")
        return False
    if not OPENROUTER_API_KEY or "your_" in str(OPENROUTER_API_KEY):
        print("❌ Configurez OPENROUTER_API_KEY dans .env") 
        return False
    print("✅ Configuration OK")
    return True
'''

with open("config.py", "w", encoding='utf-8') as f:
    f.write(config_content)
print("  ✅ config.py")

# 2. Script principal SIMPLE
main_content = '''"""SCRIPT PRINCIPAL - Lance le traitement des PDFs"""

import asyncio
import os
import glob
import time
import logging
from pathlib import Path
import pandas as pd
import fitz  # PyMuPDF
from PIL import Image
import io
import base64
import aiohttp
from datetime import datetime

from config import *

# Configuration des logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class ProcesseurPDF:
    def __init__(self):
        self.resultats = []
        
    def extraire_page(self, pdf_path, page_num):
        """Extrait texte et image d'une page PDF"""
        try:
            doc = fitz.open(pdf_path)
            page = doc[page_num]
            
            # Extraire le texte
            texte = page.get_text()
            
            # Créer l'image
            mat = fitz.Matrix(ZOOM_FACTOR, ZOOM_FACTOR)
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("png")
            image = Image.open(io.BytesIO(img_data))
            
            # Convertir en base64
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            doc.close()
            
            return {
                'texte': texte,
                'image_base64': img_base64,
                'pdf_name': os.path.basename(pdf_path),
                'page_num': page_num
            }
        except Exception as e:
            logger.error(f"Erreur page {page_num}: {e}")
            return None
    
    async def generer_requete_simple(self, texte, image_base64):
        """Génère une requête simple sans API (pour tester)"""
        # Version simple sans API pour commencer
        mots_cles = texte.split()[:10]  # Prendre les 10 premiers mots
        requete = f"Document technique contenant: {' '.join(mots_cles)}"
        return {
            'main_query': requete,
            'secondary_query': f"Détails sur: {texte[:100]}...",
            'visual_query': "Page avec diagrammes et texte technique",
            'multimodal_query': f"Recherche multimodale: {requete}"
        }
    
    def traiter_pdf(self, pdf_path):
        """Traite un PDF complet"""
        logger.info(f"🔄 Traitement de {pdf_path}")
        
        doc = fitz.open(pdf_path)
        nb_pages = len(doc)
        doc.close()
        
        logger.info(f"📄 {nb_pages} pages trouvées")
        
        for page_num in range(min(nb_pages, 5)):  # Max 5 pages pour tester
            contenu = self.extraire_page(pdf_path, page_num)
            if contenu:
                # Générer requêtes simples
                requetes = asyncio.run(self.generer_requete_simple(
                    contenu['texte'], 
                    contenu['image_base64']
                ))
                
                # Créer les entrées
                for type_req, requete in requetes.items():
                    entree = {
                        'query': requete,
                        'query_type': type_req,
                        'image': contenu['image_base64'],
                        'text': contenu['texte'],
                        'pdf_name': contenu['pdf_name'],
                        'page_number': contenu['page_num'],
                        'processed_at': datetime.now().isoformat()
                    }
                    self.resultats.append(entree)
        
        logger.info(f"✅ {len(self.resultats)} entrées créées")
    
    def sauvegarder(self):
        """Sauvegarde en Parquet"""
        if not self.resultats:
            logger.error("❌ Aucun résultat à sauvegarder")
            return
            
        df = pd.DataFrame(self.resultats)
        nom_fichier = f"{FILE_NAMES}-test.parquet"
        chemin = os.path.join(OUTPUT_FOLDER, nom_fichier)
        
        df.to_parquet(chemin, index=False)
        logger.info(f"💾 Résultats sauvés dans {chemin}")
        logger.info(f"📊 {len(df)} entrées au total")

def main():
    """FONCTION PRINCIPALE"""
    print("🚀 DÉMARRAGE DU TRAITEMENT")
    
    # Vérifier la config
    if not validate_config():
        print("❌ Configurez d'abord vos clés API dans .env")
        return
    
    # Trouver les PDFs
    pdfs = glob.glob(os.path.join(INPUT_FOLDER, "*.pdf"))
    if not pdfs:
        print(f"❌ Aucun PDF trouvé dans {INPUT_FOLDER}/")
        print(f"💡 Placez vos PDFs dans le dossier {INPUT_FOLDER}/")
        return
    
    print(f"📄 {len(pdfs)} PDFs trouvés")
    
    # Traiter
    processeur = ProcesseurPDF()
    for pdf in pdfs[:1]:  # UN SEUL PDF pour tester
        processeur.traiter_pdf(pdf)
    
    # Sauvegarder
    processeur.sauvegarder()
    print("🎉 TERMINÉ !")

if __name__ == "__main__":
    main()
'''

with open("main.py", "w", encoding='utf-8') as f:
    f.write(main_content)
print("  ✅ main.py")

# 3. Dépendances
requirements_content = '''PyMuPDF==1.23.14
Pillow==10.1.0
pandas==2.1.4
pyarrow==14.0.2
aiohttp==3.9.1
python-dotenv
'''

with open("requirements.txt", "w") as f:
    f.write(requirements_content)
print("  ✅ requirements.txt")

# 4. Configuration des clés API
env_content = '''# CONFIGUREZ VOS CLÉS API ICI
# Obtenez vos clés sur OpenRouter.ai

GEMINI_API_KEY=votre_clé_gemini_ici
OPENROUTER_API_KEY=votre_clé_openrouter_ici

# Exemple (remplacez par vos vraies clés) :
# GEMINI_API_KEY=sk-or-v1-abc123...
# OPENROUTER_API_KEY=sk-or-v1-def456...
'''

with open(".env", "w") as f:
    f.write(env_content)
print("  ✅ .env")

# 5. Script de démarrage
start_content = '''#!/bin/bash
echo "🚀 INSTALLATION ET DÉMARRAGE"
echo "=========================="

echo "📦 Installation des dépendances..."
pip3 install -r requirements.txt

echo "✅ Installation terminée !"
echo ""
echo "📋 PROCHAINES ÉTAPES :"
echo "1. Modifiez le fichier .env avec vos clés API"
echo "2. Mettez vos PDFs dans le dossier Test/"
echo "3. Lancez : python3 main.py"
echo ""
echo "🔗 Pour obtenir les clés API : https://openrouter.ai"
'''

with open("installer.sh", "w") as f:
    f.write(start_content)
os.chmod("installer.sh", stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
print("  ✅ installer.sh")

# 6. README simple
readme_content = '''# 🎯 PROJET PDF-TO-PARQUET - VERSION SIMPLE

## 🚀 DÉMARRAGE EN 3 ÉTAPES

### 1. Installation
```bash
./installer.sh
```

### 2. Configuration
Éditez le fichier `.env` avec vos clés API (obtenez-les sur openrouter.ai)

### 3. Utilisation
```bash
# Mettez vos PDFs dans Test/
cp vos-pdfs/*.pdf Test/

# Lancez le traitement
python3 main.py
```

## 📁 Structure
- `Test/` ← Vos PDFs ici
- `out_test/` ← Résultats Parquet ici
- `config.py` ← Paramètres à ajuster
- `main.py` ← Script principal

## 🔧 Si ça ne marche pas
1. Vérifiez que Python 3.8+ est installé
2. Vérifiez vos clés API dans .env
3. Commencez avec 1 seul petit PDF

## 💡 Aide
Ce script traite vos PDFs et crée des requêtes automatiquement !
'''

with open("README.md", "w") as f:
    f.write(readme_content)
print("  ✅ README.md")

print()
print("🎉 PROJET CRÉÉ AVEC SUCCÈS !")
print("=" * 30)
print()
print("📋 MAINTENANT, FAITES CECI :")
print("1. Lancez : ./installer.sh")
print("2. Éditez .env avec vos clés API")
print("3. Mettez des PDFs dans Test/")
print("4. Lancez : python3 main.py")
print()
print("💡 AIDE : Lisez README.md pour plus de détails")