# AI Delivery Multi-Agent

Référentiel hackathon pour un système multi-agents Python qui transforme une expression de besoin en artefacts principaux d'un pipeline de livraison logicielle.

## Objectif

Le dépôt contient le **générateur**.
L'application démonstration de gestion de tâches est produite dans `workspace/generated_app/`.

## Statut actuel

Le projet est aujourd'hui dans un état **démontrable** mais pas encore totalement finalisé pour un run réel Snowflake.

Ce qui fonctionne déjà :

- orchestrateur multi-agents visible
- API FastAPI du générateur
- exécution interactive par étapes
- production de plans, traces et documentation C4
- génération d'une application cible dans `workspace/generated_app/`
- outillage qualité du repo principal

Ce qui reste à finaliser :

- branchement du vrai provider Snowflake
- persistance SQLite réelle dans l'app générée
- branchement réel frontend <-> backend dans l'app générée
- CI plus substantielle de l'application générée

## Capacités

- analyse d'une spécification texte, markdown ou JSON
- plan structuré et blueprint projet
- documentation C4 Mermaid
- génération d'une application FastAPI + React/Vite/Tailwind
- génération de CI/CD et scripts de validation
- export de traces `Plan / Act / Reason`
- exécution en mode `dry-run`
- exposition du générateur sous forme d'API
- intervention utilisateur entre les étapes clés

## Stack

- Python 3.11
- LangGraph avec fallback séquentiel local
- Pydantic via couche de compatibilité
- uv pour la gestion de dépendances
- Ruff pour lint + format
- pytest pour les tests
- GitHub Actions pour la CI

## Démarrage

Avec l'environnement existant :

```bash
source .venv/bin/activate
python -m ai_delivery.cli serve --host 127.0.0.1 --port 8000
```

Avec `uv` :

```bash
uv sync --all-extras
uv run pre-commit install
uv run python -m ai_delivery.cli run --input inputs/sample_spec.md
```

Mode démonstration sans génération réelle :

```bash
uv run python -m ai_delivery.cli run --input inputs/sample_spec.md --dry-run
```

API locale :

```bash
uv run python -m ai_delivery.cli serve --host 127.0.0.1 --port 8000
```

## Préparation Snowflake

Le repo est préparé pour un futur provider Snowflake réel, mais ce provider n'est pas encore branché de bout en bout.

Préparation attendue :

1. copier le fichier d'exemple :

```bash
cp .env.example .env
```

2. renseigner les variables Snowflake dans `.env` ou dans ton shell :

- `SNOWFLAKE_ACCOUNT`
- `SNOWFLAKE_USER`
- `SNOWFLAKE_PASSWORD`
- `SNOWFLAKE_ROLE`
- `SNOWFLAKE_WAREHOUSE`
- `SNOWFLAKE_DATABASE`
- `SNOWFLAKE_SCHEMA`
- `SNOWFLAKE_HOST`
- `SNOWFLAKE_AUTHENTICATOR`
- `SNOWFLAKE_CORTEX_MODEL`

3. basculer le provider :

```bash
export AI_DELIVERY_PROVIDER=snowflake
```

4. implémenter le vrai branchement dans `src/ai_delivery/llm/snowflake_provider.py`

Statut actuel :

- la config Snowflake est préparée
- le provider `snowflake` existe comme point d'extension
- le comportement réel reste encore à implémenter

## Ce que tu pilotes réellement

L'API exposée sur `127.0.0.1:8000` pilote le **générateur**.

Tu ne pilotes pas directement l'application ToDo finale.

Le flux réel est :

1. tu démarres un run
2. le système exécute un agent
3. il persiste l'état courant
4. il s'arrête si le mode interactif est activé
5. tu consultes ou modifies l'état
6. tu relances le run
7. les artefacts finaux sont écrits dans `outputs/` et `workspace/generated_app/`

## Commandes utiles

```bash
make install
make lint
make format
make test
make run
make dry-run
make serve
make export-traces
make clean
```

## API et intervention utilisateur

Le générateur expose une API FastAPI :

- `POST /runs` pour démarrer un run
- `GET /runs/{run_id}` pour relire un état
- `POST /runs/{run_id}/resume` pour reprendre un run interactif
- `POST /runs/{run_id}/interventions` pour modifier l'état avant reprise

En mode `interactive`, le pipeline s'arrête après chaque agent. L'utilisateur peut intervenir sur :

- `parsed_requirements`
- `project_blueprint`
- `architecture_design`
- `run_metadata`

Exemple de cycle minimal :

```bash
curl -X POST http://127.0.0.1:8000/runs \
  -H 'content-type: application/json' \
  -d '{"input_path":"inputs/sample_spec.md","interactive":true,"dry_run":true}'

curl http://127.0.0.1:8000/runs/<RUN_ID>

curl -X POST http://127.0.0.1:8000/runs/<RUN_ID>/resume
```

## Structure

- `src/ai_delivery/` : orchestrateur, services, agents et outils
- `prompts/` : prompts versionnés hors du code Python
- `configs/` : configuration globale, modèles, branding démo
- `inputs/` : exemples d'entrée
- `outputs/` : plans, traces, exports C4 et rapports
- `workspace/generated_app/` : application générée
- `docs/` : documentation architecture et ADR

## Démo

Le pipeline nominal est :

1. lecture du besoin
2. analyse structurée
3. pause utilisateur optionnelle après `spec_analyst`
4. définition d'architecture
5. pause utilisateur optionnelle après `architect`
6. génération des artefacts applicatifs
7. pause utilisateur optionnelle après `developer`
8. validation qualité / CI
9. revue finale

Voir `docs/demo-script.md` pour la trame de soutenance.

## Test manuel rapide

```bash
curl -X POST http://127.0.0.1:8000/runs \
  -H 'content-type: application/json' \
  -d '{"input_path":"inputs/sample_spec.md","interactive":true,"dry_run":true}'
```

Puis :

1. récupérer le `run_id`
2. consulter `GET /runs/{run_id}`
3. intervenir si besoin via `POST /runs/{run_id}/interventions`
4. reprendre via `POST /runs/{run_id}/resume`

## Artefacts à inspecter

- `outputs/plans/` : blueprint projet
- `outputs/traces/` : traces `Plan / Act / Reason`
- `outputs/c4/` : exports C4
- `outputs/runs/` : sessions et rapports
- `workspace/generated_app/` : application générée

## Limites connues

- le provider Snowflake réel n'est pas encore branché
- le provider `snowflake` actuel retombe encore sur un comportement mock
- l'application générée est démontrable mais pas encore totalement alignée avec la cible finale :
  backend encore léger, frontend pas encore réellement branché au backend, SQLite non finalisé

## Source de configuration

Aujourd'hui, la configuration du projet repose principalement sur :

- `pyproject.toml`
- `configs/settings.yaml`
- `configs/models.yaml`
- variables d'environnement shell

Le fichier `.env.example` est prêt pour Snowflake, mais le chargement automatique de `.env` reste encore une tâche à finaliser.
