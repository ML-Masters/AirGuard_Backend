# AirGuard Cameroun - Backend API

API REST pour la plateforme de surveillance et prédiction de la qualité de l'air au Cameroun.

## Stack technique

- **Framework** : Django 6.0 + Django REST Framework
- **Auth** : JWT (SimpleJWT)
- **ML** : 5 modèles pré-entraînés (XGBoost, LightGBM, Random Forest, MLP)
- **Chatbot** : OpenAI GPT-3.5
- **Notifications** : Firebase Cloud Messaging
- **PDF** : ReportLab
- **Documentation** : Swagger / ReDoc (drf-spectacular)

## Installation locale

```bash
python -m venv venv
source venv/Scripts/activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_locations
python manage.py runserver
```

## Endpoints principaux

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/v1/villes/` | Liste des 40 villes avec coordonnées |
| GET | `/api/v1/regions/` | Liste des 10 régions |
| GET | `/api/v1/meteo/` | Relevés météorologiques |
| GET | `/api/v1/air-quality/` | Données qualité de l'air |
| POST | `/api/v1/air-quality/predict/` | Prédiction ML multi-indicateurs |
| POST | `/api/v1/air-quality/chat/` | Chatbot IA |
| GET | `/api/v1/air-quality/national_kpis/` | KPIs nationaux |
| GET | `/api/v1/air-quality/reports/pdf/` | Rapport PDF |
| GET | `/api/v1/alerts/` | Alertes actives |
| POST | `/api/v1/login/` | Authentification JWT |
| GET | `/api/docs/` | Documentation Swagger |

## Déploiement

Déployé via Docker sur VPS avec CI/CD GitHub Actions.

```bash
docker compose up -d --build
docker exec airguard-backend python manage.py migrate
docker exec airguard-backend python manage.py seed_locations
```

## Production

- API : https://api.airguard-cm.duckdns.org
- Swagger : https://api.airguard-cm.duckdns.org/api/docs/

## Équipe

Projet développé par **ML Masters** dans le cadre du Hackathon IndabaX Cameroon 2026.
