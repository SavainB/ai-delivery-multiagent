# ADR 0003 - Snowflake LLM Provider

## Decision

Introduce an abstract provider layer with a Snowflake-oriented provider.

## Rationale

- opens the path to enterprise integration
- keeps low coupling with the rest of the orchestrator
- allows a mock fallback for the local demo

## Current Status

The abstract provider layer is in place.

The mock fallback is operational and is used for local demonstrations.

The real Snowflake integration is not finished yet. The `snowflake_provider.py` file still needs to be connected to a real Snowflake call with structured outputs.

## Technical Target

The selected target is direct LLM usage through Snowflake, with:

- centralized configuration
- JSON structured outputs
- Pydantic validation on the Python side
- retention of the mock fallback for tests without external dependencies
