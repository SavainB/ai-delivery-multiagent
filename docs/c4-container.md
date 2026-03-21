# C4 Container

Container view of the generator.

```mermaid
flowchart TB
  CLI[CLI] --> Graph[Orchestrator]
  Graph --> Agents[Agents]
  Agents --> Services[Services]
  Services --> Workspace[Generated App Workspace]
```
