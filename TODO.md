# TODO.md

Backlog vivant du projet `ai-delivery-multiagent`.

Convention :

- `[x]` terminé
- `[ ]` à faire
- `P0` critique pour un vrai test du projet
- `P1` important pour une démo jury solide
- `P2` amélioration utile mais non bloquante

## État global estimé

- avancement global : `~70%`
- très avancé sur l'ossature, l'API du générateur, les tests du générateur et la démonstration interactive
- en retard principal sur le vrai provider Snowflake et sur la substance de l'application générée

## Déjà fait

- [x] structure monorepo Python du générateur
- [x] orchestrateur multi-agents visible
- [x] API FastAPI du générateur
- [x] CLI avec `run`, `resume`, `intervene`, `serve`
- [x] mode interactif avec arrêt entre étapes
- [x] état central typé
- [x] prompts versionnés hors code
- [x] docs C4 générées
- [x] outillage `uv`, `ruff`, `pytest`, `pre-commit`, CI
- [x] génération d'une application cible dans `workspace/generated_app/`
- [x] tests du générateur qui passent

## P0 - Vrai test projet

### 1. Brancher le vrai provider Snowflake

- [ ] implémenter l'appel réel Snowflake dans [ai-delivery-multiagent/src/ai_delivery/llm/snowflake_provider.py](src/ai_delivery/llm/snowflake_provider.py)
- [ ] choisir le mode d'intégration exact :
  `AI_COMPLETE` SQL, Cortex Python, ou REST
- [ ] ajouter les variables de config Snowflake dans [ai-delivery-multiagent/.env.example](.env.example)
- [ ] charger automatiquement `.env` dans [ai-delivery-multiagent/src/ai_delivery/settings.py](src/ai_delivery/settings.py)
- [ ] enrichir [ai-delivery-multiagent/configs/models.yaml](configs/models.yaml) avec la config Snowflake réelle
- [ ] convertir les schémas Pydantic en structured outputs exploitables par Snowflake
- [ ] gérer proprement les erreurs réseau, auth et parsing
- [ ] ajouter tests unitaires du provider Snowflake mocké
- [ ] ajouter un test d'intégration activable par variables d'environnement

### 2. Rendre l'application générée réellement démontrable

- [ ] remplacer le stockage mémoire par SQLite réel dans [ai-delivery-multiagent/src/ai_delivery/templates/backend/app/db.py](src/ai_delivery/templates/backend/app/db.py)
- [ ] brancher le CRUD backend sur SQLite dans [ai-delivery-multiagent/src/ai_delivery/templates/backend/app/services.py](src/ai_delivery/templates/backend/app/services.py)
- [ ] renforcer les tests du backend généré dans [ai-delivery-multiagent/src/ai_delivery/templates/backend/tests/test_tasks.py](src/ai_delivery/templates/backend/tests/test_tasks.py)
- [ ] connecter le frontend généré au backend dans [ai-delivery-multiagent/src/ai_delivery/templates/frontend/src/App.jsx](src/ai_delivery/templates/frontend/src/App.jsx)
- [ ] remplacer le faux state local frontend par de vrais appels API
- [ ] finaliser la vraie config Tailwind au lieu d'une simple dépendance déclarée
- [ ] régénérer [ai-delivery-multiagent/workspace/generated_app](workspace/generated_app) après mise à niveau des templates

## P1 - Démo jury solide

### 3. Renforcer l'expérience d'intervention utilisateur

- [ ] limiter les interventions autorisées selon l'étape courante
- [ ] ajouter des endpoints métier plus simples :
  `approve`, `pause`, `cancel`
- [ ] rendre les erreurs d'intervention plus pédagogiques
- [ ] documenter précisément le flux interactif dans [ai-delivery-multiagent/README.md](README.md)
- [ ] ajouter plus de tests d'intégration interactifs

### 4. Durcir le pipeline generated app

- [ ] transformer [ai-delivery-multiagent/.github/workflows/generated-app-ci.yml](.github/workflows/generated-app-ci.yml) en vraie CI de l'app générée
- [ ] vérifier réellement le backend généré
- [ ] vérifier réellement le frontend généré
- [ ] ajouter une procédure de bootstrap simple dans le workspace généré
- [ ] ajouter un README plus complet dans [ai-delivery-multiagent/workspace/generated_app/README.md](workspace/generated_app/README.md)

### 5. Améliorer la démo

- [ ] enrichir [ai-delivery-multiagent/inputs/sample_spec.md](inputs/sample_spec.md) avec une spec jury plus crédible
- [ ] améliorer [ai-delivery-multiagent/docs/demo-script.md](docs/demo-script.md) en script minute par minute
- [ ] préparer un exemple de branding client plus réaliste dans [ai-delivery-multiagent/configs/clients/demo_brand.yaml](configs/clients/demo_brand.yaml)
- [ ] ajouter un enchaînement de démonstration dans [ai-delivery-multiagent/scripts/run_demo.sh](scripts/run_demo.sh)

## P2 - Améliorations utiles

### 6. Industrialisation

- [ ] ajouter authentification sur l'API du générateur
- [ ] remplacer la persistance JSON simple des sessions par un stockage plus robuste
- [ ] ajouter observabilité plus détaillée
- [ ] nettoyer les fichiers `__pycache__` du repo et prévenir leur retour

### 7. Expérience développeur

- [ ] ajouter chargement automatique de `.env`
- [ ] ajouter commande `make demo`
- [ ] ajouter exemples `curl` prêts à copier dans la README
- [ ] ajouter tests API FastAPI dédiés avec `TestClient`

## Ordre recommandé

1. `P0.1` vrai provider Snowflake
2. `P0.2` SQLite réel et app générée plus solide
3. `P1.3` expérience d'intervention
4. `P1.4` vraie CI generated app
5. `P1.5` polish démo

## Definition of done revue

Le projet pourra être considéré comme vraiment conforme à l'intention initiale quand :

- [ ] le provider Snowflake réel est branché
- [ ] un run complet fonctionne sans mock
- [ ] l'utilisateur peut intervenir pendant la génération via l'API
- [ ] l'application générée tourne réellement avec backend + frontend
- [ ] le backend généré utilise SQLite
- [ ] le frontend généré appelle l'API backend
- [ ] la generated app possède une CI utile
- [ ] la démo jury est exécutable de bout en bout

## Note de méthode

Bonne pratique retenue :

- `AGENT.md` = document stable de cadrage
- `TODO.md` = backlog vivant et priorisé
- `AGENTS.md` = mode d'emploi pour les prochains appels Codex
