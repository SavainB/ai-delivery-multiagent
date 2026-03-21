# C4 Container

Vue conteneurs du generateur.

```mermaid
flowchart TB
  CLI[CLI] --> Graph[Orchestrator]
  Graph --> Agents[Agents]
  Agents --> Services[Services]
  Services --> Workspace[Generated App Workspace]
```
