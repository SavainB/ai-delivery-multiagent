# C4 Component

Component view of the generation chain.

```mermaid
flowchart LR
  Parser --> Planner
  Planner --> Architect
  Architect --> Codegen
  Codegen --> Reviewer
```
