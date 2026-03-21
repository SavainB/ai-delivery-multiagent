# AGENTS.md

## Références de travail

Lire les fichiers dans cet ordre avant toute modification substantielle :

1. [ai-delivery-multiagent/AGENT.md](AGENT.md)
2. [ai-delivery-multiagent/TODO.md](TODO.md)
3. le code réellement concerné

## Rôle de chaque fichier

- `AGENT.md`
  Contrat de projet de haut niveau. Ce fichier capture les décisions d'architecture, les contraintes IBM, la structure cible, les objectifs de démo et les principes à préserver.
- `TODO.md`
  Backlog vivant du projet. Ce fichier capture ce qu'il reste à faire, l'ordre recommandé, les priorités, les tâches bloquées et l'état d'avancement.

## Convention de maintenance

Pour les prochaines sessions Codex :

- ne pas utiliser `AGENTS.md` comme backlog détaillé
- ne pas dupliquer toute l'architecture dans `TODO.md`
- garder `AGENT.md` relativement stable
- mettre à jour `TODO.md` dès qu'une tâche importante est terminée, ajoutée, re-priorisée ou bloquée

## Quand modifier `AGENT.md`

Modifier `AGENT.md` seulement si l'un des points suivants change réellement :

- architecture cible
- rôle des agents
- contraintes non négociables
- structure attendue du repo
- stratégie produit ou démo

## Quand modifier `TODO.md`

Modifier `TODO.md` quand :

- une tâche est terminée
- une tâche devient bloquante
- une nouvelle sous-tâche apparaît
- une priorité change
- une estimation doit être révisée

## Règle pratique

Si un futur agent doit faire avancer le projet :

1. lire `AGENT.md`
2. lire `TODO.md`
3. choisir la prochaine tâche `P0` ou `P1`
4. implémenter
5. mettre à jour `TODO.md`
6. ne modifier `AGENT.md` que si une décision de fond change
