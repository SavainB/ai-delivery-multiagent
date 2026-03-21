"""Graph construction with LangGraph fallback."""

from __future__ import annotations

from dataclasses import dataclass

from ai_delivery.graph.edges import DEFAULT_FLOW

try:
    from langgraph.graph import END, START, StateGraph  # type: ignore
except ImportError:
    END = "END"
    START = "START"
    StateGraph = None


@dataclass
class SequentialGraph:
    steps: list[callable]

    def invoke(self, state):
        current = state
        for step in self.steps:
            current = step(current)
        return current


def build_graph(agent_registry: dict[str, object]):
    if StateGraph is None:
        ordered_steps = [agent_registry[name].run for name in DEFAULT_FLOW]
        return SequentialGraph(ordered_steps)

    graph = StateGraph(dict)
    for name in DEFAULT_FLOW:
        graph.add_node(name, agent_registry[name].run)

    graph.add_edge(START, DEFAULT_FLOW[0])
    for current, nxt in zip(DEFAULT_FLOW, DEFAULT_FLOW[1:], strict=False):
        graph.add_edge(current, nxt)
    graph.add_edge(DEFAULT_FLOW[-1], END)
    return graph.compile()
