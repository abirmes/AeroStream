# AeroStream

## 1. Description du projet
AeroStream est une solution de **streaming de données Twitter** pour analyser le **sentiment des utilisateurs vis-à-vis des compagnies aériennes américaines**.  
Le projet collecte, prédit et visualise les sentiments en **temps réel** à l’aide d’un pipeline orchestré par **Airflow**.  

**Objectifs :**  
- Surveiller le sentiment client.  
- Visualiser les tendances sur un dashboard interactif.  
- Démontrer un pipeline de traitement de données en temps réel.  

---

## 2. Fonctionnalités
- Collecte de tweets via un **fake API** simulant des flux en temps réel.  
- Prédiction du **sentiment** (`positive`, `neutral`, `negative`) via un **modèle SVM**.  
- Stockage des données et prédictions dans **PostgreSQL**.  
- Visualisation interactive avec **Streamlit** et **Plotly**.  
- Orchestration du pipeline avec **Airflow** (toutes les minutes).  

---

## 3. Technologies
- **Airflow** : orchestration du pipeline.  
- **Python** : scripts de traitement, API et modèle.  
- **PostgreSQL** : base de données pour stocker tweets et prédictions.  
- **Streamlit + Plotly** : dashboard interactif.  
- **Docker** : conteneurisation des services pour un déploiement facile.  
- **Jira** : suivi des tâches et gestion agile.  
- **GitHub** : gestion du code source et versioning.  


