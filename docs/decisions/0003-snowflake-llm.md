# ADR 0003 - Snowflake LLM Provider

## Décision

Introduire une couche provider abstraite avec un provider orienté Snowflake.

## Motifs

- ouverture à une intégration entreprise
- faible couplage avec le reste de l'orchestrateur
- possibilité de fallback mock pour la démo locale

## Statut actuel

La couche provider abstraite est en place.

Le fallback mock est opérationnel et utilisé pour les démonstrations locales.

L'intégration Snowflake réelle n'est pas encore finalisée. Le fichier `snowflake_provider.py` doit encore être branché sur un appel réel Snowflake avec structured outputs.

## Cible technique

La cible retenue est un usage direct du LLM via Snowflake, avec :

- configuration centralisée
- structured outputs JSON
- validation Pydantic côté Python
- conservation du fallback mock pour les tests hors dépendance externe
