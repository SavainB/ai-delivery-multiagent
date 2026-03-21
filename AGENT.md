# AGENT.md

## But du dépôt

Construire un **système multi-agents Python** qui prend une expression de besoin en entrée et produit de manière autonome les principaux artefacts d'un pipeline de livraison logicielle.

Le dépôt principal est **le générateur**.
L'application de démonstration produite par ce générateur doit être écrite dans `workspace/generated_app/`.

Le sujet source est `IBM.docx` à la racine du dépôt.

## Source de vérité

Le projet doit concilier deux sources :

1. Le brief IBM contenu dans `IBM.docx`
2. Le choix d'architecture déjà validé par l'utilisateur

En cas de tension entre plusieurs options de design :

- préférer la simplicité
- préférer le déterminisme
- préférer la fiabilité de démonstration
- éviter une autonomie agentique excessive

## Résumé fidèle du brief IBM

### Objectif fonctionnel global

Le système doit prendre comme entrée une expression de besoin, par exemple :

- spécifications fonctionnelles
- texte libre
- croquis
- supports visuels
- maquettes

Puis produire les principaux artefacts d'un pipeline logiciel :

- analyse du besoin
- plan projet
- documentation d'architecture
- arborescence de dépôt
- code applicatif
- tests
- CI/CD
- traces de raisonnement

### Capacités attendues

Le système doit être capable de :

- analyser les spécifications d'entrée
- identifier modules, parcours utilisateurs, contraintes et composants
- créer un environnement de développement
- initialiser un dépôt Git
- générer l'ossature du projet
- configurer une pipeline CI/CD
- produire une documentation d'architecture basée sur le modèle C4
- générer le code de l'application
- générer des tests unitaires
- générer une interface adaptable au contexte client
- exposer les traces de raisonnement `Plan / Act / Reason`

### Contraintes techniques IBM

- utiliser **au moins un LLM open source**
- utiliser un **framework agentique open source**
- objectiver le choix du framework agentique
- produire une solution défendable en contexte entreprise

### Application candidate fournie par IBM

L'application de démonstration attendue est une **application simple de gestion de tâches** de type ToDo / suivi de demandes avec :

- identification ou connexion utilisateur simplifiée
- tableau de bord filtrable
- création / modification / suppression de tâches
- page de détail avec description, priorité, date d'échéance, statut
- en option : assignation, commentaires, historique

## Décisions d'architecture retenues

Ces choix sont considérés comme validés et ne doivent pas être réouverts sans raison forte :

- langage principal : `Python 3.11`
- gestion de projet : `uv`
- lint et format : `ruff`
- hooks Git : `pre-commit`
- tests : `pytest`
- orchestration multi-agents : `LangGraph`
- support prompts/outils/parsing : `LangChain` seulement si utile, pas comme couche dominante
- contrats typés : `Pydantic`
- provider LLM abstrait : interface générique + implémentation orientée Snowflake
- backend généré : `FastAPI`
- frontend généré : `React + Vite + Tailwind`
- base de données démo : `SQLite`
- CI/CD : `GitHub Actions`
- documentation C4 : `Mermaid`

## Principe directeur du dépôt

Le repo principal n'est **pas** l'application ToDo.

Le repo principal contient :

- l'orchestrateur multi-agents
- les prompts
- les modèles de données
- les outils de génération
- les templates
- les scripts de démo
- les sorties et traces

L'application générée doit vivre sous :

- `workspace/generated_app/`

## Structure cible du dépôt

La structure cible de référence est :

```text
ai-delivery-multiagent/
├─ .github/workflows/
├─ prompts/
├─ configs/
├─ inputs/
├─ outputs/
├─ workspace/generated_app/
├─ src/ai_delivery/
├─ tests/
├─ docs/
└─ scripts/
```

## Agents à implémenter

### `spec_analyst`

- analyser les entrées utilisateur
- identifier user stories, modules, contraintes, parcours et composants
- produire une première structuration exploitable
- produire une sortie JSON validée

### `architect`

- définir l'architecture globale
- proposer le découpage backend/frontend
- définir le modèle de données
- préparer la structure du projet généré
- produire les artefacts C4

### `developer`

- générer le backend dans `workspace/generated_app/`
- générer le frontend dans `workspace/generated_app/`
- générer les premiers tests
- générer le README de l'application produite

### `qa_devops`

- générer la CI/CD
- ajouter la validation locale
- vérifier lint et tests
- proposer ou appliquer des corrections simples

### `reviewer`

- vérifier la cohérence entre besoin, architecture, code et traces
- produire un rapport final exploitable en démo

## Workflow recommandé

Flux nominal :

```text
START
-> spec_analyst
-> architect
-> developer
-> qa_devops
-> reviewer
-> END
```

Le graphe doit rester **simple, lisible et déterministe**.

## État central à prévoir

Le fichier `src/ai_delivery/state.py` doit définir un état central typé contenant au minimum :

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

## Couche provider LLM

Fichiers attendus :

- `src/ai_delivery/llm/base.py`
- `src/ai_delivery/llm/snowflake_provider.py`
- `src/ai_delivery/llm/structured_output.py`
- `src/ai_delivery/llm/prompt_loader.py`

Règles :

- aucune dépendance forte du reste du système à un provider concret
- possibilité de brancher ultérieurement un provider Snowflake réel
- présence d'un chemin mock/fake pour la démo locale
- sorties structurées validées par Pydantic
- gestion propre des erreurs de parsing
- retries bornés et traçables

## Gestion des prompts

Les prompts doivent être **stockés dans des fichiers**, jamais en gros blocs inline dans le code Python.

## Application générée attendue

Le système doit générer une application de gestion de tâches dans `workspace/generated_app/`.

### Backend généré

- `FastAPI`
- `SQLite`
- API CRUD de tâches
- séparation routeurs / services / modèles

### Frontend généré

- `React`
- `Vite`
- `Tailwind`
- dashboard
- liste de tâches filtrable
- détail d'une tâche
- formulaire de création / édition
- branding configurable

## Documentation C4

Le système doit produire au minimum :

- diagramme de contexte
- diagramme de conteneurs
- diagramme de composants
- description technique courte

Format recommandé :

- `Mermaid` intégré dans des `.md`

## Traces de raisonnement

Le sujet IBM impose de montrer `Plan / Act / Reason`.

Les traces doivent être :

- sauvegardées sur disque
- lisibles
- structurées
- démontrables en soutenance

Répertoire cible :

- `outputs/traces/`

## API et intervention utilisateur

Le générateur expose une API propre à piloter le pipeline.

Le mode interactif doit permettre :

- de lancer un run
- de consulter l'état courant
- d'approuver une étape
- de modifier certains champs de l'état
- de reprendre l'exécution

L'API du générateur n'est pas l'application générée.

## Qualité et outillage

Outils imposés :

- `uv`
- `ruff`
- `pytest`
- `pre-commit`
- `GitHub Actions`

## Règles de code

- typage Python complet
- pas de logique métier dans `main.py`
- pas de fichiers monolithiques
- séparation stricte entre `agents`, `graph`, `llm`, `contracts`, `tools`, `services`
- usage de `pathlib`
- pas d'état global mutable caché
- privilégier du code concret à du pseudo-code

## Définition de "done"

Le projet ne doit pas être considéré comme terminé tant que les points suivants ne sont pas vrais :

- le pipeline peut être lancé via CLI et API
- un `dry-run` fonctionne
- des traces sont écrites dans `outputs/traces/`
- un plan est écrit dans `outputs/plans/`
- des docs C4 existent dans `docs/` et `outputs/c4/`
- l'application générée existe dans `workspace/generated_app/`
- le backend généré expose un CRUD de tâches
- le frontend généré permet de manipuler les tâches
- `ruff check` passe
- `ruff format --check` passe
- `pytest` passe
- `pre-commit` est configuré
- la CI GitHub existe
- le provider Snowflake réel est branché pour un test non mock

## Anti-patterns à éviter

- architecture notebook
- script unique monolithique
- prompts cachés dans le code
- agents aux responsabilités floues
- dépendance obligatoire à un service LLM externe pour la démo locale
- frontend purement cosmétique sans intégration API

## Utilisation de ce fichier

Lors d'un prochain appel Codex :

1. lire `AGENT.md`
2. lire `TODO.md`
3. considérer `AGENT.md` comme contrat de cadrage
4. utiliser `TODO.md` comme backlog vivant
