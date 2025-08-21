# fine_tune_qa_haystack.py

import logging
import os
import json
from haystack.nodes import FARMReader
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import BM25Retriever
from haystack.pipelines import ExtractiveQAPipeline

# 1. Configuration des logs
logging.basicConfig(level=logging.INFO)

# 2. Création du dataset SQuAD-style (personnalisé)
dataset = {
    "data": [
        {
            "title": "Napoleon",
            "paragraphs": [
                {
                    "context": "Napoléon Bonaparte est né en Corse en 1769 et devint empereur des Français.",
                    "qas": [
                        {
                            "id": "1",
                            "question": "Où est né Napoléon ?",
                            "answers": [{"text": "en Corse", "answer_start": 28}],
                            "is_impossible": False
                        },
                        {
                            "id": "2",
                            "question": "Quand est né Napoléon ?",
                            "answers": [{"text": "1769", "answer_start": 37}],
                            "is_impossible": False
                        }
                    ]
                }
            ]
        }
    ]
}

# 3. Sauvegarder le dataset localement
os.makedirs("data", exist_ok=True)
with open("data/custom_dataset.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)

# 4. Initialiser le modèle pré-entraîné (Roberta base)
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=False)

# 5. Entraîner le modèle sur notre dataset personnalisé
reader.train(
    data_dir="data",
    train_filename="custom_dataset.json",
    use_gpu=False,
    n_epochs=1,
    save_dir="my_model"
)

# 6. Charger le modèle fine-tuné
custom_reader = FARMReader(model_name_or_path="my_model", use_gpu=False)

# 7. Préparer des documents à interroger
doc_store = InMemoryDocumentStore()
documents = [
    {"content": "Napoléon Bonaparte est né en Corse en 1769 et devint empereur des Français."}
]
doc_store.write_documents(documents)

# 8. Créer un retriever et pipeline QA
retriever = BM25Retriever(document_store=doc_store)
pipeline = ExtractiveQAPipeline(reader=custom_reader, retriever=retriever)

# 9. Poser des questions
queries = [
    "Où est né Napoléon ?",
    "Quand est né Napoléon ?"
]

for question in queries:
    result = pipeline.run(query=question, params={"Retriever": {"top_k": 1}})
    print(f"\nQuestion : {question}")
    print("Réponse :", result["answers"][0].answer)
