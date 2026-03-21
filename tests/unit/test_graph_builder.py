from ai_delivery.graph.builder import SequentialGraph, build_graph


class _Agent:
    def __init__(self, value: str) -> None:
        self.value = value

    def run(self, state: list[str]) -> list[str]:
        state.append(self.value)
        return state


def test_build_graph_returns_runnable_graph() -> None:
    agents = {
        "spec_analyst": _Agent("spec"),
        "architect": _Agent("arch"),
        "developer": _Agent("dev"),
        "qa_devops": _Agent("qa"),
        "reviewer": _Agent("review"),
    }
    graph = build_graph(agents)
    if isinstance(graph, SequentialGraph):
        assert graph.invoke([]) == ["spec", "arch", "dev", "qa", "review"]
