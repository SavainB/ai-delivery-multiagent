# Architecture

Le dépôt sépare explicitement :

- le générateur multi-agents Python
- l'application démonstration générée dans `workspace/generated_app/`

## Vue d'ensemble

Le système possède deux surfaces distinctes :

1. une **API du générateur** qui pilote les runs
2. une **application générée** écrite dans `workspace/generated_app/`

L'API du générateur n'est donc pas l'application métier finale. Elle sert à orchestrer le pipeline logiciel.

## Flux agentique

Le pipeline est orchestré par un flux simple :

1. `spec_analyst`
2. `architect`
3. `developer`
4. `qa_devops`
5. `reviewer`

Chaque étape lit et enrichit un état central typé.

Les artefacts intermédiaires sont persistés dans `outputs/`.

## API interactive

Le générateur expose :

- `POST /runs`
- `GET /runs/{run_id}`
- `POST /runs/{run_id}/resume`
- `POST /runs/{run_id}/interventions`

Quand le mode interactif est activé, le pipeline se met en pause entre les étapes afin que l'utilisateur puisse :

- relire la compréhension du besoin
- corriger un résumé ou un plan
- ajuster certaines décisions avant la suite

## État central

L'état partagé contient notamment :

- `raw_input`
- `parsed_requirements`
- `project_blueprint`
- `architecture_design`
- `generated_files_index`
- `c4_docs`
- `validation_report`
- `reasoning_trace`
- `run_metadata`
- `errors`

## Provider LLM

L'architecture prévoit une couche provider abstraite.

Statut actuel :

- `mock` : opérationnel
- `snowflake` : structure présente, intégration réelle encore à brancher

## Application générée

Le workspace généré contient actuellement :

- un backend FastAPI léger
- un frontend React/Vite léger
- des fichiers de base pour la démo

Ce workspace doit encore être renforcé pour atteindre la cible finale :

- vrai SQLite
- vrai branchement frontend/backend
- CI plus substantielle
