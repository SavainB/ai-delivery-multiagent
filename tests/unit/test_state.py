from ai_delivery.state import DeliveryState


def test_delivery_state_defaults() -> None:
    state = DeliveryState()
    assert state.errors == []
    assert state.reasoning_trace == []
