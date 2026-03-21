# Demo Script

## Préparation

1. Activer la venv.
2. Lancer l'API du générateur :
   `python -m ai_delivery.cli serve --host 127.0.0.1 --port 8000`

## Démo live

1. Montrer `IBM.docx` et rappeler le sujet du hackathon.
2. Expliquer la séparation entre :
   - l'API du générateur
   - l'application générée dans `workspace/generated_app/`
3. Vérifier l'API :
   `curl http://127.0.0.1:8000/health`
4. Lancer un run interactif :
   `POST /runs`
5. Montrer la pause après `spec_analyst`.
6. Consulter l'état du run avec `GET /runs/{run_id}`.
7. Reprendre le run jusqu'à la pause suivante.
8. Montrer les artefacts déjà écrits :
   - `outputs/plans/`
   - `outputs/traces/`
   - `outputs/c4/`
9. Continuer jusqu'à la fin.
10. Ouvrir `workspace/generated_app/`.
11. Montrer la structure backend/frontend générée.
12. Montrer la CI, les tests et le branding.

## Message à expliciter au jury

- le système est déjà démontrable de bout en bout
- le provider mock permet la démo locale
- le prochain jalon est le branchement Snowflake réel
